# Bear Grinder Email Campaign Command Center — Project Context
## Version: V18 | March 2026 | Upload this to every new Claude session

---

## CRITICAL: IMAGE MAPPINGS (Pixel-Verified March 2026)

The build script loads ALL images directly from `/mnt/project/`. No temp cache. No session files.
These mappings were confirmed by pixel-level comparison (numpy diff scores < 6.0).

| Template Key | Source File in /mnt/project/ | Former Cache Name | Notes |
|---|---|---|---|
| `hero` | `Main_Splash_Banner_Image.png` | `r_main_splash` | Hero banner, dark overlay |
| `side_black` | `Copy_of_Easy_Lid1.png` | `r_orig_5491` | Lid close-up, light heroes |
| `exploded` | `Chamber_1A_1.png` | `r_orig_5492` | Grinding chamber angle |
| `graphite` | `Large_Grinding_Chamber_B.png` | `r_orig_5493` | Chamber B view |
| `top_tooth` | `Copy_of_OldNew_2.png` | `r_orig_5495` | Old-to-new comparison |
| `built` | `Built_To_Last_Section_Oldtonew.png` | `r_built_to_last` | Built to last section |
| `old_new` | `Copy_of_OldNew_2.png` | `r_old_new_2` | Old vs new comparison |
| `chamber` | `Chamber_1A_1.png` | `r_chamber_1a` | Chamber detail |
| `lid` | `Copy_of_Easy_Lid.png` | `r_easy_lid` | Easy lid feature |
| `grind_a` | `Large_Grinding_Chamber_A.png` | `r_large_grind_a` | Grinding chamber A |
| `grind_b` | `Large_Grinding_Chamber_B.png` | `r_large_grind_b` | Grinding chamber B |
| `tooth` | `Copy_of_Tooth_2.png` | `r_tooth_2` | Tooth design detail |
| `collect` | `Large_Collection_Chamber.png` | `r_collection` | Collection chamber |
| `enjoy_strip` | `Main_Splash_Banner_Image.png` (bottom 50% crop, 600x70) | inline generated | Footer strip |

**All 14 source files verified present in `/mnt/project/` as of March 2026.**

The `load_img(filename, width, quality)` function in the build script handles all loading.
Images are resized to 600px wide and JPEG-compressed. No /tmp/ dependency. Build works in any new session.

---

## Build System

**Build script:** `build_v18.py`
**Run:** `python3 build_v18.py`
**Output:** `/mnt/user-data/outputs/BG_Email_Campaign_Command_Center_V18.html`
**Output size:** ~944KB (images optimized, all 13 keys x 58 instances embedded)
**After every build, verify:**
```bash
python3 -c "
with open('/mnt/user-data/outputs/BG_Email_Campaign_Command_Center_V18.html') as f:
    h = f.read()
js = h[h.find('<script>')+8:h.find('</script>')]
with open('/tmp/check.js','w') as f: f.write(js)
"
node --check /tmp/check.js && echo JS_CLEAN || echo JS_ERROR
```

**Known working base:** V15 (V16 and V17 had JS load errors — never use them as base)

---

## Template Inventory (21 Templates)

### B2C — Consumer (7 templates)
| ID | Name | Subject | Has Image |
|---|---|---|---|
| e01a | Launch Dark | The grinder that changes everything | hero |
| e01b | Launch Lifestyle | Finally. A grinder that keeps up with you. | side_black |
| e02a | Social Proof Dark | 3,200 people already made the switch | hero |
| e02b | Social Proof Light | Real people. Real results. | hero |
| e03a | Last Chance | Last chance: 20% off ends tonight | hero |
| e04a | Evergreen Dark | Still using a grinder that jams? | hero |
| e04b | Evergreen Light | The smoothest grind you've ever had | hero |

### Wholesale — Retail Buyers (5 templates)
| ID | Name | Subject | Has Image |
|---|---|---|---|
| e05a | Announcement Dark | Introducing Bear Grinder V3 to your floor | hero |
| e05b | Announcement Light | New premium grinder. Ready to order. | hero |
| e06a | Margin & Demand | 62.5% margin. Customers are asking for it. | built |
| e07a | Pre-Order Closing | Pre-order closes Friday. Secure your units. | hero |
| e08a | Reorder | Your customers are back. Are you ready? | built |

### Distributor (5 templates)
| ID | Name | Subject | Has Image |
|---|---|---|---|
| e09a | Opportunity Dark | The premium grinder category has a new leader | built |
| e09b | Opportunity Light | 62.5% margin. Patented. Ready to ship. | hero |
| e10a | Follow-Up | Following up on Bear Grinder | old_new |
| e11a | Final Call | Final call: Bear Grinder distribution | hero |
| e12a | Reactivation | Let's reconnect on Bear Grinder | hero |

### Friends & Family (2 templates)
| ID | Name | Subject | Has Image |
|---|---|---|---|
| e13a | Friends & Family Light | You're getting early access | side_black |
| e13b | Friends & Family Fun | We made something and you're getting it first | side_black |

### Special — Trade Show + Samples (2 templates)
| ID | Name | Subject | Has Image |
|---|---|---|---|
| e14a | MJBizCon | See Bear Grinder at MJBizCon | hero |
| e15a | Trade Show Sample F/U | Your Bear Grinder sample is on its way | hero |

---

## Template Helper Functions

All email bodies are built using these Python functions in `build_v18.py`:

```python
img_full(key, h=360)        # Full-width product image block, h=height in px
feat_row(ik, lbl, body, rev=False, light=False)  # 50/50 image + text row
feat_grid(items, light=False) # 2-column feature grid with images
hero_img(key, h, headline, sub, light=False)     # Hero image with overlay text
btn_w(text, url, light=False) # CTA button
stats_bar(pairs)              # Stats strip e.g. [('$49.99','MSRP'),('608','Ball Bearing')]
stripe(t, light=False)        # Light/dark striped text block
ftr(contact, light=False)     # Footer: logo + BEARGRINDER.COM + Enjoy strip + CAN-SPAM
bd(text, light=False)         # Body text block
```

Images are referenced by key from the `I` dict: `I['hero']`, `I['built']`, etc.

---

## Footer Requirements (Every Template — Non-Negotiable)

`ftr()` outputs four layers:
1. Logo + `BEARGRINDER.COM` link (right-aligned)
2. "Enjoy the Grind" image strip (600x70 crop of main splash, opacity 0.55)
3. "ENJOY THE GRIND." text label
4. CAN-SPAM compliance block:
   - Opted-in language
   - Unsubscribe link (`{{unsubscribe}}` HubSpot token)
   - Privacy Policy link
   - `Bear Grinder LLC | San Diego, CA | Hello@BearGrinder.com`

---

## Brand Rules (Enforce in Every Session — Zero Exceptions)

- **No em-dashes** — use plain hyphen or rephrase the sentence
- **No patents** in any customer-facing copy — use "precision-engineered" or "industry-leading"
- **Always B2C** — never D2C
- **BEARGRINDER.COM** visible link in every footer
- **Every template** has at least one product image
- **Reply-to:** Hello@BearGrinder.com
- **Sender name:** Amit Gorodetzer | Bear Grinder
- **Physical address:** Bear Grinder LLC, San Diego, CA
- **JS must pass** `node --check` before delivery — no exceptions
- **No external requests** — all images base64-embedded, no CDN, no Google Fonts

---

## Feature Inventory

| Feature | Status | Notes |
|---|---|---|
| Audience Picker (5 segments) | Built | filterAudience('B2C') etc. |
| See All Templates | Built | filterAudience('ALL') — shows sidebar only, no auto-nav |
| Home Button | Built | goHome() — returns to Guide, resets filter |
| See More Templates hint | Built | Arrow appears next to hamburger after template selected |
| Send Preview Email | Built | openSendPreview() — HubSpot or mailto fallback |
| Report a Bug | Built | openBugReport() — mailto kevin@ElevatedAdvisors.co |
| 1-Pager Attachment | Built | toggle1Pager() — auto-checks for Wholesale/Distributor |
| CAN-SPAM Footer | Built | On all 21 templates via ftr() |
| Enjoy the Grind Strip | Built | make_enjoy_strip() — bottom 50% crop of main splash |
| BEARGRINDER.COM Link | Built | In every ftr() call |
| Dashboard Panel | Built | refreshDashboard(), buildSendLogTable() |
| HubSpot API | Built | Campaign push, analytics sync, CSV upload, Send Preview |
| Email Compliance Check | Built | runCompliance() |
| Version History (collapsed) | Built | toggleVH() — shows V18 only, expandable |
| Mobile Bottom Nav | Built | 6-tab nav bar, safe area inset |
| Logo | Fixed in V18 | 5 toe dots + rounded paw pad, matches packaging photo |

---

## JS Functions Reference

All in a single `<script>` block. Node syntax-verified.

| Function | Purpose |
|---|---|
| `nav(id)` | Switch active template in sidebar + panel |
| `setView(v)` | Switch main view tab |
| `mobNavSet(v)` | Sync mobile bottom nav active state |
| `showToast(msg)` | Show bottom toast notification |
| `goHome()` | Return to Guide, reset filter, close sidebar |
| `filterAudience(seg)` | Filter sidebar by segment or show all |
| `toggleVH(btn)` | Expand/collapse version history |
| `openSendPreview()` | Open Send Preview Email modal |
| `doSendPreview()` | Execute preview send (HubSpot or mailto) |
| `openMailtoPreview(email,subj,html)` | Mailto fallback for preview |
| `openBugReport()` | Open Report a Bug modal |
| `submitBugReport()` | Submit bug report via mailto |
| `toggle1Pager(checked)` | Toggle 1-pager attachment note |
| `checkOnePagerSuggestion(seg)` | Auto-check 1-pager for Wholesale/Dist |
| `checkHSCoupons()` | Check promo code status vs HubSpot |
| `refreshDashboard()` | Reload dashboard metrics from local + HubSpot |
| `buildSendLogTable(analytics)` | Render send log table rows |
| `resetDashboard()` | Clear local analytics storage |
| `runCompliance()` | Run CAN-SPAM compliance check on current template |
| `doReset()` | Reset current template to original HTML |
| `addLog(type,msg)` | Add entry to activity log |
| `connectHS()` | Test HubSpot API connection |

---

## HubSpot Integration

**Base:** `https://api.hubapi.com`
**Auth:** Bearer token (Private App — entered in Connect tab, memory only)
**Required scopes:** `crm.lists.read`, `marketing.email.read`, `marketing.email.write`, `contacts.read`

**Endpoints used:**
- `GET /account-info/v3/details` — test connection
- `GET /contacts/v1/lists` — load contact lists
- `POST /marketing/v3/emails` — create campaign draft
- `POST /marketing/v3/transactional/single-email/send` — Send Preview
- `GET /marketing/v3/emails/{id}` — analytics sync
- `POST /contacts/v1/contact/batch/` — CSV upload

---

## Promo Codes

| Code | Discount | Scope | Expiry |
|---|---|---|---|
| `BEAR20` | 20% off | B2C launch | 2-week window — confirm in Shopify |
| `FAM15` | 15% off | Friends & Family | None — confirm in Shopify |
| `KevinFS` | Free shipping | Kevin personal only | None |
| `kevinf&f10` | 10% off order | Kevin personal only | None |

---

## Open Items

| Item | Owner | Priority |
|---|---|---|
| **Patent #2 issue fee $258 due May 5, 2026** | Amit | URGENT |
| HubSpot Private App token | Amit | Before first send |
| Bear_Grinder_1Pager.pdf upload to HubSpot Files | Amit | Before wholesale/dist sends |
| BEAR20 confirm active in Shopify | Amit | Before B2C launch |
| FAM15, KevinFS, kevinf&f10 confirm active | Amit | Before sends |
| Google Drive persistence layer | Kevin/EAG | Next build session |
| Lifestyle photography for templates | Amit | Future enhancement |

---

## Logged For Next Session: Google Drive Persistence

**Scope (do not build until a dedicated session):**
1. Google Drive folder structure under BG Drive ID `1TOX429fO-aThdKkkgFCCKxxG3tLVR6sc`
   - `/Email Campaign Command Center/Templates/` — 21 individual .html files
   - `/Email Campaign Command Center/Sends/` — JSON send records
   - `/Email Campaign Command Center/Assets/` — 1-pager PDF, images
   - `/Email Campaign Command Center/Backups/` — full tool HTML per version
2. Google Sheets master sync doc (Send Log, Template Library, Campaign Calendar, Health Dashboard, Contact Lists tabs)
3. Tool changes: auto-write to Sheets on send, "Save to Drive" backup button, Google OAuth in Connect tab

---

*Bear Grinder Email Campaign Command Center | Elevated Advisory Group | V18 March 2026*
