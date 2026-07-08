#!/bin/bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
tmp_script="/var/folders/4m/7t30h1t11p36kqd18tmt_35m0000gn/T/hermes-verify-$$.py"
mkdir -p "$(dirname "$tmp_script")"
cat > "$tmp_script" <<'PY'
import json, pathlib, subprocess, sys
root = pathlib.Path('/Users/user/sessionswithtoby-engine')
errors = []
for p in [*root.glob('data/*.json')]:
    try:
        json.loads(p.read_text())
    except Exception as e:
        errors.append(f'json {p.name}: {e}')
for p in [*(root/'services').glob('*.js'), *(root/'lms').glob('*.js')]:
    try:
        subprocess.check_output(['node','--check',str(p)], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        errors.append(f'js {p.name}: {e.output.decode().strip()}'[:300])
status = subprocess.check_output(['git','-C',str(root),'status','--short'], text=True).strip()
if status:
    errors.append('uncommitted files:\n'+status)
branch = subprocess.check_output(['git','-C',str(root),'rev-parse','--abbrev-ref','HEAD'], text=True).strip()
if branch != 'static-lms-engine':
    errors.append(f'unexpected branch {branch}')
if errors:
    print('\n'.join(errors[:20]))
    sys.exit(1)
print('QA: PASS')
PY
if ! python3 "$tmp_script"; then
  rm -f "$tmp_script"
  echo "QA: FAIL"
  exit 1
fi
rm -f "$tmp_script"
echo "QA: PASS"
echo "Ready to commit: git add -A && git commit -m '...' && git push"
