#!/usr/bin/env python3
"""Optional: change ONLY privacy/terms links in the user's *current* Flutter main.dart.
Run in the Flutter project root with: py path/to/update_app_legal_links.py
"""
import sys
from pathlib import Path

path=Path.cwd()/'lib'/'main.dart'
if not path.is_file():sys.exit('Not found: lib/main.dart. Run from Flutter project root.')
s=path.read_text(encoding='utf-8')
old={
    'https://dudhen.github.io/rowstrength-legal/privacy.html':'https://rowstrength.ru/privacy.html',
    'https://dudhen.github.io/rowstrength-legal/terms.html':'https://rowstrength.ru/terms.html',
}
new=s
for a,b in old.items():
    if a in new:new=new.replace(a,b)
    elif b not in new:sys.exit(f'Neither old nor new URL found: {a}. File unchanged.')
if new==s:print('App links already use rowstrength.ru. No changes.');sys.exit(0)
backup=path.with_name('main.dart.before-domain-update.bak')
if backup.exists():sys.exit(f'Backup already exists: {backup}. Move it before running. File unchanged.')
backup.write_text(s,encoding='utf-8')
path.write_text(new,encoding='utf-8')
print('Updated only legal URLs in',path,'\nBackup:',backup)
