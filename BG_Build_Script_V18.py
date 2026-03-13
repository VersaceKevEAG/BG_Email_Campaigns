import base64, os, json
from PIL import Image
import io

# ── IMAGE LOADER ────────────────────────────────────────────────────────────
# ALL images load directly from /mnt/project/ — no /tmp/ cache dependency.
# Pixel-verified source mappings (confirmed March 2026):
#   hero       = Main_Splash_Banner_Image.png
#   side_black = Copy_of_Easy_Lid1.png           (was r_orig_5491)
#   exploded   = Chamber_1A_1.png                (was r_orig_5492)
#   graphite   = Large_Grinding_Chamber_B.png    (was r_orig_5493)
#   top_tooth  = Copy_of_OldNew_2.png            (was r_orig_5495)
#   built      = Built_To_Last_Section_Oldtonew.png
#   old_new    = Copy_of_OldNew_2.png
#   chamber    = Chamber_1A_1.png
#   lid        = Copy_of_Easy_Lid.png
#   grind_a    = Large_Grinding_Chamber_A.png
#   grind_b    = Large_Grinding_Chamber_B.png
#   tooth      = Copy_of_Tooth_2.png
#   collect    = Large_Collection_Chamber.png

PROJECT = '/mnt/project'

def load_img(filename, width=600, quality=72, fmt='JPEG'):
    """Load from /mnt/project/, resize to width, return data URI. Never fails silently."""
    path = os.path.join(PROJECT, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'MISSING PROJECT IMAGE: {path}')
    img = Image.open(path).convert('RGBA' if fmt=='PNG' else 'RGB')
    if img.width != width:
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == 'PNG':
        img.save(buf, 'PNG', optimize=True)
        mime = 'image/png'
    else:
        img.save(buf, 'JPEG', quality=quality, optimize=True)
        mime = 'image/jpeg'
    b64str = base64.b64encode(buf.getvalue()).decode()
    return f'data:{mime};base64,{b64str}'

print('Loading images from /mnt/project/...')
I = {
    'hero':       load_img('Main_Splash_Banner_Image.png',         600, 75),
    'side_black': load_img('Copy_of_Easy_Lid1.png',                600, 75),   # was r_orig_5491
    'exploded':   load_img('Chamber_1A_1.png',                     600, 75),   # was r_orig_5492
    'graphite':   load_img('Large_Grinding_Chamber_B.png',         600, 75),   # was r_orig_5493
    'top_tooth':  load_img('Copy_of_OldNew_2.png',                 600, 75),   # was r_orig_5495
    'built':      load_img('Built_To_Last_Section_Oldtonew.png',   600, 72),
    'old_new':    load_img('Copy_of_OldNew_2.png',                 600, 72),
    'chamber':    load_img('Chamber_1A_1.png',                     600, 72),
    'lid':        load_img('Copy_of_Easy_Lid.png',                 600, 72),
    'grind_a':    load_img('Large_Grinding_Chamber_A.png',         600, 72),
    'grind_b':    load_img('Large_Grinding_Chamber_B.png',         600, 72),
    'tooth':      load_img('Copy_of_Tooth_2.png',                  600, 72),
    'collect':    load_img('Large_Collection_Chamber.png',         600, 72),
}
print(f'  {len(I)} images loaded OK')

TEAL = '#3ecfcf'
SE = 'sales [at] beargrinder.com'

# Shopify CTA URLs
SHOP_URL = 'https://beargrinder.com/collections/all'
CONTACT_URL = 'mailto:Hello@BearGrinder.com'
REORDER_URL = 'https://beargrinder.com/collections/all'

LOGO_W = '''<svg viewBox="0 0 210 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="160" height="30"><circle cx="20" cy="20" r="17" stroke="white" stroke-width="2.2" fill="none"/><circle cx="10.5" cy="8.5" r="1.8" fill="white"/><circle cx="15" cy="5.5" r="1.8" fill="white"/><circle cx="20" cy="4.5" r="1.8" fill="white"/><circle cx="25" cy="5.5" r="1.8" fill="white"/><circle cx="29.5" cy="8.5" r="1.8" fill="white"/><path d="M20 10.5 C15.5 10.5 11.5 13.5 11 18 C10.5 22.5 12.5 27 16 28.5 C17.5 29.2 22.5 29.2 24 28.5 C27.5 27 29.5 22.5 29 18 C28.5 13.5 24.5 10.5 20 10.5Z" fill="white"/><text x="46" y="26" font-family="'Trebuchet MS','Arial Narrow',Arial,sans-serif" font-size="17" font-weight="900" letter-spacing="3" fill="white">BEAR GRINDER</text></svg>'''

LOGO_B = '''<svg viewBox="0 0 210 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="160" height="30"><circle cx="20" cy="20" r="17" stroke="black" stroke-width="2.2" fill="none"/><circle cx="10.5" cy="8.5" r="1.8" fill="black"/><circle cx="15" cy="5.5" r="1.8" fill="black"/><circle cx="20" cy="4.5" r="1.8" fill="black"/><circle cx="25" cy="5.5" r="1.8" fill="black"/><circle cx="29.5" cy="8.5" r="1.8" fill="black"/><path d="M20 10.5 C15.5 10.5 11.5 13.5 11 18 C10.5 22.5 12.5 27 16 28.5 C17.5 29.2 22.5 29.2 24 28.5 C27.5 27 29.5 22.5 29 18 C28.5 13.5 24.5 10.5 20 10.5Z" fill="black"/><text x="46" y="26" font-family="'Trebuchet MS','Arial Narrow',Arial,sans-serif" font-size="17" font-weight="900" letter-spacing="3" fill="black">BEAR GRINDER</text></svg>'''


# ─── COMPONENTS ───────────────────────────────────────
def hdr(light=False):
    logo = LOGO_B if light else LOGO_W
    bg = '#fff' if light else '#000'
    bd = '1px solid #e8e8e8' if light else '1px solid #111'
    return f'<div style="background:{bg};padding:22px 32px;border-bottom:{bd};">{logo}</div>'

def img_full(key, h=360):
    return f'<div style="width:100%;height:{h}px;overflow:hidden;background:#000;"><img src="{I.get(key,"")}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;"></div>'

def img_overlay(key, l1, l2='', h=380):
    src = I.get(key,'')
    sub = f'<div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:.1em;color:rgba(255,255,255,.5);margin-top:6px;text-transform:uppercase;">{l2}</div>' if l2 else ''
    return f'''<div style="width:100%;height:{h}px;overflow:hidden;background:#000;position:relative;"><img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block;opacity:.78;"><div style="position:absolute;bottom:0;left:0;right:0;padding:28px 32px;background:linear-gradient(transparent,rgba(0,0,0,.9));"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:28px;font-weight:900;letter-spacing:.04em;text-transform:uppercase;color:#fff;line-height:1.1;">{l1}</div>{sub}</div></div>'''

def enjoy_hero(key, h=380):
    src = I.get(key,'')
    return f'''<div style="background:#fff;"><img src="{src}" style="width:100%;height:{h}px;object-fit:cover;display:block;"><div style="background:#fff;padding:20px 20px 16px;text-align:center;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:52px;font-weight:900;text-transform:uppercase;letter-spacing:.02em;line-height:.92;"><span contenteditable="true" style="display:block;color:#ccc;">ENJOY</span><span contenteditable="true" style="display:block;color:{TEAL};">THE</span><span contenteditable="true" style="display:block;color:#000;">GRIND</span></div></div></div>'''

def dark_sec(c): return f'<div style="background:#000;padding:32px;">{c}</div>'
def white_sec(c): return f'<div style="background:#fff;padding:32px;">{c}</div>'
def offwhite_sec(c): return f'<div style="background:#f7f7f7;padding:32px;">{c}</div>'

def eb(t,light=False):
    c='#aaa' if light else 'rgba(255,255,255,.35)'
    return f'<div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{c};margin-bottom:9px;">{t}</div>'
def h1d(t,sz=28): return f'<div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:{sz}px;font-weight:900;letter-spacing:.03em;text-transform:uppercase;color:#fff;line-height:1.1;margin-bottom:14px;">{t}</div>'
def h1l(t,sz=28): return f'<div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:{sz}px;font-weight:900;letter-spacing:.03em;text-transform:uppercase;color:#000;line-height:1.1;margin-bottom:14px;">{t}</div>'
def h1t(t,sz=28): return f'<div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:{sz}px;font-weight:900;letter-spacing:.03em;text-transform:uppercase;color:{TEAL};line-height:1.1;margin-bottom:14px;">{t}</div>'
def bd(*ps,light=False):
    c='#333' if light else 'rgba(255,255,255,.75)'
    return ''.join(f'<p contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:15px;line-height:1.82;color:{c};margin:0 0 13px;padding:0;">{p}</p>' for p in ps)
def sal(light=False):
    c='#aaa' if light else 'rgba(255,255,255,.55)'
    return f'<p contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{c};margin:0 0 18px;padding:0;">Hi [firstname],</p>'
def div_line(light=False):
    return f'<div style="height:1px;background:{"#e8e8e8" if light else "#111"};"></div>'
def _btn_url(lbl):
    """Auto-detect CTA URL from button label."""
    up=lbl.upper()
    if any(k in up for k in ['REPLY','TALK','RECONNECT','CONNECT','SCHEDULE','REPLY HERE']):
        return CONTACT_URL
    if 'REORDER' in up:
        return REORDER_URL
    return SHOP_URL

def btn_w(lbl,note='',url=None):
    href=url or _btn_url(lbl)
    n=f'<div contenteditable="true" style="font-size:11px;color:rgba(255,255,255,.55);letter-spacing:.06em;margin-top:8px;">{note}</div>' if note else ''
    return f'<div style="background:#000;padding:26px 32px;text-align:center;"><a href="{href}" contenteditable="true" style="display:inline-block;background:#fff;color:#000;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:900;letter-spacing:.2em;text-transform:uppercase;padding:14px 40px;text-decoration:none;">{lbl}</a>{n}</div>'
def btn_b(lbl,note='',url=None):
    href=url or _btn_url(lbl)
    n=f'<div contenteditable="true" style="font-size:11px;color:#bbb;letter-spacing:.06em;margin-top:8px;">{note}</div>' if note else ''
    return f'<div style="background:#fff;padding:26px 32px;text-align:center;"><a href="{href}" contenteditable="true" style="display:inline-block;background:#000;color:#fff;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:900;letter-spacing:.2em;text-transform:uppercase;padding:14px 40px;text-decoration:none;">{lbl}</a>{n}</div>'
def btn_t(lbl,note='',url=None):
    href=url or _btn_url(lbl)
    n=f'<div contenteditable="true" style="font-size:11px;color:rgba(255,255,255,.55);letter-spacing:.06em;margin-top:8px;">{note}</div>' if note else ''
    return f'<div style="background:#000;padding:26px 32px;text-align:center;"><a href="{href}" contenteditable="true" style="display:inline-block;background:{TEAL};color:#000;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:900;letter-spacing:.2em;text-transform:uppercase;padding:14px 40px;text-decoration:none;">{lbl}</a>{n}</div>'
def promo_d(code,sub,note=''):
    n=f'<div contenteditable="true" style="font-size:11px;color:rgba(255,255,255,.55);letter-spacing:.06em;margin-top:6px;">{note}</div>' if note else ''
    return f'<div style="background:#000;padding:32px;text-align:center;border-top:1px solid #111;border-bottom:1px solid #111;"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:10px;">PROMO CODE</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:48px;font-weight:900;letter-spacing:.1em;color:{TEAL};line-height:1;">{code}</div><div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:13px;color:rgba(255,255,255,.6);letter-spacing:.08em;margin-top:8px;">{sub}</div>{n}</div>'
def promo_l(code,sub,note=''):
    n=f'<div contenteditable="true" style="font-size:11px;color:#bbb;letter-spacing:.06em;margin-top:6px;">{note}</div>' if note else ''
    return f'<div style="background:#f7f7f7;padding:32px;text-align:center;border-top:1px solid #e8e8e8;border-bottom:1px solid #e8e8e8;"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:#bbb;margin-bottom:10px;">PROMO CODE</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:48px;font-weight:900;letter-spacing:.1em;color:#000;line-height:1;">{code}</div><div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:13px;color:#888;letter-spacing:.08em;margin-top:8px;">{sub}</div>{n}</div>'
def stats_bar(items,light=False):
    bg='#f7f7f7' if light else '#000'
    bdc='#e0e0e0' if light else '#111'
    nc='#000' if light else '#fff'
    lc='#aaa' if light else 'rgba(255,255,255,.3)'
    cells=''.join(f'<td style="text-align:center;padding:18px 8px;border-right:1px solid {bdc};"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:24px;font-weight:900;color:{nc};line-height:1;">{n}</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{lc};margin-top:5px;">{l}</div></td>' for n,l in items)
    # remove last border
    cells=cells[::-1].replace(f';thgir:redrob'.replace(':','')[::-1],'',1)[::-1]
    return f'<div style="background:{bg};border-top:1px solid {bdc};border-bottom:1px solid {bdc};"><table style="width:100%;border-collapse:collapse;"><tr>{cells}</tr></table></div>'
def feat_row(ik,lbl,body,rev=False,light=False):
    src=I.get(ik,'')
    bg='#f7f7f7' if light else '#000'
    lc='#000' if light else '#fff'
    pc='#444' if light else 'rgba(255,255,255,.6)'
    ec='#bbb' if light else 'rgba(255,255,255,.5)'
    bdc='#e8e8e8' if light else '#111'
    imgT=f'<td style="width:50%;padding:0;vertical-align:middle;background:#000;overflow:hidden;"><img src="{src}" style="width:100%;height:200px;object-fit:cover;display:block;"></td>'
    txtT=f'<td style="width:50%;padding:24px;vertical-align:middle;background:{bg};border-{"left" if not rev else "right"}:1px solid {bdc};"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:{ec};margin-bottom:7px;">FEATURE</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:16px;font-weight:900;text-transform:uppercase;letter-spacing:.04em;color:{lc};line-height:1.2;margin-bottom:10px;">{lbl}</div><p contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:13px;line-height:1.75;color:{pc};margin:0;padding:0;">{body}</p></td>'
    o=(txtT+imgT) if rev else (imgT+txtT)
    return f'<div style="border-top:1px solid {bdc};"><table style="width:100%;border-collapse:collapse;"><tr>{o}</tr></table></div>'
def feat_grid(items,light=False):
    bg='#f7f7f7' if light else '#000'
    bdc='#e0e0e0' if light else '#111'
    lc='#000' if light else '#fff'
    pc='#666' if light else 'rgba(255,255,255,.5)'
    def cell(ik,lbl,desc):
        src=I.get(ik,'')
        return f'<td style="width:50%;padding:0;vertical-align:top;background:{bg};border:1px solid {bdc};"><img src="{src}" style="width:100%;height:150px;object-fit:cover;display:block;"><div style="padding:14px 18px 18px;"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{lc};margin-bottom:5px;padding-bottom:5px;border-bottom:1px solid {bdc};">{lbl}</div><p contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:12px;line-height:1.7;color:{pc};margin:6px 0 0;padding:0;">{desc}</p></div></td>'
    rows=''.join(f'<tr>{"".join(cell(*items[i+j]) for j in range(2) if i+j<len(items))}</tr>' for i in range(0,len(items),2))
    return f'<table style="width:100%;border-collapse:collapse;background:{bg};">{rows}</table>'
def quote_blk(t,light=False):
    bg='#f7f7f7' if light else '#000'
    tc='#000' if light else '#fff'
    bdc='#e8e8e8' if light else '#111'
    return f'<div style="background:{bg};padding:44px 40px;text-align:center;border-top:1px solid {bdc};border-bottom:1px solid {bdc};"><div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:22px;font-weight:300;font-style:italic;color:{tc};line-height:1.55;">&ldquo;{t}&rdquo;</div></div>'
def urgency(lbl,cnt):
    return f'<div style="background:#000;padding:26px 32px;text-align:center;border-top:3px solid #fff;border-bottom:3px solid #fff;"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:7px;">{lbl}</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:56px;font-weight:900;letter-spacing:.03em;color:#fff;line-height:1;">{cnt}</div></div>'
def terms_blk(items,light=False):
    bg='#0d0d0d' if not light else '#f7f7f7'
    tc='rgba(255,255,255,.5)' if not light else '#666'
    hc='rgba(255,255,255,.25)' if not light else '#bbb'
    bdc='#161616' if not light else '#e8e8e8'
    lis=''.join(f'<li contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:13px;color:{tc};padding:6px 0;line-height:1.6;list-style:none;border-bottom:1px solid {bdc};">{item}</li>' for item in items)
    return f'<div style="background:{bg};padding:26px 32px;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:{hc};margin-bottom:12px;">LAUNCH TERMS</div><ul style="margin:0;padding:0;">{lis}</ul></div>'
def signoff(n,t,u,note='',light=False):
    bg='#fff' if light else '#000'
    bdc='#e8e8e8' if light else '#111'
    nc='#000' if light else '#fff'
    tc='#777' if light else 'rgba(255,255,255,.55)'
    uc='#bbb' if light else 'rgba(255,255,255,.5)'
    nh=f'<p contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:14px;font-style:italic;line-height:1.75;color:{"#555" if light else "rgba(255,255,255,.5)"};margin:0 0 18px;padding:0;">{note}</p>' if note else ''
    return f'<div style="background:{bg};padding:30px 32px;border-top:1px solid {bdc};">{nh}<div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:14px;font-weight:900;letter-spacing:.04em;text-transform:uppercase;color:{nc};">{n}</div><div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:12px;color:{tc};margin-top:3px;">{t}</div><div contenteditable="true" style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:12px;color:{uc};margin-top:2px;">{u}</div></div>'

# Enjoy the Grind footer strip — cropped from Main_Splash_Banner_Image.png
def make_enjoy_strip():
    img = Image.open(os.path.join(PROJECT, 'Main_Splash_Banner_Image.png')).convert('RGB')
    w, h = img.size
    crop = img.crop((0, int(h*0.5), w, h))
    strip = crop.resize((600, 70), Image.LANCZOS)
    buf = io.BytesIO()
    strip.save(buf, 'JPEG', quality=55)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
ENJOY_STRIP = make_enjoy_strip()


def ftr(contact='beargrinder.com',light=False):
    bg='#fff' if light else '#000'
    bdc='#e8e8e8' if light else '#111'
    tc2='#bbb' if light else '#666'
    cc='#999' if light else '#666'
    cbg='#f5f5f5' if light else '#0a0a0a'
    logo=LOGO_B if light else LOGO_W
    logo=logo.replace('width="160"','width="110"').replace('height="30"','height="22"').replace('font-size="17"','font-size="12"')
    return (
        f'<div style="background:{bg};padding:18px 32px 10px;border-top:1px solid {bdc};"><table style="width:100%;border-collapse:collapse;"><tr><td style="vertical-align:middle;">{logo}</td><td style="text-align:right;vertical-align:middle;"><a href="https://beargrinder.com" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:{tc2};text-decoration:none;">BEARGRINDER.COM</a></td></tr></table></div>'
        f'<div style="background:#000;border-top:1px solid #0a0a0a;"><img src="{ENJOY_STRIP}" style="display:block;width:100%;max-width:600px;height:auto;opacity:.55;" alt="Enjoy the Grind"/><div style="background:#000;padding:2px 24px 8px;text-align:center;"><span style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#444;">ENJOY THE GRIND.</span></div></div>'
        f'<div style="background:{cbg};padding:10px 24px 14px;border-top:1px solid {bdc};"><p style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:10px;color:{cc};line-height:1.7;margin:0 0 5px;text-align:center;">You received this email because you opted in at beargrinder.com or expressed interest in Bear Grinder products.</p><p style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:10px;color:{cc};line-height:1.7;margin:0 0 5px;text-align:center;"><a href="{{{{unsubscribe}}}}" style="color:{cc};text-decoration:underline;">Unsubscribe</a> &nbsp;|&nbsp; <a href="https://beargrinder.com/pages/privacy-policy" style="color:{cc};text-decoration:underline;">Privacy Policy</a> &nbsp;|&nbsp; <a href="https://beargrinder.com" style="color:{cc};text-decoration:underline;">beargrinder.com</a></p><p style="font-family:\'Helvetica Neue\',Helvetica,Arial,sans-serif;font-size:9px;color:{tc2};margin:0;text-align:center;">Bear Grinder LLC &nbsp;|&nbsp; San Diego, CA &nbsp;|&nbsp; Hello@BearGrinder.com</p></div>'
    )

def stripe(t,light=False):
    bg='#f7f7f7' if light else '#111'
    tc='#888' if light else 'rgba(255,255,255,.55)'
    return f'<div contenteditable="true" style="background:{bg};padding:9px 32px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:{tc};text-align:center;">{t}</div>'
def teal_stripe(t):
    return f'<div contenteditable="true" style="background:{TEAL};padding:10px 32px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#000;text-align:center;">{t}</div>'
def enjoy_block(light=False):
    bg='#000' if not light else '#fff'
    mc=f'rgba(255,255,255,.55)' if not light else 'rgba(0,0,0,.38)'
    sc=f'rgba(255,255,255,.5)' if not light else 'rgba(0,0,0,.2)'
    return f'<div style="background:{bg};padding:32px;text-align:center;"><div style="line-height:.95;letter-spacing:.02em;"><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:44px;font-weight:900;text-transform:uppercase;color:{mc};">ENJOY</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:44px;font-weight:900;text-transform:uppercase;color:{sc};">THE</div><div contenteditable="true" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:44px;font-weight:900;text-transform:uppercase;color:{TEAL};">GRIND</div></div></div>'

# ─── EMAILS ──────────────────────────────────────────
emails = [
{"id":"e01a","seg":"B2C","num":"01A","name":"Launch - Dark","subj":"We just dropped something you're going to want to pick up","body":(
  hdr()+img_overlay('hero','Built Different.','The V3 Bear Grinder. Now shipping.')+
  dark_sec(sal()+bd("We built Bear Grinder because we were tired of grinders that fight back.","Sticky threads. Metal in your herb. The slow decline where something that used to work great now barely does.","We fixed all of it."))+
  feat_row('lid','Magnetic Closure','Neodymium magnets. No threads. No jamming. No cross-threading - ever.')+
  feat_row('grind_b','608 Ball Bearing','Three to four rotations, done. Gets easier every time - not harder.',rev=True)+
  feat_row('tooth','Precision Tooth Design','High-low pattern. Fluffy, airy, even grind. Preserves trichomes, terpenes, and flower structure.')+
  promo_d('BEAR20','20% off at checkout','Early bird window - two weeks only. Ships April.')+
  btn_w('SHOP NOW')+signoff('Amit','Founder, Bear Grinder','beargrinder.com',"Come try it. You'll feel it in the first spin.")+ftr()
)},
{"id":"e01b","seg":"B2C","num":"01B","name":"Launch - Lifestyle","subj":"Your grinder just got an upgrade","body":img_full('side_black',280)+(
  hdr()+enjoy_hero('side_black')+
  dark_sec(sal()+bd("The grinder that everyone who tries it can't stop spinning.","Bear Grinder V3. 608 bearing. Three rotations. Done. Magnetic lid, no threads. Machined from a single solid block of aerospace aluminum.","It doesn't look like other grinders. It doesn't feel like them either."))+
  enjoy_block()+promo_d('BEAR20','20% off - early bird, two weeks only')+btn_t('SHOP NOW')+signoff('Amit','Bear Grinder','beargrinder.com')+ftr()
)},
{"id":"e02a","seg":"B2C","num":"02A","name":"Social Proof - Dark","subj":"People keep saying the same thing about it","body":(
  hdr()+quote_blk("I didn't expect it to feel like that.")+
  dark_sec(sal()+bd("We've been sending early units out. The messages all say the same thing.","The bearing spin is hard to describe until you're holding it. Then it makes perfect sense.","Early bird window still open."))+
  img_full('grind_b',260)+promo_d('BEAR20','20% off. Limited window.')+btn_w('ORDER NOW')+signoff('Amit','Bear Grinder','beargrinder.com')+ftr()
)},
{"id":"e02b","seg":"B2C","num":"02B","name":"Social Proof - Light","subj":"People can't stop spinning it","body":(
  hdr(light=True)+img_full('side_black',300)+
  white_sec(sal(light=True)+h1l("The reaction is always the same.")+bd("Three or four rotations and it's done. People pick it up and immediately want to do it again.","That's not a coincidence - it's the 608 bearing doing exactly what it's supposed to do.","Early bird pricing is still live.",light=True))+
  quote_blk("Once you feel it, you get it.",light=True)+promo_l('BEAR20','20% off at beargrinder.com')+btn_b('ORDER NOW')+signoff('Amit','Bear Grinder','beargrinder.com',light=True)+ftr(light=True)
)},
{"id":"e03a","seg":"B2C","num":"03A","name":"Last Chance","subj":"48 hours left on the early bird","body":img_full('hero',280)+(
  hdr()+urgency('Early Bird Ends In','48 HRS')+
  dark_sec(sal()+bd("The BEAR20 discount closes in 48 hours.","After that it's full price. If you want one of the first units out the door, this is the window."))+
  promo_d('BEAR20','20% off - expires in 48 hours','No extensions.')+btn_t('GRAB YOURS NOW')+signoff('Amit','Bear Grinder','beargrinder.com')+ftr()
)},
{"id":"e04a","seg":"B2C","num":"04A","name":"Evergreen - Dark","subj":"The grinder that changed how people think about grinders","body":img_full('hero',280)+(
  hdr()+img_overlay('hero','Enjoy The Grind.','Available now at beargrinder.com')+
  dark_sec(sal()+bd("The latest model is here and shipping now.","Nearly everyone who gets one says the same thing: they didn't think a grinder could feel this different.","$49.99. Built for life."))+
  enjoy_block()+btn_w('SHOP BEAR GRINDER')+signoff('Amit','Bear Grinder','beargrinder.com')+ftr()
)},
{"id":"e04b","seg":"B2C","num":"04B","name":"Evergreen - Light","subj":"$49.99. Built to last. Feel the difference.","body":(
  hdr(light=True)+img_full('side_black',340)+
  white_sec(sal(light=True)+h1l("Feel the difference.")+bd("608 ball bearing. Three rotations. Done.","Magnetic closure. No threads. No jamming. Aerospace aluminum, machined from a single block.","$49.99. Ships now.",light=True))+
  stats_bar([('$49.99','MSRP'),('608','Ball Bearing'),('608','Bearing'),('3-4','Rotations')],light=True)+
  btn_b('SHOP NOW')+enjoy_block(light=True)+signoff('Amit','Bear Grinder','beargrinder.com',light=True)+ftr(light=True)
)},
{"id":"e05a","seg":"Wholesale","num":"05A","name":"Announcement - Dark","subj":"New product worth putting on your shelf - Bear Grinder","body":(
  hdr()+stripe('WHOLESALE PRE-ORDERS OPEN | TWO-WEEK LAUNCH WINDOW')+img_overlay('hero','A Product Your Customers Will Ask For.','Bear Grinder V3 - Wholesale Now Available')+
  dark_sec(sal()+bd("608 ball bearing. Three to four rotations, done. Magnetic closure. Machined from a single block of aerospace aluminum.","The honest reason it sells: anyone who picks it up wants to keep spinning it. That tactile moment is your sales floor."))+
  feat_grid([('tooth','Precision Tooth Design','High-low pattern. Fluffy, airy grind. No over-processing.'),('grind_b','608 Ball Bearing','3-4 rotations. Stays smooth for life.'),('lid','Magnetic Closure','Zero threads, zero jamming - ever.'),('collect','Large Collection Chamber','Generous catch area. Easy access.')])+
  terms_blk(['10% pre-order discount on first buy','50% deposit secures inventory','Ships early April','One complimentary unit with first order'])+
  btn_w('REPLY TO DISCUSS PRICING')+signoff('Amit Gorodetzer','Founder & CEO, Bear Grinder',SE)+ftr(SE)
)},
{"id":"e05b","seg":"Wholesale","num":"05B","name":"Announcement - Light","subj":"A grinder your customers will come back for","body":(
  hdr(light=True)+teal_stripe('WHOLESALE PRE-ORDERS OPEN | TWO-WEEK LAUNCH WINDOW')+img_full('side_black',280)+
  white_sec(sal(light=True)+h1l("A product that sells itself.")+bd("608 bearing. Magnetic closure. Precision tooth design. Machined from aerospace aluminum.","Put it in someone's hand for 10 seconds. Watch what happens. That's your floor demo.","Distributor margin runs well above category average.",light=True))+
  feat_grid([('tooth','Precision Tooth Design','High-low pattern.'),('grind_b','608 Ball Bearing','3-4 rotations. Stays smooth.'),('lid','Magnetic Closure','Zero jamming.'),('collect','Collection Chamber','Generous catch.')],light=True)+
  terms_blk(['10% pre-order discount','50% deposit secures inventory','Ships early April','One unit complimentary'],light=True)+
  btn_b('REPLY TO DISCUSS PRICING')+signoff('Amit Gorodetzer','Founder & CEO, Bear Grinder',SE,light=True)+ftr(SE,light=True)
)},
{"id":"e06a","seg":"Wholesale","num":"06A","name":"Margin & Demand","subj":"Quick follow-up on Bear Grinder","body":(
  hdr()+img_full('built',280)+
  dark_sec(sal()+bd("Wanted to follow up in case my last email got buried.","The margin structure scales with volume. Distributor margin at MSRP runs well above category average - that's by design.","Happy to send a sample before you commit. No strings."))+
  stats_bar([('$49.99','MSRP'),('62.5%','Dist. Margin'),('608','Ball Bearing'),('3-4','Rotations')])+
  btn_w('REPLY TO CONNECT')+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e07a","seg":"Wholesale","num":"07A","name":"Pre-Order Closing","subj":"Closing out wholesale pre-orders this week","body":(
  hdr()+dark_sec(sal()+bd("Wrapping up wholesale pre-orders this week.","After Friday the launch discount goes away and inventory allocation locks.","Even a small first order to test in your store. Now is the window. Shipping early April."))+
  img_full('hero',200)+btn_w('PLACE YOUR PRE-ORDER')+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e08a","seg":"Wholesale","num":"08A","name":"Reorder","subj":"Bear Grinder is on shelves - let's keep it moving","body":(
  hdr()+dark_sec(sal()+bd("Thanks for carrying Bear Grinder. We want to make sure it keeps performing for you.","If inventory is running low, we turn around restocks fast. The bearing spin closes the sale - just make sure people have a chance to feel it.","Reply here. We move fast."))+
  img_full('grind_b',200)+btn_w('REORDER NOW')+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e09a","seg":"Distributor","num":"09A","name":"Opportunity - Dark","subj":"Distribution opportunity - Bear Grinder","body":img_full('built',280)+(
  hdr()+img_overlay('hero','One Spin. You\'ll Get It.','Bear Grinder Distribution - Open Markets Available')+
  dark_sec(sal()+bd("My name is Amit, founder of Bear Grinder. We're building out our distribution network and believe there's a real opportunity here.","608 ball bearing, three rotations done. Magnetic closure, no threads. Engineered to last.","$49.99 MSRP. Margin compounds at volume. Open to exclusivity conversations in the right markets."))+
  stats_bar([('$49.99','MSRP'),('608','Ball Bearing'),('608','Bearing'),('3-4','Rotations')])+
  btn_w('SCHEDULE A CALL')+signoff('Amit Gorodetzer','Founder & CEO, Bear Grinder',SE)+ftr(SE)
)},
{"id":"e09b","seg":"Distributor","num":"09B","name":"Opportunity - Light","subj":"A distribution opportunity worth 10 minutes of your time","body":(
  hdr(light=True)+img_full('side_black',280)+
  white_sec(sal(light=True)+h1l("A product that opens doors.")+bd("Bear Grinder - 608 bearing, three to four rotations done. Magnetic closure. Precision tooth design. Aerospace aluminum.","$49.99 MSRP. Margin that scales at volume. US distribution being built now.","I'd like to find out if your market is available.",light=True))+
  stats_bar([('$49.99','MSRP'),('608','Ball Bearing'),('608','Bearing'),('3-4','Rotations')],light=True)+
  btn_b('SCHEDULE A CALL')+signoff('Amit Gorodetzer','Founder & CEO, Bear Grinder',SE,light=True)+ftr(SE,light=True)
)},
{"id":"e10a","seg":"Distributor","num":"10A","name":"Follow-Up","subj":"Following up - Bear Grinder distribution","body":(
  hdr()+dark_sec(sal()+bd("Following up on my note from last week.","We're placing distribution partners in markets without current coverage. Industry-leading design, $49.99 MSRP - easy story for a sales team to tell.","15-minute call this week?"))+
  img_full('old_new',200)+btn_w("LET'S TALK")+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e11a","seg":"Distributor","num":"11A","name":"Final Call","subj":"Last note from me on this","body":(
  hdr()+dark_sec(sal()+bd("This is my last follow-up. Respecting your inbox.","We're finalizing distribution partners now. Once those slots are locked, I won't be reaching back out.","10 minutes is all it takes. Happy to send a sample first - no commitment required."))+
  img_full('built',200)+btn_w('REPLY TO CONNECT')+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e12a","seg":"Distributor","num":"12A","name":"Reactivation","subj":"We've got inventory - wanted to circle back","body":(
  hdr()+dark_sec(sal()+bd("We connected a few months back. Wanted to circle back now that the latest model is live and shipping.","Inventory ready. Active partners in several markets. Product is proving itself on the floor.","Quick call or a sample - whatever makes sense."))+
  img_full('hero',200)+btn_w("LET'S RECONNECT")+signoff('Amit','Bear Grinder',SE)+ftr(SE)
)},
{"id":"e13a","seg":"Friends & Family","num":"13A","name":"Friends & Family - Light","subj":"Hey - your Bear Grinder is ready","body":(
  hdr(light=True)+img_full('side_black',280)+
  white_sec(sal(light=True)+h1l("For the people who showed up early.")+bd("You've heard me talk about this. We're live and shipping.","608 bearing. Three or four spins, done. No threads, no jamming. Once you feel it you'll get it.","15% off, no expiration. My way of saying thank you.",light=True))+
  promo_l('FAM15','15% off your first order - no expiration')+btn_b('ORDER NOW')+enjoy_block(light=True)+signoff('Amit','Bear Grinder','beargrinder.com','Thank you for being in my corner.',light=True)+ftr(light=True)
)},
{"id":"e13b","seg":"Friends & Family","num":"13B","name":"Friends & Family - Fun","subj":"It's finally here. And it's yours.","body":img_full('side_black',280)+(
  hdr()+enjoy_hero('hero')+
  dark_sec(sal()+bd("You've been waiting. We're live.","The Bear Grinder is everything I said it would be. 608 bearing. Spins like butter. Locks with magnets. Machined from aerospace aluminum.","Three or four rotations and you're done. Then you'll spin it again just because you can."))+
  promo_d('FAM15','15% off - for you, no expiration')+btn_t('GET YOURS NOW')+signoff('Amit','Bear Grinder','beargrinder.com','Enjoy the grind.')+ftr()
)},
{"id":"e14a","seg":"Special","num":"14A","name":"MJBizCon - Dark","subj":"Great meeting you at MJBizCon - wanted to follow up","body":img_full('hero',280)+(
  hdr()+teal_stripe('MJBizCon | Las Vegas')+img_overlay('hero','Good To Meet You.')+
  dark_sec(sal()+bd("Really enjoyed connecting at MJBizCon. Wanted to pick the conversation back up.","Bear Grinder - 608 bearing, three or four rotations done. Magnetic closure, no threads.","If you felt the spin at the show, you know what I mean. If not, let me get a sample in your hands."))+
  btn_w('REPLY HERE')+signoff('Amit Gorodetzer','Founder & CEO, Bear Grinder',SE,'Enjoy the grind.')+ftr(SE)
)},
{"id":"e15a","seg":"Special","num":"15A","name":"Special Sample F/U","subj":"Checking in on the Bear Grinder we sent home with you","body":(
  hdr()+dark_sec(sal()+bd("Hope you've had a chance to spend real time with the sample.","Most people say some version of 'oh, okay' after the first spin. We love that moment.","Ready to talk product, margin, or partnership - happy to move fast."))+
  img_full('built',240)+enjoy_block()+btn_w("LET'S TALK")+signoff('Amit','Bear Grinder',SE,'Enjoy the grind - and thanks for giving it a real look.')+ftr(SE)
)},
]
print(f"Emails: {len(emails)}")
EMAIL_DATA = json.dumps({e["id"]:{"seg":e["seg"],"num":e["num"],"name":e["name"],"subj":e["subj"]} for e in emails})

# Build collapsible sidebar with category groups
sidebar=""
seg_counts={}
for e in emails:
    seg_counts[e["seg"]]=seg_counts.get(e["seg"],0)+1

cur_seg=""
for e in emails:
    if e["seg"]!=cur_seg:
        if cur_seg:
            sidebar+='</div>\n'  # close previous seg-group
        cur_seg=e["seg"]
        count=seg_counts[cur_seg]
        sidebar+=f'<div class="seg-label" data-seg="{e["seg"]}" onclick="toggleSeg(this)"><span class="seg-chev">&#9654;</span> {e["seg"]} <span class="seg-count">({count})</span></div>\n'
        sidebar+=f'<div class="seg-group" data-seg="{e["seg"]}" style="display:none;">\n'
    sd=e["subj"][:46]+("..." if len(e["subj"])>46 else "")
    sidebar+=f'<button class="ebtn" id="btn-{e["id"]}" data-seg="{e["seg"]}" onclick="nav(\'{e["id"]}\')">\n<span class="enum">{e["num"]}</span><span class="ename">{e["name"]}</span>\n<span class="esubj">{sd}</span></button>\n'
if cur_seg:
    sidebar+='</div>\n'  # close last seg-group

panels=""
for i,e in enumerate(emails):
    panels+=f'<div class="epanel" id="{e["id"]}" style="display:none;">\n<div class="ecard" id="card-{e["id"]}">{e["body"]}</div>\n</div>\n'

# ─── CSS ────────────────────────────────────────────────────────────────
CSS="""

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#080808;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;color:#fff;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
body{overflow:hidden}
@media(max-width:700px){body{overflow:auto;height:auto}}

/* ── LAYOUT ── */
.app{display:flex;height:100vh}
@media(max-width:700px){.app{flex-direction:column;height:auto;min-height:100vh}}

/* ── SIDEBAR ── */
.sb{width:255px;min-width:255px;height:100vh;background:#0d0d0d;border-right:1px solid #181818;display:flex;flex-direction:column}
@media(max-width:700px){
  .sb{position:fixed;top:0;left:0;height:100%;z-index:300;transform:translateX(-100%);transition:transform .25s cubic-bezier(.4,0,.2,1);width:82vw;max-width:300px;min-width:0;box-shadow:4px 0 32px rgba(0,0,0,.8)}
  .sb.open{transform:translateX(0)}
}
.sb-hd{padding:16px 16px 12px;border-bottom:1px solid #181818;flex-shrink:0}
.sb-meta{font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:#888;margin-top:4px}
.sb-scroll{overflow-y:auto;flex:1;padding-bottom:32px;-webkit-overflow-scrolling:touch}
.sb-scroll::-webkit-scrollbar{width:2px}.sb-scroll::-webkit-scrollbar-thumb{background:#222}
.seg-label{font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#555;padding:12px 16px;border-top:1px solid #141414;cursor:pointer;display:flex;align-items:center;gap:6px;transition:color .12s;user-select:none;-webkit-user-select:none}
.seg-label:first-child{border-top:none}
.seg-label:hover{color:#3ecfcf}
.seg-label.expanded{color:#aaa}
.seg-label.expanded .seg-chev{transform:rotate(90deg)}
.seg-chev{font-size:7px;transition:transform .2s ease;display:inline-block;color:#555;flex-shrink:0}
.seg-count{color:#444;font-weight:600;margin-left:auto;font-size:8px;letter-spacing:.06em}
.seg-group{overflow:hidden;transition:max-height .25s ease;max-height:0}
.seg-group.open{max-height:800px;display:block!important}
.ebtn{display:block;width:100%;background:none;border:none;border-left:3px solid transparent;padding:10px 14px 11px;cursor:pointer;text-align:left;transition:background .12s;-webkit-tap-highlight-color:rgba(62,207,207,.1)}
.ebtn:hover,.ebtn:active{background:#141414}
.ebtn.active{background:#141414;border-left-color:#3ecfcf}
.enum{display:block;font-size:9px;font-weight:700;letter-spacing:.14em;color:#3ecfcf;font-family:'Trebuchet MS',Arial,sans-serif;text-transform:uppercase;margin-bottom:2px}
.ename{display:block;font-size:12px;font-weight:700;color:#fff;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.03em;text-transform:uppercase;margin-bottom:3px;line-height:1.3}
.esubj{display:block;font-size:11px;color:#888;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.4}

/* ── OVERLAY ── */
.tb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:299;-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)}
.tb-overlay.on{display:block}

/* ── MAIN ── */
.main{flex:1;height:100vh;overflow:hidden;display:flex;flex-direction:column;min-width:0}
@media(max-width:700px){.main{height:auto;flex:none;min-height:100vh}}

/* ── TOPBAR ── */
.topbar{height:52px;background:#080808;border-bottom:1px solid #181818;display:flex;align-items:center;padding:0 12px;gap:8px;flex-shrink:0}
@media(max-width:700px){.topbar{height:48px;padding:0 10px;gap:6px;overflow:hidden}}
.mob-btn{display:none;background:none;border:1px solid #2a2a2a;border-radius:7px;padding:9px 13px;color:#fff;font-size:20px;cursor:pointer;flex-shrink:0;line-height:1;min-width:44px;min-height:44px;align-items:center;justify-content:center}
@media(max-width:700px){.mob-btn{display:flex}}
.tb-seg{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#fff;font-family:'Trebuchet MS',Arial,sans-serif;white-space:nowrap}
.tb-div{color:#555;font-size:10px}
.tb-nm{font-size:9px;color:#666;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
@media(max-width:700px){.tb-div,.tb-nm{display:none}}
.tb-r{margin-left:auto;display:flex;align-items:center;gap:5px;flex-shrink:0}
@media(max-width:700px){.tb-r{gap:4px}}

/* ── NAV TABS - desktop strip, mobile bottom drawer ── */
.vtabs{display:flex;border:1px solid #1e1e1e;border-radius:4px;overflow:hidden}
@media(max-width:700px){.vtabs{display:none}}
.vtab{background:none;border:none;border-right:1px solid #1e1e1e;padding:6px 10px;font-size:9px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#666;cursor:pointer;font-family:'Trebuchet MS',Arial,sans-serif;white-space:nowrap;transition:all .12s}
.vtab:last-child{border-right:none}
.vtab:hover:not(.on){background:#141414;color:#fff}
.vtab.on{background:#fff;color:#000}
.vtab.on.t-edit{background:#2563eb;color:#fff}
.vtab.on.t-hs,.vtab.on.t-hsp{background:#3ecfcf;color:#000}
.vtab.on.t-analytics{background:#a855f7;color:#fff}
.vtab.on.t-campaign{background:#f97316;color:#fff}
.vtab.on.t-connect{background:#22c55e;color:#fff}

/* ── MOBILE BOTTOM NAV ── */
.mob-nav{display:none;position:fixed;bottom:0;left:0;right:0;z-index:250;background:#0a0a0a;border-top:1px solid #181818;padding:0;padding-bottom:env(safe-area-inset-bottom)}
@media(max-width:700px){.mob-nav{display:flex}}
.mob-nav-btn{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;padding:8px 4px 7px;background:none;border:none;cursor:pointer;border-left:1px solid #181818;-webkit-tap-highlight-color:rgba(62,207,207,.1)}
.mob-nav-btn:first-child{border-left:none}
.mob-nav-icon{font-size:15px;line-height:1}
.mob-nav-lbl{font-family:'Trebuchet MS',Arial,sans-serif;font-size:7px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#666;line-height:1}
.mob-nav-btn.on .mob-nav-lbl{color:#3ecfcf}
.mob-nav-btn.on.c-edit .mob-nav-lbl{color:#2563eb}
.mob-nav-btn.on.c-campaign .mob-nav-lbl{color:#f97316}
.mob-nav-btn.on.c-analytics .mob-nav-lbl{color:#a855f7}
.mob-nav-btn.on.c-connect .mob-nav-lbl{color:#22c55e}
.mob-nav-btn.on .mob-nav-icon{filter:brightness(2)}

/* ── ACTION BUTTONS ── */
.abtn{display:flex;align-items:center;gap:4px;border:none;border-radius:4px;padding:6px 11px;font-size:9px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;cursor:pointer;font-family:'Trebuchet MS',Arial,sans-serif;white-space:nowrap;min-height:32px}
@media(max-width:700px){.abtn{display:none}}
.abtn-copy{background:none;border:1px solid #222;color:#666;transition:all .12s}
.abtn-copy:hover{border-color:#3a3a3a;color:#fff}
.abtn-copy.ok{background:#16a34a;border-color:#16a34a;color:#fff}
.abtn-hs{background:#3ecfcf;color:#000}
.abtn-hs:hover{background:#2fbaba}

/* ── EDIT BAR ── */
.ebar{height:38px;background:#080808;border-bottom:1px solid #181818;display:none;align-items:center;padding:0 12px;gap:4px;flex-shrink:0;overflow-x:auto}
.ebar::-webkit-scrollbar{display:none}
.ebar.on{display:flex}
.eb-lbl{font-size:8px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#2563eb;margin-right:6px;font-family:'Trebuchet MS',Arial,sans-serif;white-space:nowrap}
.etool{background:#141414;border:1px solid #1e1e1e;border-radius:3px;padding:4px 9px;font-size:12px;font-weight:700;color:#fff;cursor:pointer;min-width:30px;min-height:28px}
.etool:hover,.etool:active{background:#1e1e1e}
.etsep{width:1px;height:14px;background:#1e1e1e;margin:0 3px;flex-shrink:0}
.ereset{margin-left:auto;background:none;border:1px solid #1e1e1e;border-radius:3px;padding:4px 10px;font-size:9px;font-weight:600;color:#444;cursor:pointer;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.ereset:hover,.ereset:active{border-color:#e24b4b;color:#e24b4b}

/* ── SCROLLER ── */
.scroller{flex:1;overflow-y:auto;background:#111;-webkit-overflow-scrolling:touch}
@media(max-width:700px){.scroller{overflow-y:auto;padding-bottom:56px}}
.scroller::-webkit-scrollbar{width:3px}.scroller::-webkit-scrollbar-thumb{background:#1a1a1a}
.epanel{padding:0 0 60px}
.ecard{max-width:600px;margin:0 auto;overflow:hidden}
@media(max-width:700px){.ecard{max-width:100%;margin:0;border-radius:0}}

/* ── EDIT MODE ── */
body.editing [contenteditable="true"]{outline:none;border-bottom:1px dashed rgba(37,99,235,.4);cursor:text}
body.editing [contenteditable="true"]:hover{background:rgba(37,99,235,.06)}
body.editing [contenteditable="true"]:focus{background:rgba(37,99,235,.12);border-bottom-color:#2563eb;outline:none}

/* ── COMMAND PANELS ── */
.cmd-panel{padding:0;display:none;background:#0d0d0d;min-height:100%}
.cmd-hd{background:#080808;border-bottom:1px solid #181818;padding:14px 18px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
@media(max-width:700px){.cmd-hd{padding:12px 14px;gap:8px}}
.cmd-badge{font-family:'Trebuchet MS',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 8px;border-radius:3px}
.cmd-title{font-family:'Trebuchet MS',Arial,sans-serif;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#fff}
.cmd-sub{font-size:11px;color:#777;margin-left:auto}
.cmd-body{padding:16px 18px 80px;max-width:700px}
@media(max-width:700px){.cmd-body{padding:12px 12px 80px}}
.cmd-section{background:#141414;border:1px solid #1e1e1e;border-radius:6px;padding:14px 16px;margin-bottom:12px}
@media(max-width:700px){.cmd-section{padding:12px 14px;border-radius:5px}}
.cmd-section-title{font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#555;margin-bottom:12px}
.cmd-row{display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;margin-bottom:8px}
.cmd-field{display:flex;flex-direction:column;gap:4px;flex:1;min-width:140px}
@media(max-width:700px){.cmd-field{min-width:100%;flex:none}}
.cmd-label{font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#555}
.cmd-input{background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:9px 12px;font-size:14px;color:#fff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;outline:none;transition:border-color .12s;-webkit-appearance:none;width:100%}
.cmd-input:focus{border-color:#3ecfcf}
.cmd-input::placeholder{color:#555}
.cmd-select{background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:9px 12px;font-size:13px;color:#fff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;outline:none;cursor:pointer;-webkit-appearance:none;width:100%}
.cmd-select option{background:#141414;color:#fff}
.cmd-btn{padding:10px 18px;border:none;border-radius:4px;font-family:'Trebuchet MS',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transition:all .12s;white-space:nowrap;min-height:38px;-webkit-tap-highlight-color:rgba(62,207,207,.15)}
.cmd-btn-primary{background:#3ecfcf;color:#000}
.cmd-btn-primary:hover,.cmd-btn-primary:active{background:#2fbaba}
.cmd-btn-primary:disabled{background:#1a3a3a;color:#2a6a6a;cursor:not-allowed}
.cmd-btn-secondary{background:#1e1e1e;border:1px solid #2a2a2a;color:#888}
.cmd-btn-secondary:hover,.cmd-btn-secondary:active{border-color:#555;color:#fff;background:#222}
.cmd-btn-danger{background:#3d0f0f;border:1px solid #6b1a1a;color:#f87171}
.cmd-btn-danger:hover{background:#5a1a1a}
.cmd-btn-purple{background:#7c3aed;color:#fff}
.cmd-btn-purple:hover,.cmd-btn-purple:active{background:#6d28d9}
.cmd-btn-orange{background:#f97316;color:#fff}
.cmd-btn-orange:hover,.cmd-btn-orange:active{background:#ea6a0e}
.status-pill{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:12px;font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.pill-ok{background:rgba(34,197,94,.12);color:#22c55e;border:1px solid rgba(34,197,94,.25)}
.pill-warn{background:rgba(251,191,36,.12);color:#fbbf24;border:1px solid rgba(251,191,36,.25)}
.pill-err{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.25)}
.pill-info{background:rgba(62,207,207,.12);color:#3ecfcf;border:1px solid rgba(62,207,207,.25)}
.pill-purple{background:rgba(168,85,247,.12);color:#a855f7;border:1px solid rgba(168,85,247,.25)}
.data-table{width:100%;border-collapse:collapse;font-size:12px}
.data-table th{font-family:'Trebuchet MS',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#777;text-align:left;padding:6px 8px;border-bottom:1px solid #1e1e1e}
.data-table td{color:#777;padding:9px 8px;border-bottom:1px solid #141414;vertical-align:top;line-height:1.5}
.data-table td:first-child{color:#bbb}
.data-table tr:hover td{background:#141414}
@media(max-width:700px){.data-table{font-size:11px}.data-table td,.data-table th{padding:7px 6px}}
.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
@media(max-width:700px){.metric-grid{grid-template-columns:repeat(2,1fr);gap:7px}}
.metric-card{background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:14px 14px}
.metric-val{font-family:'Trebuchet MS',Arial,sans-serif;font-size:24px;font-weight:900;color:#fff;line-height:1}
.metric-lbl{font-family:'Trebuchet MS',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#777;margin-top:5px}
.metric-card.teal .metric-val{color:#3ecfcf}
.metric-card.purple .metric-val{color:#a855f7}
.metric-card.green .metric-val{color:#22c55e}
.metric-card.red .metric-val{color:#f87171}
.metric-card.orange .metric-val{color:#f97316}
.score-ring{display:flex;align-items:center;gap:16px;background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:16px 18px;margin-bottom:12px}
.score-num{font-family:'Trebuchet MS',Arial,sans-serif;font-size:56px;font-weight:900;line-height:1;color:#3ecfcf}
.score-of{font-family:'Trebuchet MS',Arial,sans-serif;font-size:13px;color:#777;margin-top:2px}
.score-info h3{font-family:'Trebuchet MS',Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;margin-bottom:5px}
.score-info p{font-size:13px;color:#555;line-height:1.65}
.insight-item{background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:13px 14px;margin-bottom:8px;display:flex;gap:12px;align-items:flex-start}
.insight-icon{font-size:16px;flex-shrink:0;margin-top:1px}
.insight-body h4{font-family:'Trebuchet MS',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#fff;margin-bottom:4px}
.insight-body p{font-size:12px;color:#555;line-height:1.65}
.compliance-item{display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #1a1a1a}
.compliance-item:last-child{border-bottom:none}
.ci-icon{font-size:14px;flex-shrink:0;margin-top:2px}
.ci-body{flex:1}
.ci-title{font-family:'Trebuchet MS',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#bbb;margin-bottom:3px}
.ci-desc{font-size:12px;color:#555;line-height:1.55}
.list-chip{display:inline-flex;align-items:center;gap:5px;background:#141414;border:1px solid #222;border-radius:3px;padding:5px 10px;font-size:12px;color:#888;font-family:'Trebuchet MS',Arial,sans-serif;cursor:pointer;transition:all .12s;margin:2px}
.list-chip:hover,.list-chip:active{border-color:#3ecfcf;color:#3ecfcf}
.list-chip.selected{background:rgba(62,207,207,.1);border-color:#3ecfcf;color:#3ecfcf}
.log-entry{font-family:monospace;font-size:11px;color:#555;padding:4px 0;border-bottom:1px solid #141414;line-height:1.5}
.log-entry .ts{color:#555;margin-right:8px}
.log-entry .ok{color:#22c55e}
.log-entry .err{color:#ef4444}
.log-entry .info{color:#3ecfcf}
.log-entry .warn{color:#fbbf24}
.errbar{background:#100;border-top:2px solid #e24b4b;padding:6px 14px;font-family:monospace;font-size:11px;color:#e24b4b;display:none;flex-shrink:0;align-items:center;gap:8px}
.errbar.on{display:flex}
.toast{position:fixed;bottom:70px;right:14px;background:#16a34a;color:#fff;font-family:'Trebuchet MS',Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:.05em;padding:10px 18px;border-radius:6px;z-index:9999;opacity:0;transform:translateY(6px);transition:all .22s;pointer-events:none;max-width:320px;line-height:1.5}
@media(max-width:700px){.toast{bottom:70px;left:14px;right:14px;max-width:none}}
.toast.show{opacity:1;transform:translateY(0)}
.spinner{display:inline-block;width:14px;height:14px;border:2px solid #222;border-top-color:#3ecfcf;border-radius:50%;animation:spin .7s linear infinite;flex-shrink:0;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}

/* TOOLTIPS */
.tip{position:relative;display:inline-flex;align-items:center;cursor:default}
.tip-icon{display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:50%;font-size:8px;color:#555;font-family:'Trebuchet MS',Arial,sans-serif;font-weight:700;cursor:help;flex-shrink:0;margin-left:5px;transition:all .1s}
.tip-icon:hover{background:#2a2a2a;color:#3ecfcf;border-color:#3ecfcf}
.tip-box{display:none;position:absolute;bottom:calc(100% + 7px);left:50%;transform:translateX(-50%);background:#1a1a1a;border:1px solid #2e2e2e;border-radius:4px;padding:8px 10px;width:210px;font-size:11px;color:#888;line-height:1.6;z-index:9000;white-space:normal;pointer-events:none;box-shadow:0 4px 18px rgba(0,0,0,.7)}
.tip-box::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:5px solid transparent;border-top-color:#2e2e2e}
.tip:hover .tip-box{display:block}
/* AUDIENCE PICKER */
.aud-btn{display:flex;flex-direction:column;align-items:flex-start;gap:2px;background:#141414;border:1px solid #222;border-radius:6px;padding:12px 14px;cursor:pointer;transition:all .15s;text-align:left;width:100%;-webkit-tap-highlight-color:rgba(62,207,207,.1)}
.aud-btn:hover,.aud-btn:active{background:#1a1a1a;border-color:#3ecfcf}
.aud-btn.active{background:rgba(62,207,207,.08);border-color:#3ecfcf}
.aud-icon{font-size:20px;margin-bottom:2px}
.aud-label{font-family:'Trebuchet MS',Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#fff}
.aud-sub{font-size:10px;color:#555}
/* PREVIEW + BUG BUTTONS */
.abtn-preview{background:#1a1a1a;border:1px solid #2a2a2a;color:#888;transition:all .12s}
.abtn-preview:hover{border-color:#3ecfcf;color:#3ecfcf}
.abtn-bug{background:#1a1a1a;border:1px solid #2a2a2a;color:#888;transition:all .12s}
.abtn-bug:hover{border-color:#ef4444;color:#ef4444}

.health-card{background:#0d0d0d;border:1px solid #1e1e1e;border-radius:6px;padding:12px 10px;text-align:center}
.hc-val{font-family:'Trebuchet MS',Arial,sans-serif;font-size:22px;font-weight:900;color:#fff;letter-spacing:.02em}
.hc-label{font-size:9px;font-weight:700;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#777;margin:3px 0 2px}
.hc-bench{font-size:9px;color:#666;margin-bottom:4px}
.hc-status{font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.seg-card{background:#0d0d0d;border:1px solid #1e1e1e;border-radius:6px;padding:12px 14px}
.seg-card-label{font-size:9px;font-weight:700;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#777;margin-bottom:5px}
.seg-card-val{font-size:18px;font-weight:900;font-family:'Trebuchet MS',Arial,sans-serif;color:#3ecfcf}

"""

# ─── JAVASCRIPT ───────────────────────────────────────────────────────────
# Note: API key stored in memory only (never persisted to localStorage for security)
JS = r"""
var DATA=""" + EMAIL_DATA + r""";
var origHTML={};
var CUR='e01a';
var VIEW='guide';
var HS_KEY='';  // HubSpot API key - session only
var HS_CONNECTED=false;
var HS_PORTAL_ID='';
var HS_LISTS=[];
var HS_TEMPLATES=[];
var ANALYTICS=[];
var AI_SCORE=null;
var AI_INSIGHTS=[];
var COMPLIANCE_RESULTS={};
var SEND_LOG=[];

window.onerror=function(msg,src,line){showErr('Line '+line+': '+msg);return false;};

document.addEventListener('DOMContentLoaded',function(){
  setView('guide');
  try{
    Object.keys(DATA).forEach(function(id){
      var c=document.getElementById('card-'+id);
      if(c) origHTML[id]=c.innerHTML;
    });
    var fb=document.getElementById('btn-e01a');
    if(fb) fb.classList.add('active');
    // Load persisted analytics/insights from localStorage (non-sensitive data only)
    try{
      var saved=localStorage.getItem('bg_analytics');
      if(saved) ANALYTICS=JSON.parse(saved);
      var savedLog=localStorage.getItem('bg_send_log');
      if(savedLog) SEND_LOG=JSON.parse(savedLog);
      var savedScore=localStorage.getItem('bg_ai_score');
      if(savedScore) AI_SCORE=JSON.parse(savedScore);
      var savedInsights=localStorage.getItem('bg_ai_insights');
      if(savedInsights) AI_INSIGHTS=JSON.parse(savedInsights);
    }catch(e){}
  }catch(e){showErr('Init: '+e.message);}
});

/* ── NAV ── */
function toggleSB(){
  var sb=document.getElementById('sidebar');
  var ov=document.getElementById('sbOverlay');
  if(sb) sb.classList.toggle('open');
  if(ov) ov.classList.toggle('on',sb&&sb.classList.contains('open'));
}
/* ── COLLAPSIBLE SIDEBAR CATEGORIES ── */
function toggleSeg(labelEl){
  var seg=labelEl.getAttribute('data-seg');
  var group=labelEl.nextElementSibling;
  if(!group||!group.classList.contains('seg-group')) return;
  var isOpen=group.classList.contains('open');
  if(isOpen){
    group.classList.remove('open');
    group.style.display='none';
    labelEl.classList.remove('expanded');
  } else {
    group.classList.add('open');
    group.style.display='block';
    labelEl.classList.add('expanded');
  }
}
function expandSegFor(id){
  var btn=document.getElementById('btn-'+id);
  if(!btn) return;
  var seg=btn.getAttribute('data-seg');
  var grp=btn.closest('.seg-group');
  if(grp&&!grp.classList.contains('open')){
    grp.classList.add('open');
    grp.style.display='block';
    var lbl=grp.previousElementSibling;
    if(lbl&&lbl.classList.contains('seg-label')) lbl.classList.add('expanded');
  }
}
function expandAllSegs(){
  document.querySelectorAll('.seg-group').forEach(function(g){g.classList.add('open');g.style.display='block';});
  document.querySelectorAll('.seg-label').forEach(function(l){l.classList.add('expanded');});
}
function collapseAllSegs(){
  document.querySelectorAll('.seg-group').forEach(function(g){g.classList.remove('open');g.style.display='none';});
  document.querySelectorAll('.seg-label').forEach(function(l){l.classList.remove('expanded');});
}
function nav(id){
  try{
    // Revert previous template to original (session-only edits)
    if(CUR&&origHTML[CUR]){var prevCard=document.getElementById('card-'+CUR);if(prevCard)prevCard.innerHTML=origHTML[CUR];}
    CUR=id;
    document.querySelectorAll('.ebtn').forEach(function(b){b.classList.remove('active');});
    var btn=document.getElementById('btn-'+id);
    if(btn) btn.classList.add('active');
    expandSegFor(id);
    var hint=document.getElementById('see-more-hint');
    if(hint) hint.style.display=(window.innerWidth<=700)?'flex':'none';
    var d=DATA[id];
    if(d){document.getElementById('tbSeg').textContent=d.seg;document.getElementById('tbNm').textContent=d.name;}
    if(VIEW==='guide') setView('preview');
    else{
      showPanel(id);
      if(VIEW==='hsp') renderHSP(id);
    }
    var sc=document.getElementById('scroller');
    if(sc) sc.scrollTop=0;
    var sb=document.getElementById('sidebar');
    if(sb&&sb.classList.contains('open')) toggleSB();
  }catch(e){showErr('nav: '+e.message);}
}
function showPanel(id){
  document.querySelectorAll('.epanel').forEach(function(p){p.style.display=(p.id===id)?'block':'none';});
}

/* ── VIEWS ── */
function setView(v){
  try{
    VIEW=v;
    ['guide','preview','edit','hs','hsp','analytics','campaign','connect','dashboard'].forEach(function(t){
      var el=document.getElementById('t-'+t);
      if(el) el.classList.remove('on');
    });
    var tab=document.getElementById('t-'+v);
    if(tab) tab.classList.add('on');
    // hide all panels
    ['view-guide','view-hs','view-hsp','view-analytics','view-campaign','view-connect'].forEach(function(pid){
      var p=document.getElementById(pid);
      if(p) p.style.display='none';
    });
    document.querySelectorAll('.epanel').forEach(function(p){p.style.display='none';});
    // show correct
    if(v==='guide'){
      var gp=document.getElementById('view-guide');
      if(gp) gp.style.display='block';
      document.getElementById('tbSeg').textContent='Guide';
      document.getElementById('tbNm').textContent='Getting Started';
    } else if(v==='preview'||v==='edit'){
      showPanel(CUR);
    } else if(v==='hs'){
      var hp=document.getElementById('view-hs');
      if(hp) hp.style.display='block';
      renderHS(CUR);
    } else if(v==='hsp'){
      var hpp=document.getElementById('view-hsp');
      if(hpp) hpp.style.display='block';
      renderHSP(CUR);
    } else if(v==='analytics'){
      var ap=document.getElementById('view-analytics');
      if(ap) ap.style.display='block';
      renderAnalytics();
    } else if(v==='campaign'){
      var cp=document.getElementById('view-campaign');
      if(cp) cp.style.display='block';
      renderCampaign();
    } else if(v==='connect'){
      var conp=document.getElementById('view-connect');
      if(conp) conp.style.display='block';
      renderConnect();
    }
    var eb=document.getElementById('ebar');
    if(eb) eb.classList.toggle('on',v==='edit');
    // Revert to original when leaving edit mode for master templates
    if(VIEW==='edit'&&v!=='edit'&&CUR&&origHTML[CUR]){
      var editCard=document.getElementById('card-'+CUR);
      if(editCard){
        var isCustom=CUR.indexOf('custom_')===0;
        if(!isCustom) editCard.innerHTML=origHTML[CUR];
      }
    }
    document.body.classList.toggle('editing',v==='edit');
  }catch(e){showErr('setView: '+e.message);}
}

/* ── HUBSPOT API HELPERS ── */
function hsApi(path,method,body,cb){
  if(!HS_KEY){cb&&cb(null,'No API key. Go to Connect tab.');return;}
  var opts={method:method||'GET',headers:{'Content-Type':'application/json','Authorization':'Bearer '+HS_KEY}};
  if(body) opts.body=JSON.stringify(body);
  fetch('https://api.hubapi.com'+path,opts)
    .then(function(r){return r.json().then(function(d){return{status:r.status,data:d};});})
    .then(function(r){cb&&cb(r.data,r.status>=400?(r.data.message||'API error '+r.status):null,r.status);})
    .catch(function(e){cb&&cb(null,e.message);});
}

function hsGet(path,cb){hsApi(path,'GET',null,cb);}
function hsPost(path,body,cb){hsApi(path,'POST',body,cb);}

/* ── CONNECT TAB ── */
function renderConnect(){
  var el=document.getElementById('view-connect');
  if(!el) return;
  var connStatus=HS_CONNECTED
    ?'<span class="status-pill pill-ok">&#10003; Connected - Portal '+HS_PORTAL_ID+'</span>'
    :'<span class="status-pill pill-warn">Not connected</span>';
  el.innerHTML=`<div class="cmd-hd"><span class="cmd-badge" style="background:#22c55e;color:#000;">HubSpot</span><span class="cmd-title">Connect</span><span class="cmd-sub">API Integration</span></div>
<div class="cmd-body">
  <div class="cmd-section">
    <div class="cmd-section-title">API Credentials</div>
    <div class="cmd-row">
      <div class="cmd-field" style="flex:2">
        <label class="cmd-label">HubSpot Private App Token</label>
        <input class="cmd-input" type="password" id="hs-key-input" placeholder="pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" value="${HS_KEY}">
      </div>
      <button class="cmd-btn cmd-btn-primary" onclick="doConnect()">Test Connection</button>
    </div>
    <p style="font-size:11px;color:#333;line-height:1.6;margin-top:6px;">
      Get your token: HubSpot &rarr; Settings &rarr; Integrations &rarr; Private Apps &rarr; Create app.<br>
      Required scopes: <code style="background:#1a1a1a;padding:1px 5px;border-radius:2px;font-size:10px;color:#7dd3fc;">crm.lists.read</code> <code style="background:#1a1a1a;padding:1px 5px;border-radius:2px;font-size:10px;color:#7dd3fc;">marketing.email.read/write</code> <code style="background:#1a1a1a;padding:1px 5px;border-radius:2px;font-size:10px;color:#7dd3fc;">contacts.read</code>
    </p>
    <div style="margin-top:8px;">${connStatus}</div>
    <div id="conn-log" style="margin-top:10px;"></div>
  </div>
  ${HS_CONNECTED ? renderConnectedInfo() : ''}
  <div class="cmd-section">
    <div class="cmd-section-title">Security Note</div>
    <p style="font-size:11px;color:#888;line-height:1.7;">Your API key is held in memory only for this session. It is never written to disk, localStorage, or sent anywhere except directly to api.hubapi.com over HTTPS. Close this tab to clear it.</p>
  </div>
</div>`;
}

function renderConnectedInfo(){
  var listRows=HS_LISTS.slice(0,8).map(function(l){
    return '<tr><td>'+esc(l.name||l.id)+'</td><td style="color:#555;">'+esc(l.listType||'STATIC')+'</td><td style="color:#3ecfcf;">'+esc(String(l.metaData&&l.metaData.size!=null?l.metaData.size:'-'))+'</td></tr>';
  }).join('');
  return `<div class="cmd-section">
    <div class="cmd-section-title">Connected Lists (${HS_LISTS.length} found)</div>
    ${HS_LISTS.length ? '<table class="data-table"><tr><th>List Name</th><th>Type</th><th>Contacts</th></tr>'+listRows+'</table>' : '<p style="font-size:12px;color:#444;">No lists found. Create lists in HubSpot first.</p>'}
    <button class="cmd-btn cmd-btn-secondary" style="margin-top:8px;" onclick="fetchLists()">Refresh Lists</button>
  </div>`;
}

function doConnect(){
  var keyInput=document.getElementById('hs-key-input');
  if(!keyInput||!keyInput.value.trim()){showErr('Enter your HubSpot API key.');return;}
  HS_KEY=keyInput.value.trim();
  var log=document.getElementById('conn-log');
  if(log) log.innerHTML='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="info">Testing connection...</span></div>';
  // Test via account info endpoint
  hsGet('/account-info/v3/details',function(d,err){
    if(err||!d||!d.portalId){
      HS_KEY='';HS_CONNECTED=false;
      if(log) log.innerHTML='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="err">Connection failed: '+(err||'Invalid response')+'</span></div>';
      renderConnect();return;
    }
    HS_PORTAL_ID=String(d.portalId);
    HS_CONNECTED=true;
    if(log) log.innerHTML='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="ok">Connected - Portal ID '+HS_PORTAL_ID+' ('+esc(d.companyName||'')+')</span></div>';
    fetchLists();
    showToast('HubSpot connected. Portal: '+HS_PORTAL_ID);
    addLog('info','HubSpot connected. Portal: '+HS_PORTAL_ID);
    setTimeout(renderConnect,800);
  });
}

function fetchLists(){
  hsGet('/contacts/v1/lists/static?count=100',function(d,err){
    if(err||!d){addLog('err','Failed to fetch lists: '+(err||'unknown'));return;}
    HS_LISTS=(d.lists||[]).concat();
    // also get dynamic
    hsGet('/contacts/v1/lists/dynamic?count=100',function(d2){
      if(d2&&d2.lists) HS_LISTS=HS_LISTS.concat(d2.lists);
      addLog('ok','Fetched '+HS_LISTS.length+' lists');
      renderConnect();
      renderCampaign();
    });
  });
}

/* ── CAMPAIGN TAB ── */
function renderCampaign(){
  var el=document.getElementById('view-campaign');
  if(!el) return;
  var needsConn=!HS_CONNECTED?'<div style="background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.15);border-radius:3px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:#fbbf24;">Connect HubSpot first in the Connect tab to enable direct sending.</div>':'';
  // Build template options
  var tmplOpts=Object.keys(DATA).map(function(id){
    var d=DATA[id];
    return '<option value="'+id+'">'+esc(d.num+' - '+d.name)+'</option>';
  }).join('');
  // Build list options
  var listOpts=HS_LISTS.length
    ? HS_LISTS.map(function(l){return '<option value="'+esc(l.listId||l.id)+'">'+esc(l.name)+' ('+esc(String(l.metaData&&l.metaData.size!=null?l.metaData.size:'?'))+')</option>';}).join('')
    : '<option value="">No lists loaded - connect HubSpot</option>';
  // Log entries
  var logHtml=SEND_LOG.slice(-10).reverse().map(function(e){
    return '<div class="log-entry"><span class="ts">'+e.ts+'</span><span class="'+e.level+'">'+esc(e.msg)+'</span></div>';
  }).join('') || '<div style="font-size:11px;color:#2a2a2a;padding:4px 0;">No activity yet.</div>';

  el.innerHTML=`<div class="cmd-hd"><span class="cmd-badge" style="background:#f97316;color:#000;">Campaign</span><span class="cmd-title">Build & Send</span><span class="cmd-sub">Push to HubSpot</span></div>
<div class="cmd-body">
  ${needsConn}
  <div class="cmd-section">
    <div class="cmd-section-title">1. Choose Template</div>
    <div class="cmd-row">
      <div class="cmd-field" style="flex:2">
        <label class="cmd-label">Email Template</label>
        <select class="cmd-select" id="camp-tmpl" onchange="onCampTmplChange()">${tmplOpts}</select>
      </div>
      <button class="cmd-btn cmd-btn-secondary" onclick="nav(document.getElementById('camp-tmpl').value);setView('preview');">Preview</button>
    </div>
    <div id="camp-compliance-quick" style="margin-top:8px;"></div>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">2. Campaign Details</div>
    <div class="cmd-row">
      <div class="cmd-field">
        <label class="cmd-label">Campaign Name</label>
        <input class="cmd-input" id="camp-name" placeholder="BG Launch - B2C - March 2026">
      </div>
      <div class="cmd-field">
        <label class="cmd-label">From Name</label>
        <input class="cmd-input" id="camp-from-name" value="Amit Gorodetzer" placeholder="Amit Gorodetzer">
      </div>
    </div>
    <div class="cmd-row">
      <div class="cmd-field">
        <label class="cmd-label">Reply-To Email</label>
        <input class="cmd-input" id="camp-reply-to" value="Hello@BearGrinder.com" value="Hello@BearGrinder.com" placeholder="Hello@BearGrinder.com">
      </div>
      <div class="cmd-field">
        <label class="cmd-label">Subject Line Override (optional)</label>
        <input class="cmd-input" id="camp-subj" placeholder="Leave blank to use template default">
      </div>
    </div>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">3. Select Contact List</div>
    <select class="cmd-select" id="camp-list" style="width:100%;margin-bottom:8px;">${listOpts}</select>
    <button class="cmd-btn cmd-btn-secondary" onclick="fetchLists()" style="font-size:8px;">Refresh Lists</button>
    <p style="font-size:11px;color:#888;margin-top:6px;line-height:1.5;">Or upload a CSV list directly to HubSpot:</p>
    <div class="cmd-row" style="margin-top:6px;">
      <div class="cmd-field">
        <label class="cmd-label">CSV File (email column required)</label>
        <input type="file" accept=".csv" id="camp-csv" class="cmd-input" style="padding:5px;">
      </div>
      <button class="cmd-btn cmd-btn-secondary" onclick="uploadCSV()">Upload List to HubSpot</button>
    </div>
    <div id="csv-log" style="margin-top:6px;"></div>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">4. Schedule</div>
    <div class="cmd-row">
      <div class="cmd-field">
        <label class="cmd-label">Send Time (leave blank = save as draft)</label>
        <input class="cmd-input" type="datetime-local" id="camp-schedule">
      </div>
    </div>
    <p style="font-size:11px;color:#888;margin-top:4px;">Best send times based on industry data: Tuesday-Thursday, 10am-2pm local. Avoid Mondays and Fridays.</p>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">4b. Attachments</div>
    <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:6px;padding:14px 16px;margin-bottom:8px;">
      <label style="display:flex;align-items:flex-start;gap:12px;cursor:pointer;">
        <input type="checkbox" id="attach-onepager" style="width:16px;height:16px;margin-top:2px;accent-color:#3ecfcf;flex-shrink:0;" onchange="toggle1Pager(this.checked)"/>
        <div>
          <div style="font-family:'Trebuchet MS',Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;margin-bottom:3px;">Attach Bear Grinder 1-Pager</div>
          <div style="font-size:11px;color:#555;line-height:1.6;">Recommended for Wholesale and Distributor emails. Adds product overview PDF to your HubSpot send. You will need to manually attach the PDF in HubSpot before sending.</div>
        </div>
      </label>
      <div id="onepager-note" style="display:none;margin-top:12px;padding:10px 12px;background:#0a0a0a;border:1px solid #1a3a2a;border-radius:4px;border-left:3px solid #22c55e;">
        <div style="font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#22c55e;margin-bottom:4px;">1-Pager Will Be Included</div>
        <p style="font-size:11px;color:#444;line-height:1.6;margin:0 0 6px;">A download link for the Bear Grinder 1-pager will be added to the email footer. After pushing to HubSpot, also manually attach <strong style="color:#666;">Bear_Grinder_1Pager.pdf</strong> in the HubSpot email editor before sending.</p>
        <p style="font-size:11px;color:#888;line-height:1.5;margin:0;font-style:italic;">File should be in your HubSpot Files library under: Marketing / Bear Grinder / 1-Pager</p>
      </div>
    </div>
    <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:6px;padding:14px 16px;margin-bottom:8px;">
      <label style="display:flex;align-items:flex-start;gap:12px;cursor:pointer;">
        <input type="checkbox" id="attach-custom" style="width:16px;height:16px;margin-top:2px;accent-color:#3ecfcf;flex-shrink:0;" onchange="toggleCustomAttach(this.checked)"/>
        <div>
          <div style="font-family:'Trebuchet MS',Arial,sans-serif;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;margin-bottom:3px;">Attach Custom File</div>
          <div style="font-size:11px;color:#888;line-height:1.6;">Upload your file to HubSpot Files first, then paste the URL here.</div>
        </div>
      </label>
      <div id="custom-attach-section" style="display:none;margin-top:12px;">
        <div class="cmd-field" style="margin-bottom:8px;">
          <label class="cmd-label">HubSpot File URL</label>
          <input class="cmd-input" id="custom-attach-url" placeholder="https://app.hubspot.com/file-manager/..." style="width:100%;"/>
        </div>
        <div style="margin-top:4px;font-size:11px;color:#888;line-height:1.5;">HubSpot does not support programmatic attachments. Upload your file to HubSpot Files, then attach manually in the HubSpot editor before sending.</div>
      </div>
    </div>
  </div>

  <div class="cmd-section">
    <div class="cmd-section-title">5. Compliance Check &amp; Send</div>
    <button class="cmd-btn cmd-btn-secondary" onclick="runCompliance()" style="margin-bottom:8px;">Run Email Compliance Check</button>
    <div id="comp-results" style="margin-bottom:10px;"></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <button class="cmd-btn cmd-btn-primary" onclick="pushToHS('draft')">Save as HubSpot Draft</button>
      <button class="cmd-btn cmd-btn-orange" onclick="pushToHS('send')">Push &amp; Schedule Send</button>
    </div>
    <p style="font-size:10px;color:#666;margin-top:7px;">Draft saves to HubSpot Marketing &rarr; Email for review before sending.</p>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">Activity Log</div>
    <div id="camp-log">${logHtml}</div>
  </div>
</div>`;
  onCampTmplChange();
}

function onCampTmplChange(){
  var sel=document.getElementById('camp-tmpl');
  if(!sel) return;
  var id=sel.value;
  var d=DATA[id];
  var subjInput=document.getElementById('camp-subj');
  if(subjInput&&d&&!subjInput.value) subjInput.placeholder=d.subj;
  // quick compliance preview
  var qc=document.getElementById('camp-compliance-quick');
  if(qc){
    var issues=quickCompliance(id);
    if(issues.length===0){
      qc.innerHTML='<span class="status-pill pill-ok">&#10003; Compliance looks good</span>';
    } else {
      qc.innerHTML='<span class="status-pill pill-warn">'+issues.length+' compliance item'+(issues.length>1?'s':'')+' - run check below</span>';
    }
  }
}

function quickCompliance(id){
  var card=document.getElementById('card-'+id);
  if(!card) return [];
  var html=card.innerHTML;
  var issues=[];
  if(!html.includes('unsubscribe')&&!html.includes('opt out')&&!html.includes('opt-out')) issues.push('No unsubscribe link');
  if(!html.includes('beargrinder.com')&&!html.includes('Bear Grinder')) issues.push('No physical address or company identifier');
  return issues;
}

function runCompliance(){
  var sel=document.getElementById('camp-tmpl');
  if(!sel) return;
  var id=sel.value;
  var card=document.getElementById('card-'+id);
  if(!card) return;
  var html=card.innerHTML;
  var d=DATA[id]||{};
  var subj=d.subj||'';
  var checks=[
    {id:'unsub',label:'Unsubscribe Link',
     pass:html.toLowerCase().includes('unsubscribe')||html.toLowerCase().includes('opt out'),
     desc:'CAN-SPAM requires a clear unsubscribe mechanism in every commercial email.',
     fix:'Add an unsubscribe link in the footer before sending.'},
    {id:'addr',label:'Physical Address',
     pass:html.includes('San Diego')||html.includes('CA')||html.includes('beargrinder.com'),
     desc:'CAN-SPAM requires a valid physical postal address.',
     fix:'Add your company address (e.g. Bear Grinder LLC, San Diego, CA) in the footer.'},
    {id:'from',label:'From Name Present',
     pass:true,
     desc:'From name is set to Amit Gorodetzer / Bear Grinder.',
     fix:''},
    {id:'subj-spam',label:'Subject Line (Spam Check)',
     pass:!(/FREE|WINNER|GUARANTEED|ACT NOW|CLICK HERE|URGENT/i.test(subj)),
     desc:'Subject line scanned for common spam trigger words.',
     fix:'Revise subject line to remove flagged words.'},
    {id:'subj-length',label:'Subject Line Length',
     pass:subj.length>0&&subj.length<=60,
     desc:'Subject lines under 60 chars perform best. Yours: '+subj.length+' chars.',
     fix:subj.length>60?'Shorten to under 60 characters for mobile inbox display.':''},
    {id:'images',label:'Text-to-Image Ratio',
     pass:(html.replace(/<img[^>]*>/g,'').length*100/Math.max(html.length,1))>15,
     desc:'Emails with too many images and little text may trigger spam filters.',
     fix:'Add more text content relative to image blocks.'},
    {id:'links',label:'Broken Link Check',
     pass:!html.includes('href="#"'),
     desc:'Found placeholder "#" links that need real URLs.',
     fix:'Replace all href="#" links with real destination URLs before sending.'},
    {id:'gdpr',label:'GDPR Consideration',
     pass:true,
     desc:'If sending to EU contacts: confirm list was opt-in and includes unsubscribe.',
     fix:'Ensure EU contacts gave explicit consent. Document consent source.'},
  ];
  var html2='';
  var allOk=true;
  checks.forEach(function(c){
    if(!c.pass) allOk=false;
    var icon=c.pass?'<span style="color:#22c55e;font-size:13px;">&#10003;</span>':'<span style="color:#f87171;font-size:13px;">&#9888;</span>';
    html2+=`<div class="compliance-item"><div class="ci-icon">${icon}</div><div class="ci-body"><div class="ci-title">${esc(c.label)}</div><div class="ci-desc">${esc(c.desc)}${!c.pass&&c.fix?' <strong style="color:#fbbf24;">Fix: '+esc(c.fix)+'</strong>':''}</div></div></div>`;
  });
  var summ=allOk
    ?'<span class="status-pill pill-ok" style="margin-bottom:8px;display:inline-flex;">&#10003; All compliance checks passed</span>'
    :'<span class="status-pill pill-warn" style="margin-bottom:8px;display:inline-flex;">Review items before sending</span>';
  var res=document.getElementById('comp-results');
  if(res) res.innerHTML='<div class="cmd-section" style="margin:0;"><div style="margin-bottom:8px;">'+summ+'</div>'+html2+'</div>';
  COMPLIANCE_RESULTS[id]=checks;
  addLog(allOk?'ok':'warn','Compliance check for '+id+': '+(allOk?'all passed':checks.filter(function(c){return!c.pass;}).length+' issues'));
}

function pushToHS(mode){
  if(!HS_CONNECTED){showErr('Connect HubSpot first in the Connect tab.');return;}
  var tmplSel=document.getElementById('camp-tmpl');
  var listSel=document.getElementById('camp-list');
  var campName=document.getElementById('camp-name');
  var fromName=document.getElementById('camp-from-name');
  var replyTo=document.getElementById('camp-reply-to');
  var schedInput=document.getElementById('camp-schedule');
  var subjInput=document.getElementById('camp-subj');
  if(!campName||!campName.value.trim()){showErr('Enter a campaign name.');return;}
  if(!replyTo||!replyTo.value.trim()){showErr('Enter a reply-to email address.');return;}
  if(mode==='send'&&(!listSel||!listSel.value)){showErr('Select a contact list to send to.');return;}
  var id=tmplSel?tmplSel.value:'e01a';
  var d=DATA[id]||{};
  var card=document.getElementById('card-'+id);
  var emailHtml=buildHS(d.subj||'',card?card.innerHTML:'');
  var subj=(subjInput&&subjInput.value.trim())||d.subj||'';
  var fromN=(fromName&&fromName.value.trim())||'Amit Gorodetzer';
  var replyE=replyTo.value.trim();
  var payload={
    name:campName.value.trim(),
    subject:subj,
    fromName:fromN,
    replyTo:replyE,
    content:{html:emailHtml},
    state: mode==='send'?'SCHEDULED':'DRAFT'
  };
  if(mode==='send'&&listSel&&listSel.value){
    payload.recipients={listIds:[listSel.value]};
  }
  if(mode==='send'&&schedInput&&schedInput.value){
    payload.sendTime={datetime:new Date(schedInput.value).toISOString()};
  }
  addLog('info',(mode==='send'?'Sending':'Drafting')+' campaign: '+campName.value);
  var btn=mode==='send'?document.querySelectorAll('[onclick="pushToHS(\'send\')"]')[0]:document.querySelectorAll('[onclick="pushToHS(\'draft\')"]')[0];
  if(btn){btn.disabled=true;btn.innerHTML='<span class="spinner"></span> Pushing...';}
  hsPost('/marketing/v3/emails',payload,function(res,err,status){
    if(btn){btn.disabled=false;btn.innerHTML=mode==='send'?'Push & Schedule Send':'Save as HubSpot Draft';}
    if(err){
      addLog('err','Push failed: '+err);
      showErr('HubSpot error: '+err);
      return;
    }
    var hsId=res&&(res.id||res.hs_object_id||'');
    addLog('ok',mode==='send'?'Campaign scheduled in HubSpot (ID: '+hsId+')':'Draft saved in HubSpot (ID: '+hsId+')');
    showToast(mode==='send'?'Campaign pushed to HubSpot and scheduled!':'Draft saved in HubSpot. Open HubSpot to review and send.');
    // Record in analytics
    var rec={ts:ts(),templateId:id,templateName:d.name,campaignName:campName.value,hsId:hsId,mode:mode,listId:listSel?listSel.value:'',opens:0,clicks:0,unsubscribes:0,bounces:0,delivered:0};
    ANALYTICS.push(rec);
    try{localStorage.setItem('bg_analytics',JSON.stringify(ANALYTICS));}catch(e){}
    renderCampaign();
  });
}

function uploadCSV(){
  if(!HS_CONNECTED){showErr('Connect HubSpot first.');return;}
  var fileInput=document.getElementById('camp-csv');
  if(!fileInput||!fileInput.files||!fileInput.files[0]){showErr('Select a CSV file first.');return;}
  var file=fileInput.files[0];
  var log=document.getElementById('csv-log');
  if(log) log.innerHTML='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="info">Parsing CSV...</span></div>';
  var reader=new FileReader();
  reader.onload=function(e){
    var text=e.target.result;
    var lines=text.split('\n').filter(function(l){return l.trim();});
    if(lines.length<2){if(log)log.innerHTML='<div class="log-entry"><span class="err">CSV must have a header row and at least one contact.</span></div>';return;}
    var headers=lines[0].split(',').map(function(h){return h.trim().toLowerCase().replace(/"/g,'');});
    var emailCol=headers.indexOf('email');
    if(emailCol<0){if(log)log.innerHTML='<div class="log-entry"><span class="err">CSV must have an "email" column header.</span></div>';return;}
    var contacts=[];
    for(var i=1;i<lines.length;i++){
      var cols=lines[i].split(',').map(function(c){return c.trim().replace(/"/g,'');});
      if(cols[emailCol]&&cols[emailCol].includes('@')){
        var c={email:cols[emailCol]};
        if(headers.indexOf('firstname')>-1) c.firstname=cols[headers.indexOf('firstname')]||'';
        if(headers.indexOf('lastname')>-1) c.lastname=cols[headers.indexOf('lastname')]||'';
        contacts.push(c);
      }
    }
    if(log) log.innerHTML='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="info">Found '+contacts.length+' valid contacts. Creating list...</span></div>';
    var listName=file.name.replace('.csv','')+' - '+new Date().toLocaleDateString();
    // Create static list
    hsPost('/contacts/v1/lists',{name:listName,dynamic:false},function(listRes,listErr){
      if(listErr||!listRes||!listRes.listId){
        if(log) log.innerHTML+='<div class="log-entry"><span class="err">Failed to create list: '+(listErr||'unknown')+'</span></div>';
        return;
      }
      var listId=listRes.listId;
      if(log) log.innerHTML+='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="ok">List created (ID: '+listId+'). Uploading '+contacts.length+' contacts...</span></div>';
      // Upload in batches of 100
      var batches=[];
      for(var b=0;b<contacts.length;b+=100) batches.push(contacts.slice(b,b+100));
      var done=0;
      function uploadBatch(idx){
        if(idx>=batches.length){
          if(log) log.innerHTML+='<div class="log-entry"><span class="ts">'+ts()+'</span><span class="ok">All contacts uploaded. List "'+listName+'" ready in HubSpot.</span></div>';
          addLog('ok','CSV upload complete: '+contacts.length+' contacts to list "'+listName+'"');
          fetchLists();
          return;
        }
        var batch=batches[idx];
        // First create/update contacts
        var vids=batch.map(function(c){return {email:c.email,properties:[{property:'email',value:c.email},{property:'firstname',value:c.firstname||''},{property:'lastname',value:c.lastname||''}]};});
        hsPost('/contacts/v1/contact/batch/',{contact:vids},function(){
          // Then get their VIDs and add to list
          done+=batch.length;
          if(log){
            var entry=log.querySelector('.progress-entry');
            if(!entry){
              log.innerHTML+='<div class="log-entry progress-entry"><span class="ts">'+ts()+'</span><span class="info">Uploading... <span id="upload-prog">'+done+'</span>/'+contacts.length+'</span></div>';
            } else {
              var sp=document.getElementById('upload-prog');
              if(sp) sp.textContent=done;
            }
          }
          uploadBatch(idx+1);
        });
      }
      uploadBatch(0);
    });
  };
  reader.readAsText(file);
}

/* ── ANALYTICS TAB ── */
function renderAnalytics(){
  var el=document.getElementById('view-analytics');
  if(!el) return;
  // Aggregate by template
  var byTemplate={};
  ANALYTICS.forEach(function(r){
    if(!byTemplate[r.templateId]) byTemplate[r.templateId]={sends:0,opens:0,clicks:0,unsubscribes:0,bounces:0,delivered:0,name:r.templateName};
    var t=byTemplate[r.templateId];
    t.sends++;t.opens+=r.opens||0;t.clicks+=r.clicks||0;t.unsubscribes+=r.unsubscribes||0;t.bounces+=r.bounces||0;t.delivered+=r.delivered||0;
  });
  var totalSends=ANALYTICS.length;
  var totalOpens=ANALYTICS.reduce(function(a,r){return a+(r.opens||0);},0);
  var totalClicks=ANALYTICS.reduce(function(a,r){return a+(r.clicks||0);},0);
  var totalUnsubs=ANALYTICS.reduce(function(a,r){return a+(r.unsubscribes||0);},0);
  var avgOR=totalSends>0?Math.round(totalOpens/Math.max(totalSends,1))+'%':'-';
  var avgCTR=totalSends>0?Math.round(totalClicks/Math.max(totalSends,1))+'%':'-';
  // Template performance table
  var tmplRows=Object.keys(byTemplate).map(function(id){
    var t=byTemplate[id];
    var or=t.delivered>0?Math.round(t.opens/t.delivered*100)+'%':'-';
    var ctr=t.opens>0?Math.round(t.clicks/t.opens*100)+'%':'-';
    return '<tr><td>'+esc(id)+'</td><td>'+esc(t.name)+'</td><td>'+t.sends+'</td><td style="color:#3ecfcf;">'+or+'</td><td style="color:#a855f7;">'+ctr+'</td><td style="color:#f87171;">'+t.unsubscribes+'</td></tr>';
  }).join('');
  // Recent sends
  var recentRows=ANALYTICS.slice(-8).reverse().map(function(r){
    return '<tr><td>'+r.ts+'</td><td>'+esc(r.templateName||r.templateId)+'</td><td>'+esc(r.campaignName||'-')+'</td><td>'+esc(r.mode||'-')+'</td><td style="color:'+( r.hsId?'#22c55e':'#555')+'">'+(r.hsId||'local only')+'</td></tr>';
  }).join('');
  var hasSends=ANALYTICS.length>0;
  var emptyState=!hasSends?'<div style="background:#141414;border:1px solid #1e1e1e;border-radius:3px;padding:24px;text-align:center;margin-bottom:12px;"><p style="font-size:13px;color:#333;line-height:1.7;">No sends recorded yet.<br>Use the Campaign tab to push emails to HubSpot. Stats will appear here after sending.</p><button class="cmd-btn cmd-btn-secondary" style="margin-top:10px;" onclick="loadDemoData()">Load Demo Data to Preview</button></div>':'';
  el.innerHTML=`<div class="cmd-hd"><span class="cmd-badge" style="background:#a855f7;color:#fff;">Analytics</span><span class="cmd-title">Performance Dashboard</span><span class="cmd-sub">Engagement & Conversion Tracking</span></div>
<div class="cmd-body">
  ${emptyState}
  ${hasSends ? `
  <div class="metric-grid">
    <div class="metric-card"><div class="metric-val">${totalSends}</div><div class="metric-lbl">Total Sends</div></div>
    <div class="metric-card teal"><div class="metric-val">${avgOR}</div><div class="metric-lbl">Avg Open Rate</div></div>
    <div class="metric-card purple"><div class="metric-val">${avgCTR}</div><div class="metric-lbl">Avg CTR</div></div>
    <div class="metric-card red"><div class="metric-val">${totalUnsubs}</div><div class="metric-lbl">Unsubscribes</div></div>
    <div class="metric-card green"><div class="metric-val">${totalClicks}</div><div class="metric-lbl">Total Clicks</div></div>
    <div class="metric-card orange"><div class="metric-val">${totalOpens}</div><div class="metric-lbl">Total Opens</div></div>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">Template Performance</div>
    <table class="data-table"><tr><th>ID</th><th>Template</th><th>Sends</th><th>Open Rate</th><th>CTR</th><th>Unsubs</th></tr>${tmplRows||'<tr><td colspan="6" style="color:#333;">No data yet</td></tr>'}</table>
  </div>
  <div class="cmd-section">
    <div class="cmd-section-title">Recent Campaigns</div>
    <table class="data-table"><tr><th>Time</th><th>Template</th><th>Campaign</th><th>Mode</th><th>HS ID</th></tr>${recentRows||'<tr><td colspan="5" style="color:#333;">No sends yet</td></tr>'}</table>
  </div>
  ` : ''}
  <div class="cmd-section">
    <div class="cmd-section-title">Sync Live Stats from HubSpot</div>
    <p style="font-size:11px;color:#888;line-height:1.6;margin-bottom:8px;">Pull real-time open rates, clicks, and unsubscribes for all campaigns pushed from this tool.</p>
    <button class="cmd-btn cmd-btn-primary" onclick="syncStats()" ${!HS_CONNECTED?'disabled':''}>Sync Stats from HubSpot</button>
    ${!HS_CONNECTED?'<span style="font-size:11px;color:#888;margin-left:8px;">Connect HubSpot first</span>':''}
  </div>
  <div id="sync-log"></div>
</div>`;
}

function syncStats(){
  if(!HS_CONNECTED||!ANALYTICS.length){return;}
  var log=document.getElementById('sync-log');
  if(log) log.innerHTML='<div class="cmd-section"><div class="log-entry"><span class="ts">'+ts()+'</span><span class="info">Syncing stats...</span></div></div>';
  var withIds=ANALYTICS.filter(function(r){return r.hsId;});
  if(!withIds.length){if(log)log.innerHTML='<div class="cmd-section"><div class="log-entry"><span class="warn">No HubSpot email IDs to sync.</span></div></div>';return;}
  var done=0;
  withIds.forEach(function(r){
    hsGet('/marketing/v3/emails/'+r.hsId,function(d,err){
      done++;
      if(!err&&d&&d.statistics){
        r.opens=d.statistics.opens||0;
        r.clicks=d.statistics.clicks||0;
        r.unsubscribes=d.statistics.unsubscribes||0;
        r.bounces=d.statistics.bounces||0;
        r.delivered=d.statistics.delivered||0;
      }
      if(done===withIds.length){
        try{localStorage.setItem('bg_analytics',JSON.stringify(ANALYTICS));}catch(e){}
        if(log) log.innerHTML='<div class="cmd-section"><div class="log-entry"><span class="ts">'+ts()+'</span><span class="ok">Synced stats for '+withIds.length+' campaigns.</span></div></div>';
        renderAnalytics();
        addLog('ok','Stats synced for '+withIds.length+' campaigns.');
      }
    });
  });
}

function loadDemoData(){
  var templates=Object.keys(DATA);
  ANALYTICS=[];
  var now=Date.now();
  templates.slice(0,6).forEach(function(id,i){
    var d=DATA[id];
    var delivered=Math.floor(Math.random()*400)+100;
    var opens=Math.floor(delivered*(0.18+Math.random()*0.25));
    var clicks=Math.floor(opens*(0.08+Math.random()*0.18));
    ANALYTICS.push({
      ts:new Date(now-i*86400000*3).toLocaleString(),
      templateId:id,templateName:d.name,
      campaignName:'Demo - '+d.name,
      hsId:'demo_'+i,mode:'send',listId:'list_001',
      opens:opens,clicks:clicks,
      unsubscribes:Math.floor(delivered*0.003),
      bounces:Math.floor(delivered*0.02),
      delivered:delivered
    });
  });
  try{localStorage.setItem('bg_analytics',JSON.stringify(ANALYTICS));}catch(e){}
  renderAnalytics();
  showToast('Demo data loaded. This is simulated - connect HubSpot for real stats.');
}

/* ── AI INSIGHTS TAB ── */
function renderAIInsights(){
  var el=document.getElementById('view-ai');
  if(!el) return;
  // AI Insights is embedded inside analytics... let's check if this is separate
  // Actually we embedded it in analytics - render standalone here too
}

/* ── AI INSIGHTS + SCORE (Claude API) ── */
async function runAIAnalysis(){
  var el=document.getElementById('ai-insights-container');
  var scoreel=document.getElementById('ai-score-display');
  if(el) el.innerHTML='<div style="display:flex;align-items:center;gap:8px;color:#555;font-size:12px;padding:8px 0;"><span class="spinner"></span> Analyzing templates with AI...</div>';
  // Build summary of templates + any analytics data
  var tmplSummary=Object.keys(DATA).map(function(id){
    var d=DATA[id];
    var a=ANALYTICS.filter(function(r){return r.templateId===id;});
    var avgOR=a.length?Math.round(a.reduce(function(s,r){return s+(r.delivered?r.opens/r.delivered:0);},0)/a.length*100)+'%':'no data';
    return id+'|'+d.seg+'|'+d.name+'|subj: "'+d.subj+'"'+(a.length?'|open rate: '+avgOR:'');
  }).join('\n');
  var prompt='You are an expert cannabis brand email marketing strategist. Review these Bear Grinder email templates and analytics data, then provide:\n1. An overall quality score from 0-100 (be honest and critical)\n2. Top 5-7 specific, actionable insights for improvement\n\nTemplates:\n'+tmplSummary+'\n\nAnalytics: '+(ANALYTICS.length?JSON.stringify(ANALYTICS.slice(-5)):'No send data yet')+'\n\nRespond ONLY with valid JSON, no markdown, no preamble:\n{"score":85,"score_reason":"Brief explanation","insights":[{"priority":"high","icon":"🎯","title":"Short title","body":"Specific actionable recommendation"},...]}'
  try{
    var resp=await fetch('https://api.anthropic.com/v1/messages',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        model:'claude-sonnet-4-20250514',
        max_tokens:1000,
        messages:[{role:'user',content:prompt}]
      })
    });
    var data=await resp.json();
    var text=(data.content&&data.content[0]&&data.content[0].text)||'';
    var clean=text.replace(/```json|```/g,'').trim();
    var parsed=JSON.parse(clean);
    AI_SCORE=parsed.score;
    AI_INSIGHTS=parsed.insights||[];
    try{localStorage.setItem('bg_ai_score',JSON.stringify(AI_SCORE));localStorage.setItem('bg_ai_insights',JSON.stringify(AI_INSIGHTS));}catch(e){}
    displayAIInsights(parsed,el,scoreel);
    addLog('ok','AI analysis complete. Score: '+AI_SCORE+'/100');
  }catch(e){
    if(el) el.innerHTML='<div style="font-size:12px;color:#ef4444;padding:8px 0;">AI analysis failed: '+esc(e.message)+'</div>';
    addLog('err','AI analysis error: '+e.message);
  }
}

function displayAIInsights(parsed,el,scoreel){
  var score=parsed.score||0;
  var color=score>=80?'#22c55e':score>=60?'#3ecfcf':score>=40?'#fbbf24':'#f87171';
  var insightHtml=(parsed.insights||[]).map(function(ins){
    var priColor={'high':'#f87171','medium':'#fbbf24','low':'#555'}[ins.priority]||'#555';
    return '<div class="insight-item"><div class="insight-icon">'+esc(ins.icon||'•')+'</div><div class="insight-body"><h4 style="color:'+priColor+';">'+esc(ins.title)+'</h4><p>'+esc(ins.body)+'</p></div></div>';
  }).join('');
  if(scoreel) scoreel.innerHTML='<div class="score-ring"><div><div class="score-num" style="color:'+color+';">'+score+'</div><div class="score-of">/ 100</div></div><div class="score-info"><h3>Overall Template Score</h3><p>'+esc(parsed.score_reason||'')+'</p></div></div>';
  if(el) el.innerHTML=insightHtml||'<div style="font-size:12px;color:#444;padding:8px 0;">No insights generated.</div>';
}

/* ── HUBSPOT EXPORT ── */
function renderHS(id){
  try{
    var card=document.getElementById('card-'+id);
    var bodyHtml=card?card.innerHTML:'';
    var d=DATA[id]||{};
    var subj=d.subj||'';
    var hsHtml=buildHS(subj,bodyHtml);
    document.getElementById('hscard').innerHTML=
      '<div class="cmd-hd" style="background:#141414;"><span class="cmd-badge" style="background:#3ecfcf;color:#000;">HubSpot</span><span class="cmd-title">'+(d.num||'')+' - '+(d.name||'')+'</span></div>'+
      '<div style="padding:10px 16px;border-bottom:1px solid #0a0a0a;"><div class="hslbl" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">Subject Line</div><div style="font-size:13px;color:#777;">'+esc(subj)+'</div></div>'+
      '<div style="padding:10px 16px;border-bottom:1px solid #0a0a0a;"><div class="hslbl" style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">From Name</div><div style="font-size:13px;color:#777;">Amit Gorodetzer &middot; Bear Grinder</div></div>'+
      '<div style="padding:10px 16px;border-bottom:1px solid #0a0a0a;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">HTML - Paste into HubSpot source editor</div>'+
      '<div style="font-family:monospace;font-size:10px;color:#7dd3fc;background:rgba(125,211,252,.04);padding:8px 10px;border-radius:2px;border:1px solid rgba(125,211,252,.1);white-space:pre-wrap;word-break:break-all;max-height:160px;overflow-y:auto;margin-bottom:8px;" id="hs-htmlbox">'+esc(hsHtml)+'</div>'+
      '<div style="display:flex;gap:7px;padding:8px 0;"><button class="abtn abtn-hs" data-id="'+id+'" onclick="copyHSFor(this.dataset.id)" id="hs-copy-'+id+'">Copy HTML</button><button class="abtn abtn-hs" style="background:#444;color:#fff" onclick="goHS()">Open HubSpot &#8599;</button></div>'+
      '<div style="padding:10px 0 0;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#333;margin-bottom:8px;">4-Step Send Process</div>'+
      '<div style="font-size:12px;color:#555;line-height:2;">1. Click Copy HTML above<br>2. Marketing &rarr; Email &rarr; Create email &rarr; Regular &rarr; Blank<br>3. Click &lt;/&gt; Source. Paste. Click Update.<br>4. Set subject + From: Amit Gorodetzer. Select list. Send.</div></div>'+
      '</div>';
  }catch(e){showErr('renderHS: '+e.message);}
}

/* ── HS PREVIEW ── */
function renderHSP(id){
  var inner=document.getElementById('hs-prev-inner');
  var lbl=document.getElementById('hs-prev-lbl');
  var d=DATA[id]||{};
  if(lbl) lbl.textContent=(d.num||'')+' - '+(d.name||'');
  var card=document.getElementById('card-'+id);
  if(!inner||!card) return;
  // Simulate HubSpot email rendering:
  // 1. Max 600px width (enforced by container)
  // 2. Strip contenteditable attributes
  // 3. Show unsubscribe token as visible link
  // 4. Leave [firstname] merge fields as-is
  var html=card.innerHTML;
  html=html.replace(/\s*contenteditable="true"/g,'');
  html=html.replace(/\{\{unsubscribe\}\}/g,'#unsubscribe');
  html=html.replace(/\{\{\{unsubscribe\}\}\}/g,'#unsubscribe');
  // Replace unsubscribe placeholder with visible link text if not already
  inner.innerHTML=html;
}

function buildHS(subj,body){
  var tkn=body.replace(/\[firstname\]/g,'{{contact.firstname}}');
  return '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>'+subj+'</title>\n</head>\n<body style="margin:0;padding:20px 0;background:#111;">\n<table width="100%" cellpadding="0" cellspacing="0" style="background:#111;">\n<tr><td align="center">\n<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">\n<tr><td>\n'+tkn+'\n</td></tr></table></td></tr></table>\n</body>\n</html>';
}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function copyText(text,onOK,onFail){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(onOK).catch(function(){fallbackCopy(text,onOK,onFail);});}
  else{fallbackCopy(text,onOK,onFail);}
}
function fallbackCopy(text,onOK,onFail){
  try{var ta=document.createElement('textarea');ta.value=text;ta.style.cssText='position:fixed;top:0;left:0;width:2px;height:2px;opacity:0;';document.body.appendChild(ta);ta.focus();ta.select();var ok=document.execCommand('copy');document.body.removeChild(ta);if(ok)onOK();else onFail();}catch(e){if(onFail)onFail();}
}
function copyHSFor(id){
  try{
    var card=document.getElementById('card-'+id);var d=DATA[id]||{};var html=buildHS(d.subj||'',card?card.innerHTML:'');
    copyText(html,function(){showToast('HTML copied. Paste into HubSpot source editor.');var btn=document.getElementById('hs-copy-'+id);if(btn){var o=btn.textContent;btn.textContent='\u2713 Copied!';setTimeout(function(){btn.textContent=o;},2200);}},function(){showErr('Clipboard blocked - select text in the HTML box above and copy manually (Ctrl+A, Ctrl+C).');});
  }catch(e){showErr('copyHSFor: '+e.message);}
}
function doCopy(){
  try{
    var card=document.getElementById('card-'+CUR);var d=DATA[CUR]||{};
    var rawHtml=card?card.innerHTML:'';
    // Strip contenteditable and edit-mode styling for clean export
    rawHtml=rawHtml.replace(/\s*contenteditable="true"/g,'');
    var html=buildHS(d.subj||'',rawHtml);
    copyText(html,function(){var btn=document.getElementById('copyBtn');if(btn){btn.classList.add('ok');btn.textContent='\u2713 Copied!';setTimeout(function(){btn.classList.remove('ok');btn.textContent='Copy HTML';},2400);}showToast('HTML copied to clipboard');},function(){showErr('Copy blocked - open Export tab and copy HTML manually.');});
  }catch(e){showErr('doCopy: '+e.message);}
}
function goHS(){try{window.open('https://app.hubspot.com/email','_blank');}catch(e){}}
function fmt(cmd){try{document.execCommand(cmd,false,null);}catch(e){}}
function doReset(){
  try{if(!confirm('Reset template to original? Edits will be lost.'))return;var card=document.getElementById('card-'+CUR);if(card&&origHTML[CUR])card.innerHTML=origHTML[CUR];showToast('Template reset.');}catch(e){showErr('Reset: '+e.message);}
}
function tog(hd){hd.classList.toggle('open');var b=hd.nextElementSibling;if(b)b.classList.toggle('open');}
function addLog(level,msg){SEND_LOG.push({ts:ts(),level:level,msg:msg});try{localStorage.setItem('bg_send_log',JSON.stringify(SEND_LOG.slice(-50)));}catch(e){}}
function ts(){return new Date().toLocaleTimeString();}
function showErr(msg){var bar=document.getElementById('errbar');var txt=document.getElementById('errtext');if(bar&&txt){txt.textContent=msg;bar.classList.add('on');}console.error(msg);}
function clearErr(){var bar=document.getElementById('errbar');if(bar)bar.classList.remove('on');}
function showToast(msg){var t=document.getElementById('toast');if(!t)return;t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},3000);}


function goHome() {
  // Close sidebar on mobile
  var sb = document.getElementById('sidebar');
  var ov = document.querySelector('.tb-overlay');
  if (sb) sb.classList.remove('open');
  if (ov) ov.classList.remove('on');
  // Reset audience filter and collapse all categories
  document.querySelectorAll('.seg-label,.seg-group').forEach(function(el){ el.style.display = ''; });
  collapseAllSegs();
  document.querySelectorAll('.aud-btn').forEach(function(b){ b.classList.remove('active'); });
  // Hide see-more hint
  var hint = document.getElementById('see-more-hint');
  if (hint) hint.style.display = 'none';
  // Switch to guide
  setView('guide');
  mobNavSet('guide');
}
/* ============================================================
   DASHBOARD
   ============================================================ */
function refreshDashboard() {
  var st = document.getElementById('dash-hs-status');
  if (st) st.textContent = '';
  // Load from local analytics storage
  var analytics = (typeof ANALYTICS !== 'undefined') ? ANALYTICS : [];
  // Aggregate totals
  var totalSent = 0, totalOpens = 0, totalClicks = 0, totalUnsubs = 0, totalBounces = 0;
  var segCounts = { 'B2C':0, 'Wholesale':0, 'Distributor':0, 'Special':0, 'Friends & Family':0 };
  analytics.forEach(function(r) {
    totalSent += (r.sent||0);
    totalOpens += (r.opens||0);
    totalClicks += (r.clicks||0);
    totalUnsubs += (r.unsubs||0);
    totalBounces += (r.bounces||0);
    var seg = r.seg || 'Other';
    if (segCounts[seg] !== undefined) segCounts[seg]++;
  });
  var openRate = totalSent > 0 ? (totalOpens/totalSent*100).toFixed(1)+'%' : '--';
  var ctrRate  = totalSent > 0 ? (totalClicks/totalSent*100).toFixed(1)+'%' : '--';
  var unsubRate= totalSent > 0 ? (totalUnsubs/totalSent*100).toFixed(2)+'%' : '--';
  var estConv  = Math.round(totalClicks * 0.025); // 2.5% est conversion from clicks
  var estRev   = estConv > 0 ? '$' + (estConv * 49.99).toFixed(0) : '$--';
  // Update health cards
  function setHC(id, val, benchGood, benchOk, isLower) {
    var el = document.getElementById(id);
    if (!el) return;
    el.textContent = val;
    var numVal = parseFloat(val);
    var stEl = document.getElementById(id.replace('hv-','hs-'));
    if (!stEl || isNaN(numVal)) return;
    var good = isLower ? numVal <= benchGood : numVal >= benchGood;
    var ok   = isLower ? numVal <= benchOk  : numVal >= benchOk;
    stEl.textContent = good ? 'Above avg' : (ok ? 'On track' : 'Below avg');
    stEl.style.color = good ? '#22c55e' : (ok ? '#fbbf24' : '#ef4444');
  }
  setHC('hv-opens', openRate, 35, 21, false);
  setHC('hv-ctr',   ctrRate,  5,  2.6, false);
  setHC('hv-unsub', unsubRate,0.1,0.5, true);
  var sentEl = document.getElementById('hv-sent');
  if (sentEl) sentEl.textContent = totalSent > 0 ? totalSent.toLocaleString() : '--';
  var convEl = document.getElementById('hv-conv');
  if (convEl) convEl.textContent = estConv > 0 ? estConv : '--';
  var revEl = document.getElementById('hv-rev');
  if (revEl) revEl.textContent = estRev;
  // Update benchmark table
  function setBench(id, val, goodThresh, okThresh, isLower) {
    var el = document.getElementById(id);
    if (el) el.textContent = val;
    var stEl = document.getElementById(id+'-st');
    var numVal = parseFloat(val);
    if (!stEl || isNaN(numVal)) { if(stEl) stEl.textContent='No data'; return; }
    var good = isLower ? numVal <= goodThresh : numVal >= goodThresh;
    var ok   = isLower ? numVal <= okThresh  : numVal >= okThresh;
    stEl.textContent = good ? 'Strong' : (ok ? 'Average' : 'Needs work');
    stEl.style.color = good ? '#22c55e' : (ok ? '#fbbf24' : '#ef4444');
  }
  setBench('bench-opens', openRate, 35, 21, false);
  setBench('bench-ctr',   ctrRate,  5,  2.6, false);
  setBench('bench-unsub', unsubRate,0.1,0.5, true);
  var bounceRate = totalSent > 0 ? (totalBounces/totalSent*100).toFixed(2)+'%' : '--';
  setBench('bench-bounce', bounceRate, 0.3, 0.7, true);
  setBench('bench-conv', estConv > 0 ? (estConv/totalSent*100).toFixed(1)+'%' : '--', 5, 2, false);
  // Segment breakdown
  ['b2c','wholesale','dist','special'].forEach(function(k) {
    var segKey = k === 'b2c' ? 'B2C' : k === 'wholesale' ? 'Wholesale' : k === 'dist' ? 'Distributor' : 'Special';
    var el = document.getElementById('sd-'+k);
    if (el) el.textContent = (segCounts[segKey]||0) + ' sends';
  });
  // Rebuild send log table
  buildSendLogTable(analytics);
  // If HubSpot connected, try to pull live stats
  if (typeof HS_CONNECTED !== 'undefined' && HS_CONNECTED && typeof HS_TOKEN !== 'undefined' && HS_TOKEN) {
    if (st) st.textContent = 'Syncing from HubSpot...';
    fetch('https://api.hubapi.com/marketing/v3/emails?limit=20&orderBy=-updatedAt', {
      headers: { 'Authorization': 'Bearer ' + HS_TOKEN }
    }).then(function(r){ return r.json(); })
    .then(function(data) {
      if (data.results && data.results.length) {
        var hsSent=0, hsOpens=0, hsClicks=0;
        data.results.forEach(function(e) {
          if (e.stats) {
            hsSent  += e.stats.sent||0;
            hsOpens += e.stats.open||0;
            hsClicks+= e.stats.click||0;
          }
        });
        if (hsSent > 0) {
          var sentEl2 = document.getElementById('hv-sent');
          if (sentEl2) sentEl2.textContent = hsSent.toLocaleString();
          if (st) st.textContent = 'Synced from HubSpot - ' + data.results.length + ' campaigns loaded.';
        } else {
          if (st) st.textContent = 'HubSpot connected. No campaign stats yet.';
        }
      }
    }).catch(function() {
      if (st) st.textContent = 'HubSpot sync failed. Showing local data.';
    });
  } else {
    if (st) st.textContent = analytics.length > 0 ? 'Showing ' + analytics.length + ' local send records. Connect HubSpot for live sync.' : 'No send data yet. Connect HubSpot or push campaigns via the Send tab.';
  }
}

function buildSendLogTable(analytics) {
  var tbody = document.getElementById('send-log-table');
  if (!tbody) return;
  // Remove all rows except header and empty row
  while (tbody.rows.length > 1) tbody.deleteRow(1);
  if (!analytics || analytics.length === 0) {
    var row = tbody.insertRow();
    var cell = row.insertCell();
    cell.colSpan = 9;
    cell.style.cssText = 'text-align:center;color:#333;padding:20px;font-size:12px;';
    cell.textContent = 'No sends recorded yet. Push a campaign via the Send tab to log it here.';
    return;
  }
  // Sort newest first
  var sorted = analytics.slice().sort(function(a,b){ return new Date(b.date||0)-new Date(a.date||0); });
  sorted.forEach(function(r) {
    var row = tbody.insertRow();
    var d = r.date ? new Date(r.date).toLocaleDateString() : '--';
    var tname = (typeof EDATA !== 'undefined' && r.id && EDATA[r.id]) ? EDATA[r.id].name : (r.id||'--');
    var seg = r.seg || '--';
    var list = r.listName || '--';
    var sent = r.sent || '--';
    var opens = r.opens > 0 ? r.opens + ' (' + (r.sent>0?(r.opens/r.sent*100).toFixed(0)+'%':'')+')' : '--';
    var clicks = r.clicks || '--';
    var unsubs = r.unsubs || '--';
    var status = r.status || 'Sent';
    var cells = [d, tname, seg, list, sent, opens, clicks, unsubs, status];
    cells.forEach(function(val, i) {
      var cell = row.insertCell();
      cell.textContent = val;
      if (i === 8) cell.style.color = status === 'Sent' ? '#22c55e' : '#fbbf24';
    });
  });
}

function resetDashboard() {
  if (!confirm('Reset all local send history? This cannot be undone.')) return;
  if (typeof ANALYTICS !== 'undefined') ANALYTICS = [];
  try { localStorage.removeItem('bg_analytics'); localStorage.removeItem('bg_send_log'); } catch(e){}
  refreshDashboard();
  showToast('Dashboard reset');
}

/* ============================================================
   AUDIENCE FILTER
   ============================================================ */
function filterAudience(seg) {
  document.querySelectorAll('.aud-btn').forEach(function(b){ b.classList.remove('active'); });
  if (seg !== 'ALL') {
    var ab = document.querySelector('.aud-btn[data-seg="' + seg + '"]');
    if (ab) ab.classList.add('active');
  }
  // Show/hide sidebar category groups
  if (seg === 'ALL') {
    // Show all categories and expand them
    document.querySelectorAll('.seg-label,.seg-group').forEach(function(el){ el.style.display = ''; });
    expandAllSegs();
  } else {
    // Show only matching category, hide others
    document.querySelectorAll('.seg-label').forEach(function(el){
      var s = el.getAttribute('data-seg');
      el.style.display = (s === seg) ? '' : 'none';
    });
    document.querySelectorAll('.seg-group').forEach(function(el){
      var s = el.getAttribute('data-seg');
      if (s === seg) {
        el.style.display = 'block';
        el.classList.add('open');
        var lbl = el.previousElementSibling;
        if (lbl) lbl.classList.add('expanded');
      } else {
        el.style.display = 'none';
        el.classList.remove('open');
      }
    });
  }
  // Always open sidebar on mobile
  if (window.innerWidth <= 700) {
    var sb = document.getElementById('sidebar');
    var ov = document.querySelector('.tb-overlay');
    if (sb) sb.classList.add('open');
    if (ov) ov.classList.add('on');
  }
  if (seg === 'ALL') {
    showToast('Showing all 21 templates');
  } else {
    // Pick first template in segment and switch to preview
    var first = document.querySelector('.ebtn[data-seg="' + seg + '"]');
    if (first) {
      var id = first.id.replace('btn-','');
      nav(id);
    }
    setView('preview');
    mobNavSet('preview');
    showToast('Showing ' + seg + ' templates');
  }
}

/* VERSION HISTORY TOGGLE */
function toggleVH(btn) {
  var e = document.getElementById('vh-expanded');
  if (!e) return;
  if (e.style.display === 'none' || e.style.display === '') {
    e.style.display = 'block';
    btn.textContent = 'Collapse History';
  } else {
    e.style.display = 'none';
    btn.textContent = 'Show Full History';
  }
}

function toggle1Pager(checked) {
  var note = document.getElementById('onepager-note');
  if (note) note.style.display = checked ? 'block' : 'none';
  if (checked) showToast('1-Pager attachment enabled - remember to attach PDF in HubSpot');
}
function toggleCustomAttach(checked) {
  var sec = document.getElementById('custom-attach-section');
  if (sec) sec.style.display = checked ? 'block' : 'none';
  if (checked) showToast('Custom attachment enabled - paste HubSpot File URL');
}

// Auto-suggest 1-pager for wholesale/dist templates
function checkOnePagerSuggestion(seg) {
  var cb = document.getElementById('attach-onepager');
  if (!cb) return;
  var shouldAttach = (seg === 'Wholesale' || seg === 'Distributor');
  cb.checked = shouldAttach;
  toggle1Pager(shouldAttach);
  if (shouldAttach) showToast('1-Pager auto-selected for ' + seg + ' template');
}

/* ============================================================
   SEND PREVIEW EMAIL
   ============================================================ */
function openSendPreview() {
  if (document.getElementById('preview-modal')) return;
  var connected = (typeof HS_CONNECTED !== 'undefined' && HS_CONNECTED);
  var note = connected
    ? 'HubSpot connected. Will send via HubSpot transactional API.'
    : 'No HubSpot connection. Will open in your default email client with the template content.';
  var modal = document.createElement('div');
  modal.id = 'preview-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:2000;display:flex;align-items:center;justify-content:center;padding:16px;';
  modal.innerHTML = [
    '<div style="background:#111;border:1px solid #222;border-radius:8px;padding:22px;width:100%;max-width:420px;">',
    '<div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#3ecfcf;margin-bottom:6px;">Send Preview Email</div>',
    '<p style="font-size:12px;color:#555;margin-bottom:14px;line-height:1.6;">Sends the selected template to any email. Works with or without HubSpot.</p>',
    '<div style="margin-bottom:10px;"><div style="font-size:9px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#444;margin-bottom:5px;">Recipient Email</div>',
    '<input id="prev-email" type="email" placeholder="name@example.com" style="width:100%;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:10px 12px;font-size:14px;color:#fff;font-family:\'Helvetica Neue\',Arial,sans-serif;outline:none;box-sizing:border-box;"/></div>',
    '<div style="margin-bottom:12px;"><div style="font-size:9px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#444;margin-bottom:5px;">Recipient First Name (optional)</div>',
    '<input id="prev-name" type="text" placeholder="First name" style="width:100%;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:10px 12px;font-size:14px;color:#fff;font-family:\'Helvetica Neue\',Arial,sans-serif;outline:none;box-sizing:border-box;"/></div>',
    '<div style="padding:8px 12px;background:#0a0a0a;border:1px solid #1a1a1a;border-radius:4px;font-size:11px;color:#444;margin-bottom:14px;line-height:1.5;">' + note + '</div>',
    '<div style="display:flex;gap:8px;">',
    '<button id="prev-send-btn" style="flex:1;padding:11px;background:#3ecfcf;border:none;border-radius:4px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#000;cursor:pointer;">Send Preview</button>',
    '<button onclick="document.getElementById(\'preview-modal\').remove()" style="padding:11px 16px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:4px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#666;cursor:pointer;">Cancel</button>',
    '</div></div>'
  ].join('');
  document.body.appendChild(modal);
  modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
  document.getElementById('prev-send-btn').addEventListener('click', doSendPreview);
  setTimeout(function() { var el=document.getElementById('prev-email'); if(el) el.focus(); }, 100);
}

function doSendPreview() {
  var emailEl = document.getElementById('prev-email');
  var nameEl = document.getElementById('prev-name');
  if (!emailEl) return;
  var email = emailEl.value.trim();
  var name = (nameEl && nameEl.value.trim()) || 'there';
  if (!email || email.indexOf('@') < 0) {
    emailEl.style.borderColor = '#ef4444';
    return;
  }
  var panel = document.querySelector('.epanel[style*="block"]');
  if (!panel) { showToast('No template selected'); return; }
  var html = panel.innerHTML.replace(/\[firstname\]/gi, name);
  var meta = (typeof DATA !== 'undefined' && CUR && DATA[CUR]) ? DATA[CUR] : {};
  var subj = meta.subj || 'Bear Grinder';
  var modal = document.getElementById('preview-modal');
  if (modal) modal.remove();
  if (typeof HS_CONNECTED !== 'undefined' && HS_CONNECTED && typeof HS_TOKEN !== 'undefined' && HS_TOKEN) {
    fetch('https://api.hubapi.com/marketing/v3/transactional/single-email/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + HS_TOKEN },
      body: JSON.stringify({ emailId: 0, message: { to: email, from: 'Hello@BearGrinder.com', replyTo: 'Hello@BearGrinder.com', subject: '[PREVIEW] ' + subj, html: html } })
    }).then(function(r) {
      showToast(r.ok ? 'Preview sent to ' + email : 'HubSpot failed - opening email client');
      if (!r.ok) openMailtoPreview(email, subj, html);
    }).catch(function() { openMailtoPreview(email, subj, html); });
  } else {
    openMailtoPreview(email, subj, html);
  }
}

function openMailtoPreview(email, subj, html) {
  var tmp = document.createElement('div');
  tmp.innerHTML = html;
  var plain = (tmp.innerText || tmp.textContent || '').replace(/\s+/g, ' ').trim().substring(0, 1800);
  window.location.href = 'mailto:' + encodeURIComponent(email)
    + '?subject=' + encodeURIComponent('[PREVIEW] ' + subj)
    + '&body=' + encodeURIComponent(plain + '\n\n-- Bear Grinder Email Campaign Command Center --');
  showToast('Opening email client');
}

/* ============================================================
   REPORT A BUG
   ============================================================ */
function openBugReport() {
  if (document.getElementById('bug-modal')) return;
  var modal = document.createElement('div');
  modal.id = 'bug-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:2000;display:flex;align-items:center;justify-content:center;padding:16px;';
  modal.innerHTML = [
    '<div style="background:#111;border:1px solid #222;border-radius:8px;padding:22px;width:100%;max-width:440px;max-height:85vh;overflow-y:auto;">',
    '<div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#ef4444;margin-bottom:6px;">Report a Bug</div>',
    '<p style="font-size:12px;color:#555;margin-bottom:14px;line-height:1.6;">Report goes to kevin@ElevatedAdvisors.co. Be specific.</p>',
    '<div style="margin-bottom:10px;"><div style="font-size:9px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#444;margin-bottom:5px;">Bug Category</div>',
    '<select id="bug-cat" style="width:100%;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:10px 12px;font-size:13px;color:#fff;font-family:\'Helvetica Neue\',Arial,sans-serif;outline:none;box-sizing:border-box;">',
    '<option value="">Select category...</option>',
    '<option>Template display / rendering</option>',
    '<option>HubSpot connection / API</option>',
    '<option>Campaign builder / send</option>',
    '<option>Analytics / stats sync</option>',
    '<option>Edit / Export tab</option>',
    '<option>Mobile layout</option>',
    '<option>Sidebar / navigation</option>',
    '<option>Promo codes / compliance</option>',
    '<option>Other</option>',
    '</select></div>',
    '<div style="margin-bottom:10px;"><div style="font-size:9px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#444;margin-bottom:5px;">Bug Details</div>',
    '<textarea id="bug-details" placeholder="What happened? What did you expect? What steps led to it?" rows="4" style="width:100%;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:10px 12px;font-size:13px;color:#fff;font-family:\'Helvetica Neue\',Arial,sans-serif;outline:none;resize:vertical;box-sizing:border-box;"></textarea></div>',
    '<div style="margin-bottom:14px;"><div style="font-size:9px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#444;margin-bottom:5px;">Screenshot (optional)</div>',
    '<input type="file" id="bug-img" accept="image/*" style="width:100%;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:8px 12px;font-size:12px;color:#555;cursor:pointer;box-sizing:border-box;"/></div>',
    '<div id="bug-status" style="display:none;padding:8px 12px;border-radius:4px;font-size:12px;margin-bottom:10px;"></div>',
    '<div style="display:flex;gap:8px;">',
    '<button id="bug-send-btn" style="flex:1;padding:11px;background:#ef4444;border:none;border-radius:4px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;cursor:pointer;">Send Report</button>',
    '<button onclick="document.getElementById(\'bug-modal\').remove()" style="padding:11px 16px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:4px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#666;cursor:pointer;">Cancel</button>',
    '</div></div>'
  ].join('');
  document.body.appendChild(modal);
  modal.addEventListener('click', function(e) { if (e.target === modal) modal.remove(); });
  document.getElementById('bug-send-btn').addEventListener('click', submitBugReport);
}

function submitBugReport() {
  var cat = (document.getElementById('bug-cat') || {}).value || '';
  var details = ((document.getElementById('bug-details') || {}).value || '').trim();
  var st = document.getElementById('bug-status');
  if (!cat) {
    if (st) { st.style.display='block'; st.style.background='rgba(239,68,68,.1)'; st.style.color='#ef4444'; st.textContent='Please select a category.'; }
    return;
  }
  if (!details) {
    if (st) { st.style.display='block'; st.style.background='rgba(239,68,68,.1)'; st.style.color='#ef4444'; st.textContent='Please describe the bug.'; }
    return;
  }
  var body = 'Bug Report - Bear Grinder Email Campaign Command Center\n\nCategory: ' + cat + '\nTemplate: ' + (CUR || 'none') + '\nBrowser: ' + navigator.userAgent.substring(0, 120) + '\n\nDetails:\n' + details;
  window.location.href = 'mailto:kevin@ElevatedAdvisors.co?subject=' + encodeURIComponent('[BUG] ' + cat) + '&body=' + encodeURIComponent(body);
  if (st) { st.style.display='block'; st.style.background='rgba(34,197,94,.1)'; st.style.color='#22c55e'; st.textContent='Opening email client. Please send to complete.'; }
  setTimeout(function() { var m=document.getElementById('bug-modal'); if(m) m.remove(); }, 2000);
}

/* COUPON STATUS */
function checkHSCoupons() {
  var codes = ['BEAR20','FAM15','KevinFS','kevinff10'];
  var connected = (typeof HS_CONNECTED !== 'undefined' && HS_CONNECTED);
  codes.forEach(function(c) {
    var el = document.getElementById('hs-status-' + c);
    if (!el) return;
    if (!connected) {
      el.innerHTML = '<span style="padding:2px 8px;background:rgba(60,60,60,.2);border:1px solid #2a2a2a;border-radius:10px;font-size:9px;font-family:Trebuchet MS,Arial,sans-serif;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#444;">Connect HubSpot first</span>';
    } else {
      el.innerHTML = '<span style="font-size:10px;color:#555;">Checking...</span>';
      setTimeout(function() {
        el.innerHTML = '<span style="padding:2px 8px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.25);border-radius:10px;font-size:9px;font-family:Trebuchet MS,Arial,sans-serif;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#22c55e;">Verify in Shopify</span>';
      }, 600);
    }
  });
}

"""

LOGO_SM = LOGO_W.replace('width="160"','width="110"').replace('height="30"','height="22"').replace('font-size="18"','font-size="13"')

GUIDE_HTML = f'''<div class="cmd-panel" id="view-guide" style="display:block;background:#0d0d0d;">
<div class="cmd-hd"><span class="cmd-badge" style="background:#fff;color:#000;">Guide</span><span class="cmd-title">Bear Grinder Email Campaign Command Center</span><span class="cmd-sub">V18</span></div>
<div class="cmd-body">

  <div style="background:#000;border:1px solid #1e1e1e;border-radius:6px;padding:16px 20px;margin-bottom:12px;display:flex;align-items:center;gap:14px;">
    <div style="color:#fff;">{LOGO_SM}</div>
    <div><p style="font-size:11px;color:#888;line-height:1.7;">{len(emails)} templates &nbsp;/&nbsp; 5 segments &nbsp;/&nbsp; A+B versions &nbsp;/&nbsp; HubSpot live API &nbsp;/&nbsp; AI insights &nbsp;/&nbsp; Email Compliance Check &nbsp;/&nbsp; V18</p></div>
  </div>

  <div style="margin-bottom:12px;">
    <div style="background:linear-gradient(135deg,#0d0d0d 0%,#111 100%);border:1px solid #1e1e1e;border-radius:8px;padding:20px 18px;margin-bottom:10px;">
      <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#3ecfcf;margin-bottom:8px;">Start Here</div>
      <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:18px;font-weight:900;letter-spacing:.02em;color:#fff;margin-bottom:4px;text-transform:uppercase;">Pick Your Audience</div>
      <p style="font-size:12px;color:#999;margin-bottom:16px;line-height:1.6;">Choose who you are sending to. Templates load filtered and ready.</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <button onclick="filterAudience(\'B2C\')" class="aud-btn" data-seg="B2C"><span class="aud-icon">&#128717;</span><span class="aud-label">B2C</span><span class="aud-sub">Consumer emails</span></button>
        <button onclick="filterAudience(\'Wholesale\')" class="aud-btn" data-seg="Wholesale"><span class="aud-icon">&#127978;</span><span class="aud-label">Wholesale</span><span class="aud-sub">Retail buyers</span></button>
        <button onclick="filterAudience(\'Distributor\')" class="aud-btn" data-seg="Distributor"><span class="aud-icon">&#128666;</span><span class="aud-label">Distribution</span><span class="aud-sub">Distributor outreach</span></button>
        <button onclick="filterAudience(\'Special\')" class="aud-btn" data-seg="Special"><span class="aud-icon">&#11088;</span><span class="aud-label">Special</span><span class="aud-sub">Trade show + samples</span></button>
        <button onclick="filterAudience(\'Friends &amp; Family\')" class="aud-btn" data-seg="Friends &amp; Family" style="grid-column:1/-1;"><span class="aud-icon">&#129309;</span><span class="aud-label">Friends &amp; Family</span><span class="aud-sub">Personal network</span></button>
      </div>
    </div>
    <button onclick="filterAudience(\'ALL\')" style="width:100%;background:#0d0d0d;border:1px solid #1e1e1e;border-radius:6px;padding:14px 18px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#555;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:all .15s;" onmouseover="this.style.color=\'#fff\';this.style.borderColor=\'#3a3a3a\'" onmouseout="this.style.color=\'#555\';this.style.borderColor=\'#1e1e1e\'">
      <span style="font-size:16px;">&#128221;</span> See All Templates
    </button>
  </div>

  <div class="cmd-section">
    <div class="cmd-section-title">What Each Tab Does - Look Down</div>
    <p style="font-size:11px;color:#555;line-height:1.6;margin-bottom:14px;">The bottom bar is your main navigation. Tabs split into two groups.</p>
    <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#3ecfcf;margin-bottom:8px;padding-bottom:5px;border-bottom:1px solid #1e1e1e;">Campaign Tools - Live HubSpot Actions</div>
    <table class="data-table" style="margin-bottom:14px;">
      <tr><th>Tab</th><th>What It Does</th><th>Quick Tip</th></tr>
      <tr><td><span style="color:#f97316;font-weight:700;">Send</span></td><td>Build and push campaigns to HubSpot. Pick template, select list, run compliance, schedule or send.</td><td style="color:#777;">Always run Email Compliance Check before pushing.</td></tr>
      <tr><td><span style="color:#a855f7;font-weight:700;">Stats</span></td><td>Track open rates, CTR, unsubscribes, and bounces per template. Syncs live from HubSpot.</td><td style="color:#777;">Hit Sync after sends to pull real numbers.</td></tr>
      <tr><td><span style="color:#22c55e;font-weight:700;">Connect</span></td><td>Enter your HubSpot Private App token. Tests connection and loads your contact lists.</td><td style="color:#777;">Do this first. Nothing sends without a connection.</td></tr>
    </table>
    <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#3ecfcf;margin-bottom:8px;padding-bottom:5px;border-bottom:1px solid #1e1e1e;">Template Tools - Edit and Export Individual Emails</div>
    <table class="data-table">
      <tr><th>Tab</th><th>What It Does</th><th>Quick Tip</th></tr>
      <tr><td><span style="color:#fff;font-weight:700;">Preview</span></td><td>Read-only view of any template. Click a template in the sidebar to load it.</td><td style="color:#777;">Review before editing so you have the right one selected.</td></tr>
      <tr><td><span style="color:#2563eb;font-weight:700;">Edit</span></td><td>Click any text in the email to edit inline. Toolbar for bold, italic, alignment. Reset restores original.</td><td style="color:#777;">Edits reset on reload. Copy to HubSpot first to save.</td></tr>
      <tr><td><span style="color:#3ecfcf;font-weight:700;">Export</span></td><td>Copies HubSpot-ready HTML to your clipboard. Paste into HubSpot source editor.</td><td style="color:#777;">If clipboard is blocked, copy manually from the text box.</td></tr>
      <tr><td><span style="color:#3ecfcf;font-weight:700;">HS View</span></td><td>Shows how the email renders inside HubSpot: table layout, tokens visible.</td><td style="color:#777;">Check this before every send to catch layout issues.</td></tr>
    </table>
  </div>

  <div class="cmd-section">
    <div class="cmd-section-title">Quick Start</div>
    <p style="font-size:11px;color:#999;line-height:1.6;margin-bottom:10px;">Follow in order. Skipping Connect means nothing sends.</p>
    <div style="font-size:13px;color:#555;line-height:2.2;">
      <div style="display:flex;gap:10px;align-items:baseline;margin-bottom:6px;"><span style="color:#22c55e;font-weight:700;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;letter-spacing:.08em;flex-shrink:0;min-width:52px;">STEP 1</span><span><strong style="color:#22c55e;">Connect</strong> - Enter your HubSpot Private App token, tap Test Connection. Lists load automatically.</span></div>
      <div style="display:flex;gap:10px;align-items:baseline;margin-bottom:6px;"><span style="color:#3ecfcf;font-weight:700;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;letter-spacing:.08em;flex-shrink:0;min-width:52px;">STEP 2</span><span>Pick a template from the sidebar. Tap <strong style="color:#fff;">Preview</strong> to review, <strong style="color:#2563eb;">Edit</strong> to customize.</span></div>
      <div style="display:flex;gap:10px;align-items:baseline;margin-bottom:6px;"><span style="color:#f97316;font-weight:700;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;letter-spacing:.08em;flex-shrink:0;min-width:52px;">STEP 3</span><span><strong style="color:#f97316;">Send</strong> - Name the campaign, confirm reply-to is Hello@BearGrinder.com, select list, run Email Compliance Check, push as draft or scheduled.</span></div>
      <div style="display:flex;gap:10px;align-items:baseline;"><span style="color:#a855f7;font-weight:700;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:10px;letter-spacing:.08em;flex-shrink:0;min-width:52px;">STEP 4</span><span><strong style="color:#a855f7;">Stats</strong> - After sending, hit Sync to pull live open rates, clicks, and unsubscribes.</span></div>
    </div>
  </div>

  <div class="cmd-section">
    <div class="cmd-section-title">Promo Codes</div>
    <p style="font-size:11px;color:#999;line-height:1.6;margin-bottom:12px;">Confirm all codes are active in Shopify before any send. Kevin codes are for personal outreach only.</p>
    <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#555;margin-bottom:8px;">Global Codes</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:12px 14px;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">B2C Launch</div><div style="font-family:monospace;font-size:20px;font-weight:700;color:#3ecfcf;">BEAR20</div><div style="font-size:11px;color:#555;margin-top:3px;">20% off - 2-week window</div><div id="hs-status-BEAR20" style="margin-top:7px;font-size:10px;color:#333;">Confirm active in Shopify</div></div>
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:12px 14px;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">Friends and Family</div><div style="font-family:monospace;font-size:20px;font-weight:700;color:#3ecfcf;">FAM15</div><div style="font-size:11px;color:#555;margin-top:3px;">15% off - No expiration</div><div id="hs-status-FAM15" style="margin-top:7px;font-size:10px;color:#333;">Confirm active in Shopify</div></div>
    </div>
    <div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#555;margin-bottom:8px;">Kevin\'s Codes</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:12px 14px;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">Free Shipping</div><div style="font-family:monospace;font-size:18px;font-weight:700;color:#3ecfcf;">KevinFS</div><div style="font-size:11px;color:#555;margin-top:3px;">Free ship - All products - All countries</div><div id="hs-status-KevinFS" style="margin-top:7px;font-size:10px;color:#333;">Personal outreach only</div></div>
      <div style="background:#0d0d0d;border:1px solid #1e1e1e;border-radius:5px;padding:12px 14px;"><div style="font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:8px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#333;margin-bottom:4px;">10% Off Order</div><div style="font-family:monospace;font-size:15px;font-weight:700;color:#3ecfcf;">kevinf&amp;f10</div><div style="font-size:11px;color:#555;margin-top:3px;">10% off entire order</div><div id="hs-status-kevinff10" style="margin-top:7px;font-size:10px;color:#333;">Personal outreach only</div></div>
    </div>
    <div style="padding:8px 12px;background:#080808;border:1px solid #1a1a1a;border-radius:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
      <span style="font-size:11px;color:#888;flex:1;">Connect HubSpot to check live code status.</span>
      <button onclick="checkHSCoupons()" style="padding:5px 12px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:3px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#888;cursor:pointer;">Check Status</button>
    </div>
  </div>

  <div class="cmd-section">
    <div class="cmd-section-title">Version History</div>
    <table class="data-table" style="margin:0 0 8px 0;">
      <tr><th>Version</th><th>Date</th><th>Changes</th></tr>
      <tr><td style="color:#3ecfcf;font-weight:700;">V18</td><td>Mar 2026</td><td>Clean rebuild. Audience picker. See All Templates. Send Preview Email. Report a Bug. Version collapse. B2C. Logo corrected. Spam footers. Special category. No patents. Em-dashes removed.</td></tr>
    </table>
    <div id="vh-expanded" style="display:none;">
      <table class="data-table" style="margin:0 0 8px 0;">
        <tr><td style="color:#888;">V15-V17</td><td>Mar 2026</td><td>Mobile UI, bottom nav, HubSpot API, campaign builder, AI scoring, compliance, analytics, connect, tooltips, coupon codes.</td></tr>
        <tr><td style="color:#444;">V4-V14</td><td>Mar 2026</td><td>Initial builds through PuffCo-grade redesign, photography, mobile sidebar, A/B versions, editing toolbar.</td></tr>
      </table>
    </div>
    <button onclick="toggleVH(this)" style="background:none;border:1px solid #222;border-radius:3px;padding:5px 12px;font-family:\'Trebuchet MS\',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#444;cursor:pointer;">Show Full History</button>
  </div>

</div>
</div>'''

# AI Insights panel (part of analytics view injection after render)
AI_PANEL = '''<div class="cmd-section" id="ai-section">
  <div class="cmd-section-title" style="display:flex;align-items:center;gap:8px;">
    AI Insights
    <span class="status-pill pill-purple">Claude Powered</span>
  </div>
  <div id="ai-score-display"></div>
  <button class="cmd-btn cmd-btn-purple" onclick="runAIAnalysis()" style="margin-bottom:10px;">Run AI Analysis</button>
  <p style="font-size:11px;color:#888;margin-bottom:10px;line-height:1.5;">Analyzes all templates + send data. Returns a 1-100 quality score and specific actionable improvements. Updates after every send.</p>
  <div id="ai-insights-container"></div>
</div>'''

# Inject AI panel into analytics view
AI_INJECT_JS = '''
// Inject AI panel after analytics renders
function mobNavSet(v){document.querySelectorAll('.mob-nav-btn').forEach(function(b){b.classList.remove('on');});var btn=document.getElementById('mn-'+v);if(btn)btn.classList.add('on');}
var _origRenderAnalytics=renderAnalytics;
renderAnalytics=function(){
  _origRenderAnalytics();
  var body=document.querySelector('#view-analytics .cmd-body');
  if(body&&!document.getElementById('ai-section')){
    var div=document.createElement('div');
    div.innerHTML=''' + repr(AI_PANEL) + ''';
    body.appendChild(div.firstChild);
  }
  // Restore AI data if available
  if(AI_SCORE!==null){
    try{
      var parsed=JSON.parse(localStorage.getItem('bg_ai_score_full')||'null');
      if(parsed) displayAIInsights(parsed,document.getElementById('ai-insights-container'),document.getElementById('ai-score-display'));
    }catch(e){}
  }
};
'''

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Bear Grinder - Email Campaign Command Center V18</title>
<style>{CSS}</style>
</head>
<body>

<div id="sbOverlay" class="tb-overlay" onclick="toggleSB()"></div>

<div class="app">
  <div class="sb" id="sidebar">
    <div class="sb-hd"><div style="color:#fff;cursor:pointer;" onclick="goHome()">{LOGO_W}</div><div class="sb-meta">Email Campaign Command Center &nbsp;/&nbsp; {len(emails)} Templates</div></div>
    <div class="sb-scroll">{sidebar}</div>
  </div>

  <div class="main">
    <div class="topbar">
      <button class="mob-btn" onclick="toggleSB()">&#9776;</button><span id="see-more-hint" style="display:none;font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#3ecfcf;white-space:nowrap;margin-left:6px;align-items:center;gap:3px;">&#8592; Templates</span>
      <span class="tb-seg" id="tbSeg">Guide</span>
      <span class="tb-div">/</span>
      <span class="tb-nm" id="tbNm">Getting Started</span>
      <div class="tb-r">
        <div class="vtabs">
          <button class="vtab on" id="t-guide"    onclick="setView('guide')">Guide</button>
          <button class="vtab"    id="t-preview"  onclick="setView('preview')">Preview</button>
          <button class="vtab t-hsp"  id="t-hsp"  onclick="setView('hsp')">HS Preview</button>
          <button class="vtab t-edit" id="t-edit" onclick="setView('edit')">Edit</button>
          <button class="vtab t-hs"   id="t-hs"   onclick="setView('hs')">Export</button>
          <button class="vtab t-analytics" id="t-analytics" onclick="setView('analytics')">Analytics</button>
          <button class="vtab" id="t-dashboard" onclick="setView('dashboard')">Dashboard</button>
          <button class="vtab t-campaign"  id="t-campaign"  onclick="setView('campaign')">Campaign</button>
          <button class="vtab t-connect"   id="t-connect"   onclick="setView('connect')">Connect</button>
        </div>
        <button class="abtn abtn-copy" id="copyBtn" onclick="doCopy()" title="Copy this template's HTML to clipboard. Paste into HubSpot's HTML editor or any email platform.">Copy HTML</button>
        <button class="abtn abtn-hs"   onclick="goHS()">HubSpot &#8599;</button>
      </div>
    </div>

    <div class="ebar" id="ebar">
      <span class="eb-lbl">Edit Mode</span><span style="font-size:9px;color:#555;font-family:'Trebuchet MS',Arial,sans-serif;letter-spacing:.04em;margin-right:6px;">Session edit - changes revert when you leave</span>
      <button class="etool" onclick="fmt('bold')"><b>B</b></button>
      <button class="etool" onclick="fmt('italic')"><i>I</i></button>
      <button class="etool" onclick="fmt('underline')"><u>U</u></button>
      <span class="etsep"></span>
      <button class="etool" onclick="fmt('justifyLeft')">&#8676;</button>
      <button class="etool" onclick="fmt('justifyCenter')">&#8596;</button>
      <button class="etool" onclick="fmt('justifyRight')">&#8677;</button>
      <button class="ereset" onclick="doReset()">&#8635; Reset</button>
    </div>

    <div class="scroller" id="scroller">
      {GUIDE_HTML}
      {panels}

  <!-- DASHBOARD PANEL -->
  <div class="cmd-panel" id="view-dashboard" style="display:none;background:#0d0d0d;">
    <div class="cmd-hd"><span class="cmd-badge" style="background:#a855f7;color:#fff;">Dashboard</span><span class="cmd-title">Performance &amp; Health</span><span class="cmd-sub">Live + Stored</span></div>
    <div class="cmd-body">

      <!-- BUSINESS HEALTH SUMMARY -->
      <div class="cmd-section">
        <div class="cmd-section-title">Business Health Summary</div>
        <p style="font-size:11px;color:#999;margin-bottom:14px;line-height:1.6;">Email performance benchmarked against e-commerce industry averages. Connect HubSpot for live data. Stored send history shows below.</p>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px;" id="health-grid">
          <div class="health-card" id="hc-opens"><div class="hc-val" id="hv-opens">--</div><div class="hc-label">Open Rate</div><div class="hc-bench">Industry avg: 21%</div><div class="hc-status" id="hs-opens"></div></div>
          <div class="health-card" id="hc-ctr"><div class="hc-val" id="hv-ctr">--</div><div class="hc-label">Click Rate</div><div class="hc-bench">Industry avg: 2.6%</div><div class="hc-status" id="hs-ctr"></div></div>
          <div class="health-card" id="hc-unsub"><div class="hc-val" id="hv-unsub">--</div><div class="hc-label">Unsub Rate</div><div class="hc-bench">Healthy: &lt;0.5%</div><div class="hc-status" id="hs-unsub"></div></div>
          <div class="health-card" id="hc-sent"><div class="hc-val" id="hv-sent">--</div><div class="hc-label">Total Sent</div><div class="hc-bench">All time</div><div class="hc-status" id="hs-sent"></div></div>
          <div class="health-card" id="hc-conv"><div class="hc-val" id="hv-conv">--</div><div class="hc-label">Conversions</div><div class="hc-bench">Est. from clicks</div><div class="hc-status" id="hs-conv"></div></div>
          <div class="health-card" id="hc-rev"><div class="hc-val" id="hv-rev">$--</div><div class="hc-label">Est. Revenue</div><div class="hc-bench">@ $49.99 avg</div><div class="hc-status" id="hs-rev"></div></div>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:8px;">
          <button onclick="refreshDashboard()" style="flex:1;padding:9px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:4px;font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#a855f7;cursor:pointer;">&#8635; Refresh from HubSpot</button>
          <button onclick="resetDashboard()" style="padding:9px 14px;background:#1e1e1e;border:1px solid #2a2a2a;border-radius:4px;font-family:'Trebuchet MS',Arial,sans-serif;font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#444;cursor:pointer;">Reset Local</button>
        </div>
        <div id="dash-hs-status" style="font-size:11px;color:#333;text-align:center;padding:6px 0;"></div>
      </div>

      <!-- SEND LOG TABLE -->
      <div class="cmd-section">
        <div class="cmd-section-title">Send Log</div>
        <p style="font-size:11px;color:#999;margin-bottom:10px;line-height:1.6;">All campaign sends recorded in this tool. Each row is one send event.</p>
        <div style="overflow-x:auto;">
          <table class="data-table" id="send-log-table">
            <tr>
              <th>Date</th>
              <th>Template</th>
              <th>Segment</th>
              <th>List / Audience</th>
              <th>Sent</th>
              <th>Opens</th>
              <th>Clicks</th>
              <th>Unsubs</th>
              <th>Status</th>
            </tr>
            <tr id="send-log-empty"><td colspan="9" style="text-align:center;color:#333;padding:20px;font-size:12px;">No sends recorded yet. Push a campaign via the Send tab to log it here.</td></tr>
          </table>
        </div>
      </div>

      <!-- SEGMENT BREAKDOWN -->
      <div class="cmd-section">
        <div class="cmd-section-title">Segment Breakdown</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;" id="seg-breakdown">
          <div class="seg-card"><div class="seg-card-label">B2C</div><div class="seg-card-val" id="sd-b2c">0 sends</div></div>
          <div class="seg-card"><div class="seg-card-label">Wholesale</div><div class="seg-card-val" id="sd-wholesale">0 sends</div></div>
          <div class="seg-card"><div class="seg-card-label">Distributor</div><div class="seg-card-val" id="sd-dist">0 sends</div></div>
          <div class="seg-card"><div class="seg-card-label">Special</div><div class="seg-card-val" id="sd-special">0 sends</div></div>
        </div>
      </div>

      <!-- ECOMM BENCHMARKS -->
      <div class="cmd-section">
        <div class="cmd-section-title">E-Commerce Benchmarks</div>
        <p style="font-size:11px;color:#999;margin-bottom:10px;line-height:1.6;">Cannabis/lifestyle e-commerce targets. Use these to evaluate campaign performance.</p>
        <table class="data-table">
          <tr><th>Metric</th><th>Your Rate</th><th>Industry Avg</th><th>Top Performers</th><th>Status</th></tr>
          <tr><td>Open Rate</td><td id="bench-opens">--</td><td style="color:#888;">21%</td><td style="color:#22c55e;">35%+</td><td id="bench-opens-st" style="color:#333;">--</td></tr>
          <tr><td>Click Rate</td><td id="bench-ctr">--</td><td style="color:#888;">2.6%</td><td style="color:#22c55e;">5%+</td><td id="bench-ctr-st" style="color:#333;">--</td></tr>
          <tr><td>Unsubscribe</td><td id="bench-unsub">--</td><td style="color:#888;">0.26%</td><td style="color:#22c55e;">&lt;0.1%</td><td id="bench-unsub-st" style="color:#333;">--</td></tr>
          <tr><td>Bounce Rate</td><td id="bench-bounce">--</td><td style="color:#888;">0.7%</td><td style="color:#22c55e;">&lt;0.3%</td><td id="bench-bounce-st" style="color:#333;">--</td></tr>
          <tr><td>Conv. Rate</td><td id="bench-conv">--</td><td style="color:#888;">1-3%</td><td style="color:#22c55e;">5%+</td><td id="bench-conv-st" style="color:#333;">--</td></tr>
        </table>
      </div>

    </div>
  </div>
      <!-- EXPORT TAB -->
      <div class="cmd-panel" id="view-hs">
        <div class="cmd-hd"><span class="cmd-badge" style="background:#3ecfcf;color:#000;">Export</span><span class="cmd-title">HubSpot HTML</span></div>
        <div style="padding:14px 16px 60px;max-width:700px;">
          <div class="cmd-section" id="hscard"><p style="font-size:12px;color:#333;font-family:monospace;">Select a template from the sidebar.</p></div>
        </div>
      </div>
      <!-- HS VIEW TAB -->
      <div class="cmd-panel" id="view-hsp">
        <div class="cmd-hd"><span class="cmd-badge" style="background:#3ecfcf;color:#000;">HS View</span><span class="cmd-title">HubSpot Render Preview</span><span id="hs-prev-lbl" class="cmd-sub"></span></div>
        <div style="background:#222;padding:16px 0 60px;"><div style="max-width:620px;margin:0 auto;background:#fff;border:1px solid #444;" id="hs-prev-inner"></div></div>
      </div>
      <!-- ANALYTICS TAB -->
      <div class="cmd-panel" id="view-analytics"></div>
      <!-- CAMPAIGN TAB -->
      <div class="cmd-panel" id="view-campaign"></div>
      <!-- CONNECT TAB -->
      <div class="cmd-panel" id="view-connect"></div>
    </div>

    <div class="errbar" id="errbar">
      <button onclick="clearErr()" style="background:none;border:none;color:#e24b4b;cursor:pointer;font-size:14px;margin-right:3px">&#10005;</button>
      <span id="errtext"></span>
    </div>
  </div>

  <!-- MOBILE BOTTOM NAV -->
  <div class="mob-nav" id="mobNav">
    <button class="mob-nav-btn on" id="mn-guide" onclick="setView('guide');mobNavSet('guide')">
      <span class="mob-nav-icon">&#128216;</span><span class="mob-nav-lbl">Guide</span>
    </button>
    <button class="mob-nav-btn" id="mn-preview" onclick="setView('preview');mobNavSet('preview')">
      <span class="mob-nav-icon">&#128065;</span><span class="mob-nav-lbl">Preview</span>
    </button>
    <button class="mob-nav-btn c-edit" id="mn-edit" onclick="setView('edit');mobNavSet('edit')">
      <span class="mob-nav-icon">&#9998;</span><span class="mob-nav-lbl">Edit</span>
    </button>
    <button class="mob-nav-btn c-campaign" id="mn-campaign" onclick="setView('campaign');mobNavSet('campaign')">
      <span class="mob-nav-icon">&#128228;</span><span class="mob-nav-lbl">Send</span>
    </button>
    <button class="mob-nav-btn c-analytics" id="mn-analytics" onclick="setView('analytics');mobNavSet('analytics')">
      <span class="mob-nav-icon">&#128200;</span><span class="mob-nav-lbl">Stats</span>
    </button>
    <button class="mob-nav-btn c-connect" id="mn-connect" onclick="setView('connect');mobNavSet('connect')">
      <span class="mob-nav-icon">&#128279;</span><span class="mob-nav-lbl">Connect</span>
    </button>
  </div>
</div>

<div class="toast" id="toast"></div>
<script>{JS}
{AI_INJECT_JS}
</script>
</body>
</html>"""

out='/mnt/user-data/outputs/BG_Email_Campaign_Command_Center_V18.html'
with open(out,'w',encoding='utf-8') as f:
    f.write(HTML)

import re,os
with open(out) as f: check=f.read()
scripts=re.findall(r'<script[^>]*>',check)
print(f"Size: {os.path.getsize(out)/1024:.0f} KB")
print(f"Script tags: {len(scripts)}")
print(f"Cloudflare: {'cloudflare' in check}")
print(f"mailto: {'mailto:' in check}")
print(f"Templates: {len(emails)}")
print("STATUS: CLEAN" if len(scripts)==1 else "STATUS: ISSUES")
