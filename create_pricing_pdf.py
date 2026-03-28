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

OUTPUT_PATH = r"C:\Users\jaros\OneDrive\Plocha\AGENT\cenova-nabidka.pdf"

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
RED        = HexColor("#e63946")
DARK       = HexColor("#1a1a1a")
WHITE      = colors.white
LIGHT_GRAY = HexColor("#f8f8f8")
MID_GRAY   = HexColor("#cccccc")
TEXT_GRAY  = HexColor("#555555")
GREEN_CHECK = RED  # checkmarks rendered in red per spec

# ---------------------------------------------------------------------------
# Page geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN    = 2 * cm
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
    return _make_logo(40, 40, "LEFT")


def logo_large():
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
    s["note"] = ParagraphStyle(
        "NoteStyle",
        fontName="Arial",
        fontSize=10,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=15,
    )
    s["url"] = ParagraphStyle(
        "URLStyle",
        fontName="Arial-Bold",
        fontSize=12,
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
        leading=24,
    )
    s["contact_question"] = ParagraphStyle(
        "ContactQuestion",
        fontName="Arial",
        fontSize=13,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=12,
    )
    s["contact_email"] = ParagraphStyle(
        "ContactEmail",
        fontName="Arial-Bold",
        fontSize=18,
        textColor=RED,
        alignment=TA_CENTER,
        leading=26,
    )
    s["footer"] = ParagraphStyle(
        "FooterStyle",
        fontName="Arial",
        fontSize=10,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        leading=14,
    )
    s["price_label"] = ParagraphStyle(
        "PriceLabel",
        fontName="Arial",
        fontSize=13,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=4,
    )
    s["price_big"] = ParagraphStyle(
        "PriceBig",
        fontName="Arial-Bold",
        fontSize=48,
        textColor=RED,
        alignment=TA_CENTER,
        leading=58,
        spaceAfter=2,
    )
    s["price_sub"] = ParagraphStyle(
        "PriceSub",
        fontName="Arial",
        fontSize=11,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=16,
    )
    s["demo_label"] = ParagraphStyle(
        "DemoLabel",
        fontName="Arial",
        fontSize=12,
        textColor=TEXT_GRAY,
        alignment=TA_CENTER,
        leading=18,
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
        spaceAfter=14,
        spaceBefore=14,
    )


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def page1(S):
    """Title page."""
    story = []
    story.append(Spacer(1, 2.5 * cm))

    lg = logo_large()
    if lg:
        story.append(lg)
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("Cenov\u00e1 nab\u00eddka", S["title"]))
    story.append(Paragraph("AI Lead Responder", S["subtitle"]))

    story.append(HRFlowable(
        width="55%",
        thickness=2,
        color=RED,
        spaceAfter=18,
        spaceBefore=6,
        hAlign="CENTER",
    ))

    story.append(Paragraph(
        "Automatick\u00e1 odpov\u011b\u010f na ka\u017edou popt\u00e1vku \u2014 bez pr\u00e1ce z va\u0161\u00ed strany.",
        S["tagline"]
    ))

    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph("2026", S["year"]))
    return story


def page2(S):
    """Offer / pricing page."""
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Co z\u00edsk\u00e1te", S["page_title"]))
    story.append(red_underline())

    # Big pricing box
    price_box_content = [
        [Paragraph("M\u011bs\u00ed\u010dn\u00ed p\u0159edplatn\u00e9", S["price_label"])],
        [Paragraph("1 490 K\u010d", S["price_big"])],
        [Paragraph("/ m\u011bs\u00edc \u00b7 bez z\u00e1vazk\u016f \u00b7 zru\u0161en\u00ed kdykoliv", S["price_sub"])],
    ]

    price_tbl = Table(price_box_content, colWidths=[CONTENT_W])
    price_tbl.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 2, RED),
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(price_tbl)
    story.append(Spacer(1, 0.8 * cm))

    # Checklist
    checklist_items = [
        u"\u2713  Automatick\u00e1 AI odpov\u011b\u010f na ka\u017edou popt\u00e1vku do 30 sekund",
        u"\u2713  Personalizovan\u00fd email s podpisem va\u0161\u00ed firmy",
        u"\u2713  Provoz 24/7 bez v\u00fdpadk\u016f",
        u"\u2713  Nastaven\u00ed a spu\u0161t\u011bn\u00ed syst\u00e9mu v cen\u011b",
        u"\u2713  Podpora p\u0159i jak\u00e9mkoliv probl\u00e9mu",
    ]

    check_style = ParagraphStyle(
        "CheckItem",
        fontName="Arial",
        fontSize=12,
        textColor=RED,
        alignment=TA_LEFT,
        leading=24,
    )
    check_text_style = ParagraphStyle(
        "CheckText",
        fontName="Arial",
        fontSize=12,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=24,
    )

    for item in checklist_items:
        # Split checkmark and text so checkmark is red, text is dark
        parts = item.split("  ", 1)
        check_mark = parts[0]
        text_part = parts[1] if len(parts) > 1 else ""
        row = [
            [
                Paragraph(
                    '<font color="#e63946">\u2713</font>  ' + text_part,
                    check_text_style
                )
            ]
        ]
        tbl = Table(row, colWidths=[CONTENT_W])
        tbl.setStyle(TableStyle([
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(tbl)

    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        "N\u00e1klady na provoz (server, AI, emaily) jsou zahrnuty v cen\u011b.",
        S["note"]
    ))

    return story


def page3(S):
    """How to start + contact page."""
    story = []

    sm = logo_small()
    if sm:
        story.append(sm)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Jak za\u010d\u00edt", S["page_title"]))
    story.append(red_underline())

    steps = [
        (1, "Napi\u0161te n\u00e1m na email n\u00ed\u017ee"),
        (2, "Za\u0161lete n\u00e1m podklady (n\u00e1zev firmy, kontakt, web)"),
        (3, "Do 24 hodin m\u00e1te syst\u00e9m spu\u0161t\u011bn\u00fd"),
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

    story.append(Spacer(1, 0.4 * cm))
    story.append(thin_gray_line())
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("P\u0159ipraveni za\u010d\u00edt?", S["contact_question"]))
    story.append(Paragraph("kopejskojaroslav@gmail.com", S["contact_email"]))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("Vyzkou\u0161ejte demo zdarma:", S["demo_label"]))
    story.append(Spacer(1, 0.2 * cm))

    url_cell = Paragraph(
        "https://kopifko.github.io/ai-lead-responder/demo.html",
        S["url"]
    )
    url_tbl = Table([[url_cell]], colWidths=[CONTENT_W])
    url_tbl.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.5, RED),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("BACKGROUND",    (0, 0), (-1, -1), WHITE),
    ]))
    story.append(url_tbl)

    story.append(Spacer(1, 2.5 * cm))
    story.append(thin_gray_line())
    story.append(Paragraph("AI Lead Responder \u00b7 2026", S["footer"]))

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
        title="AI Lead Responder - Cenov\u00e1 nab\u00eddka",
        author="AI Lead Responder",
    )

    S = build_styles()

    story = []
    story.extend(page1(S)); story.append(PageBreak())
    story.extend(page2(S)); story.append(PageBreak())
    story.extend(page3(S))

    doc.build(story)
    print(f"PDF created successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
