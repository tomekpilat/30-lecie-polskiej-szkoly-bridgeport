#!/usr/bin/env python3
"""Create one guide PDF and append every print-size template."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "assets" / "downloads"
TMP_DIR = ROOT / "tmp" / "pdfs"
OUTPUT_DIR = ROOT / "output" / "pdf"
GUIDE_PAGES = TMP_DIR / "przewodnik-informacje.pdf"
FINAL_PDF = OUTPUT_DIR / "przewodnik-wpisow-30-lecie-polskiej-szkoly-bridgeport.pdf"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

INK = HexColor("#151713")
MUTED = HexColor("#656860")
PAPER = HexColor("#FBFAF6")
WHITE = HexColor("#FFFFFF")
RED = HexColor("#DF3F38")
RED_SOFT = HexColor("#FBE9E7")
LINE = HexColor("#DDDCD5")


def setup_fonts() -> None:
    pdfmetrics.registerFont(TTFont("GuideRegular", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("GuideBold", FONT_BOLD))


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str,
    size: float,
    leading: float,
    color=INK,
) -> float:
    """Draw wrapped text and return the next baseline position."""
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdf.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_header(pdf: canvas.Canvas, page_number: int) -> None:
    width, height = letter
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    pdf.setFillColor(RED)
    pdf.roundRect(42, height - 68, 74, 25, 12.5, fill=1, stroke=0)
    pdf.setFillColor(WHITE)
    pdf.setFont("GuideBold", 10)
    pdf.drawCentredString(79, height - 59, "30 LAT")

    pdf.setFillColor(MUTED)
    pdf.setFont("GuideBold", 9)
    pdf.drawRightString(width - 42, height - 57, "POLSKA SZKOLA W BRIDGEPORT")

    pdf.setStrokeColor(LINE)
    pdf.setLineWidth(0.8)
    pdf.line(42, 44, width - 42, 44)
    pdf.setFillColor(MUTED)
    pdf.setFont("GuideRegular", 8)
    pdf.drawString(42, 29, "Wytyczne do przygotowania wpisu")
    pdf.drawRightString(width - 42, 29, str(page_number))


def draw_format_row(
    pdf: canvas.Canvas,
    y: float,
    name: str,
    size: str,
    pixels: str,
    note: str = "",
) -> None:
    x = 42
    width = 528
    row_height = 52
    pdf.setFillColor(WHITE)
    pdf.roundRect(x, y - row_height, width, row_height - 5, 8, fill=1, stroke=0)
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y - row_height, width, row_height - 5, 8, fill=0, stroke=1)

    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 10.5)
    pdf.drawString(x + 13, y - 21, name)
    if note:
        pdf.setFillColor(RED)
        pdf.setFont("GuideBold", 7.5)
        pdf.drawString(x + 13, y - 34, note)

    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 10)
    pdf.drawString(x + 260, y - 21, size)
    pdf.setFillColor(MUTED)
    pdf.setFont("GuideRegular", 8.5)
    pdf.drawString(x + 380, y - 21, pixels)


def create_information_pages(path: Path) -> None:
    width, height = letter
    pdf = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    pdf.setTitle("Wytyczne i szablony - 30-lecie Polskiej Szkoły w Bridgeport")
    pdf.setAuthor("Polska Szkoła w Bridgeport")

    # Page 1: overview and dimensions.
    draw_header(pdf, 1)
    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 27)
    pdf.drawString(42, height - 118, "Dodaj swoją historię")
    pdf.drawString(42, height - 151, "do publikacji na 30-lecie szkoły.")
    draw_wrapped(
        pdf,
        "Rodzinna dedykacja, wspomnienie, gratulacje lub reklama lokalnej firmy - wybierz format i przygotuj plik według poniższych wskazówek.",
        42,
        height - 182,
        510,
        "GuideRegular",
        11,
        16,
        MUTED,
    )

    pdf.setFillColor(RED_SOFT)
    pdf.roundRect(42, height - 268, 528, 50, 9, fill=1, stroke=0)
    pdf.setFillColor(RED)
    pdf.setFont("GuideBold", 10)
    pdf.drawString(57, height - 239, "NAJLEPSZY FORMAT")
    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 11)
    pdf.drawString(173, height - 239, "JPG w wysokiej jakości")
    pdf.setFillColor(MUTED)
    pdf.setFont("GuideRegular", 9.5)
    pdf.drawString(353, height - 239, "PDF również jest akceptowany")

    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 14)
    pdf.drawString(42, height - 300, "Dostępne rozmiary")
    pdf.setFillColor(MUTED)
    pdf.setFont("GuideRegular", 8.5)
    pdf.drawRightString(570, height - 298, "Wymiary w pikselach podano dla 300 DPI")

    y = height - 316
    draw_format_row(pdf, y, "Pelna strona", '8.5 x 11"', "2550 x 3300 px", "BEZ SPADU")
    y -= 54
    draw_format_row(pdf, y, "Pelna strona", '9 x 11.5"', "2700 x 3450 px", "ZE SPADEM 0.25\" Z KAZDEJ STRONY")
    y -= 54
    draw_format_row(pdf, y, "Pol strony", '7.25 x 4.75"', "2175 x 1425 px")
    y -= 54
    draw_format_row(pdf, y, "1/4 strony", '3.5 x 4.75"', "1050 x 1425 px")
    y -= 54
    draw_format_row(pdf, y, "Format wizytowki", '3.5 x 2"', "1050 x 600 px")

    draw_wrapped(
        pdf,
        "Wersji ze spadem użyj tylko wtedy, gdy tło lub zdjęcie ma dochodzić do samej krawędzi pełnej strony.",
        42,
        131,
        528,
        "GuideRegular",
        9.5,
        14,
        MUTED,
    )
    pdf.showPage()

    # Page 2: practical rules and contact.
    draw_header(pdf, 2)
    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 27)
    pdf.drawString(42, height - 118, "Pięć prostych zasad")
    draw_wrapped(
        pdf,
        "Dzięki nim tekst i zdjęcia będą czytelne, a gotowy wpis będzie łatwy do umieszczenia w publikacji.",
        42,
        height - 148,
        515,
        "GuideRegular",
        11,
        16,
        MUTED,
    )

    rules = [
        ("01", "Użyj dokładnego rozmiaru", "Nie zmieniaj proporcji szablonu i nie dodawaj przypadkowych marginesów."),
        ("02", "Przygotuj plik w 300 DPI", "To zalecana jakość. Minimum to 200 DPI."),
        ("03", "Zostaw bezpieczny margines", 'Ważne teksty i logo umieść co najmniej 3/8\" od krawędzi. Zalecane jest 1/2-3/4\".'),
        ("04", "Dodaj spad tylko do pełnej strony", 'Gdy tło dochodzi do krawędzi, użyj szablonu 9 x 11.5\". Gotowy format po przycięciu ma 8.5 x 11\".'),
        ("05", "Zapisz jako JPG lub PDF", "Preferowany jest JPG w najwyższej jakości. PDF także może zostać przesłany."),
    ]

    y = height - 194
    for number, title, body in rules:
        pdf.setFillColor(RED)
        pdf.circle(57, y - 6, 15, fill=1, stroke=0)
        pdf.setFillColor(WHITE)
        pdf.setFont("GuideBold", 8.5)
        pdf.drawCentredString(57, y - 9, number)
        pdf.setFillColor(INK)
        pdf.setFont("GuideBold", 11)
        pdf.drawString(84, y, title)
        draw_wrapped(pdf, body, 84, y - 17, 470, "GuideRegular", 9.5, 13, MUTED)
        y -= 73

    pdf.setFillColor(INK)
    pdf.setFont("GuideBold", 14)
    pdf.drawString(42, 214, "Jak korzystać z szablonów")
    draw_wrapped(
        pdf,
        "Kolejne strony tego dokumentu są szablonami w ich rzeczywistych wymiarach. Wstaw tekst, zdjęcia lub gotowy projekt w wybrany obszar. Różne rozmiary stron w tym pliku są zamierzone.",
        42,
        192,
        528,
        "GuideRegular",
        9.5,
        14,
        MUTED,
    )

    pdf.setFillColor(RED)
    pdf.roundRect(42, 86, 528, 67, 10, fill=1, stroke=0)
    pdf.setFillColor(WHITE)
    pdf.setFont("GuideBold", 12)
    pdf.drawString(57, 130, "Potrzebujesz pomocy?")
    draw_wrapped(
        pdf,
        "W sprawie wyboru rozmiaru lub przygotowania pliku skontaktuj się z Izą z zarządu Polskiej Szkoły.",
        57,
        111,
        490,
        "GuideRegular",
        9.5,
        13,
        WHITE,
    )
    pdf.save()


def combine_pdfs(info_pages: Path, output_path: Path) -> None:
    templates = [
        ("Pelna strona bez spadu", DOWNLOADS / "reklama-pelna-strona-8.5x11in.pdf"),
        ("Pelna strona ze spadem", DOWNLOADS / "reklama-pelna-strona-9x11.5in.pdf"),
        ("Pol strony", DOWNLOADS / "reklama-pol-strony-7.25x4.75in.pdf"),
        ("1/4 strony", DOWNLOADS / "reklama-cwierc-strony-3.5x4.75in.pdf"),
        ("Format wizytowki", DOWNLOADS / "reklama-wizytowka-3.5x2in.pdf"),
    ]

    writer = PdfWriter()
    for page in PdfReader(str(info_pages)).pages:
        writer.add_page(page)
    writer.add_outline_item("Informacje i wytyczne", 0)

    for label, template_path in templates:
        page_index = len(writer.pages)
        reader = PdfReader(str(template_path))
        for page in reader.pages:
            writer.add_page(page)
        writer.add_outline_item(label, page_index)

    writer.add_metadata(
        {
            "/Title": "Wytyczne i szablony - 30-lecie Polskiej Szkoły w Bridgeport",
            "/Author": "Polska Szkoła w Bridgeport",
            "/Subject": "Rozmiary, zasady przygotowania plików i szablony",
        }
    )
    with output_path.open("wb") as handle:
        writer.write(handle)


def main() -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_fonts()
    create_information_pages(GUIDE_PAGES)
    combine_pdfs(GUIDE_PAGES, FINAL_PDF)
    print(FINAL_PDF)


if __name__ == "__main__":
    main()
