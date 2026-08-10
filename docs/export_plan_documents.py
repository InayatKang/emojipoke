#!/usr/bin/env python3
"""Export the Alberta 3/4 science co-teaching plan to polished DOCX and PDF."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT_DIR = Path(__file__).resolve().parent
DOCX_PATH = OUT_DIR / "Alberta_Grade_3_4_Science_CoTeaching_Plan.docx"
PDF_PATH = OUT_DIR / "Alberta_Grade_3_4_Science_CoTeaching_Plan.pdf"

# Brand-ish colours (professional education look; not purple)
NAVY = RGBColor(0x1B, 0x3A, 0x4B)
TEAL = RGBColor(0x2F, 0x6F, 0x6A)
ACCENT = RGBColor(0xC4, 0x7B, 0x2C)
LIGHT_BG = "E8F0F0"
HEADER_BG = "1B3A4B"
ALT_ROW = "F4F7F7"

RL_NAVY = colors.HexColor("#1B3A4B")
RL_TEAL = colors.HexColor("#2F6F6A")
RL_ACCENT = colors.HexColor("#C47B2C")
RL_LIGHT = colors.HexColor("#E8F0F0")
RL_ALT = colors.HexColor("#F4F7F7")
RL_LINE = colors.HexColor("#D0D8D8")


def set_cell_shading(cell, hex_color: str) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_run_font(run, name="Calibri", size=11, bold=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def add_heading_styled(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if level == 0:
        set_run_font(run, size=22, bold=True, color=NAVY)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(6)
    elif level == 1:
        set_run_font(run, size=16, bold=True, color=NAVY)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
    elif level == 2:
        set_run_font(run, size=13, bold=True, color=TEAL)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
    else:
        set_run_font(run, size=11, bold=True, color=TEAL)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
    return p


def add_body(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, size=11, bold=bold)
    run.italic = italic
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.space_before = Pt(0)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    run = p.add_run(text)
    set_run_font(run, size=11)
    p.paragraph_format.left_indent = Inches(0.25 + 0.2 * level)
    p.paragraph_format.space_after = Pt(3)
    return p


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=10, bold=True, color=RGBColor(255, 255, 255))
        set_cell_shading(cell, HEADER_BG)

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(val)
            set_run_font(run, size=9)
            if r_idx % 2 == 1:
                set_cell_shading(cell, ALT_ROW)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph()
    return table


def build_docx():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(1.8)
        section.right_margin = Cm(1.8)

    # Title block
    add_heading_styled(doc, "Alberta Grade 3 & 4 Science", level=0)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Combined-Class Co-Teaching Plan")
    set_run_font(run, size=16, bold=True, color=TEAL)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        "Based on Alberta Education new K–6 Science curriculum (finalized March 2023)"
    )
    set_run_font(run, size=10, color=RGBColor(0x55, 0x55, 0x55))
    run.italic = True

    add_body(
        doc,
        "Official curriculum: curriculum.learnalberta.ca  ·  Snapshot: alberta.ca/curriculum-science",
        italic=True,
    )

    # Callout
    p = doc.add_paragraph()
    run = p.add_run("Bottom line: ")
    set_run_font(run, size=11, bold=True, color=ACCENT)
    run = p.add_run(
        "Both grades share the same seven organizing ideas. Teach shared big ideas together, "
        "then use grade-specific exit tickets, journals, and projects so each grade still meets its learner outcomes."
    )
    set_run_font(run, size=11)

    # Section 1
    add_heading_styled(doc, "1. How the Two Grades Are Organized", level=1)
    add_body(
        doc,
        "Both grades use the same seven organizing ideas. That is the main reason a split 3/4 class can share many lessons.",
    )
    add_table(
        doc,
        ["Organizing Idea", "Grade 3 Focus", "Grade 4 Focus"],
        [
            ["Matter", "How substances change, including water & the water cycle", "Waste management & environmental impacts"],
            ["Energy", "Contact forces & simple machines", "Non-contact forces: gravity & magnetism"],
            ["Earth Systems", "Changes to Earth’s surface; layers/fossils; FNMI land knowledge", "Earth’s systems (land, air, water, organisms) & conservation"],
            ["Living Systems", "Interactions among plants, humans, animals & environment", "External structures & sensory organs related to function"],
            ["Space", "Not a Grade 3 organizing focus", "Objects in space connected to daily life"],
            ["Computer Science", "Creativity + computational / divergent thinking", "Design processes to solve problems"],
            ["Scientific Methods", "Sources, accuracy & analysis of data", "Role of data & evidence in science"],
        ],
    )

    # Section 2
    add_heading_styled(doc, "2. Similarity Map — What You Can Co-Teach", level=1)
    add_heading_styled(doc, "Strongest co-teach overlaps (plan these as joint units)", level=2)
    add_table(
        doc,
        ["Shared Theme", "Grade 3 Angle", "Grade 4 Angle", "Split-Class Strategy"],
        [
            [
                "Water & Earth’s systems",
                "Water cycle; states of water; local water safety",
                "Hydrosphere; water connecting land, air & life; conservation",
                "Shared mini water-cycle experiments; Gr 3 diagrams cycle; Gr 4 maps spheres & conservation",
            ],
            [
                "Human impact / stewardship",
                "Human, plant & animal activities change Earth’s surface; farming; respect for land",
                "Waste management; reduce/reuse/recycle/repurpose/repair/compost",
                "Shared “Our impact” inquiry; Gr 3 land/farming; Gr 4 waste audit + conservation plan",
            ],
            [
                "Forces (push/pull)",
                "Contact forces; friction; simple machines; FNMI simple machines",
                "Gravity & magnetism; poles attract/repel",
                "Shared force language; Gr 3 machine stations; Gr 4 magnet/gravity stations",
            ],
            [
                "Living things & environments",
                "Food chains; human effects; protection; FNMI relationships",
                "External structures → function; sensory organs",
                "Shared organism walk; Gr 3 food chains; Gr 4 structure–function & senses",
            ],
            [
                "Inquiry / data / design",
                "Data sources & accuracy; creativity & computational thinking",
                "Evidence in science; design process",
                "Weave into every unit: same investigation, different analysis depth",
            ],
        ],
    )

    add_heading_styled(doc, "Partial overlaps (shared launch, then diverge)", level=2)
    add_table(
        doc,
        ["Theme", "Shared Launch", "Grade-Specific Finish"],
        [
            [
                "Matter / materials",
                "Properties of materials; natural vs processed",
                "Gr 3: reversible/permanent change, melting/freezing/boiling, water cycle. Gr 4: hazard symbols, waste methods, personal waste plan",
            ],
            [
                "Earth’s surface stories",
                "Alberta landscapes, erosion, land changes",
                "Gr 3: fossils, layers, dinosaurs, FNMI land knowledge. Gr 4: spheres & how they sustain life",
            ],
            [
                "Computer Science",
                "Creative problem solving with steps/instructions",
                "Gr 3: creative/divergent thinking. Gr 4: full design cycle (need → plan → prototype → test → improve)",
            ],
        ],
    )

    add_heading_styled(doc, "Teach separately (do not force together)", level=2)
    add_table(
        doc,
        ["Grade 3-Only Priority", "Grade 4-Only Priority"],
        [
            ["Simple machines design challenge", "Space & daily life (day/night, seasons, sky objects)"],
            ["Deep dive: fossils / paleontology in Alberta", "Magnetism investigations (poles, magnetizing materials)"],
            ["Contact-force investigations with machines", "Formal waste-management / dangerous-materials unit"],
        ],
    )
    add_body(
        doc,
        "Practical tip: When one grade has a unique topic (e.g. Grade 4 Space), use workshop rotation — one grade with you on the unique outcome, the other on an independent inquiry, reading, or coding/design task tied to Scientific Methods / Computer Science.",
        italic=True,
    )

    # Section 3
    add_heading_styled(doc, "3. Suggested Year Sequence for a 3/4 Combined Class", level=1)
    add_table(
        doc,
        ["Term Block", "Joint Theme", "Grade 3 Must-Hit", "Grade 4 Must-Hit"],
        [
            ["1", "Matter + Scientific Methods", "Changes of state; water cycle", "Waste & dangerous materials"],
            ["2", "Energy (Forces) + CS design", "Contact forces; simple machines", "Gravity & magnetism"],
            ["3", "Earth Systems + Living Systems", "Surface change; fossils; interactions", "Earth spheres; conservation; structures & senses"],
            ["4", "Capstone + Grade 4 Space", "Integrated inquiry fair", "Space & daily life + evidence project"],
        ],
    )
    add_body(
        doc,
        "Weave Scientific Methods and Computer Science through all blocks rather than isolating them as short units.",
    )

    # Section 4
    add_heading_styled(doc, "4. Co-Teachable Unit Kits", level=1)

    # Unit A
    add_heading_styled(doc, "Unit A — Water, Change, and Earth’s Systems", level=2)
    add_body(doc, "Gr 3: substances change / water cycle  ·  Gr 4: water in Earth systems + conservation", italic=True)
    add_body(doc, "In-class activities", bold=True)
    for item in [
        "Bag/jar mini water cycle (warm water + ice lid): both observe; Gr 3 labels evaporation/condensation/precipitation; Gr 4 links to hydrosphere and conservation.",
        "Alberta seasonal water walk (ice, snow, puddles, runoff) — include ice safety (Gr 3).",
        "Conservation action plan / classroom water–litter audit (stronger Gr 4 product; Gr 3 contributes observations).",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Videos", bold=True)
    for item in [
        "Crash Course Kids – The Great Aqua Adventure (#24.1): youtube.com/watch?v=z5G4NCwWUxY",
        "NASA – Exploring the Water Cycle: nasa.gov/stem-content/exploring-the-water-cycle/",
        "NASA GPM – Animated Water Cycle: gpm.nasa.gov/education/interactive/animated-water-cycle",
        "PBS LearningMedia – Water Cycle Animation (Clue into Climate)",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Books", bold=True)
    for item in [
        "The Water Cycle — Bobbie Kalman (Crabtree)",
        "Water — National Geographic Kids Readers (Level 3)",
        "The Lost Drop",
        "Autumn Peltier, Water Warrior (water respect / stewardship)",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Alberta planning hubs", bold=True)
    for item in [
        "library.ulethbridge.ca/Science3/matter",
        "library.ulethbridge.ca/Sciencegrade4/EarthSystems",
        "APLC CPAR Grade 3 Matter (PDF on aplc.ca)",
        "RDPSD Science 3 – Matter (sites.google.com/rdpsd.ab.ca/rdpsdscience)",
    ]:
        add_bullet(doc, item)

    # Unit B
    add_heading_styled(doc, "Unit B — Waste, Land Change, and Stewardship", level=2)
    add_body(doc, "Gr 3: humans/plants/animals change Earth’s surface; farming  ·  Gr 4: waste management", italic=True)
    add_body(doc, "In-class activities", bold=True)
    for item in [
        "Classroom waste sort (reduce / reuse / recycle / repurpose / repair / compost).",
        "“Before & after land” photo inquiry (Alberta farming, roads, parks, erosion).",
        "Action plan: Gr 3 protecting land/plants/animals; Gr 4 waste reduction + hazard symbol hunt.",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Books & materials", bold=True)
    for item in [
        "Little Land; Nature Is a Sculptor; The Dirt Book",
        "Older EPS unit Waste and Our World (pre-2023 Gr 4 Topic A) — free at epsb-resources.sellfy.store",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Alberta hubs: ULethbridge Gr 4 Matter; Gr 3 Earth Systems; APLC Earth Systems PD", italic=True)

    # Unit C
    add_heading_styled(doc, "Unit C — Forces: Contact Machines + Gravity/Magnets", level=2)
    add_body(doc, "Gr 3: contact forces & simple machines  ·  Gr 4: gravity & magnetism", italic=True)
    add_body(doc, "Station day model", bold=True)
    for item in [
        "Push/pull & friction stations (both grades).",
        "Lever / ramp / wheel challenges (Gr 3 required: design a device using simple machines).",
        "Magnet poles & magnetizing a paperclip (Gr 4 required).",
        "Drop-height / gravity predictions (Gr 4; Gr 3 can observe and help graph).",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Videos", bold=True)
    for item in [
        "Crash Course Kids – Defining Gravity (#4.1)",
        "PBS LearningMedia – Simple Machines (DIY Science Time)",
        "Magnetism shorts via LearnAlberta / RDPSD Energy pages",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Books", bold=True)
    for item in [
        "Push-Pull Morning; How Do Pushes and Pulls Affect Motion?; Hands-On Science: Motion",
        "Operation Cupcake (force/design hook)",
        "Magnets Push, Magnets Pull / Attract and Repel: A Look at Magnets",
    ]:
        add_bullet(doc, item)

    # Unit D
    add_heading_styled(doc, "Unit D — Living Systems: Interactions + Structures", level=2)
    add_body(doc, "Gr 3: how plants/animals interact  ·  Gr 4: external structures & sensory organs", italic=True)
    add_body(doc, "In-class activities", bold=True)
    for item in [
        "Schoolyard organism census (appearance, habitat, structures).",
        "Food-chain construction for local Alberta environments (Gr 3 focus).",
        "Structure–function cards: claw/beak/leaf/root/shell → job (Gr 4 focus).",
        "Senses investigation + plant response to light (window experiment).",
    ]:
        add_bullet(doc, item)
    add_body(doc, "Books", bold=True)
    for item in [
        "Creep, Leap, Crunch! A Food Chain Story; Bringing Back the Wolves",
        "Finding Moose; Raven, Rabbit, Deer; A Night in Fernwood Forest",
        "Planting a Garden in Room 6; Butterflies in Room 6",
        "Exploring Ecosystems with Max Axiom (graphic novel, Gr 3–4)",
    ]:
        add_bullet(doc, item)

    # Unit E & F
    add_heading_styled(doc, "Unit E — Fossils & Alberta Land Stories (Gr 3 heavy)", level=2)
    add_body(
        doc,
        "Gr 3 required: layers hold stories of the past; dinosaur fossils; FNMI relationships with land. "
        "Gr 4: enrichment while deepening spheres/conservation, or as a reading/inquiry centre.",
    )
    for item in [
        "Activities: cookie/layered-cup fossil dig; Alberta Badlands virtual tour; Knowledge Keeper/Elder protocols via school FNMI lead.",
        "Books: Dinosaurs of the Alberta Badlands; The Fossil Whisperer; Kid Paleontologist; Over and Under the Canyon.",
    ]:
        add_bullet(doc, item)

    add_heading_styled(doc, "Unit F — Space & Daily Life (Grade 4 required)", level=2)
    add_body(
        doc,
        "Run as a Grade 4 focus block with Grade 3 on review/inquiry centres or CS design tasks. "
        "Hub: library.ulethbridge.ca/Sciencegrade4/Space + APLC Space implementation PD.",
    )

    # Section 5
    add_heading_styled(doc, "5. Best Alberta One-Stop Resource Hubs", level=1)
    hubs = [
        "Official outcomes: curriculum.learnalberta.ca (Science)",
        "Resource search + Pearson Spark eBooks: curriculum.learnalberta.ca/resources (teacher login)",
        "ULethbridge Curriculum Lab: library.ulethbridge.ca/Science3 and Sciencegrade4",
        "Science Curriculum Wayfinder (UAlberta CMASTE): sciencecurriculumwayfinder.ca",
        "APLC CPAR (sample activities & assessments): aplc.ca",
        "CESD shared planning: sites.google.com/cesd73.ca/cesd-new-curriculum",
        "Red Deer Public Science: sites.google.com/rdpsd.ab.ca/rdpsdscience",
    ]
    for i, item in enumerate(hubs, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. {item}")
        set_run_font(run, size=11)
        p.paragraph_format.space_after = Pt(4)

    # Section 6
    add_heading_styled(doc, "6. Differentiation Checklist (Both Grades Compliant)", level=1)
    add_body(doc, "For every joint lesson, prepare:", bold=True)
    for item in [
        "One shared hook / investigation",
        "Grade 3 success criteria tied to their learner outcome",
        "Grade 4 success criteria tied to their learner outcome",
        "Two exit products (can be short) — e.g. Gr 3 labelled diagram; Gr 4 explanation with evidence",
        "One FNMI / local Alberta connection where curriculum names it",
        "Scientific Methods skill (observe → record → compare sources → conclude)",
        "Optional CS extension (sequence instructions, design loop, Scratch/unplugged coding)",
    ]:
        add_bullet(doc, "☐  " + item)

    # Section 7
    add_heading_styled(doc, "7. Quick “Teach Both Grades Today” Lesson Pattern", level=1)
    steps = [
        ("Hook (5–10 min)", "Video or object demo for both"),
        ("Shared investigation (20–25 min)", "Same materials"),
        ("Split processing (15–20 min)", "Grade-specific notebook prompt / centre"),
        ("Share-out (5–10 min)", "Mixed pairs teach one new idea to the other grade"),
        ("Assessment", "Sticky-note exit ticket with grade-coded question"),
    ]
    for title, detail in steps:
        p = doc.add_paragraph()
        run = p.add_run(f"{title}: ")
        set_run_font(run, size=11, bold=True, color=TEAL)
        run = p.add_run(detail)
        set_run_font(run, size=11)
        p.paragraph_format.space_after = Pt(4)

    add_body(
        doc,
        "This pattern keeps one prep load while protecting curriculum fidelity.",
        italic=True,
    )

    # Sources
    add_heading_styled(doc, "Sources", level=1)
    for item in [
        "Alberta Education Science curriculum (Gr 3–4 organizing ideas & KUSP via new LearnAlberta)",
        "Alberta.ca Science curriculum snapshot and New K–6 Science fact sheet PDF",
        "University of Lethbridge Curriculum Laboratory Science Grade 3 & Grade 4 resource guides",
        "APLC CPAR / implementation resources",
        "Science Curriculum Wayfinder (CMASTE, University of Alberta)",
        "NASA, PBS LearningMedia, Crash Course Kids (free classroom media)",
    ]:
        add_bullet(doc, item)

    # Footer note
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    run = p.add_run(
        "Editable Word document for classroom planning. Adapt timelines to your school calendar and available field trips."
    )
    set_run_font(run, size=9, color=RGBColor(0x66, 0x66, 0x66))
    run.italic = True

    doc.save(DOCX_PATH)
    print(f"Wrote {DOCX_PATH}")


def rl_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=RL_NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
            leading=24,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=RL_TEAL,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=RL_NAVY,
            spaceBefore=16,
            spaceAfter=8,
            borderPadding=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=RL_TEAL,
            spaceBefore=10,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Callout",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=RL_NAVY,
            backColor=RL_LIGHT,
            borderPadding=8,
            spaceAfter=10,
            spaceBefore=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Cell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CellHead",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            leftIndent=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterNote",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=colors.HexColor("#666666"),
            spaceBefore=12,
        )
    )
    return styles


def make_table(data, col_widths, styles):
    formatted = []
    for r_idx, row in enumerate(data):
        style = styles["CellHead"] if r_idx == 0 else styles["Cell"]
        formatted.append([Paragraph(str(c), style) for c in row])
    t = Table(formatted, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), RL_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, RL_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), RL_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t


def bullets(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(i, styles["BulletBody"]), leftIndent=12, value="•") for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=15,
        bulletFontName="Helvetica",
        bulletFontSize=9,
    )


def build_pdf():
    styles = rl_styles()
    story = []
    usable = letter[0] - 1.4 * inch

    story.append(Paragraph("Alberta Grade 3 &amp; 4 Science", styles["CoverTitle"]))
    story.append(Paragraph("Combined-Class Co-Teaching Plan", styles["CoverSub"]))
    story.append(
        Paragraph(
            "Based on Alberta Education new K–6 Science curriculum (finalized March 2023)<br/>"
            "Official: curriculum.learnalberta.ca &nbsp;·&nbsp; Snapshot: alberta.ca/curriculum-science",
            styles["Meta"],
        )
    )
    story.append(
        Paragraph(
            "<b>Bottom line:</b> Both grades share the same seven organizing ideas. Teach shared big ideas together, "
            "then use grade-specific exit tickets, journals, and projects so each grade still meets its learner outcomes.",
            styles["Callout"],
        )
    )

    story.append(Paragraph("1. How the Two Grades Are Organized", styles["H1Custom"]))
    story.append(
        Paragraph(
            "Both grades use the same seven organizing ideas. That is the main reason a split 3/4 class can share many lessons.",
            styles["BodyCustom"],
        )
    )
    story.append(
        make_table(
            [
                ["Organizing Idea", "Grade 3 Focus", "Grade 4 Focus"],
                ["Matter", "Substances change, including water & water cycle", "Waste management & environmental impacts"],
                ["Energy", "Contact forces & simple machines", "Gravity & magnetism"],
                ["Earth Systems", "Surface change; layers/fossils; FNMI land knowledge", "Earth systems & conservation"],
                ["Living Systems", "Plant/human/animal/environment interactions", "External structures & sensory organs"],
                ["Space", "Not a Grade 3 focus", "Objects in space connected to daily life"],
                ["Computer Science", "Creativity + computational thinking", "Design processes to solve problems"],
                ["Scientific Methods", "Sources, accuracy & analysis of data", "Role of data & evidence"],
            ],
            [1.3 * inch, 2.6 * inch, 2.6 * inch],
            styles,
        )
    )

    story.append(Paragraph("2. Similarity Map — What You Can Co-Teach", styles["H1Custom"]))
    story.append(Paragraph("Strongest co-teach overlaps", styles["H2Custom"]))
    story.append(
        make_table(
            [
                ["Shared Theme", "Grade 3", "Grade 4", "Strategy"],
                [
                    "Water & Earth systems",
                    "Water cycle; states; safety",
                    "Hydrosphere; conservation",
                    "Shared experiment; split products",
                ],
                [
                    "Stewardship / impact",
                    "Land change; farming; respect",
                    "Waste management; 6 Rs",
                    "Shared inquiry; split action plans",
                ],
                [
                    "Forces",
                    "Contact forces; simple machines",
                    "Gravity; magnetism",
                    "Shared language; grade stations",
                ],
                [
                    "Living systems",
                    "Food chains; human effects",
                    "Structures & senses",
                    "Shared walk; split analysis",
                ],
                [
                    "Inquiry / design",
                    "Data accuracy; creativity",
                    "Evidence; design process",
                    "Same investigation, deeper analysis",
                ],
            ],
            [1.35 * inch, 1.7 * inch, 1.7 * inch, 1.75 * inch],
            styles,
        )
    )

    story.append(Paragraph("Partial overlaps", styles["H2Custom"]))
    story.append(
        make_table(
            [
                ["Theme", "Shared Launch", "Grade-Specific Finish"],
                [
                    "Matter / materials",
                    "Properties; natural vs processed",
                    "Gr 3: changes of state/water cycle. Gr 4: hazards & waste plan",
                ],
                [
                    "Earth surface stories",
                    "Alberta landscapes & erosion",
                    "Gr 3: fossils/FNMI land. Gr 4: spheres sustaining life",
                ],
                [
                    "Computer Science",
                    "Steps / creative problem solving",
                    "Gr 3: divergent thinking. Gr 4: full design cycle",
                ],
            ],
            [1.5 * inch, 2.4 * inch, 2.6 * inch],
            styles,
        )
    )

    story.append(Paragraph("Teach separately", styles["H2Custom"]))
    story.append(
        make_table(
            [
                ["Grade 3-Only", "Grade 4-Only"],
                ["Simple machines design challenge", "Space & daily life"],
                ["Fossils / paleontology deep dive", "Magnetism investigations"],
                ["Contact-force + machines investigations", "Formal waste / dangerous materials unit"],
            ],
            [3.25 * inch, 3.25 * inch],
            styles,
        )
    )
    story.append(
        Paragraph(
            "<i>Tip:</i> Use workshop rotation for unique topics — one grade with you, the other on inquiry/reading/CS.",
            styles["BodyCustom"],
        )
    )

    story.append(Paragraph("3. Suggested Year Sequence", styles["H1Custom"]))
    story.append(
        make_table(
            [
                ["Block", "Joint Theme", "Grade 3 Must-Hit", "Grade 4 Must-Hit"],
                ["1", "Matter + Scientific Methods", "Changes of state; water cycle", "Waste & dangerous materials"],
                ["2", "Energy (Forces) + CS", "Contact forces; simple machines", "Gravity & magnetism"],
                ["3", "Earth + Living Systems", "Surface change; fossils; interactions", "Spheres; conservation; structures"],
                ["4", "Capstone + Space", "Integrated inquiry fair", "Space & daily life + evidence"],
            ],
            [0.6 * inch, 1.9 * inch, 2.0 * inch, 2.0 * inch],
            styles,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("4. Co-Teachable Unit Kits", styles["H1Custom"]))

    story.append(Paragraph("Unit A — Water, Change, and Earth’s Systems", styles["H2Custom"]))
    story.append(
        Paragraph(
            "<i>Gr 3:</i> substances change / water cycle &nbsp;·&nbsp; <i>Gr 4:</i> water in Earth systems + conservation",
            styles["BodyCustom"],
        )
    )
    story.append(Paragraph("<b>Activities</b>", styles["BodyCustom"]))
    story.append(
        bullets(
            [
                "Bag/jar mini water cycle — Gr 3 labels cycle stages; Gr 4 links hydrosphere & conservation.",
                "Alberta seasonal water walk (include ice safety).",
                "Classroom water/litter audit → conservation action plan.",
            ],
            styles,
        )
    )
    story.append(Paragraph("<b>Videos</b>", styles["BodyCustom"]))
    story.append(
        bullets(
            [
                "Crash Course Kids – The Great Aqua Adventure (#24.1)",
                "NASA Exploring the Water Cycle; NASA GPM Animated Water Cycle",
                "PBS LearningMedia – Water Cycle Animation (Clue into Climate)",
            ],
            styles,
        )
    )
    story.append(Paragraph("<b>Books</b>", styles["BodyCustom"]))
    story.append(
        bullets(
            [
                "The Water Cycle (Bobbie Kalman); Water (Nat Geo Kids Level 3)",
                "The Lost Drop; Autumn Peltier, Water Warrior",
            ],
            styles,
        )
    )

    story.append(Paragraph("Unit B — Waste, Land Change, and Stewardship", styles["H2Custom"]))
    story.append(
        bullets(
            [
                "Waste sort (reduce/reuse/recycle/repurpose/repair/compost).",
                "Before & after Alberta land photo inquiry; hazard symbol hunt (Gr 4).",
                "Books: Little Land; Nature Is a Sculptor; The Dirt Book; EPS Waste and Our World activities.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Unit C — Forces: Machines + Gravity/Magnets", styles["H2Custom"]))
    story.append(
        bullets(
            [
                "Stations: push/pull & friction (both); levers/ramps/wheels (Gr 3); magnets & gravity (Gr 4).",
                "Videos: Crash Course Kids Defining Gravity; PBS Simple Machines.",
                "Books: Push-Pull Morning; Hands-On Science: Motion; Magnets Push, Magnets Pull.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Unit D — Living Systems: Interactions + Structures", styles["H2Custom"]))
    story.append(
        bullets(
            [
                "Schoolyard organism census; local food chains (Gr 3); structure–function cards (Gr 4); senses/light experiments.",
                "Books: Creep, Leap, Crunch!; Bringing Back the Wolves; Finding Moose; Raven, Rabbit, Deer; Max Axiom Ecosystems.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Unit E — Fossils & Alberta Land Stories (Gr 3 heavy)", styles["H2Custom"]))
    story.append(
        bullets(
            [
                "Cookie/layered fossil dig; Badlands virtual tour; FNMI land knowledge via school protocols.",
                "Books: Dinosaurs of the Alberta Badlands; The Fossil Whisperer; Kid Paleontologist.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Unit F — Space & Daily Life (Grade 4 required)", styles["H2Custom"]))
    story.append(
        Paragraph(
            "Run as a Grade 4 focus block; Grade 3 on inquiry/CS centres. Hub: ULethbridge Gr 4 Space + APLC Space PD.",
            styles["BodyCustom"],
        )
    )

    story.append(Paragraph("5. Best Alberta One-Stop Resource Hubs", styles["H1Custom"]))
    story.append(
        bullets(
            [
                "Official outcomes — curriculum.learnalberta.ca (Science)",
                "LearnAlberta resources + Pearson Spark eBooks (teacher login)",
                "ULethbridge Curriculum Lab — library.ulethbridge.ca/Science3 and Sciencegrade4",
                "Science Curriculum Wayfinder — sciencecurriculumwayfinder.ca",
                "APLC CPAR — aplc.ca (sample activities & assessments)",
                "CESD New Curriculum site; RDPSD Science site",
            ],
            styles,
        )
    )

    story.append(Paragraph("6. Differentiation Checklist", styles["H1Custom"]))
    story.append(Paragraph("For every joint lesson, prepare:", styles["BodyCustom"]))
    story.append(
        bullets(
            [
                "One shared hook / investigation",
                "Grade 3 success criteria tied to their learner outcome",
                "Grade 4 success criteria tied to their learner outcome",
                "Two exit products (e.g. Gr 3 labelled diagram; Gr 4 evidence explanation)",
                "FNMI / local Alberta connection where curriculum names it",
                "Scientific Methods skill + optional CS extension",
            ],
            styles,
        )
    )

    story.append(Paragraph("7. Quick Lesson Pattern", styles["H1Custom"]))
    story.append(
        make_table(
            [
                ["Step", "Time", "What Happens"],
                ["Hook", "5–10 min", "Video or object demo for both"],
                ["Shared investigation", "20–25 min", "Same materials"],
                ["Split processing", "15–20 min", "Grade-specific notebook / centre"],
                ["Share-out", "5–10 min", "Mixed pairs teach one idea"],
                ["Assessment", "Exit", "Sticky-note ticket with grade-coded question"],
            ],
            [1.8 * inch, 1.1 * inch, 3.6 * inch],
            styles,
        )
    )

    story.append(Paragraph("Sources", styles["H1Custom"]))
    story.append(
        bullets(
            [
                "Alberta Education Science curriculum via new LearnAlberta",
                "Alberta.ca Science snapshot and K–6 Science fact sheet",
                "ULethbridge Curriculum Lab; APLC CPAR; Science Curriculum Wayfinder",
                "NASA, PBS LearningMedia, Crash Course Kids",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "Presentable planning document for classroom use. Adapt timelines to your school calendar.",
            styles["FooterNote"],
        )
    )

    def header_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RL_TEAL)
        canvas.setLineWidth(1.5)
        canvas.line(0.7 * inch, letter[1] - 0.55 * inch, letter[0] - 0.7 * inch, letter[1] - 0.55 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(RL_TEAL)
        canvas.drawString(0.7 * inch, letter[1] - 0.45 * inch, "Alberta Gr. 3 & 4 Science · Co-Teaching Plan")
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawRightString(
            letter[0] - 0.7 * inch,
            0.45 * inch,
            f"Page {doc.page}",
        )
        canvas.restoreState()

    pdf = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
        title="Alberta Grade 3 & 4 Science Co-Teaching Plan",
        author="Classroom Planning Guide",
    )
    pdf.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    build_docx()
    build_pdf()
