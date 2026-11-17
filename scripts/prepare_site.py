#!/usr/bin/env python3
"""Inject multilingual site chrome without replacing existing legal texts or delete-account JS.
Run from a clone of Dudhen/rowstrength-legal, after copying the site overlay.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent  # copy scripts into the repo root
marker = '<!-- ROWSTRENGTH_SITE_V2 -->'
nav = '''<!-- ROWSTRENGTH_SITE_V2 -->
<header class="topbar"><div class="wrap"><a class="brand" href="index.html" data-local-nav><img class="brand-badge" src="assets/rowstrength-icon.png" alt="RowStrength">RowStrength</a><nav class="navlinks"><a href="index.html" data-local-nav data-i18n="home">Home</a><a href="download.html" data-local-nav data-i18n="download">Download</a><a href="index.html#guide" data-local-nav data-i18n="guide">How it works</a><label class="lang" for="site-language"><span data-i18n="language">Language</span><select id="site-language" aria-label="Site language"><option value="en">EN</option><option value="ru">RU</option><option value="de">DE</option><option value="fr">FR</option><option value="es">ES</option></select></label></nav></div></header>
'''
footer = '''<footer class="site-footer"><div class="wrap"><div><strong>RowStrength</strong><p data-i18n="footer">© 2026 Arsenii Dudchenko · RowStrength</p></div><div class="flinks"><a href="index.html" data-local-nav data-i18n="home">Home</a><a href="download.html" data-local-nav data-i18n="download">Download</a><a href="privacy.html" data-local-nav data-i18n="privacy">Privacy</a><a href="terms.html" data-local-nav data-i18n="terms">Terms</a><a href="delete-account.html" data-local-nav data-i18n="delete">Delete account</a><a href="mailto:arseny.dudchenko1998@gmail.com" data-i18n="contact">Support</a></div></div></footer>'''

for name in ('privacy.html', 'terms.html', 'delete-account.html'):
    file = root / name
    if not file.exists():
        raise SystemExit(f'Missing original {name}. Clone the repository first, then copy the overlay.')
    source = file.read_text(encoding='utf-8')
    if marker in source:
        print('Already prepared:', name)
        continue
    if '<main>' not in source or '</body>' not in source or '</style>' not in source:
        raise SystemExit(f'Unexpected structure: {name}. Original file not changed.')
    source = source.replace('</style>', '</style>\n<link rel="stylesheet" href="site.css">', 1)
    source = source.replace('<body>', '<body class="rslegal">\n' + nav, 1)
    # Keep the verified English policy in full, visible on demand; provide clearly
    # labeled translated summaries. Never replace authoritative legal paragraphs.
    if name in ('privacy.html', 'terms.html'):
        m = re.search(r'(<section>.*?)(\s*</article>)', source, flags=re.S)
        if not m:
            raise SystemExit(f'Cannot locate legal sections in {name}')
        kind = 'privacy' if name == 'privacy.html' else 'terms'
        localized = f'<div id="rsLegalSummary" class="legal-summary" data-kind="{kind}"></div>\n'
        english = ('<details class="original-english" open>\n'
                   '<summary data-i18n="legalFull">Read the full English document</summary>\n'
                   '<div class="en-full">\n' + m.group(1) + '\n</div>\n</details>')
        source = source[:m.start()] + localized + english + source[m.start(2):]
        source = source.replace('https://dudhen.github.io/rowstrength-legal/privacy.html', 'https://rowstrength.ru/privacy.html')
        js = '<script src="translations.js" defer></script>\n<script src="legal-summaries.js" defer></script>\n<script src="site.js" defer></script>'
    else:
        # Keep original OTP verification and account-deletion JavaScript intact.
        replacements = [
            (r'<p>Enter the email address used for your RowStrength account\.', '<p id="rsDelIntro">Enter the email address used for your RowStrength account.'),
            (r'<div class="notice">\s*<strong>Subscription notice:</strong>.*?</div>', '<div class="notice" id="rsDelNotice">Subscription notice: deleting your account does not cancel store subscriptions. Cancel separately in the store.</div>'),
            (r'<p>Verified account: <strong id="verifiedEmail">', '<p><span id="rsVerifiedLabel">Verified account: </span><strong id="verifiedEmail">'),
            (r'<p>RowStrength will delete account data', '<p id="rsDelData">RowStrength will delete account data'),
            (r'This action is permanent and cannot be undone\.', '<span id="rsDelDanger">This action is permanent and cannot be undone.</span>'),
            (r'<span>I understand that this permanently deletes', '<span id="rsConfirmLabel">I understand that this permanently deletes'),
            (r'<p>Your RowStrength account and associated RowStrength data have been deleted\.</p>', '<p id="rsDelSuccess">Your RowStrength account and associated RowStrength data have been deleted.</p>'),
            (r'<p>If you had an active subscription, remember to cancel it separately through Apple App Store or Google Play if you do not want it to renew\.</p>', '<p id="rsDelCancel">If you had an active subscription, remember to cancel it separately through Apple App Store or Google Play if you do not want it to renew.</p>'),
            (r'<p>If you cannot complete the automated process, contact <a', '<p id="rsDelHelp">If you cannot complete the automated process, contact <a'),
        ]
        for pattern, replacement in replacements:
            changed, count = re.subn(pattern, lambda _:replacement, source, count=1, flags=re.S)
            if count != 1:
                raise SystemExit(f'Original delete page changed. Cannot safely match: {pattern}')
            source=changed
        source=source.replace('<p id="rsDelIntro">', '<p id="rsDelIntro">', 1)
        # The language selector and translated warning are informational; original
        # authentication and deletion logic remains the implementation of record.
        source=source.replace('<section id="authSection"', '<div class="legal-summary"><h2 data-i18n="deleteTitle">Delete your RowStrength account</h2><p data-i18n="deleteSummary"></p><p data-i18n="spam"></p></div>\n<section id="authSection"',1)
        js = '<script src="translations.js" defer></script>\n<script src="delete-translations.js" defer></script>\n<script src="site.js" defer></script>'
    source = source.replace('</body>', footer + '\n' + js + '\n</body>', 1)
    file.write_text(source, encoding='utf-8')
    print('Prepared:', name)
print('Done: all original server-side account deletion calls and full English legal documents are preserved.')
