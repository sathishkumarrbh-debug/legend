---
name: "college-brochure"
description: "St. Joseph's College of Engineering and Technology (SJCET, Thanjavur) event brochures and posters: FDP, workshop, seminar, conference, guest lecture, industrial visit. House design (purple/gold, Times New Roman, tri-fold A4 landscape with ribbon headings, tech illustration, DMI logo badge), template.html, render.js, college names and checks. Use for any SJCET brochure, flyer or poster."
---

# SJCET event brochure (house design)

The user approved this look (it follows a ChatGPT-made reference they liked). Use it for every future SJCET brochure/poster unless they ask otherwise.

## Files
- `template.html`: tri-fold, A4 landscape, 3 panels of 99 mm. Copy it next to `assets/` and edit only the text. Keep the classes.
- `render.js`: `NODE_PATH=$(npm root -g) node render.js my.html OutName` writes `OutName.pdf` (print) and `OutName.png` (WhatsApp). It warns if a panel overflows. Always open the PNG and look at it before sending.
- `assets/header.webp`: the official college banner (2000x198). The template crops the DMI logo (left) and the NAAC / Anna University / AICTE logos (right) out of it. Don't redraw the logos.

## Design rules
- Font: Times New Roman everywhere (Liberation Serif in the container is metric-identical). Headings bold, uppercase.
- Colours: purple `#4a1d8c`, dark purple `#2a0d5c`, light purple `#7b4fd0`, gold `#e2a614`, light gold `#ffd666` (dates), red `#b3261e` only for "Organised by". Light lavender panel gradients.
- Section headings: purple gradient ribbon, slanted right end, gold slash after it, thin purple rule running to the panel edge (`h3 > span`; the script adds the gold `<em>`).
- Panel 1 (inside-left): event title (uppercase, centred) → gold line-diamond-line divider → keyword subtitle → purple trapezoid banner with gold side bars ("FACULTY DEVELOPMENT PROGRAMME", mode, dates in gold) → tech illustration (glow, network mesh, gears with "AI", diagonal purple/gold streaks) → DMI logo in a white+gold ring with shadow → Organised by / Department / college name / address / approval line / three accreditation logos.
- Panel 2: About the College, About the Department, Organising Committee, Who Can Attend, "Programme at a Glance" white box with gold left bar.
- Panel 3: About the Programme, Programme Objectives (purple dot bullets), Key Resource Persons (gold left bar; purple date · bold name; affiliation; purple italic topic).
- Corner decorations: purple/gold triangular shards (top-left and bottom-left of panel 1, bottom-right of panel 3), dotted grid patches at top corners.
- Change the illustration's gear label/icons to suit the topic (e.g. no "AI" for a non-AI event).
- Single-page A4 portrait poster (e.g. a WhatsApp invite): same colours, fonts, ribbons and banner; college banner image across the top.

## College facts (check every time; ask if a name or title is missing)
- St. Joseph's College of Engineering and Technology, A.S. Nagar, Elupatti, Thanjavur – 613 403. Approved by AICTE, New Delhi; affiliated to Anna University, Chennai; NAAC accredited. Run by DMI Foundations, motto "Fully Human & Fully Alive".
- Rev. Sr. P. Mariya Alangaram, DMI: Administrator (Chief Patron).
- Prof. Dr. R. Ravikumar: Principal (i/c) (Patron).
- Mr. M. Sureshkumar: HoD, Mechanical (the Oct 2026 PPCE seminar poster also lists him as AP/Mech when he is the speaker).
- Dr. S. R. Sathishkumar: AP/Mech, event co-ordinator (PPCE seminar, Oct 2026).
- Mechanical student lists: III year 821924114xxx (26 students), IV year 821923114xxx.
- Prof. Mr. A. Manikandan: HOD, MBA.
- Dr. C. Anand: Mechanical, FDP co-ordinator (Oct 2026 FDP).

## Event file (seminar/FDP report .docx)
Use the college letterhead .docx the user supplies (its header1.xml carries the logo/address). Order: Requisition letter → Circular → Report (details table, programme details, objectives, outcomes, photographs with figure captions, 4 signatures: Event Co-ordinator, HoD, IQAC Co-ordinator, Principal) → Attendance → Feedback (4 blocks/page). Times New Roman 12 pt, proper tables (no space-padding), numbered lists, each section on a new page, and check the render so signatures don't fall onto a page by themselves. LibreOffice Writer may need `apt-get install -y libreoffice-writer-nogui` before rendering.

## Checks before sending
- Never add a role or word the sources don't give (the ChatGPT version wrote "Dr. C. Anand Chairman").
- Fix obvious typos from request letters (e.g. "12.1026" → 12.10.2026) and tell the user what you changed.
- Weekday matches each date; dates in order; no duplicate dates.
- Don't invent time, platform link, registration fee or phone numbers. List what is missing and ask.
- Text that is general wording (About the College, About the Department) must be flagged so they can swap in the official text.
- Deliver PNG + PDF.
