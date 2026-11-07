"""Offline merge: create a NEW settings file; never change live Magpie settings."""
import argparse,json,os
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--settings',required=True,type=Path,help='Existing Magpie settings.json')
p.add_argument('--output',required=True,type=Path,help='New output path, must not exist')
a=p.parse_args()
source=a.settings.expanduser().resolve(); target=a.output.expanduser().resolve()
if source==target or target.exists():p.error('Output must be a new file, distinct from input')
s=json.loads(source.read_text(encoding='utf-8')); assert isinstance(s,dict)
patch=json.loads((Path(__file__).resolve().parent/'strict-settings.patch.json').read_text())
rs=list(s.get('redactRules') or [])
for r in patch['redactRules']:
    if r not in rs:rs.append(r)
if len(rs)>32:p.error(f'Merged rules = {len(rs)} > Magpie limit 32; resolve existing rules first. No output written.')
allow_count=len(s.get('redactAllow') or [])
actions=s.get('redactActions') or {}
warn_count=sum(v=='warn' for v in actions.values())
# Strict profile deliberately removes unmasked exceptions and warning-only actions.
s.update(patch);s['redactRules']=rs
s['redactAllow']=[];s['redactRouteTo']='';s['redactShape']=False
s['redactActions']={k:v for k,v in actions.items() if v=='block'}
s['redactWordsWhole']=False
# Preserve existing words, model selection, thresholds, and personal categories.
# Select AstrLink Guard and enable additional categories explicitly in Magpie UI.
target.parent.mkdir(parents=True,exist_ok=True)
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(s,f,ensure_ascii=False,indent=2);f.write('\n')
print(f'Created new merged file: {target}')
print(f'Rules: {len(rs)}; removed {allow_count} allowlist values and {warn_count} warn actions; preserved block actions.')
print('No live configuration modified. Output may contain pre-existing private settings: keep it local.')
print('Select AstrLink Guard in UI; verify additional categories, provider bypasses and gateway routing.')
