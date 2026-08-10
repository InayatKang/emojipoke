#!/usr/bin/env python3
"""Place Value Houses worksheets: Millions, Ten Thousands, Thousands, Hundreds."""

from pathlib import Path

import cairosvg
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Image,
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


def make_houses_svg(path: Path, mode="blank"):
    """
    Four houses left→right (large to small):
      Millions | Ten Thousands | Thousands | Hundreds (H-T-O)
    mode: blank | example
    """
    W, H = 1000, 320
    # House specs: (label, roof_color, windows labels)
    houses = [
        ("MILLIONS", "#A074B5", ["Millions"]),
        ("TEN\nTHOUSANDS", "#F0D03C", ["Ten\nThousands"]),
        ("THOUSANDS", "#F29B3A", ["Thousands"]),
        ("HUNDREDS", "#EF6B73", ["Hundreds", "Tens", "Ones"]),
    ]

    # geometry
    margin = 20
    gap = 18
    usable = W - 2 * margin - gap * 3
    # widths proportional to window count
    win_counts = [len(h[2]) for h in houses]
    unit = usable / sum(max(c, 1) + 0.35 for c in win_counts)
    widths = [(max(c, 1) + 0.35) * unit for c in win_counts]

    body_h = 130
    roof_h = 55
    chimney_w, chimney_h = 14, 18
    body_top = 70
    label_band_h = 70
    ground_y = body_top + body_h

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace("\n", "")

    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>\n'
        f'<defs><pattern id="bricks" patternUnits="userSpaceOnUse" width="6" height="5">'
        f'<rect width="6" height="5" fill="#fff"/>'
        f'<path d="M0 0H6M0 2.5H6M0 5H6M3 0V2.5M0 2.5V5M6 2.5V5" stroke="#333" stroke-width="0.6" fill="none"/>'
        f"</pattern></defs>\n"
    ]

    x = margin
    example_digits = {
        0: ["3"],  # millions
        1: ["2"],  # ten thousands
        2: ["5"],  # thousands
        3: ["4", "1", "8"],  # hundreds tens ones → 3,025,418
    }

    for i, (period, roof, windows) in enumerate(houses):
        w = widths[i]
        # body
        parts.append(
            f'<rect x="{x:.1f}" y="{body_top}" width="{w:.1f}" height="{body_h}" '
            f'fill="#fff" stroke="#111" stroke-width="2"/>\n'
        )
        nwin = len(windows)
        win_w = w / nwin
        for wi, wlabel in enumerate(windows):
            wx = x + wi * win_w
            if wi > 0:
                parts.append(
                    f'<line x1="{wx:.1f}" y1="{body_top}" x2="{wx:.1f}" y2="{body_top + body_h}" '
                    f'stroke="#111" stroke-width="1.5"/>\n'
                )
            # digit box area
            box_y = body_top + 18
            box_h = 52
            pad = 8
            parts.append(
                f'<rect x="{wx + pad:.1f}" y="{box_y}" width="{win_w - 2 * pad:.1f}" height="{box_h}" '
                f'fill="#fafafa" stroke="#555" stroke-width="1.2" rx="3"/>\n'
            )
            if mode == "example":
                dig = example_digits[i][wi]
                parts.append(
                    f'<text x="{wx + win_w / 2:.1f}" y="{box_y + 38:.1f}" text-anchor="middle" '
                    f'font-family="Arial" font-size="32" font-weight="700" fill="#1B3A4B">{dig}</text>\n'
                )
            # window place label under digit box
            lines = wlabel.split("\n")
            ty = body_top + body_h - 28
            for li, line in enumerate(lines):
                parts.append(
                    f'<text x="{wx + win_w / 2:.1f}" y="{ty + li * 12:.1f}" text-anchor="middle" '
                    f'font-family="Arial" font-size="10" fill="#222">{esc(line)}</text>\n'
                )

        # roof
        peak_x = x + w / 2
        peak_y = body_top - roof_h
        left = x - 4
        right = x + w + 4
        parts.append(
            f'<polygon points="{left:.1f},{body_top + 1:.1f} {peak_x:.1f},{peak_y:.1f} {right:.1f},{body_top + 1:.1f}" '
            f'fill="{roof}" stroke="#111" stroke-width="2"/>\n'
        )
        # chimney
        chim_x = x + w * 0.72
        t = (chim_x - peak_x) / (right - peak_x) if right != peak_x else 0.5
        roof_y = peak_y + (body_top - peak_y) * max(0.2, t)
        parts.append(
            f'<rect x="{chim_x:.1f}" y="{roof_y - chimney_h + 2:.1f}" width="{chimney_w}" height="{chimney_h}" '
            f'fill="url(#bricks)" stroke="#111" stroke-width="1.2"/>\n'
        )
        # period label on roof
        roof_lines = period.split("\n")
        for li, line in enumerate(roof_lines):
            parts.append(
                f'<text x="{peak_x:.1f}" y="{peak_y + 28 + li * 13:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="11" font-weight="700" fill="#111">{esc(line)}</text>\n'
            )

        # arrow ×10 / ÷10 between houses
        if i < len(houses) - 1:
            mid = x + w + gap / 2
            parts.append(
                f'<text x="{mid:.1f}" y="{body_top + body_h / 2 - 4:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="9" font-weight="700" fill="#2F6F6A">← ×10</text>\n'
            )
            parts.append(
                f'<text x="{mid:.1f}" y="{body_top + body_h / 2 + 10:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="9" font-weight="700" fill="#2F6F6A">→ ÷10</text>\n'
            )

        x += w + gap

    # street line
    parts.append(
        f'<line x1="{margin}" y1="{ground_y + 8}" x2="{W - margin}" y2="{ground_y + 8}" '
        f'stroke="#888" stroke-width="2"/>\n'
    )
    if mode == "example":
        parts.append(
            '<text x="500" y="300" text-anchor="middle" font-family="Arial" font-size="14" '
            'font-weight="700" fill="#1B3A4B">Example number: 3,025,418</text>\n'
        )
    else:
        parts.append(
            '<text x="500" y="300" text-anchor="middle" font-family="Arial" font-size="12" '
            'fill="#444">Place Value Houses · Millions → Ten Thousands → Thousands → Hundreds / Tens / Ones</text>\n'
        )

    parts.append("</svg>")
    path.write_text("".join(parts), encoding="utf-8")
    png = path.with_suffix(".png")
    cairosvg.svg2png(url=str(path), write_to=str(png), output_width=1600)
    return png


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("Banner", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY, alignment=TA_CENTER, spaceAfter=3, leading=18))
    s.add(ParagraphStyle("Sub", fontName="Helvetica", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6))
    s.add(ParagraphStyle("Meta", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#444"), spaceAfter=5))
    s.add(ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY, spaceBefore=6, spaceAfter=4))
    s.add(ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=13, spaceAfter=4))
    s.add(ParagraphStyle("Q", fontName="Helvetica", fontSize=10, leading=13, spaceAfter=6))
    s.add(ParagraphStyle("Ans", fontName="Helvetica", fontSize=9.5, leading=12, spaceAfter=2))
    return s


def hf(canvas, doc, label):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.4)
    canvas.line(0.55 * inch, letter[1] - 0.42 * inch, letter[0] - 0.55 * inch, letter[1] - 0.42 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEAL)
    canvas.drawString(0.55 * inch, letter[1] - 0.32 * inch, label)
    canvas.setFillColor(colors.HexColor("#777"))
    canvas.drawRightString(letter[0] - 0.55 * inch, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    st = styles()
    blank_png = make_houses_svg(OUT / "houses_blank.svg", mode="blank")
    example_png = make_houses_svg(OUT / "houses_example.svg", mode="example")

    story = []

    # Page 1 - Chart / mat
    story += [
        Paragraph("Place Value Houses", st["Banner"]),
        Paragraph("Millions · Ten Thousands · Thousands · Hundreds", st["Sub"]),
        Paragraph(
            "Name: _________________________ &nbsp;&nbsp; Date: ______________",
            st["Meta"],
        ),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=6),
        Paragraph(
            "<b>Each house is a place!</b> Put one digit in each window. "
            "Read the number from the Millions house toward the Ones window.",
            st["Body"],
        ),
        Spacer(1, 4),
        Image(str(example_png), width=7.2 * inch, height=2.3 * inch),
        Spacer(1, 6),
        Paragraph("<b>Your turn — build these numbers in the houses</b> (write digits in order):", st["H2"]),
        Paragraph("1. <b>4,000,000</b> &nbsp;→&nbsp; Millions: ___ &nbsp; Ten Thousands: ___ &nbsp; Thousands: ___ &nbsp; Hundreds: ___ &nbsp; Tens: ___ &nbsp; Ones: ___", st["Q"]),
        Paragraph("2. <b>70,000</b> &nbsp;→&nbsp; M: ___ &nbsp; TTh: ___ &nbsp; Th: ___ &nbsp; H: ___ &nbsp; T: ___ &nbsp; O: ___", st["Q"]),
        Paragraph("3. <b>5,208</b> &nbsp;→&nbsp; M: ___ &nbsp; TTh: ___ &nbsp; Th: ___ &nbsp; H: ___ &nbsp; T: ___ &nbsp; O: ___", st["Q"]),
        Paragraph("4. <b>1,036,549</b> &nbsp;→&nbsp; M: ___ &nbsp; TTh: ___ &nbsp; Th: ___ &nbsp; H: ___ &nbsp; T: ___ &nbsp; O: ___", st["Q"]),
        Paragraph("5. Make your own number and write it: ____________________", st["Q"]),
        PageBreak(),
    ]

    # Page 2 - Grade 3
    story += [
        Paragraph("Place Value Houses · Grade 3", st["Banner"]),
        Paragraph("Find the place — Hundreds, Thousands, Ten Thousands, Millions", st["Sub"]),
        Paragraph("Name: _________________________ &nbsp;&nbsp; Date: ______________", st["Meta"]),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=6),
        Image(str(blank_png), width=7.2 * inch, height=2.3 * inch),
        Spacer(1, 4),
        Paragraph("<b>A. Which house?</b> Write <i>millions</i>, <i>ten thousands</i>, <i>thousands</i>, <i>hundreds</i>, <i>tens</i>, or <i>ones</i>.", st["H2"]),
    ]
    g3a = [
        ("In <b>6,000</b>, the 6 lives in the ________________ house/place."),
        ("In <b>40,000</b>, the 4 lives in the ________________ house/place."),
        ("In <b>2,000,000</b>, the 2 lives in the ________________ house/place."),
        ("In <b>800</b>, the 8 lives in the ________________ house/place."),
        ("In <b>1,050,000</b>, the 5 lives in the ________________ house/place."),
        ("In <b>3,792</b>, the 9 lives in the ________________ house/place."),
    ]
    for i, t in enumerate(g3a, 1):
        story.append(Paragraph(f"<b>{i}.</b> {t}", st["Q"]))

    story.append(Paragraph("<b>B. Put digits in the houses</b> (write the digit for each place).", st["H2"]))
    headers = ["Number", "Millions", "Ten Thousands", "Thousands", "Hundreds", "Tens", "Ones"]
    rows = [headers]
    for num in ["382", "7,041", "50,600", "1,204,090"]:
        rows.append([num] + ["____"] * 6)
    t = Table(rows, colWidths=[1.15 * inch] + [0.95 * inch] * 6)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.6, NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>C. Build a number</b>", st["H2"]))
    story.append(Paragraph("7. 3 in the millions house, 4 in the thousands house, 5 in the tens place. All other windows are 0.<br/>Number: ____________________", st["Q"]))
    story.append(Paragraph("8. 6 in the ten-thousands house, 2 in the hundreds house, 9 in the ones. All other windows are 0.<br/>Number: ____________________", st["Q"]))
    story.append(PageBreak())

    # Page 3 - Grade 4
    story += [
        Paragraph("Place Value Houses · Grade 4", st["Banner"]),
        Paragraph("Use the houses to find place, value, and ×10 relationships", st["Sub"]),
        Paragraph("Name: _________________________ &nbsp;&nbsp; Date: ______________", st["Meta"]),
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=6),
        Image(str(blank_png), width=7.2 * inch, height=2.3 * inch),
        Spacer(1, 4),
        Paragraph("<b>A. Place and value</b> — Name the house/place and the value of the digit.", st["H2"]),
    ]
    story.append(Paragraph("1. In <b>6,000,000</b>, the 6 is in the ________________ house. Value: ____________________", st["Q"]))
    story.append(Paragraph("2. In <b>80,000</b>, the 8 is in the ________________ house. Value: ____________________", st["Q"]))
    story.append(Paragraph("3. In <b>9,000</b>, the 9 is in the ________________ house. Value: ____________________", st["Q"]))
    story.append(Paragraph("4. In <b>500</b>, the 5 is in the ________________ house. Value: ____________________", st["Q"]))
    story.append(Paragraph("5. In <b>2,046,318</b>, the 4 is in the ________________ house. Value: ____________________", st["Q"]))
    story.append(Paragraph("6. In <b>2,046,318</b>, the 3 is in the ________________ place. Value: ____________________", st["Q"]))

    story.append(Paragraph("<b>B. Moving between houses (×10 / ÷10)</b>", st["H2"]))
    story.append(Paragraph("7. A digit in the <b>thousands</b> house moves to the <b>ten thousands</b> house. Its value is multiplied by ______. ", st["Q"]))
    story.append(Paragraph("8. A digit in the <b>millions</b> house moves to the <b>hundreds</b> house (same digit). How many times smaller is its value now? ______", st["Q"]))
    story.append(Paragraph("9. Complete: 7 → 70 → 700 → 7,000 → ______ → ______ → 7,000,000", st["Q"]))

    story.append(Paragraph("<b>C. House puzzles</b>", st["H2"]))
    story.append(Paragraph("10. Fill the houses to make <b>3,050,200</b>:<br/>Millions ___ &nbsp; Ten Thousands ___ &nbsp; Thousands ___ &nbsp; Hundreds ___ &nbsp; Tens ___ &nbsp; Ones ___", st["Q"]))
    story.append(Paragraph("11. Which is greater: a 5 in the <b>ten thousands</b> house or a 5 in the <b>thousands</b> house? Explain.<br/>________________________________________________________________", st["Q"]))
    story.append(Paragraph("12. Write the number: 1 in millions, 6 in ten thousands, 4 in thousands, 0 in hundreds, 8 in tens, 2 in ones.<br/>____________________", st["Q"]))
    story.append(PageBreak())

    # Answer key
    story += [
        Paragraph("Answer Key · Place Value Houses", st["Banner"]),
        Paragraph("Chart practice + Grade 3 + Grade 4", st["Sub"]),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#C47B2C"), spaceAfter=8),
        Paragraph("<b>Page 1 — Build numbers</b>", st["H2"]),
        Paragraph("1) 4, 0, 0, 0, 0, 0 &nbsp; 2) 0, 7, 0, 0, 0, 0 &nbsp; 3) 0, 0, 5, 2, 0, 8 &nbsp; 4) 1, 3, 6, 5, 4, 9 &nbsp; 5) answers vary", st["Ans"]),
        Paragraph("<b>Grade 3</b>", st["H2"]),
        Paragraph("A: 1) thousands &nbsp; 2) ten thousands &nbsp; 3) millions &nbsp; 4) hundreds &nbsp; 5) ten thousands &nbsp; 6) tens", st["Ans"]),
        Paragraph("B: 382 → 0,0,0,3,8,2 &nbsp;|&nbsp; 7,041 → 0,0,7,0,4,1 &nbsp;|&nbsp; 50,600 → 0,5,0,6,0,0 &nbsp;|&nbsp; 1,204,090 → 1,0,4,0,9,0", st["Ans"]),
        Paragraph("C: 7) 3,004,050 &nbsp; 8) 60,209", st["Ans"]),
        Paragraph("<b>Grade 4</b>", st["H2"]),
        Paragraph("A: 1) millions; 6,000,000 &nbsp; 2) ten thousands; 80,000 &nbsp; 3) thousands; 9,000 &nbsp; 4) hundreds; 500 &nbsp; 5) ten thousands; 40,000 &nbsp; 6) tens; 10", st["Ans"]),
        Paragraph("B: 7) 10 &nbsp; 8) 10,000 times smaller &nbsp; 9) 70,000; 700,000", st["Ans"]),
        Paragraph("C: 10) 3, 5, 0, 2, 0, 0 &nbsp; 11) ten thousands (50,000 &gt; 5,000) &nbsp; 12) 1,064,082", st["Ans"]),
        Spacer(1, 10),
        Paragraph(
            "<i>Note for teachers:</i> The four houses match Millions, Ten Thousands, Thousands, and the Hundreds house "
            "(with Tens and Ones windows). This keeps the street small while still covering ones through millions.",
            st["Body"],
        ),
    ]

    out = OUT / "Place_Value_Houses_Worksheets.pdf"
    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.5 * inch,
        title="Place Value Houses Worksheets",
    )
    doc.build(story, onFirstPage=lambda c, d: hf(c, d, "Place Value Houses · Gr. 3 & 4"), onLaterPages=lambda c, d: hf(c, d, "Place Value Houses · Gr. 3 & 4"))
    print("Wrote", out)
    return out


if __name__ == "__main__":
    build_pdf()
