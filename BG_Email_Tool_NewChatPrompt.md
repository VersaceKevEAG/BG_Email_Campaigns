# Bear Grinder Email Tool — New Chat Startup Prompt
## Copy and paste this EXACTLY when starting a new Claude session to work on this tool.

---

## PASTE THIS TO START A NEW SESSION:

---

I'm working on the Bear Grinder Email Campaign Command Center, a single-file HTML email tool built for Bear Grinder LLC (beargrinder.com). Current version is V18.

**Files I'm uploading to this chat:**
- `BG_Build_Script_V18.py` — the Python build script (source of truth)
- `BG_Email_Tool_ProjectContext.md` — full context, image mappings, template inventory

**Your role:**
You are editing `BG_Build_Script_V18.py` only. Never rewrite the whole file from scratch. Make targeted changes using `str_replace` or Python patch scripts. Copy the build script to `/home/claude/build_v18.py` first, then edit it there.

After every change, run:

```bash
python3 /home/claude/build_v18.py
```

Then verify:
```bash
python3 -c "
with open('/mnt/user-data/outputs/BG_Email_Campaign_Command_Center_V18.html') as f:
    h = f.read()
js = h[h.find('<script>')+8:h.find('</script>')]
with open('/tmp/check.js','w') as f: f.write(js)
"
node --check /tmp/check.js && echo 'JS CLEAN' || echo 'JS ERROR'
```

**IMAGE SYSTEM — CRITICAL:**
The build script loads ALL images directly from /mnt/project/ using load_img(). There is NO /tmp/ cache dependency. Do not add any image loading that reads from /tmp/. Full mapping table is in BG_Email_Tool_ProjectContext.md.

If you need to add a new image:
```python
I['newkey'] = load_img('Filename_In_Project.png', 600, 75)
```
Source file must exist in /mnt/project/. That's it.

**Hard rules — zero exceptions:**
- No em-dashes anywhere — use plain hyphen or rephrase
- No patent mentions in any customer-facing copy
- Always "B2C" not "D2C"
- BEARGRINDER.COM link in every template footer via ftr()
- Every template must have at least one product image
- CAN-SPAM footer required on every template via ftr()
- Reply-to is always Hello@BearGrinder.com
- JS must pass node --check before delivery

**Brand:**
- Black (#000) + White (#FFF) + Teal (#3ecfcf)
- Headers: Trebuchet MS / Arial Narrow | Body: Helvetica Neue
- Tone: sharp, direct, no AI fluff

**Here's what I need in this session:**
[DESCRIBE YOUR CHANGES HERE]

---

## CONTEXT FOR SPECIFIC TASKS:

### Editing templates:
- Templates are Python functions in build_v18.py using helpers: img_full(), feat_row(), feat_grid(), btn_w(), stats_bar(), stripe(), ftr()
- Each email dict has: id, seg, num, name, subj, body
- Segments: B2C, Wholesale, Distributor, Friends & Family, Special
- ftr() outputs: BEARGRINDER.COM link + Enjoy the Grind strip + CAN-SPAM block

### Editing Guide or Dashboard:
- GUIDE_HTML is a Python f-string triple-quoted variable
- Dashboard panel is id="view-dashboard"
- Audience picker buttons call filterAudience('SegName')
- All JS is in a single <script> block — keep it that way

### Versioning:
- Increment output filename: BG_Email_Campaign_Command_Center_VXX.html
- Update tb-ver span text in HTML
- Add entry to version history table in GUIDE_HTML
- Save updated build script as BG_Build_Script_VXX.py

---

## FILE LOCATIONS

| File | Path |
|---|---|
| Build script (after upload) | /home/claude/build_v18.py |
| Output HTML | /mnt/user-data/outputs/BG_Email_Campaign_Command_Center_V18.html |
| Project images | /mnt/project/*.png and /mnt/project/*.jpg |
| Project context | Upload alongside build script |

---

Bear Grinder Email Campaign Command Center | Built by EAG | V18 March 2026
