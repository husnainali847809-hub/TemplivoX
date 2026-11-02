import calendar, os, subprocess
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as CL
from data import *

GREEN, BEIGE, LINE, GREY = HexColor("#1F3D2B"), HexColor("#F6F1E7"), HexColor("#C9BFA8"), HexColor("#6B6F68")
M = 36
FOOT = "TemplivoX  |  Free Templates. Made Simple."


# ======================= PDF =======================
def frame(c, W, H, title):
    c.setFillColor(GREEN); c.rect(0, H - 62, W, 62, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Times-Bold", 22); c.drawString(M, H - 40, title)
    c.setFont("Helvetica", 8); c.drawRightString(W - M, H - 40, "TemplivoX")
    c.setFillColor(GREY); c.setFont("Helvetica", 7.5); c.drawCentredString(W / 2, 20, FOOT)
    return H - 62 - 16


def fields(c, W, y, labels):
    if not labels: return y
    per = 3 if len(labels) > 4 else 2
    cw = (W - 2 * M) / per
    for i, lab in enumerate(labels):
        col, row = i % per, i // per
        x, yy = M + col * cw, y - row * 24
        c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 8.5); c.drawString(x, yy, lab)
        lw = c.stringWidth(lab, "Helvetica-Bold", 8.5) + 5
        c.setStrokeColor(LINE); c.setLineWidth(.7); c.line(x + lw, yy - 2, x + cw - 12, yy - 2)
    return y - ((len(labels) - 1) // per + 1) * 24 - 4


def title(c, x, y, text):
    c.setFillColor(GREEN); c.setFont("Times-Bold", 12); c.drawString(x, y, text)


def lines(c, x, y, w, n, rh):
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    for i in range(n):
        c.line(x, y - (i + 1) * rh, x + w, y - (i + 1) * rh)


def checks(c, x, y, w, n, rh):
    c.setStrokeColor(GREEN); c.setLineWidth(.8)
    for i in range(n):
        yy = y - (i + 1) * rh
        c.rect(x, yy + 3, 9, 9, fill=0)
        c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(x + 16, yy, x + w, yy); c.setStrokeColor(GREEN)


def grid(c, x, y, w, cols, n, rh, wts=None, pre=None):
    wts = wts or [1.6] + [1] * (len(cols) - 1)
    tot = sum(wts); xs = [x]
    for k in wts: xs.append(xs[-1] + w * k / tot)
    c.setFillColor(GREEN); c.rect(x, y - rh, w, rh, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 8)
    for i, t in enumerate(cols): c.drawString(xs[i] + 4, y - rh + rh / 2 - 3, t)
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    for r in range(1, n + 1):
        yy = y - (r + 1) * rh
        c.line(x, yy, x + w, yy)
        if pre and r <= len(pre):
            c.setFillColor(GREY); c.setFont("Helvetica", 8); c.drawString(xs[0] + 4, yy + rh / 2 - 3, pre[r - 1])
    for xx in xs: c.line(xx, y - rh, xx, y - (n + 1) * rh)


def stack(c, W, y, sp):
    avail = y - 36
    units = sum({"lines": 1.9, "check": 1.9, "grid": 2.5, "totals": 4}[b[0]] + (b[2] if b[0] != "grid" and b[0] != "totals" else 0) +
                (b[3] if b[0] == "grid" else 0) for b in sp["blocks"])
    rh = max(14, min(36, avail / units)); w = W - 2 * M
    for b in sp["blocks"]:
        k = b[0]
        if k == "totals":
            y -= rh * .3
            for lab in ("Subtotal", "Tax", "Total"):
                c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 9); c.drawRightString(W - M - 110, y - rh + 5, lab)
                c.setStrokeColor(LINE); c.rect(W - M - 100, y - rh + 1, 100, rh - 2, fill=0); y -= rh
            y -= rh * .5; continue
        title(c, M, y - 10, b[1]); y -= rh * 1.5
        if k == "lines": lines(c, M, y, w, b[2], rh); y -= b[2] * rh + rh * .4
        elif k == "check": checks(c, M, y, w, b[2], rh); y -= b[2] * rh + rh * .4
        else:
            grid(c, M, y, w, b[2], b[3], rh, b[4].get("w"), b[4].get("pre")); y -= (b[3] + 1) * rh + rh * .6


def days(c, W, y, sp):
    boxes = sp["days"] + sp["extras"]; rows = (len(boxes) + 1) // 2
    gap = 10; bw = (W - 2 * M - gap) / 2; bh = (y - 40 - (rows - 1) * gap) / rows
    for i, name in enumerate(boxes):
        x = M + (i % 2) * (bw + gap); top = y - (i // 2) * (bh + gap)
        c.setFillColor(BEIGE); c.setStrokeColor(LINE); c.setLineWidth(.8); c.rect(x, top - bh, bw, bh, fill=1, stroke=1)
        c.setFillColor(GREEN); c.setFont("Times-Bold", 11); c.drawString(x + 8, top - 15, name)
        c.setStrokeColor(LINE); c.setLineWidth(.5)
        yy = top - 34
        while yy > top - bh + 6: c.line(x + 8, yy, x + bw - 8, yy); yy -= 17


def panels(c, x, y, w, items, avail):
    units = sum(1.9 + n for _, n, _ in items); rh = max(14, min(26, avail / units))
    for name, n, kind in items:
        title(c, x, y - 10, name); y -= rh * 1.5
        if kind == "check": checks(c, x, y, w, n, rh)
        elif kind == "num":
            lines(c, x + 14, y, w - 14, n, rh); c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 9)
            for i in range(n): c.drawString(x, y - (i + 1) * rh + 3, str(i + 1))
        else: lines(c, x, y, w, n, rh)
        y -= n * rh + rh * .4


def schedule(c, W, y, sp):
    avail = y - 36; lw = (W - 2 * M) * .52; rows = sp["end"] - sp["start"] + 1
    rh = avail / (rows + 1); title(c, M, y - 10, "Schedule"); top = y - rh * .9
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    for i in range(rows):
        yy = top - (i + 1) * rh * .94 - 0
        c.setFillColor(GREY); c.setFont("Helvetica", 8); c.drawString(M, yy + 4, "%02d:00" % (sp["start"] + i))
        c.line(M + 34, yy, M + lw, yy)
    px = M + lw + 20; panels(c, px, y, W - M - px, sp["panels"], avail)


def habit(c, W, y, sp):
    avail = y - 36 - (3 + 1.5) * 18; n = sp["rows"]; rh = min(26, avail / (n + 1)); w = W - 2 * M
    fw = 100; cw = (w - fw) / 31
    c.setFillColor(GREEN); c.rect(M, y - rh, w, rh, fill=1, stroke=0); c.setFillColor(white); c.setFont("Helvetica-Bold", 8)
    c.drawString(M + 4, y - rh + rh / 2 - 3, "Habit"); c.setFont("Helvetica", 6)
    for d in range(31): c.drawCentredString(M + fw + d * cw + cw / 2, y - rh + rh / 2 - 2, str(d + 1))
    c.setStrokeColor(LINE); c.setLineWidth(.5)
    for r in range(1, n + 1): c.line(M, y - (r + 1) * rh, M + w, y - (r + 1) * rh)
    for d in range(32): c.line(M + fw + d * cw, y - rh, M + fw + d * cw, y - (n + 1) * rh)
    c.line(M, y - rh, M, y - (n + 1) * rh)
    y -= (n + 1) * rh + 14; title(c, M, y - 10, sp["notes"][0]); lines(c, M, y - 18, w, sp["notes"][1], 18)


def month(c, W, y, sp):
    w = W - 2 * M; notes = sp.get("notes"); nb = (notes[1] * 18 + 30) if notes else 0
    ch = (y - 36 - nb - 20) / 6; cw = w / 7
    c.setFillColor(GREEN); c.rect(M, y - 20, w, 20, fill=1, stroke=0); c.setFillColor(white); c.setFont("Helvetica-Bold", 8.5)
    for i, d in enumerate(WK): c.drawCentredString(M + i * cw + cw / 2, y - 14, d)
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    for r in range(7): c.line(M, y - 20 - r * ch, M + w, y - 20 - r * ch)
    for k in range(8): c.line(M + k * cw, y - 20, M + k * cw, y - 20 - 6 * ch)
    if notes: title(c, M, y - 20 - 6 * ch - 18, notes[0]); lines(c, M, y - 20 - 6 * ch - 24, w, notes[1], 18)


def year(c, W, y, sp):
    cols, rows, gap = 3, 4, 14; bw = (W - 2 * M - (cols - 1) * gap) / cols; bh = (y - 36 - (rows - 1) * gap) / rows
    for m in range(12):
        x = M + (m % cols) * (bw + gap); top = y - (m // cols) * (bh + gap)
        c.setFillColor(BEIGE); c.setStrokeColor(LINE); c.rect(x, top - bh, bw, bh, fill=1, stroke=1)
        c.setFillColor(GREEN); c.setFont("Times-Bold", 11); c.drawString(x + 8, top - 15, calendar.month_name[m + 1])
        cw = (bw - 12) / 7; c.setFont("Helvetica-Bold", 7); c.setFillColor(GREY)
        for i, d in enumerate("MTWTFSS"): c.drawCentredString(x + 6 + i * cw + cw / 2, top - 30, d)
        c.setFont("Helvetica", 7.5); c.setFillColor(HexColor("#1c231e"))
        for r, wk in enumerate(calendar.monthcalendar(sp["year"], m + 1)):
            for i, d in enumerate(wk):
                if d: c.drawCentredString(x + 6 + i * cw + cw / 2, top - 44 - r * ((bh - 52) / 6), str(d))


DRAW = dict(stack=stack, days=days, schedule=schedule, habit=habit, month=month, year=year)


def make_pdf(t, path, size):
    W, H = size; c = canvas.Canvas(path, pagesize=size)
    c.setTitle(t["title"] + " - TemplivoX"); c.setAuthor("TemplivoX"); c.setSubject("Free printable template")
    y = frame(c, W, H, t["title"]); sp = t["spec"]
    y = fields(c, W, y, sp.get("fields")) if sp["kind"] != "year" else y
    DRAW[sp["kind"]](c, W, y, sp); c.showPage(); c.save()


# ======================= DOCX =======================
def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hexc); tcPr.append(s)


def dtable(d, cols, n, pre=None, rh=None, size=10):
    tb = d.add_table(rows=n + 1, cols=len(cols)); tb.style = "Table Grid"
    for i, name in enumerate(cols):
        cell = tb.rows[0].cells[i]; shade(cell, "1F3D2B"); cell.text = ""
        r = cell.paragraphs[0].add_run(name); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = RGBColor(255, 255, 255)
    for k in range(1, n + 1):
        if rh: tb.rows[k].height = Cm(rh)
        if pre and k <= len(pre): tb.rows[k].cells[0].text = pre[k - 1]
    d.add_paragraph(); return tb


def heading(d, text): 
    p = d.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(13); r.font.color.rgb = RGBColor(0x1F, 0x3D, 0x2B)


def blocks_docx(d, blocks):
    for b in blocks:
        k = b[0]
        if k == "totals":
            for lab in ("Subtotal", "Tax", "Total"): d.add_paragraph(lab + ": ______________")
            continue
        heading(d, b[1])
        if k == "lines": dtable(d, [" "], b[2], rh=.8)
        elif k == "check":
            for _ in range(b[2]): d.add_paragraph("\u2610  ")
        else: dtable(d, b[2], b[3], b[4].get("pre"))


def make_docx(t, path):
    d = Document(); sec = d.sections[0]; sp = t["spec"]
    wide = sp["kind"] == "habit" or (sp["kind"] == "stack" and any(b[0] == "grid" and len(b[2]) >= 6 for b in sp["blocks"]))
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    if wide:
        sec.orientation = WD_ORIENT.LANDSCAPE; sec.page_width, sec.page_height = Cm(29.7), Cm(21)
    for s in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, s, Cm(1.6))
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    h = d.add_paragraph(); r = h.add_run(t["title"]); r.bold = True; r.font.size = Pt(24); r.font.color.rgb = RGBColor(0x1F, 0x3D, 0x2B)
    p = d.add_paragraph(); r = p.add_run("TemplivoX - Free Templates. Made Simple."); r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x6B, 0x6F, 0x68)
    if sp["kind"] != "year":
        for f in sp.get("fields", []): d.add_paragraph(f + ": ____________________________")
    k = sp["kind"]
    if k == "stack": blocks_docx(d, sp["blocks"])
    elif k == "days":
        dtable(d, ["Day", "Plan and notes"], len(sp["days"] + sp["extras"]), sp["days"] + sp["extras"], rh=2.4, size=11)
    elif k == "schedule":
        dtable(d, ["Time", "Plan"], sp["end"] - sp["start"] + 1, ["%02d:00" % h for h in range(sp["start"], sp["end"] + 1)], rh=.8)
        for name, n, kind in sp["panels"]:
            heading(d, name)
            for i in range(n): d.add_paragraph(("\u2610  " if kind == "check" else ("%d. " % (i + 1) if kind == "num" else "")) + "")
    elif k == "habit":
        dtable(d, ["Habit"] + [str(i) for i in range(1, 32)], sp["rows"], rh=.9, size=7)
        heading(d, sp["notes"][0]); dtable(d, [" "], sp["notes"][1], rh=.8)
    elif k == "month":
        dtable(d, WK, 6, rh=2.4, size=9)
        if sp.get("notes"): heading(d, sp["notes"][0]); dtable(d, [" "], sp["notes"][1], rh=.8)
    elif k == "year":
        for m in range(1, 13):
            heading(d, "%s %d" % (calendar.month_name[m], sp["year"]))
            tb = dtable(d, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 6, size=8)
            for r, wk in enumerate(calendar.monthcalendar(sp["year"], m)):
                for i, dd in enumerate(wk):
                    if dd: tb.rows[r + 1].cells[i].text = str(dd)
    d.core_properties.title = t["title"] + " - TemplivoX"; d.core_properties.author = "TemplivoX"
    d.save(path)


# ======================= XLSX =======================
thin = Side(style="thin", color="C9BFA8"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
INPUT = PatternFill("solid", fgColor="FBF8F1"); HEAD = PatternFill("solid", fgColor="1F3D2B")
F = "Arial"; NUM = '#,##0.00;(#,##0.00);-'


def make_xlsx(t, path):
    wb = Workbook(); ws = wb.active; ws.title = t["title"][:31]; sp = t["spec"]
    ws["A1"] = t["title"]; ws["A1"].font = Font(name=F, size=16, bold=True, color="1F3D2B")
    ws["A2"] = "Type in the cream cells. Grey italic rows are examples you can overwrite. Amounts use any currency; totals calculate automatically."
    ws["A2"].font = Font(name=F, size=9, italic=True, color="6B6F68")
    r = 4
    for f in sp.get("fields", []):
        ws.cell(r, 1, f).font = Font(name=F, bold=True); c = ws.cell(r, 2); c.fill = INPUT; c.border = BOX; r += 1
    r += 1
    if sp["kind"] == "habit":
        hdr = ["Habit"] + list(range(1, 32)) + ["Days done"]
        for i, h in enumerate(hdr, 1):
            c = ws.cell(r, i, h); c.fill = HEAD; c.font = Font(name=F, bold=True, color="FFFFFF", size=9); c.alignment = Alignment(horizontal="center")
        for k in range(1, sp["rows"] + 1):
            for i in range(1, 33):
                c = ws.cell(r + k, i); c.fill = INPUT; c.border = BOX; c.font = Font(name=F, size=9); c.alignment = Alignment(horizontal="center")
            ws.cell(r + k, 33, "=COUNTA(B%d:AF%d)" % (r + k, r + k)).font = Font(name=F, bold=True)
        ws.cell(r, 33, "Days done").fill = HEAD; ws.cell(r, 33).font = Font(name=F, bold=True, color="FFFFFF", size=9)
        ws.column_dimensions["A"].width = 28
        for i in range(2, 33): ws.column_dimensions[CL(i)].width = 3.6
        ws.column_dimensions["AG"].width = 11; ws.cell(r + 1, 1, "Example: Drink water").font = Font(name=F, italic=True, color="6B6F68")
        wb.save(path); return
    last_total = None
    for b in sp["blocks"]:
        if b[0] == "totals":
            ws.cell(r, 3, "Tax rate").font = Font(name=F, bold=True); c = ws.cell(r, 4, 0); c.number_format = "0.0%"; c.fill = INPUT; c.border = BOX
            c.font = Font(name=F, color="0000FF"); ws.cell(r + 1, 3, "Tax").font = Font(name=F, bold=True)
            ws.cell(r + 1, 4, "=%s*D%d" % (last_total, r)).number_format = NUM
            ws.cell(r + 2, 3, "Total due").font = Font(name=F, bold=True)
            c = ws.cell(r + 2, 4, "=%s+D%d" % (last_total, r + 1)); c.number_format = NUM; c.font = Font(name=F, bold=True)
            r += 4; continue
        ws.cell(r, 1, b[1]).font = Font(name=F, bold=True, size=12, color="1F3D2B"); r += 1
        if b[0] != "grid":
            for _ in range(b[2]): c = ws.cell(r, 1); c.fill = INPUT; c.border = BOX; r += 1
            r += 1; continue
        cols, n, o = b[2], b[3], b[4]; calc = o.get("calc", {}); pre = o.get("pre"); ex = o.get("ex")
        for i, h in enumerate(cols, 1):
            c = ws.cell(r, i, h); c.fill = HEAD; c.font = Font(name=F, bold=True, color="FFFFFF")
        r += 1
        if ex:
            for i, v in enumerate(ex, 1):
                try: v = float(v) if "." in v and v.replace(".", "").isdigit() else (int(v) if v.isdigit() else v)
                except Exception: pass
                c = ws.cell(r, i, v if v != "" else None); c.font = Font(name=F, italic=True, color="6B6F68")
            for i, f in calc.items():
                a, bb = CL(f[1] + 1), CL(f[2] + 1)
                if f[0] == "sub": ws.cell(r, i + 1, "=%s%d-%s%d" % (a, r, bb, r))
                elif f[0] == "mul": ws.cell(r, i + 1, "=%s%d*%s%d" % (a, r, bb, r))
                else: ws.cell(r, i + 1, "=%s%d-%s%d" % (a, r, bb, r))
                ws.cell(r, i + 1).font = Font(name=F, italic=True, color="6B6F68"); ws.cell(r, i + 1).number_format = NUM
            r += 1
        first = r
        for k in range(n):
            for i in range(1, len(cols) + 1):
                c = ws.cell(r, i); c.fill = INPUT; c.border = BOX; c.font = Font(name=F)
                if i - 1 in o.get("num", []): c.number_format = NUM
            if pre and k < len(pre): ws.cell(r, 1, pre[k])
            for i, f in calc.items():
                a, bb = CL(f[1] + 1), CL(f[2] + 1)
                if f[0] == "sub": fm = "=%s%d-%s%d" % (a, r, bb, r)
                elif f[0] == "mul": fm = "=%s%d*%s%d" % (a, r, bb, r)
                else: fm = ("=%s%d-%s%d" % (a, r, bb, r)) if k == 0 else "=%s%d+%s%d-%s%d" % (CL(i + 1), r - 1, a, r, bb, r)
                c = ws.cell(r, i + 1, fm); c.number_format = NUM; c.font = Font(name=F)
            r += 1
        tcols = sorted(set(o.get("num", [])) | set(k for k, f in calc.items() if f[0] != "cum"))
        if tcols:
            ws.cell(r, 1, "Total").font = Font(name=F, bold=True)
            for i in tcols:
                c = ws.cell(r, i + 1, "=SUM(%s%d:%s%d)" % (CL(i + 1), first, CL(i + 1), r - 1)); c.font = Font(name=F, bold=True); c.number_format = NUM
            if "mul" in [f[0] for f in calc.values()]: last_total = "%s%d" % (CL(max(calc) + 1), r)
            r += 1
        r += 1
    ws.column_dimensions["A"].width = 30
    for i in range(2, 9): ws.column_dimensions[CL(i)].width = 16
    wb.save(path)


# ======================= BUILD ALL =======================
def build_files(root):
    for d in ("pdf", "docx", "xlsx"): os.makedirs(f"{root}/downloads/{d}", exist_ok=True)
    os.makedirs(f"{root}/assets/images", exist_ok=True)
    for t in TEMPLATES:
        s = t["slug"]
        make_pdf(t, f"{root}/downloads/pdf/{s}.pdf", A4)
        make_pdf(t, f"{root}/downloads/pdf/{s}-us-letter.pdf", letter)
        make_docx(t, f"{root}/downloads/docx/{s}-editable.docx") if "docx" in t["fmts"] else None
        make_xlsx(t, f"{root}/downloads/xlsx/{s}-editable.xlsx") if "xlsx" in t["fmts"] else None
        img = f"{root}/assets/images/{s}"
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=78", "-r", "85", "-singlefile", f"{root}/downloads/pdf/{s}.pdf", img + "-preview"], check=True)
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=72", "-r", "45", "-singlefile", f"{root}/downloads/pdf/{s}.pdf", img + "-thumb"], check=True)
