#!/usr/bin/env python3
"""Generate Grade 3 and Grade 4 place-value worksheets (ones to millions)."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent
NAVY = colors.HexColor("#1B3A4B")
TEAL = colors.HexColor("#2F6F6A")
LIGHT = colors.HexColor("#E8F1F1")
LINE = colors.HexColor("#CCCCCC")
ACCENT = colors.HexColor("#C47B2C")


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="Banner", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4, leading=19))
    s.add(ParagraphStyle(name="SubBanner", fontName="Helvetica", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=8))
    s.add(ParagraphStyle(name="Meta", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#444444"), spaceAfter=6))
    s.add(ParagraphStyle(name="H2", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY, spaceBefore=8, spaceAfter=5))
    s.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=10, leading=13, spaceAfter=4))
    s.add(ParagraphStyle(name="Q", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=7))
    s.add(ParagraphStyle(name="Small", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#555555"), spaceAfter=4))
    s.add(ParagraphStyle(name="Answer", fontName="Helvetica", fontSize=9.5, leading=12, spaceAfter=3, textColor=colors.HexColor("#222222")))
    s.add(ParagraphStyle(name="Footer", fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#777777"), alignment=TA_CENTER))
    return s


def header_footer(canvas, doc, grade_label):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.5)
    canvas.line(0.6 * inch, letter[1] - 0.45 * inch, letter[0] - 0.6 * inch, letter[1] - 0.45 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEAL)
    canvas.drawString(0.6 * inch, letter[1] - 0.35 * inch, grade_label)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def name_line(st):
    return Paragraph(
        "Name: _________________________ &nbsp;&nbsp; Date: ______________ &nbsp;&nbsp; Score: ______ / ______",
        st["Meta"],
    )


def directions(st, text):
    return Paragraph(f"<b>Directions:</b> {text}", st["Body"])


def chart_table(places, blank=True):
    """Simple place-value chart headers."""
    headers = places
    row = ["______" if blank else "" for _ in places]
    data = [headers, row]
    t = Table(data, colWidths=[1.15 * inch] * len(places))
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.6, NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def q(st, n, text):
    return Paragraph(f"<b>{n}.</b> {text}", st["Q"])


def build_grade3(path: Path):
    st = styles()
    story = []
    label = "Grade 3 Math · Place Value (Ones to Millions)"

    # ---- Worksheet 1 ----
    story += [
        Paragraph("Place Value Worksheet 1", st["Banner"]),
        Paragraph("Grade 3 · Identify the Place", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "Look at the underlined digit. Write the <b>place</b> of that digit (ones, tens, hundreds, thousands, ten thousands, hundred thousands, or millions)."),
        Spacer(1, 6),
    ]
    g3_w1 = [
        ("4<u>7</u>2", "tens"),
        ("8<u>3</u>5,201", "ten thousands"),
        ("1,4<u>6</u>2", "tens"),
        ("<u>9</u>03,418", "hundred thousands"),
        ("52,<u>7</u>30", "hundreds"),
        ("6,0<u>8</u>4,215", "ten thousands"),
        ("3<u>5</u>,906", "thousands"),
        ("2,1<u>9</u>8", "tens"),
        ("7<u>0</u>4,563", "ten thousands"),
        ("1,<u>5</u>00,000", "hundred thousands"),
        ("48<u>2</u>", "ones"),
        ("9,876,<u>5</u>43", "hundreds"),
    ]
    for i, (num, _) in enumerate(g3_w1, 1):
        story.append(q(st, i, f"In <b>{num}</b>, the underlined digit is in the ________________ place."))
    story.append(PageBreak())

    # ---- Worksheet 2 ----
    story += [
        Paragraph("Place Value Worksheet 2", st["Banner"]),
        Paragraph("Grade 3 · Value of a Digit", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "Write the <b>value</b> of the underlined digit. Example: in 3<u>5</u>2, the 5 is worth <b>50</b>."),
        Spacer(1, 6),
    ]
    g3_w2 = [
        ("2<u>4</u>6", "40"),
        ("1,<u>8</u>05", "800"),
        ("<u>7</u>,320", "7,000"),
        ("45,<u>6</u>12", "600"),
        ("3<u>9</u>0,184", "90,000"),
        ("6,4<u>2</u>5,000", "20,000"),
        ("80,<u>0</u>15", "0"),
        ("1,<u>5</u>00,700", "500,000"),
        ("9<u>3</u>7", "30"),
        ("2,70<u>8</u>", "8"),
        ("5<u>1</u>,463", "1,000"),
        ("4,000,<u>2</u>00", "200"),
    ]
    for i, (num, _) in enumerate(g3_w2, 1):
        story.append(q(st, i, f"In <b>{num}</b>, the underlined digit is worth ____________________."))
    story.append(PageBreak())

    # ---- Worksheet 3 ----
    story += [
        Paragraph("Place Value Worksheet 3", st["Banner"]),
        Paragraph("Grade 3 · Standard, Expanded & Word Form", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        Paragraph("<b>A. Write each number in expanded form.</b>", st["H2"]),
    ]
    g3_expanded = [
        ("3,482", "3,000 + 400 + 80 + 2"),
        ("25,706", "20,000 + 5,000 + 700 + 6"),
        ("140,090", "100,000 + 40,000 + 90"),
        ("2,305,000", "2,000,000 + 300,000 + 5,000"),
    ]
    for i, (num, _) in enumerate(g3_expanded, 1):
        story.append(q(st, i, f"<b>{num}</b> = _______________________________________________"))
    story.append(Paragraph("<b>B. Write each expanded form as a standard number.</b>", st["H2"]))
    g3_standard = [
        ("5,000 + 200 + 40 + 1", "5,241"),
        ("30,000 + 600 + 8", "30,608"),
        ("400,000 + 20,000 + 3,000 + 50", "423,050"),
        ("1,000,000 + 70,000 + 900", "1,070,900"),
    ]
    for i, (expr, _) in enumerate(g3_standard, 1):
        story.append(q(st, i, f"<b>{expr}</b> = ____________________"))
    story.append(Paragraph("<b>C. Match the number to its word form.</b> Write the letter.", st["H2"]))
    story.append(Paragraph("1. 4,016 &nbsp;&nbsp; ____ &nbsp;&nbsp;&nbsp; 2. 40,160 &nbsp;&nbsp; ____ &nbsp;&nbsp;&nbsp; 3. 416,000 &nbsp;&nbsp; ____ &nbsp;&nbsp;&nbsp; 4. 4,160,000 &nbsp;&nbsp; ____", st["Q"]))
    story.append(Paragraph("A. four hundred sixteen thousand<br/>B. four thousand sixteen<br/>C. four million one hundred sixty thousand<br/>D. forty thousand one hundred sixty", st["Body"]))
    story.append(PageBreak())

    # ---- Worksheet 4 ----
    story += [
        Paragraph("Place Value Worksheet 4", st["Banner"]),
        Paragraph("Grade 3 · Build Numbers in a Place-Value Chart", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "Write each number in the place-value chart. Then answer the questions."),
        Spacer(1, 4),
        Paragraph("<b>Places:</b> Millions | Hundred Thousands | Ten Thousands | Thousands | Hundreds | Tens | Ones", st["Small"]),
        Spacer(1, 4),
    ]
    places = ["Millions", "Hundred\nThousands", "Ten\nThousands", "Thousands", "Hundreds", "Tens", "Ones"]
    headers = ["M", "HTh", "TTh", "Th", "H", "T", "O"]
    nums = ["382", "4,157", "26,090", "350,804", "1,206,573"]
    data = [headers] + [["____"] * 7 for _ in nums]
    # put number labels beside via paragraphs before table chunks
    for i, n in enumerate(nums, 1):
        story.append(Paragraph(f"<b>{i}.</b> Write <b>{n}</b> in the chart:", st["Body"]))
        row = [["____"] * 7]
        t = Table([headers] + row, colWidths=[0.85 * inch] * 7)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.7, NAVY),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.append(t)
        story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Think about it</b>", st["H2"]))
    story.append(q(st, 6, "In 26,090, which digit is in the thousands place? __________"))
    story.append(q(st, 7, "In 1,206,573, what is the value of the digit 2? __________"))
    story.append(q(st, 8, "Write a number with 5 in the ten-thousands place and 0 in the hundreds place: ____________________"))
    story.append(PageBreak())

    # ---- Worksheet 5 ----
    story += [
        Paragraph("Place Value Worksheet 5", st["Banner"]),
        Paragraph("Grade 3 · Compare & Order Numbers", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        Paragraph("<b>A. Compare.</b> Write &lt;, &gt;, or =.", st["H2"]),
    ]
    g3_compare = [
        ("3,458", "3,485"),
        ("12,070", "12,007"),
        ("450,000", "405,000"),
        ("2,600,000", "2,060,000"),
        ("89,999", "90,000"),
        ("1,005,200", "1,050,200"),
    ]
    for i, (a, b) in enumerate(g3_compare, 1):
        story.append(q(st, i, f"<b>{a}</b> &nbsp;&nbsp; ______ &nbsp;&nbsp; <b>{b}</b>"))
    story.append(Paragraph("<b>B. Order each set from least to greatest.</b>", st["H2"]))
    story.append(q(st, 7, "4,820 &nbsp;&nbsp; 4,280 &nbsp;&nbsp; 4,802<br/>____________________________________________"))
    story.append(q(st, 8, "35,100 &nbsp;&nbsp; 31,500 &nbsp;&nbsp; 35,010<br/>____________________________________________"))
    story.append(q(st, 9, "600,040 &nbsp;&nbsp; 604,000 &nbsp;&nbsp; 640,000<br/>____________________________________________"))
    story.append(Paragraph("<b>C. Word problems</b>", st["H2"]))
    story.append(q(st, 10, "A town has a population of <b>48,275</b>. Another town has <b>48,725</b> people. Which town has more people? ________________"))
    story.append(q(st, 11, "Mia scored <b>1,250,000</b> points in a game. Leo scored <b>1,205,000</b> points. Who scored fewer points? ________________"))
    story.append(PageBreak())

    # ---- Answer Key Grade 3 ----
    story += [
        Paragraph("Answer Key · Grade 3", st["Banner"]),
        Paragraph("Place Value Worksheets 1–5", st["SubBanner"]),
        HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8),
        Paragraph("<b>Worksheet 1 — Identify the Place</b>", st["H2"]),
    ]
    for i, (_, ans) in enumerate(g3_w1, 1):
        story.append(Paragraph(f"{i}. {ans}", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 2 — Value of a Digit</b>", st["H2"]))
    for i, (_, ans) in enumerate(g3_w2, 1):
        story.append(Paragraph(f"{i}. {ans}", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 3 — Forms</b>", st["H2"]))
    story.append(Paragraph("A: 1) 3,000+400+80+2 &nbsp; 2) 20,000+5,000+700+6 &nbsp; 3) 100,000+40,000+90 &nbsp; 4) 2,000,000+300,000+5,000", st["Answer"]))
    story.append(Paragraph("B: 1) 5,241 &nbsp; 2) 30,608 &nbsp; 3) 423,050 &nbsp; 4) 1,070,900", st["Answer"]))
    story.append(Paragraph("C: 1-B, 2-D, 3-A, 4-C", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 4 — Charts</b>", st["H2"]))
    story.append(Paragraph("1) 0,0,0,0,3,8,2 &nbsp; 2) 0,0,0,4,1,5,7 &nbsp; 3) 0,0,2,6,0,9,0 &nbsp; 4) 0,3,5,0,8,0,4 &nbsp; 5) 1,2,0,6,5,7,3", st["Answer"]))
    story.append(Paragraph("6) 6 &nbsp; 7) 200,000 &nbsp; 8) answers vary (e.g., 50,000 with 0 hundreds)", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 5 — Compare & Order</b>", st["H2"]))
    story.append(Paragraph("A: 1) &lt; &nbsp; 2) &gt; &nbsp; 3) &gt; &nbsp; 4) &gt; &nbsp; 5) &lt; &nbsp; 6) &lt;", st["Answer"]))
    story.append(Paragraph("B: 7) 4,280; 4,802; 4,820 &nbsp; 8) 31,500; 35,010; 35,100 &nbsp; 9) 600,040; 604,000; 640,000", st["Answer"]))
    story.append(Paragraph("C: 10) 48,725 town &nbsp; 11) Leo", st["Answer"]))

    def hf(c, d):
        header_footer(c, d, label)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.55 * inch,
        title="Grade 3 Place Value Worksheets",
        author="Classroom Worksheets",
    )
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("Wrote", path)


def build_grade4(path: Path):
    st = styles()
    story = []
    label = "Grade 4 Math · Place Value (Ones to Millions)"

    # ---- Worksheet 1 ----
    story += [
        Paragraph("Place Value Worksheet 1", st["Banner"]),
        Paragraph("Grade 4 · Identify Place & Value to Millions", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "For each number, write the <b>place</b> and the <b>value</b> of the underlined digit."),
        Spacer(1, 4),
        Paragraph("<i>Example:</i> 3,<u>8</u>41,206 → place: <b>hundred thousands</b> &nbsp; value: <b>800,000</b>", st["Small"]),
        Spacer(1, 6),
    ]
    g4_w1 = [
        ("5,2<u>6</u>4,183", "thousands", "6,000"),
        ("7<u>0</u>9,452", "ten thousands", "0"),
        ("1,<u>4</u>08,365", "hundred thousands", "400,000"),
        ("93,<u>5</u>17", "hundreds", "500"),
        ("<u>8</u>,001,240", "millions", "8,000,000"),
        ("2,67<u>3</u>,900", "thousands", "3,000"),
        ("450,0<u>8</u>2", "tens", "80"),
        ("6,1<u>9</u>0,007", "ten thousands", "90,000"),
        ("3,000,<u>4</u>56", "hundreds", "400"),
        ("9<u>8</u>7,654", "ten thousands", "80,000"),
    ]
    for i, (num, _, _) in enumerate(g4_w1, 1):
        story.append(q(st, i, f"<b>{num}</b><br/>Place: ____________________ &nbsp;&nbsp; Value: ____________________"))
    story.append(PageBreak())

    # ---- Worksheet 2 ----
    story += [
        Paragraph("Place Value Worksheet 2", st["Banner"]),
        Paragraph("Grade 4 · ×10 and ÷10 Place Relationships", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "Use place-value patterns. Moving one place to the <b>left</b> multiplies a digit’s value by 10. Moving one place to the <b>right</b> divides its value by 10."),
        Paragraph("<b>A. Complete the pattern.</b>", st["H2"]),
    ]
    patterns = [
        "4 &nbsp; → &nbsp; 40 &nbsp; → &nbsp; 400 &nbsp; → &nbsp; ______ &nbsp; → &nbsp; ______",
        "70 &nbsp; → &nbsp; 700 &nbsp; → &nbsp; ______ &nbsp; → &nbsp; ______ &nbsp; → &nbsp; 7,000,000",
        "900 &nbsp; → &nbsp; ______ &nbsp; → &nbsp; 90,000 &nbsp; → &nbsp; ______ &nbsp; → &nbsp; ______",
        "______ &nbsp; → &nbsp; 5,000 &nbsp; → &nbsp; 50,000 &nbsp; → &nbsp; ______ &nbsp; → &nbsp; 5,000,000",
    ]
    for i, line in enumerate(patterns, 1):
        story.append(q(st, i, line))
    story.append(Paragraph("<b>B. Compare the value of the digit 6 in each pair.</b>", st["H2"]))
    story.append(q(st, 5, "In <b>6,000</b>, the 6 is ______ times the value of the 6 in <b>600</b>."))
    story.append(q(st, 6, "In <b>60,000</b>, the 6 is ______ times the value of the 6 in <b>6,000</b>."))
    story.append(q(st, 7, "In <b>600</b>, the 6 is ______ the value of the 6 in <b>6,000</b>. (Hint: use a fraction or “one-tenth”)"))
    story.append(q(st, 8, "In <b>6,000,000</b>, the 6 is ______ times the value of the 6 in <b>6,000</b>."))
    story.append(Paragraph("<b>C. True or False.</b> Fix each false statement.", st["H2"]))
    story.append(q(st, 9, "The digit 3 in 3,250,000 is worth 30,000. __________"))
    story.append(q(st, 10, "100,000 is 10 times as much as 10,000. __________"))
    story.append(q(st, 11, "If a digit moves two places left, its value is multiplied by 100. __________"))
    story.append(PageBreak())

    # ---- Worksheet 3 ----
    story += [
        Paragraph("Place Value Worksheet 3", st["Banner"]),
        Paragraph("Grade 4 · Expanded Form & Different Compositions", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        Paragraph("<b>A. Write in expanded form using place values.</b>", st["H2"]),
    ]
    g4_exp = [
        ("4,582,031", "4,000,000 + 500,000 + 80,000 + 2,000 + 30 + 1"),
        ("7,060,409", "7,000,000 + 60,000 + 400 + 9"),
        ("920,005", "900,000 + 20,000 + 5"),
    ]
    for i, (num, _) in enumerate(g4_exp, 1):
        story.append(q(st, i, f"<b>{num}</b> = ________________________________________________"))
    story.append(Paragraph("<b>B. Write the standard number.</b>", st["H2"]))
    g4_std = [
        ("3,000,000 + 40,000 + 200 + 8", "3,040,208"),
        ("800,000 + 5,000 + 70", "805,070"),
        ("1,000,000 + 900,000 + 9", "1,900,009"),
    ]
    for i, (expr, _) in enumerate(g4_std, 1):
        story.append(q(st, i, f"<b>{expr}</b> = ____________________"))
    story.append(Paragraph("<b>C. Show another way to compose the number using place value.</b>", st["H2"]))
    story.append(Paragraph("Example: 2,300 = 23 hundreds &nbsp; or &nbsp; 2,300 = 230 tens", st["Small"]))
    story.append(q(st, 7, "<b>5,400</b> = __________ hundreds &nbsp;&nbsp; or &nbsp;&nbsp; __________ tens"))
    story.append(q(st, 8, "<b>36,000</b> = __________ thousands &nbsp;&nbsp; or &nbsp;&nbsp; __________ hundreds"))
    story.append(q(st, 9, "<b>2,500,000</b> = __________ hundred thousands &nbsp;&nbsp; or &nbsp;&nbsp; __________ thousands"))
    story.append(q(st, 10, "<b>780,000</b> = __________ ten thousands"))
    story.append(PageBreak())

    # ---- Worksheet 4 ----
    story += [
        Paragraph("Place Value Worksheet 4", st["Banner"]),
        Paragraph("Grade 4 · Missing Digits, Rounding & Numbers in Context", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        Paragraph("<b>A. Fill in the missing digits.</b>", st["H2"]),
        q(st, 1, "A number has 6 millions, 0 hundred thousands, 4 ten thousands, 2 thousands, 8 hundreds, 0 tens, and 5 ones.<br/>Number: ____________________"),
        q(st, 2, "___ , 3 0 5 , 1 7 2 &nbsp;&nbsp; The millions digit is 9. Write the number: ____________________"),
        q(st, 3, "2, __ 8 __, 604 &nbsp;&nbsp; The hundred-thousands digit is 5 and the thousands digit is 1.<br/>Number: ____________________"),
        Paragraph("<b>B. Round each number as directed.</b>", st["H2"]),
        q(st, 4, "Round <b>4,682</b> to the nearest thousand: __________"),
        q(st, 5, "Round <b>37,249</b> to the nearest ten thousand: __________"),
        q(st, 6, "Round <b>856,031</b> to the nearest hundred thousand: __________"),
        q(st, 7, "Round <b>2,450,890</b> to the nearest million: __________"),
        Paragraph("<b>C. Solve.</b>", st["H2"]),
        q(st, 8, "A stadium sold <b>1,284,650</b> tickets in a year. What is the value of the digit 2? __________"),
        q(st, 9, "Which number is greater: <b>3,089,500</b> or <b>3,098,500</b>? Explain using place value.<br/>________________________________________________________________"),
        q(st, 10, "Write the smallest 7-digit number that uses each digit 0–6 exactly once. (The millions digit cannot be 0.)<br/>____________________"),
        q(st, 11, "Write the largest 6-digit number that has 4 in the thousands place.<br/>____________________"),
    ]
    story.append(PageBreak())

    # ---- Worksheet 5 ----
    story += [
        Paragraph("Place Value Worksheet 5", st["Banner"]),
        Paragraph("Grade 4 · Challenge: Mixed Place-Value Practice", st["SubBanner"]),
        name_line(st),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=8),
        directions(st, "Complete all parts. Show your thinking for word problems."),
        Paragraph("<b>A. Quick check</b>", st["H2"]),
        q(st, 1, "In <b>4,182,706</b>, which digit is in the hundred-thousands place? __________"),
        q(st, 2, "Write 6,040,208 in words: ________________________________________________"),
        q(st, 3, "Write seven million twenty thousand five as a number: ____________________"),
        Paragraph("<b>B. Compare, order, and reason</b>", st["H2"]),
        q(st, 4, "Order from greatest to least: 2,905,000 &nbsp; 2,950,000 &nbsp; 2,095,000<br/>____________________________________________"),
        q(st, 5, "Find a number between 1,499,999 and 1,500,010: ____________________"),
        q(st, 6, "How many times greater is the value of 5 in <b>5,000,000</b> than the value of 5 in <b>500</b>? __________"),
        Paragraph("<b>C. Place-value puzzles</b>", st["H2"]),
        q(st, 7, "I am a 6-digit number. My ten-thousands digit is 7. My ones digit is 2. All other digits are 0. What number am I? __________"),
        q(st, 8, "I am the number 3,333,333. How much greater is the leftmost 3 than the rightmost 3? __________"),
        q(st, 9, "A city has 2,450,000 people. Another city has two hundred forty-five thousand people. How many more people does the first city have? __________"),
        q(st, 10, "Create your own 7-digit number. Underline one digit and write its place and value.<br/>Number: ____________________ &nbsp; Place: __________ &nbsp; Value: __________"),
    ]
    story.append(PageBreak())

    # ---- Answer Key ----
    story += [
        Paragraph("Answer Key · Grade 4", st["Banner"]),
        Paragraph("Place Value Worksheets 1–5", st["SubBanner"]),
        HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8),
        Paragraph("<b>Worksheet 1</b>", st["H2"]),
    ]
    for i, (_, place, val) in enumerate(g4_w1, 1):
        story.append(Paragraph(f"{i}. place: {place}; value: {val}", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 2</b>", st["H2"]))
    story.append(Paragraph("A: 1) 4,000; 40,000 &nbsp; 2) 7,000; 70,000 &nbsp; 3) 9,000; 900,000; 9,000,000 &nbsp; 4) 500; 500,000", st["Answer"]))
    story.append(Paragraph("B: 5) 10 &nbsp; 6) 10 &nbsp; 7) 1/10 (one-tenth) &nbsp; 8) 1,000", st["Answer"]))
    story.append(Paragraph("C: 9) False — worth 3,000,000 &nbsp; 10) True &nbsp; 11) True", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 3</b>", st["H2"]))
    story.append(Paragraph("A: 1) 4,000,000+500,000+80,000+2,000+30+1 &nbsp; 2) 7,000,000+60,000+400+9 &nbsp; 3) 900,000+20,000+5", st["Answer"]))
    story.append(Paragraph("B: 1) 3,040,208 &nbsp; 2) 805,070 &nbsp; 3) 1,900,009", st["Answer"]))
    story.append(Paragraph("C: 7) 54 hundreds / 540 tens &nbsp; 8) 36 thousands / 360 hundreds &nbsp; 9) 25 hundred thousands / 2,500 thousands &nbsp; 10) 78 ten thousands", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 4</b>", st["H2"]))
    story.append(Paragraph("A: 1) 6,042,805 &nbsp; 2) 9,305,172 &nbsp; 3) 2,581,604", st["Answer"]))
    story.append(Paragraph("B: 4) 5,000 &nbsp; 5) 40,000 &nbsp; 6) 900,000 &nbsp; 7) 2,000,000", st["Answer"]))
    story.append(Paragraph("C: 8) 200,000 &nbsp; 9) 3,098,500 (greater ten-thousands digit) &nbsp; 10) 1,023,456 &nbsp; 11) 984,999", st["Answer"]))
    story.append(Paragraph("<b>Worksheet 5</b>", st["H2"]))
    story.append(Paragraph("1) 1 &nbsp; 2) six million forty thousand two hundred eight &nbsp; 3) 7,020,005", st["Answer"]))
    story.append(Paragraph("4) 2,950,000; 2,905,000; 2,095,000 &nbsp; 5) any valid, e.g. 1,500,000 &nbsp; 6) 10,000 times", st["Answer"]))
    story.append(Paragraph("7) 70,002 &nbsp; 8) 2,999,997 &nbsp; 9) 2,205,000 &nbsp; 10) answers vary", st["Answer"]))

    def hf(c, d):
        header_footer(c, d, label)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.55 * inch,
        title="Grade 4 Place Value Worksheets",
        author="Classroom Worksheets",
    )
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("Wrote", path)


def build_combined_overview(path: Path):
    st = styles()
    story = [
        Paragraph("Place Value Worksheets", st["Banner"]),
        Paragraph("Grade 3 & Grade 4 · Ones to Millions", st["SubBanner"]),
        HRFlowable(width="100%", thickness=1.2, color=TEAL, spaceAfter=10),
        Paragraph(
            "These printable packs help students find and use place value from the <b>ones</b> place through the <b>millions</b> place. "
            "Grade 3 sheets are more scaffolded; Grade 4 sheets add ×10/÷10 relationships, rounding, and richer problem solving "
            "(aligned with Alberta Number outcomes around place value).",
            st["Body"],
        ),
        Paragraph("<b>Grade 3 pack</b> — <i>Grade3_Place_Value_Worksheets.pdf</i>", st["H2"]),
        Paragraph("1. Identify the Place<br/>2. Value of a Digit<br/>3. Standard, Expanded & Word Form<br/>4. Build Numbers in a Place-Value Chart<br/>5. Compare & Order Numbers<br/>+ Answer Key", st["Body"]),
        Paragraph("<b>Grade 4 pack</b> — <i>Grade4_Place_Value_Worksheets.pdf</i>", st["H2"]),
        Paragraph("1. Identify Place & Value to Millions<br/>2. ×10 and ÷10 Place Relationships<br/>3. Expanded Form & Different Compositions<br/>4. Missing Digits, Rounding & Context<br/>5. Mixed Challenge Practice<br/>+ Answer Key", st["Body"]),
        Spacer(1, 8),
        Paragraph("<b>Suggested use in a 3/4 split</b>", st["H2"]),
        Paragraph("• Shared mini-lesson on place-value chart (ones → millions)<br/>• Grade 3 completes Pack sheets 1–3 while Grade 4 completes Pack sheets 1–2<br/>• Swap: Grade 3 compare/order; Grade 4 ×10 relationships<br/>• Use answer keys for quick self-check or peer marking", st["Body"]),
    ]
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.6 * inch,
        title="Place Value Worksheets Overview",
    )
    doc.build(story)
    print("Wrote", path)


if __name__ == "__main__":
    build_grade3(OUT / "Grade3_Place_Value_Worksheets.pdf")
    build_grade4(OUT / "Grade4_Place_Value_Worksheets.pdf")
    build_combined_overview(OUT / "Place_Value_Worksheets_Overview.pdf")
