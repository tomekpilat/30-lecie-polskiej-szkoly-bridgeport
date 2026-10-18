from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "downloads"
OUT.mkdir(parents=True, exist_ok=True)

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
pdfmetrics.registerFont(TTFont("GuideRegular", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("GuideBold", FONT_BOLD))

INK = HexColor("#102d3f")
BRICK = HexColor("#d64f3f")
CREAM = HexColor("#f5f0e7")
MINT = HexColor("#dce9dc")
GRAY = HexColor("#6c848f")
PT = 72

SPECS = [
    {
        "slug": "reklama-pelna-strona-8.5x11in",
        "title": "PEŁNA STRONA",
        "subtitle": "format strony",
        "w": 8.5,
        "h": 11.0,
        "pixels": "2550 x 3300 px przy 300 DPI",
        "full_page": True,
    },
    {
        "slug": "reklama-pol-strony-7.25x4.75in",
        "title": "PÓŁ STRONY",
        "subtitle": "orientacja pozioma",
        "w": 7.25,
        "h": 4.75,
        "pixels": "2175 x 1425 px przy 300 DPI",
        "full_page": False,
    },
    {
        "slug": "reklama-cwierc-strony-3.5x4.75in",
        "title": "ĆWIERĆ STRONY",
        "subtitle": "orientacja pionowa",
        "w": 3.5,
        "h": 4.75,
        "pixels": "1050 x 1425 px przy 300 DPI",
        "full_page": False,
    },
    {
        "slug": "reklama-wizytowka-3.5x2in",
        "title": "FORMAT WIZYTÓWKI",
        "subtitle": "orientacja pozioma",
        "w": 3.5,
        "h": 2.0,
        "pixels": "1050 x 600 px przy 300 DPI",
        "full_page": False,
    },
]


def center_text(c, text, y, size, font="GuideBold", color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(c._pagesize[0] / 2, y, text)


def make_pdf(spec):
    w, h = spec["w"] * PT, spec["h"] * PT
    path = OUT / f'{spec["slug"]}.pdf'
    c = canvas.Canvas(str(path), pagesize=(w, h), pageCompression=1)
    c.setTitle(f'Szablon reklamy - {spec["title"]}')
    c.setAuthor("Przewodnik reklam do rocznika")

    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    if spec["full_page"]:
        c.setFillColor(HexColor("#fffdf8"))
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(MINT)
        c.setStrokeColor(HexColor("#5a9a76"))
        c.setDash(3, 3)
        c.rect(0.375 * PT, 0.375 * PT, 7.75 * PT, 10.25 * PT, fill=1, stroke=1)
        c.setDash()
        center_text(c, "MINIMALNA STREFA BEZPIECZNA 7,75 x 10,25 cala", h / 2 - 15, 11)
        center_text(c, "Tekst, logo i ważne elementy umieść w tym polu", h / 2 - 34, 8.5, "GuideRegular", GRAY)
        center_text(c, "FORMAT STRONY: 8,5 x 11 cala", h - 0.18 * PT, 6.5, "GuideBold", INK)
    else:
        inset = min(0.25 * PT, w * 0.09, h * 0.16)
        c.setFillColor(HexColor("#fffdf8"))
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setStrokeColor(BRICK)
        c.setLineWidth(2)
        c.rect(1, 1, w - 2, h - 2, fill=0, stroke=1)
        c.setFillColor(MINT)
        c.setStrokeColor(HexColor("#5a9a76"))
        c.setDash(4, 3)
        c.rect(inset, inset, w - 2 * inset, h - 2 * inset, fill=1, stroke=1)
        c.setDash()
        center_text(c, "TEKST I LOGO W TYM POLU", h / 2 - 3, min(10, max(6, w / 42)))
        center_text(c, "zalecany odstęp 0,25 cala", h / 2 - 20, min(8, max(5, w / 55)), "GuideRegular", GRAY)

    if spec["full_page"]:
        title_y = h - 0.84 * PT
        subtitle_y = h - 1.08 * PT
        pixels_y = 0.32 * PT
    else:
        title_y = h - min(0.46 * PT, h * 0.24)
        subtitle_y = h - min(0.72 * PT, h * 0.38)
        pixels_y = min(0.15 * PT, h * 0.065)
    center_text(c, spec["title"], title_y, min(18, max(9, w / 24)))
    center_text(c, f'{spec["w"]:g} x {spec["h"]:g} cala | {spec["subtitle"]}', subtitle_y, min(9, max(5.5, w / 45)), "GuideRegular", BRICK)
    center_text(c, spec["pixels"], pixels_y, min(8, max(5, w / 55)), "GuideRegular", GRAY)
    c.save()
    return path


def make_svg(spec):
    scale = 96
    w, h = spec["w"] * scale, spec["h"] * scale
    path = OUT / f'{spec["slug"]}.svg'
    title = escape(spec["title"])
    subtitle = escape(f'{spec["w"]:g} x {spec["h"]:g} cala | {spec["subtitle"]}')
    pixels = escape(spec["pixels"])
    if spec["full_page"]:
        guides = f'''<rect width="{w}" height="{h}" fill="#fffdf8" stroke="#d64f3f" stroke-width="4"/>
  <rect x="36" y="36" width="{7.75*scale}" height="{10.25*scale}" fill="#dce9dc" stroke="#5a9a76" stroke-width="2" stroke-dasharray="5 5"/>
  <text x="50%" y="52%" text-anchor="middle" class="label">MINIMALNA STREFA BEZPIECZNA 7,75 x 10,25 cala</text>
  <text x="50%" y="55%" text-anchor="middle" class="small">Tekst, logo i ważne elementy umieść w tym polu</text>'''
    else:
        inset = min(24, w * 0.09, h * 0.16)
        guides = f'''<rect width="{w}" height="{h}" fill="#fffdf8" stroke="#d64f3f" stroke-width="4"/>
  <rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{h-2*inset}" fill="#dce9dc" stroke="#5a9a76" stroke-width="2" stroke-dasharray="5 5"/>
  <text x="50%" y="52%" text-anchor="middle" class="label">TEKST I LOGO W TYM POLU</text>
  <text x="50%" y="60%" text-anchor="middle" class="small">zalecany odstęp 0,25 cala</text>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{spec['w']}in" height="{spec['h']}in" viewBox="0 0 {w} {h}">
  <title>Szablon reklamy - {title}</title>
  <style>.head{{font:700 {max(12,min(24,w/18))}px Arial,sans-serif;fill:#102d3f}}.sub{{font:400 {max(8,min(13,w/32))}px Arial,sans-serif;fill:#d64f3f}}.label{{font:700 {max(8,min(14,w/28))}px Arial,sans-serif;fill:#102d3f}}.small{{font:400 {max(7,min(11,w/38))}px Arial,sans-serif;fill:#6c848f}}.tiny{{font:700 {max(6,min(9,w/55))}px Arial,sans-serif;fill:#6c848f}}.red{{fill:#d64f3f}}</style>
  {guides}
  <text x="50%" y="{min(48,h*0.19)}" text-anchor="middle" class="head">{title}</text>
  <text x="50%" y="{min(70,h*0.3)}" text-anchor="middle" class="sub">{subtitle}</text>
  <text x="50%" y="{h-min(16,h*0.08)}" text-anchor="middle" class="tiny">{pixels}</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")
    return path


if __name__ == "__main__":
    for item in SPECS:
        make_pdf(item)
        make_svg(item)
    print(f"Wygenerowano {len(SPECS)} pliki PDF i {len(SPECS)} pliki SVG w {OUT}")
