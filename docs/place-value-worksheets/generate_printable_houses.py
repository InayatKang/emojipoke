#!/usr/bin/env python3
"""Printable Place Value Houses — ones through millions (full places)."""

from pathlib import Path

import cairosvg
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent
NAVY = colors.HexColor("#1B3A4B")
TEAL = colors.HexColor("#2F6F6A")
LIGHT = colors.HexColor("#EEF5F5")

# Three period houses covering all places the teacher requested:
# Millions | Hundred Thousands, Ten Thousands, Thousands | Hundreds, Tens, Ones
HOUSES = [
    ("MILLIONS", "#A074B5", ["Millions"]),
    ("THOUSANDS", "#F29B3A", ["Hundred\nThousands", "Ten\nThousands", "Thousands"]),
    ("ONES", "#EF6B73", ["Hundreds", "Tens", "Ones"]),
]


def houses_svg(path: Path, with_example=False):
    W, H = 1100, 310
    # Example: 3,152,418
    example = {
        0: ["3"],
        1: ["1", "5", "2"],
        2: ["4", "1", "8"],
    }
    margin, gap = 18, 22
    usable = W - 2 * margin - gap * (len(HOUSES) - 1)
    win_counts = [len(h[2]) for h in HOUSES]
    unit = usable / sum(c for c in win_counts)
    widths = [c * unit for c in win_counts]
    body_h, roof_h = 150, 60
    body_top = 68

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
    for i, (title, color, windows) in enumerate(HOUSES):
        w = widths[i]
        digits = example[i] if with_example else [""] * len(windows)
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
            pad = 9
            by, bh = body_top + 14, 68
            p.append(
                f'<rect x="{wx+pad:.1f}" y="{by}" width="{ww-2*pad:.1f}" height="{bh}" '
                f'fill="#fff" stroke="#444" stroke-width="1.4" rx="4"/>\n'
            )
            if digits[wi]:
                p.append(
                    f'<text x="{wx+ww/2:.1f}" y="{by+46:.1f}" text-anchor="middle" '
                    f'font-family="Arial" font-size="34" font-weight="700" fill="#1B3A4B">{digits[wi]}</text>\n'
                )
            else:
                p.append(
                    f'<line x1="{wx+pad+6:.1f}" y1="{by+bh-12:.1f}" x2="{wx+ww-pad-6:.1f}" y2="{by+bh-12:.1f}" '
                    f'stroke="#bbb" stroke-width="1" stroke-dasharray="3 3"/>\n'
                )
            lines = label.split("\n")
            ty = body_top + body_h - (28 if len(lines) > 1 else 20)
            for li, line in enumerate(lines):
                p.append(
                    f'<text x="{wx+ww/2:.1f}" y="{ty + li*12:.1f}" text-anchor="middle" '
                    f'font-family="Arial" font-size="10.5" font-weight="600" fill="#222">{esc(line)}</text>\n'
                )
        peak_x, peak_y = x + w / 2, body_top - roof_h
        left, right = x - 5, x + w + 5
        p.append(
            f'<polygon points="{left:.1f},{body_top+1:.1f} {peak_x:.1f},{peak_y:.1f} {right:.1f},{body_top+1:.1f}" '
            f'fill="{color}" stroke="#111" stroke-width="2.2"/>\n'
        )
        chim_x = x + w * 0.72
        t = max(0.2, (chim_x - peak_x) / (right - peak_x))
        ry = peak_y + (body_top - peak_y) * t
        p.append(
            f'<rect x="{chim_x:.1f}" y="{ry-20:.1f}" width="15" height="20" '
            f'fill="url(#bricks)" stroke="#111" stroke-width="1.2"/>\n'
        )
        p.append(
            f'<text x="{peak_x:.1f}" y="{peak_y+34:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="13" font-weight="700" fill="#111">{esc(title)}</text>\n'
        )
        if i < len(HOUSES) - 1:
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
    # place strip reminder
    places = "Millions  ·  Hundred Thousands  ·  Ten Thousands  ·  Thousands  ·  Hundreds  ·  Tens  ·  Ones"
    p.append(
        f'<text x="{W/2}" y="292" text-anchor="middle" font-family="Arial" font-size="12" '
        f'fill="#333">{places}</text>\n'
    )
    if with_example:
        p.append(
            '<text x="550" y="275" text-anchor="middle" font-family="Arial" font-size="14" '
            'font-weight="700" fill="#1B3A4B">Example: 3,152,418</text>\n'
        )
    p.append("</svg>")
    path.write_text("".join(p), encoding="utf-8")
    png = path.with_suffix(".png")
    cairosvg.svg2png(url=str(path), write_to=str(png), output_width=1800)
    return png


def build():
    blank = houses_svg(OUT / "printable_houses_blank.svg", with_example=False)
    example = houses_svg(OUT / "printable_houses_example.svg", with_example=True)

    out = OUT / "Place_Value_Houses_Printable_Mat.pdf"
    c = canvas.Canvas(str(out), pagesize=landscape(letter))
    pw, ph = landscape(letter)

    # ===== PAGE 1: Landscape mat =====
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.45 * inch, ph - 0.35 * inch, pw - 0.45 * inch, ph - 0.35 * inch)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(pw / 2, ph - 0.62 * inch, "Place Value Houses")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10)
    c.drawCentredString(
        pw / 2,
        ph - 0.85 * inch,
        "Ones · Tens · Hundreds · Thousands · Ten Thousands · Hundred Thousands · Millions",
    )

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(0.5 * inch, ph - 1.15 * inch, "Name: ________________________________")
    c.drawString(5.1 * inch, ph - 1.15 * inch, "Date: ____________________")
    c.drawString(8.2 * inch, ph - 1.15 * inch, "Grade: ______")

    c.drawImage(str(blank), 0.35 * inch, ph - 4.0 * inch, width=10.3 * inch, height=2.65 * inch, mask="auto")

    c.setFont("Helvetica", 10)
    c.drawString(
        0.5 * inch,
        3.7 * inch,
        "Directions: Write one digit in each window. Read from the Millions house to the Ones window.",
    )
    y = 3.3 * inch
    c.setFont("Helvetica", 11)
    for i in range(1, 5):
        c.drawString(
            0.5 * inch,
            y,
            f"{i}. Number: ____________________     "
            f"M ___   HTh ___   TTh ___   Th ___   H ___   T ___   O ___",
        )
        y -= 0.4 * inch

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(0.5 * inch, 0.35 * inch, "Printable Place Value Houses · Grades 3–4 · Full places to millions")
    c.drawRightString(pw - 0.5 * inch, 0.35 * inch, "Page 1")
    c.showPage()

    # ===== PAGE 2: Practice worksheet =====
    c.setPageSize(letter)
    pw, ph = letter
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.55 * inch, ph - 0.4 * inch, pw - 0.55 * inch, ph - 0.4 * inch)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(pw / 2, ph - 0.68 * inch, "Place Value Houses Worksheet")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(
        pw / 2,
        ph - 0.9 * inch,
        "Ones · Tens · Hundreds · Thousands · Ten Thousands · Hundred Thousands · Millions",
    )
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(0.6 * inch, ph - 1.18 * inch, "Name: ______________________________     Date: ______________     Score: _____ / 14")

    c.drawImage(str(example), 0.5 * inch, ph - 3.25 * inch, width=7.5 * inch, height=1.85 * inch, mask="auto")

    y = ph - 3.5 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "A. Name the place of the underlined digit")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10.5)
    y -= 0.28 * inch
    section_a = [
        "1. 4<u>2</u>8  →  ____________________",
        "2. 3,<u>5</u>17  →  ____________________",
        "3. <u>8</u>0,246  →  ____________________",
        "4. 1<u>6</u>0,000  →  ____________________",
        "5. <u>7</u>,045,219  →  ____________________",
        "6. 2,9<u>3</u>8,100  →  ____________________",
    ]
    # PDF canvas doesn't render HTML underline — use plain wording
    section_a = [
        "1. In 428, the digit 2 is in the ____________________ place.",
        "2. In 3,517, the digit 5 is in the ____________________ place.",
        "3. In 80,246, the digit 8 is in the ____________________ place.",
        "4. In 160,000, the digit 6 is in the ____________________ place.",
        "5. In 7,045,219, the digit 7 is in the ____________________ place.",
        "6. In 2,938,100, the digit 3 is in the ____________________ place.",
    ]
    for q in section_a:
        c.drawString(0.65 * inch, y, q)
        y -= 0.25 * inch

    y -= 0.06 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "B. Put each number in the houses (write every digit)")
    c.setFillColor(colors.black)
    y -= 0.2 * inch

    headers = ["Number", "M", "HTh", "TTh", "Th", "H", "T", "O"]
    rows = [
        ["5,284", "", "", "", "", "", "", ""],
        ["40,706", "", "", "", "", "", "", ""],
        ["318,052", "", "", "", "", "", "", ""],
        ["1,604,973", "", "", "", "", "", "", ""],
    ]
    col_w = [1.25 * inch, 0.75 * inch, 0.85 * inch, 0.85 * inch, 0.75 * inch, 0.75 * inch, 0.7 * inch, 0.7 * inch]
    x0 = 0.55 * inch
    row_h = 0.3 * inch
    c.setFillColor(LIGHT)
    c.rect(x0, y - row_h, sum(col_w), row_h, fill=1, stroke=0)
    c.setStrokeColor(NAVY)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 8)
    xx = x0
    for i, h in enumerate(headers):
        c.rect(xx, y - row_h, col_w[i], row_h, fill=0, stroke=1)
        c.drawCentredString(xx + col_w[i] / 2, y - row_h + 0.1 * inch, h)
        xx += col_w[i]
    y -= row_h
    c.setFont("Helvetica", 10)
    for row in rows:
        xx = x0
        for i, cell in enumerate(row):
            c.rect(xx, y - row_h, col_w[i], row_h, fill=0, stroke=1)
            if i == 0:
                c.drawCentredString(xx + col_w[i] / 2, y - row_h + 0.1 * inch, cell)
            xx += col_w[i]
        y -= row_h

    y -= 0.18 * inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(NAVY)
    c.drawString(0.6 * inch, y, "C. Build a number")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10.5)
    y -= 0.28 * inch
    c.drawString(0.65 * inch, y, "11. 6 millions, 4 hundred thousands, 0 ten thousands, 2 thousands, 5 hundreds, 1 ten, 8 ones")
    y -= 0.22 * inch
    c.drawString(0.85 * inch, y, "Number: ____________________")
    y -= 0.3 * inch
    c.drawString(0.65 * inch, y, "12. 9 in the ten-thousands place, 3 in the hundreds place, 7 in the ones place. All other digits 0.")
    y -= 0.22 * inch
    c.drawString(0.85 * inch, y, "Number: ____________________")
    y -= 0.3 * inch
    c.drawString(0.65 * inch, y, "13–14. Write the value of the digit 5 in each number:")
    y -= 0.24 * inch
    c.drawString(0.85 * inch, y, "13. 5,000  →  __________          14. 500,000  →  __________")

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(0.55 * inch, 0.38 * inch, "M=Millions  HTh=Hundred Thousands  TTh=Ten Thousands  Th=Thousands  H=Hundreds  T=Tens  O=Ones")
    c.drawRightString(pw - 0.55 * inch, 0.38 * inch, "Page 2")
    c.showPage()

    # ===== PAGE 3: Answer key =====
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(0.55 * inch, ph - 0.4 * inch, pw - 0.55 * inch, ph - 0.4 * inch)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(pw / 2, ph - 0.72 * inch, "Answer Key")
    c.setFillColor(TEAL)
    c.setFont("Helvetica", 10)
    c.drawCentredString(pw / 2, ph - 0.95 * inch, "Place Value Houses · Ones through Millions")

    c.setFillColor(colors.black)
    y = ph - 1.4 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, y, "Section A")
    c.setFont("Helvetica", 10.5)
    for line in [
        "1. tens",
        "2. thousands",
        "3. ten thousands",
        "4. ten thousands",
        "5. millions",
        "6. ten thousands",
    ]:
        y -= 0.22 * inch
        c.drawString(0.85 * inch, y, line)

    y -= 0.3 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, y, "Section B  (M, HTh, TTh, Th, H, T, O)")
    c.setFont("Helvetica", 10.5)
    for line in [
        "5,284 → 0, 0, 0, 5, 2, 8, 4",
        "40,706 → 0, 0, 4, 0, 7, 0, 6",
        "318,052 → 0, 3, 1, 8, 0, 5, 2",
        "1,604,973 → 1, 6, 0, 4, 9, 7, 3",
    ]:
        y -= 0.22 * inch
        c.drawString(0.85 * inch, y, line)

    y -= 0.3 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, y, "Section C")
    c.setFont("Helvetica", 10.5)
    for line in [
        "11. 6,402,518",
        "12. 90,307",
        "13. 5,000",
        "14. 500,000",
    ]:
        y -= 0.22 * inch
        c.drawString(0.85 * inch, y, line)

    y -= 0.35 * inch
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(0.7 * inch, y, "Houses: MILLIONS | THOUSANDS (HTh · TTh · Th) | ONES (Hundreds · Tens · Ones)")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawRightString(pw - 0.55 * inch, 0.4 * inch, "Page 3")
    c.save()
    print("Wrote", out)
    return out


if __name__ == "__main__":
    build()
