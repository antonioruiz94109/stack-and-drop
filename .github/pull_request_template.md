## Change and motivation
Describe the issue and affected catalog or application behavior.

## Author / independent review
- Author (human / Qwen / ChatGPT / other):
- Independent reviewer (must not be same author):
- Review status: NOT REVIEWED / PASS / CHANGES REQUESTED / BLOCKED
- Harness/model executed and verified? Provide reproducible logs; do not assume local model availability.

## Evidence and safety
- Exact source URL, manufacturer/model/gender/variant, checked date (catalog changes):
- Before/after and expected effect:
- Security/access/permissions affected? (If yes, obtain Antonio's approval):
- Automatic publication? **No**.
- Does this touch Product Fit Kit or hosting? **No unless explicitly approved**.

## Checks
- [ ] `python3 -m unittest discover -s scripts -p 'test_check_catalog.py'`
- [ ] `python3 -m json.tool shoes.json > /dev/null`
- [ ] PR validation workflow completed
- [ ] Catalog unchanged except expressly approved correction; any intentional coverage-quality failure explained
- [ ] Live smoke-test plan and rollback documented

## Approval
- [ ] Independent diff review complete
- [ ] Antonio approves catalog/material publication when applicable
- [ ] Post-merge GitHub Pages verification completed (update after merge)

Related issue / run artifact:
