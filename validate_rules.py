"""RE2 syntax, Magpie limits and synthetic coverage; not a gateway E2E test."""
import json, re
from pathlib import Path
import re2
p=Path(__file__).resolve().parent
patch=json.loads((p/'strict-settings.patch.json').read_text())
tests=json.loads((p/'synthetic-tests.json').read_text())
rules=patch['redactRules']; assert len(rules)<=32
compiled={}
for r in rules:
    assert len(r['regex'].encode())<=300, (r['kind'],len(r['regex'].encode()))
    assert re.fullmatch('[A-Z][A-Z0-9_]{0,23}',r['kind'])
    c=re2.compile(r['regex']); assert not c.search(''); assert c.groups==1
    compiled.setdefault(r['kind'],[]).append(c)
fail=[]
for t in tests['positive']:
    hits=[m.group(1) for c in compiled[t['kind']] for m in c.finditer(t['text']) if len(m.group(1).encode())>=4]
    if t['value'] not in hits: fail.append({'case':t,'actual':hits})
for text in tests['negative']:
    for rules_of_kind in compiled.values():
        for c in rules_of_kind:
            if c.search(text):fail.append({'negative':text,'regex':c.pattern})
report={'rule_count':len(rules),'max_regex_bytes':max(len(r['regex'].encode()) for r in rules),'positive_cases':len(tests['positive']),'negative_texts':len(tests['negative']),'failures':fail,'scope':'Google RE2 syntax and custom-rule isolated matching only; not Go full engine, AstrLink inference or Magpie end-to-end; no clinical recall estimate.'}
(p/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2)); assert not fail
