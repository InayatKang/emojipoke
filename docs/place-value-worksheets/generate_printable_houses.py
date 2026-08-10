#!/usr/bin/env python3
"""Clean printable Place Value Houses worksheet (Gr. 3 & 4)."""

from pathlib import Path

import cairosvg
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
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
LIGHT = colors.HexColor("#EEF5F5")


def houses_svg(path: Path, with_example=False):
    W, H = 1100, 300
    houses = [
        ("MILLIONS", "#A074B5", ["Millions"], ["3"] if with_example else [""]),
        ("TEN THOUSANDS", "#F0D03C", ["Ten Thousands"], ["2"] if with_example else [""]),
        ("THOUSANDS", "#F29B3A", ["Thousands"], ["5"] if with_example else [""]),
        ("HUNDREDS", "#EF6B73", ["Hundreds", "Tens", "Ones"], ["4", "1", "8"] if with_example else ["", "", ""]),
    ]
    margin, gap = 16, 16
    usable = W - 2 * margin - gap * 3
    win_counts = [len(h[2]) for h in houses]
    unit = usable / sum(max(c, 1) + 0.4 for c in win_counts)
    widths = [(max(c, 1) + 0.4) * unit for c in win_counts]
    body_h, roof_h = 145, 58
    body_top = 62

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;")

    p = [
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>\n'
        '<defs><pattern id="bricks" patternUnits="userSpaceOnUse" width="6" height="5">'
        '<rect width="6" height="5" fill="#fff"/>'
        '<path d="M0 0H6M0 2.5H6M0 5H6M3 0V2.5M0 2.5V5M6 2.5V5" stroke="#333" stroke-width="0.65" fill="none"/>'
        "</pattern></defs>\n"
    ]
    x = margin
    for i, (title, color, windows, digits) in enumerate(houses):
        w = widths[i]
        p.append(
            f'<rect x="{x:.1f}" y="{body_top}" width="{w:.1f}" height="{body_h}" '
            f'fill="#fff" stroke="#111" stroke-width="2.2"/>\n'
        )
        n = len(windows)
        ww = w / n
        for wi, label in enumerate(windows):
            wx = x + wi * ww
            if wi:
                p.append(
                    f'<line x1="{wx:.1f}" y1="{body_top}" x2="{wx:.1f}" y2="{body_top+body_h}" '
                    f'stroke="#111" stroke-width="1.6"/>\n'
                )
            pad = 10
            by, bh = body_top + 16, 70
            p.append(
                f'<rect x="{wx+pad:.1f}" y="{by}" width="{ww-2*pad:.1f}" height="{bh}" '
                f'fill="#fff" stroke="#444" stroke-width="1.4" rx="4"/>\n'
            )
            if digits[wi]:
                p.append(
                    f'<text x="{wx+ww/2:.1f}" y="{by+48:.1f}" text-anchor="middle" '
                    f'font-family="Arial" font-size="36" font-weight="700" fill="#1B3A4B">{digits[wi]}</text>\n'
                )
            # dotted writing guides if blank
            else:
                p.append(
                    f'<line x1="{wx+pad+8:.1f}" y1="{by+bh-14:.1f}" x2="{wx+ww-pad-8:.1f}" y2="{by+bh-14:.1f}" '
                    f'stroke="#bbb" stroke-width="1" stroke-dasharray="3 3"/>\n'
                )
            p.append(
                f'<text x="{wx+ww/2:.1f}" y="{body_top+body_h-18:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="12" font-weight="600" fill="#222">{esc(label)}</text>\n'
            )
        # roof
        peak_x, peak_y = x + w / 2, body_top - roof_h
        left, right = x - 5, x + w + 5
        p.append(
            f'<polygon points="{left:.1f},{body_top+1:.1f} {peak_x:.1f},{peak_y:.1f} {right:.1f},{body_top+1:.1f}" '
            f'fill="{color}" stroke="#111" stroke-width="2.2"/>\n'
        )
        chim_x = x + w * 0.74
        t = max(0.2, (chim_x - peak_x) / (right - peak_x))
        ry = peak_y + (body_top - peak_y) * t
        p.append(
            f'<rect x="{chim_x:.1f}" y="{ry-20:.1f}" width="15" height="20" '
            f'fill="url(#bricks)" stroke="#111" stroke-width="1.2"/>\n'
        )
        p.append(
            f'<text x="{peak_x:.1f}" y="{peak_y+32:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="12" font-weight="700" fill="#111">{esc(title)}</text>\n'
        )
        if i < len(houses) - 1:
            mid = x + w + gap / 2
            p.append(
                f'<text x="{mid:.1f}" y="{body_top+body_h/2-2:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="10" font-weight="700" fill="#2F6F6A">← ×10</text>\n'
            )
            p.append(
                f'<text x="{mid:.1f}" y="{body_top+body_h/2+12:.1f}" text-anchor="middle" '
                f'font-family="Arial" font-size="10" font-weight="700" fill="#2F6F6A">→ ÷10</text>\n'
            )
        x += w + gap

    p.append(
        f'<line x1="{margin}" y1="{body_top+body_h+10}" x2="{W-margin}" y2="{body_top+body_h+10}" '
        f'stroke="#999" stroke-width="2"/>\n'
    )
    if with_example:
        p.append(
            '<text x="550" y="285" text-anchor="middle" font-family="Arial" font-size="15" '
            'font-weight="700" fill="#1B3A4B">Example: 3,025,418</text>\n'
        )
    p.append("</svg>")
    path.write_text("".join(p), encoding="utf-8")
    png = path.with_suffix(".png")
    cairosvg.svg2png(url=str(path), write_to=str(png), output_width=1800)
    return png


def build():
    blank = houses_svg(OUT / "printable_houses_blank.svg", with_example=False)
    example = houses_svg(OUT / "printable_houses_example.svg", with_example=True)

    # ---- Page 1: Landscape printable mat (write-in houses) ----
    mat_path = OUT / "Place_Value_Houses_Printable_Mat.pdf"
    c = canvas.Canvas(str(mat_path), pagesize=landscape(letter))
    pw, ph = landscape(letter)

    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.5 * inch, ph - 0.4 * inch, pw - 0.5 * inch, ph - 0.4 * inch)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(pw / 2, ph - 0.7 * inch, "Place Value Houses")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 11)
    c.drawCentredString(pw / 2, ph - 0.95 * inch, "Millions  ·  Ten Thousands  ·  Thousands  ·  Hundreds / Tens / Ones")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(0.55 * inch, ph - 1.25 * inch, "Name: ________________________________")
    c.drawString(5.2 * inch, ph - 1.25 * inch, "Date: ____________________")
    c.drawString(8.3 * inch, ph - 1.25 * inch, "Grade: ______")

    # houses image
    c.drawImage(str(blank), 0.4 * inch, ph - 4.05 * inch, width=10.2 * inch, height=2.55 * inch, mask="auto")

    c.setFont("Helvetica", 10)
    c.drawString(0.55 * inch, 3.85 * inch, "Directions: Write one digit in each window. Then write the full number on the line.")
    y = 3.45 * inch
    problems = [
        "1. Number: ____________________   Digits in houses (left → right): ___ , ___ , ___ , ___ , ___ , ___",
        "2. Number: ____________________   Digits in houses (left → right): ___ , ___ , ___ , ___ , ___ , ___",
        "3. Number: ____________________   Digits in houses (left → right): ___ , ___ , ___ , ___ , ___ , ___",
        "4. Teacher number: ____________________   What number did you build? ____________________",
    ]
    c.setFont("Helvetica", 11)
    for line in problems:
        c.drawString(0.55 * inch, y, line)
        y -= 0.42 * inch

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(0.55 * inch, 0.4 * inch, "Printable Place Value Houses mat · Grades 3–4")
    c.drawRightString(pw - 0.55 * inch, 0.4 * inch, "Page 1")
    c.showPage()

    # ---- Page 2: Portrait practice worksheet ----
    c.setPageSize(letter)
    pw, ph = letter
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.55 * inch, ph - 0.4 * inch, pw - 0.55 * inch, ph - 0.4 * inch)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(pw / 2, ph - 0.7 * inch, "Place Value Houses Worksheet")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10)
    c.drawCentredString(pw / 2, ph - 0.92 * inch, "Grade 3 & Grade 4  ·  Find the place")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(0.6 * inch, ph - 1.2 * inch, "Name: ______________________________     Date: ______________     Score: _____ / 12")

    c.drawImage(str(example), 0.55 * inch, ph - 3.35 * inch, width=7.4 * inch, height=1.9 * inch, mask="auto")

    y = ph - 3.6 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "A. Which house / place?")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10.5)
    y -= 0.28 * inch
    qs_a = [
        "1. In 7,000 the 7 is in the ____________________ house.",
        "2. In 50,000 the 5 is in the ____________________ house.",
        "3. In 2,000,000 the 2 is in the ____________________ house.",
        "4. In 900 the 9 is in the ____________________ house.",
        "5. In 1,040,000 the 4 is in the ____________________ house.",
        "6. In 3,856 the 5 is in the ____________________ place.",
    ]
    for q in qs_a:
        c.drawString(0.65 * inch, y, q)
        y -= 0.26 * inch

    y -= 0.08 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "B. Put each number into the houses")
    c.setFillColor(colors.black)
    y -= 0.22 * inch

    # table
    data = [
        ["Number", "Millions", "Ten Thousands", "Thousands", "Hundreds", "Tens", "Ones"],
        ["482", "", "", "", "", "", ""],
        ["6,305", "", "", "", "", "", ""],
        ["40,070", "", "", "", "", "", ""],
        ["2,058,906", "", "", "", "", "", ""],
    ]
    # draw simple table manually
    col_w = [1.2 * inch, 1.0 * inch, 1.2 * inch, 1.0 * inch, 1.0 * inch, 0.85 * inch, 0.85 * inch]
    x0 = 0.55 * inch
    row_h = 0.32 * inch
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(LIGHT)
    c.rect(x0, y - row_h, sum(col_w), row_h, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setStrokeColor(NAVY)
    xx = x0
    for i, h in enumerate(data[0]):
        c.rect(xx, y - row_h, col_w[i], row_h, fill=0, stroke=1)
        c.drawCentredString(xx + col_w[i] / 2, y - row_h + 0.1 * inch, h)
        xx += col_w[i]
    y -= row_h
    c.setFont("Helvetica", 10)
    for row in data[1:]:
        xx = x0
        for i, cell in enumerate(row):
            c.rect(xx, y - row_h, col_w[i], row_h, fill=0, stroke=1)
            if i == 0:
                c.drawCentredString(xx + col_w[i] / 2, y - row_h + 0.1 * inch, cell)
            xx += col_w[i]
        y -= row_h

    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "C. Build a number")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10.5)
    y -= 0.28 * inch
    c.drawString(0.65 * inch, y, "11. 5 in millions, 3 in thousands, 7 in ones. Other windows = 0.   Number: ______________")
    y -= 0.28 * inch
    c.drawString(0.65 * inch, y, "12. 9 in ten thousands, 4 in hundreds, 2 in tens. Other windows = 0. Number: ______________")

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(0.55 * inch, 0.4 * inch, "Printable worksheet · Answer key on next page")
    c.drawRightString(pw - 0.55 * inch, 0.4 * inch, "Page 2")
    c.showPage()

    # ---- Page 3: Answer key ----
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.55 * inch, ph - 0.4 * inch, pw - 0.55 * inch, ph - 0.4 * inch)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(pw / 2, ph - 0.75 * inch, "Answer Key")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10)
    c.drawCentredString(pw / 2, ph - 0.98 * inch, "Place Value Houses Printable Worksheet")

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    y = ph - 1.4 * inch
    c.drawString(0.7 * inch, y, "Page 2 — Section A")
    c.setFont("Helvetica", 10.5)
    answers_a = [
        "1. thousands",
        "2. ten thousands",
        "3. millions",
        "4. hundreds",
        "5. ten thousands",
        "6. tens",
    ]
    y -= 0.25 * inch
    for a in answers_a:
        c.drawString(0.85 * inch, y, a)
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, y, "Page 2 — Section B")
    c.setFont("Helvetica", 10.5)
    y -= 0.25 * inch
    for line in [
        "482 → 0, 0, 0, 4, 8, 2",
        "6,305 → 0, 0, 6, 3, 0, 5",
        "40,070 → 0, 4, 0, 0, 7, 0",
        "2,058,906 → 2, 5, 8, 9, 0, 6",
    ]:
        c.drawString(0.85 * inch, y, line)
        y -= 0.22 * inch

    y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, y, "Page 2 — Section C")
    c.setFont("Helvetica", 10.5)
    y -= 0.25 * inch
    c.drawString(0.85 * inch, y, "11. 5,003,007")
    y -= 0.22 * inch
    c.drawString(0.85 * inch, y, "12. 90,420")

    y -= 0.4 * inch
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(0.7 * inch, y, "Page 1 mat: answers vary (student-built numbers).")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawRightString(pw - 0.55 * inch, 0.4 * inch, "Page 3")
    c.save()
    print("Wrote", mat_path)
    return mat_path


if __name__ == "__main__":
    build()
