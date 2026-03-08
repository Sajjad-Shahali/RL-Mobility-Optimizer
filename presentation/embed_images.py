import base64, os, re

html_path = 'final_presentation.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

def replace_src(match):
    path = match.group(1)
    if not os.path.exists(path):
        print(f'  MISSING: {path}')
        return match.group(0)
    ext = path.rsplit('.', 1)[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else 'image/png'
    with open(path, 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode()
    print(f'  Embedded: {path} ({len(b64)} chars)')
    return f'src="data:{mime};base64,{b64}"'

print('Embedding local images...')
html_new = re.sub(r'src="(screenshot/[^"]+)"', replace_src, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_new)

print('Done! All local images embedded as base64.')
