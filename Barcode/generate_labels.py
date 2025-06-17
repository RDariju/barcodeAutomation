from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import date
import os

def generate_serial(year, week, index):
    return f"{year:02d}{week:02d}{index:04d}"

def generate_barcode(serial, path):
    barcode = Code128(serial, writer=ImageWriter())
    filename = os.path.join(path, serial)
    return barcode.save(filename)  # returns '.../serial.png'

def create_final_label_pdf(start=40, end=119,
                           bg_image="bg_new.png",
                           output_pdf="final_labels.pdf"):
    # Prepare
    bg = ImageReader(bg_image)
    c = canvas.Canvas(output_pdf, pagesize=A4)
    page_w, page_h = A4
    codes = os.makedirs("barcodes", exist_ok=True) or \
            [generate_serial(0, 0, i) for i in []]

    today = date.today()
    year, week = today.year % 100, today.isocalendar()[1]
    serials = [generate_serial(year, week, i) for i in range(start, end + 1)]

    # Layout: 2 cols x 4 rows per page
    cols, rows = 4, 10
    lw, lh = 50 * mm, 24 * mm
    mx, my = 5 * mm, 10 * mm
    sx, sy = lw + 0.5 * mm, lh + 0.5 * mm

    for idx, serial in enumerate(serials):
        if idx and idx % (cols * rows) == 0:
            c.showPage()

        col = idx % cols
        row = (idx // cols) % rows
        x = mx + col * sx
        y = page_h - my - (row + 1) * sy

        # Draw your label template
        c.drawImage(bg, x, y, width=lw, height=lh)

        # Generate & place barcode
        bar = generate_barcode(serial, "barcodes")
        c.drawImage(bar, x +8 * mm, y + 8 * mm, width=15 * mm, height=8 * mm, preserveAspectRatio=False, mask='auto')

    c.save()
    print(f"✅ Created: {output_pdf}")

    # Optional: cleanup barcodes
    for f in os.listdir("barcodes"):
        os.remove(os.path.join("barcodes", f))
    os.rmdir("barcodes")

# Run
create_final_label_pdf()
