import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Try both possible logo filenames
LOGO_PATH = None
for candidate in [
    r"C:\Users\jaros\OneDrive\Plocha\AGENT\logo.png",
    r"C:\Users\jaros\OneDrive\Plocha\AGENT\logo.png.jpeg",
    r"C:\Users\jaros\OneDrive\Plocha\AGENT\logo.jpeg",
    r"C:\Users\jaros\OneDrive\Plocha\AGENT\logo.jpg",
]:
    if os.path.exists(candidate):
        LOGO_PATH = candidate
        break

OUTPUT_PATH = r"C:\Users\jaros\OneDrive\Plocha\AGENT\onboarding-klient.pdf"

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
RED       = HexColor("#e63946")
DARK      = HexColor("#1a1a1a")
WHITE     = colors.white
LIGHT_GRAY = HexColor("#f7f7f7")
MID_GRAY  = HexColor("#cccccc")
TEXT_GRAY = HexColor("#555555")

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = 2 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

# ---------------------------------------------------------------------------
# Logo helpers
# ---------------------------------------------------------------------------

def _make_logo(width, height, h_align="LEFT"):
    if LOGO_PATH is None:
        return None
    try:
        img = RLImage(LOGO_PATH, width=width, height=height)
        img.hAlign = h_align
        return img
    except Exception:
        return None


def logo_small():
    """40x40 logo for page headers, aligned left."""
    return _make_logo(40, 40, "LEFT")


def logo_large():
    """120x120 centered logo for title page."""
    return _make_logo(120, 120, "CENTER")


# ---------------------------------------------------------------------------
# Custom flowable: red circle with white number
# ---------------------------------------------------------------------------

class RedCircleNumber(Flowable):
    def __init__(self, number, radius=14):
        Flowable.__init__(self)
        self.number = str(number)
        self.radius = radius
        self.width  = radius * 2
        self.height = radius * 2

    def draw(self):
        c = self.canv
        r = self.radius
        c.setFillColor(RED)
        c.setStrokeColor(RED)
        c.circle(r, r, r, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Arial-Bold", 12)
        c.drawCentredString(r, r - 4, self.number)


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def build_styles():
    s = {}

    s["title"] = ParagraphStyle(
        "TitleStyle",
        fontName="Arial-Bold",
        fontSize=30,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=36,
    )
    s["subtitle"] = ParagraphStyle(
        "SubtitleStyle",
        fontName="Arial",
        fontSize=15,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        spaceAfter=14,
        leading=22,
    )
    s["tagline"] = ParagraphStyle(
        "TaglineStyle",
        fontName="Arial",
        fontSize=12,
        textColor=HexColor("#444444"),
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=18,
    )
    s["year"] = ParagraphStyle(
        "YearStyle",
        fontName="Arial",
        fontSize=10,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
    )
    s["page_title"] = ParagraphStyle(
        "PageTitleStyle",
        fontName="Arial-Bold",
        fontSize=22,
        textColor=DARK,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=28,
    )
    s["body"] = ParagraphStyle(
        "BodyStyle",
        fontName="Arial",
        fontSize=11,
        textColor=DARK,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=17,
    )
    s["step_text"] = ParagraphStyle(
        "StepText",
        fontName="Arial",
        fontSize=12,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=18,
    )
    s["table_header"] = ParagraphStyle(
        "TableHeader",
        fontName="Arial-Bold",
        fontSize=11,
        textColor=WHITE,
        alignment=TA_LEFT,
        leading=16,
    )
    s["table_cell"] = ParagraphStyle(
        "TableCell",
        fontName="Arial",
        fontSize=11,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=16,
    )
    s["note"] = ParagraphStyle(
        "NoteStyle",
        fontName="Arial",
        fontSize=10,
        textColor=TEXT_GRAY,
        alignment=TA_LEFT,
        leading=15,
    )
    s["url"] = ParagraphStyle(
        "URLStyle",
        fontName="Arial-Bold",
        fontSize=13,
        textColor=RED,
        alignment=TA_CENTER,
        leading=18,
    )
    s["checklist"] = ParagraphStyle(
        "ChecklistStyle",
        fontName="Arial",
        fontSize=12,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=22,
    )
    s["contact_question"] = ParagraphStyle(
        "ContactQuestion",
        fontName="Arial",
        fontSize=13,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=16,
    )
    s["contact_email"] = ParagraphStyle(
        "ContactEmail",
        fontName="Arial-Bold",
        fontSize=18,
        textColor=RED,
        alignment=TA_CENTER,
        leading=26,
    )
    s["thanks"] = ParagraphStyle(
        "ThanksStyle",
        fontName="Arial",
        fontSize=12,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=18,
        spaceAfter=16,
    )
    s["footer"] = ParagraphStyle(
        "FooterStyle",
        fontName="Arial",
        fontSize=10,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        leading=14,
    )
    return s


# ---------------------------------------------------------------------------
# Reusable dividers
# ---------------------------------------------------------------------------

def red_underline():
    return HRFlowable(
        width="100%",
        thickness=2,
        color=RED,
        spaceAfter=22,
        spaceBefore=2,
    )


def thin_gray_line():
    return HRFlowable(
        width="100%",
        thickness=0.5,
        color=MID_GRAY,
        spaceAfter=10,
        spaceBefore=10,
    )


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def page1(S):
    story = []
    story.append(Spacer(1, 2.5 * cm))

    lg = logo_large()
    if lg:
        story.append(lg)
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("AI Lead Responder", S["title"]))
    story.append(Paragraph("Onboarding příručka", S["subtitle"]))

    story.append(HRFlowable(
        width="55%",
        thickness=2,
        color=RED,
        spaceAfter=18,
        spaceBefore=6,
        hAlign="CENTER",
    ))

    story.append(Paragraph(
        "Automatická odpověď na každý dotaz do 30 sekund",
        S["tagline"]
    ))

    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph("2026", S["year"]))
    return story


def page2(S):
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Jak to funguje", S["page_title"]))
    story.append(red_underline())

    steps = [
        (1, "Zákazník vyplní formulář na vašem webu"),
        (2, "Systém okamžitě zaznamená poptávku"),
        (3, "AI vygeneruje personalizovanou odpověď"),
        (4, "Email dorazí zákazníkovi do 30 sekund"),
    ]

    for num, text in steps:
        row = [[RedCircleNumber(num), Paragraph(text, S["step_text"])]]
        tbl = Table(row, colWidths=[34, CONTENT_W - 34])
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.45 * cm))

    return story


def page3(S):
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Co budete potřebovat", S["page_title"]))
    story.append(red_underline())

    col = CONTENT_W / 2
    header = [
        Paragraph("Údaj", S["table_header"]),
        Paragraph("Popis", S["table_header"]),
    ]
    rows = [
        ("Název společnosti",  "Jméno vaší firmy"),
        ("Kontaktní osoba",    "Vaše jméno nebo jméno kolegy"),
        ("Telefon",            "Kontaktní telefon"),
        ("Web",                "Vaše webová stránka"),
        ("Email",              "Pro příjem odpovědí od zákazníků"),
    ]

    data = [header] + [
        [Paragraph(r[0], S["table_cell"]), Paragraph(r[1], S["table_cell"])]
        for r in rows
    ]

    tbl = Table(data, colWidths=[col, col])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), RED),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Arial-Bold"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(tbl)
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "Vše ostatní nastavíme za vás do 24 hodin.",
        S["note"]
    ))
    return story


def page4(S):
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Vyzkoušejte demo", S["page_title"]))
    story.append(red_underline())

    story.append(Paragraph(
        "Navštivte naši demo stránku a uvidíte přesně, "
        "jak bude vaše automatizace fungovat.",
        S["body"]
    ))
    story.append(Spacer(1, 0.5 * cm))

    # Red-bordered URL box
    url_cell = Paragraph(
        "https://kopifko.github.io/ai-lead-responder/demo.html",
        S["url"]
    )
    url_tbl = Table([[url_cell]], colWidths=[CONTENT_W])
    url_tbl.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.5, RED),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("BACKGROUND",    (0, 0), (-1, -1), WHITE),
    ]))
    story.append(url_tbl)
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph(
        "Po obdržení platby budete mít systém spuštěný do 24 hodin.",
        S["body"]
    ))
    story.append(Spacer(1, 0.5 * cm))

    for item in [
        u"\u2713  Nastavení systému",
        u"\u2713  Propojení s vaším emailem",
        u"\u2713  Testovací spuštění",
        u"\u2713  Předání přístupových údajů",
    ]:
        story.append(Paragraph(item, S["checklist"]))

    return story


def page5(S):
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Kontakt", S["page_title"]))
    story.append(red_underline())

    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(
        "Máte otázky nebo jste připraveni začít?",
        S["contact_question"]
    ))
    story.append(Paragraph(
        "kopejskojaroslav@gmail.com",
        S["contact_email"]
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(
        "Děkujeme za zájem. Těšíme se na spolupráci.",
        S["thanks"]
    ))
    story.append(thin_gray_line())
    story.append(Paragraph("AI Lead Responder 2026", S["footer"]))

    return story


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="AI Lead Responder - Onboarding příručka",
        author="AI Lead Responder",
    )

    S = build_styles()

    story = []
    story.extend(page1(S)); story.append(PageBreak())
    story.extend(page2(S)); story.append(PageBreak())
    story.extend(page3(S)); story.append(PageBreak())
    story.extend(page4(S)); story.append(PageBreak())
    story.extend(page5(S))

    doc.build(story)
    print(f"PDF created successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
