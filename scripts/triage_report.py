#!/usr/bin/env python3
"""Bounded Stack & Drop — READ-ONLY report triage (EXACT-ID matching repair, 2026-11-16).

Qwen-authored matching logic. ChatGPT packaged required CLI paths and independent tests.
Repairs the fuzzy model-identity matching:

(1) Fuzzy identity_matches REMOVED entirely. New candidates are triaged
    conservatively: spike/track-field-event exclusions are preserved; otherwise a
    candidate is DUPLICATE only when it carries an EXACT catalog id that matches
    exactly one current-catalog entry. No model identity is parsed from slugs,
    labels or URLs. Anything without an exact catalog id is HOLD (extra holds are
    acceptable — human verification resolves them).

(2) possible_spec_changes: look up catalog entries by e["id"] == sid EXACTLY.
    Exactly one matching entry -> MATCH, returning that raw entry (id/brand/model/
    gender + numeric fields); zero or multiple -> HOLD. Other genders are NOT
    flattened/merged.

(3) All other report counts / SHA256 hashes / per-brand coverage logic is
    unchanged from the pilot.

Now parameterized: --report / --catalog / --output (all required),
so the same reviewed script can process each new weekly artifact without edits.

No web access, no catalog edits, nothing written outside --output.
"""
import argparse
import hashlib
import json
import re
from collections import Counter

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pick(d, names):
    if not isinstance(d, dict):
        return None
    low = {str(k).lower(): k for k in d}
    for n in names:
        if n in low:
            return d[low[n]]
    return None


def numeric_fields(e):
    """All int/float fields of a catalog entry (bools excluded)."""
    return {k: v for k, v in e.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}


def main():
    ap = argparse.ArgumentParser(
        description="READ-ONLY report triage with exact catalog-id matching (no fuzzy identity).")
    ap.add_argument("--report", required=True,
                    help="Input checker report JSON")
    ap.add_argument("--catalog", required=True,
                    help="Input catalog JSON")
    ap.add_argument("--output", required=True,
                    help="Output triage JSON")
    args = ap.parse_args()

    REPORT, CATALOG, OUT = args.report, args.catalog, args.output

    report = json.load(open(REPORT))
    catalog_doc = json.load(open(CATALOG))

    res = {
        "triage_version": "exact-id-v1",
        "scope": ("report triage only; EXACT catalog-id matching (fuzzy identity removed); "
                  "no web research, no catalog edits"),
        "files": {
            "report.json": sha256(REPORT),
            "remote-shoes.json": sha256(CATALOG),
        },
    }

    # ---------- report scalars + per-brand coverage (brand_coverage dict) ----------
    reported_checks = report.get("source_checks")
    reported_fetches = report.get("successful_fetches")
    brand_coverage = report.get("brand_coverage", {})

    per_brand_raw = {}
    sums = Counter()
    for brand, rec in brand_coverage.items():
        per_brand_raw[brand] = rec  # keep raw for results.json
        if isinstance(rec, dict):
            for k, v in rec.items():
                kl = str(k).lower()
                if isinstance(v, (int, float)):
                    sums[kl] += v

    res["report_scalar_fields"] = {
        k: report[k] for k in sorted(report) if isinstance(report.get(k), (int, str, bool))
    }
    res["per_brand_coverage_raw"] = per_brand_raw
    res["independent_totals"] = {
        "summed_numeric_fields_per_field": dict(sums),
        "reported_source_checks": reported_checks,
        "reported_successful_fetches": reported_fetches,
    }

    # ---------- coverage problem categorization (strings: "Brand Model (g): reason — url") ----------
    cat = Counter()
    for p in report.get("coverage_problems", []):
        s = str(p)
        m = re.match(r"^(?P<lead>[^:]+):\s*(?P<reason>.+)$", s)
        reason = m.group("reason").strip() if m else s
        reason = re.sub(r"\s*—\s*\S+$", "", reason).strip()  # strip trailing url
        if not reason:
            reason = "unlabeled"
        cat[reason[:90]] += 1

    res["coverage_problem_categories"] = dict(cat.most_common())
    res["coverage_problem_count"] = len(report.get("coverage_problems", []))

    # ---------- catalog entries (schema: catalog_doc["shoes"] list) ----------
    entries = catalog_doc if isinstance(catalog_doc, list) else pick(
        catalog_doc, ["shoes", "catalog", "entries"])
    assert isinstance(entries, list), "catalog entry list not found"

    res["catalog_entry_count"] = sum(1 for e in entries if isinstance(e, dict))

    # Exact id -> list of raw entries (no coercion; keep all duplicates for the exactly-one check).
    catalog_by_id = {}
    for e in entries:
        if isinstance(e, dict):
            eid = pick(e, ["id"])
            if isinstance(eid, str) and eid:  # nonempty string id only; no coercion
                catalog_by_id.setdefault(eid, []).append(e)

    # ---------- triage new candidates (exact-id only; conservative HOLD otherwise) ----------
    SPIKE_HINTS = ("spike", "triple jump", "long jump", "high jump",
                   "hurdle", "sprint")

    triage = []
    for c in report.get("new_candidates", []):
        if isinstance(c, dict):
            brand = pick(c, ["brand", "manufacturer"]) or ""
            label = (pick(c, ["label", "name", "model"]) or "")
            url = pick(c, ["url", "link"]) or ""
            explicit_id = pick(c, ["id", "catalog_id", "shoe_id"])
        else:
            brand, label, url, explicit_id = "", str(c), "", None

        blob = f"{brand} {label} {url}".lower()
        matches = []
        if any(h in blob for h in SPIKE_HINTS):
            verdict = "EXCLUDE: spikes/track field events (out of scope, AGENTS rule 3)"
        elif isinstance(explicit_id, str) and explicit_id:
            hits = catalog_by_id.get(explicit_id, [])
            if len(hits) == 1:
                e = hits[0]
                matches = [f"{pick(e, ['brand', 'manufacturer']) or '?'} "
                           f"{pick(e, ['model', 'name', 'shoe', 'title']) or '?'}".strip()]
                verdict = "DUPLICATE: explicit catalog id matches exactly one current-catalog entry"
            else:
                verdict = f"HOLD: expected exactly one catalog entry for explicit id; found {len(hits)}"
        else:
            verdict = "HOLD: no exact catalog id supplied; human verification required"
        triage.append({
            "brand": brand, "label": label, "url": url,
            "catalog_identity_matches": matches, "verdict": verdict,
        })

    res["new_candidates_triage"] = triage
    res["new_candidate_count"] = len(triage)

    # ---------- possible spec changes vs catalog (EXACT id lookup) ----------
    spec_triage = []
    for s in report.get("possible_spec_changes", []):
        if not isinstance(s, dict):
            spec_triage.append({"raw": str(s), "verdict": "HOLD: non-dict spec change entry"})
            continue
        sid = pick(s, ["id"])
        url = pick(s, ["url"]) or ""
        before = [str(x) for x in (pick(s, ["before"]) or [])]
        after = [str(x) for x in (pick(s, ["after"]) or [])]
        changed = [{"before": b, "after": a} for b, a in zip(before, after) if b != a]

        # sid must be a nonempty string; exact equality, no coercion. Missing/empty ids HOLD (never match).
        if isinstance(sid, str) and sid:
            hits = [e for e in entries if isinstance(e, dict) and e.get("id") == sid]
        else:
            hits = []
        if len(hits) == 1:
            e = hits[0]
            spec_triage.append({
                "id": sid, "url": url, "before": before, "after": after,
                "changed_lines": changed,
                "verdict": "MATCH: exactly one catalog entry with this id",
                "catalog_entry_raw": e,  # full raw entry: id/brand/model/gender + numeric fields
                "catalog_entry": {
                    "id": pick(e, ["id"]),
                    "brand": pick(e, ["brand", "manufacturer"]),
                    "model": pick(e, ["model", "name", "shoe", "title"]),
                    "gender": pick(e, ["gender"]),
                },
                "catalog_numeric_fields": numeric_fields(e),
            })
        else:
            spec_triage.append({
                "id": sid, "url": url, "before": before, "after": after,
                "changed_lines": changed,
                "verdict": f"HOLD: expected exactly one catalog entry with this id; found {len(hits)}",
                "catalog_entry_raw": None,
            })

    res["possible_spec_changes"] = spec_triage

    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)

    # ---------- print ONLY the required summary ----------
    print("== SHA256 ==")
    print("report.json        ", res["files"]["report.json"])
    print("remote-shoes.json  ", res["files"]["remote-shoes.json"])
    print("\n== Counts ==")
    print("catalog entries (identity base):", res["catalog_entry_count"])
    print("source_checks (reported scalar) :", reported_checks)
    print("successful_fetches (reported)   :", reported_fetches)
    print("coverage problems               :", res["coverage_problem_count"])
    print("new candidates                  :", res["new_candidate_count"])
    print("possible spec changes           :", len(spec_triage))
    print("\n== Per-brand coverage (raw brand_coverage) ==")
    for b in sorted(per_brand_raw):
        print(f"  {b:<14} {json.dumps(per_brand_raw[b])}")
    print("\n== Independent verification (summed per-brand numeric fields) ==")
    for k, v in sums.items():
        print(f"  sum({k} across brands) = {v}")
    print("\n== Coverage problem categories ==")
    for k, v in cat.most_common():
        print(f"  {v:>4}  {k}")
    print("\n== New candidates — triage (exact-id only) ==")
    for i, t in enumerate(triage, 1):
        print(f"  {i:>2}. [{t['verdict'].split(':')[0]}] {t['brand']} | {t['label'][:75]}")
        print(f"      url: {t['url'][:110]}")
        if t["catalog_identity_matches"]:
            print(f"      catalog matches: {t['catalog_identity_matches']}")
    print("\n== Possible spec changes vs catalog (exact id) ==")
    for s in spec_triage:
        print(f"  id={s.get('id')}")
        for ch in s.get("changed_lines", []):
            print(f"      before: {ch['before'][:120]}")
            print(f"      after : {ch['after'][:120]}")
        print(f"      verdict: {s.get('verdict')}")
        ce = s.get("catalog_entry") or {}
        if ce:
            print(f"      catalog entry: id={ce.get('id')} brand={ce.get('brand')} "
                  f"model={ce.get('model')} gender={ce.get('gender')}")
            print(f"      catalog numeric: {s.get('catalog_numeric_fields')}")
    print("\nresults saved:", OUT)


if __name__ == "__main__":
    main()
