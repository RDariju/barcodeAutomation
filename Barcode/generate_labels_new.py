from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import date
import os
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm


def generate_serial(year, week, index):
    return f"{year:02d}{week:02d}{index:04d}"

def generate_barcode(serial, path):
    barcode = Code128(serial, writer=ImageWriter())
    filename = os.path.join(path, serial)
    barcode.save(filename, {
        'module_height': 10.0,
        'font_size': 8,         # Small readable font
        'quiet_zone': 1
    })
    return filename + '.png'

def draw_label(c, x, y, serial, barcode_path):
    label_width = 60 * mm
    label_height = 30 * mm
    corner_radius = 5 * mm

    # Draw label border
    c.roundRect(x, y, label_width, label_height, corner_radius, stroke=1, fill=0)

    # === 1. Label Title ===
    title = "GSM Siren"
    c.setFont("Helvetica-Bold", 10)
    text_width = c.stringWidth(title, "Helvetica-Bold", 10)
    title_x = x + (label_width - text_width) / 2
    title_y = y + label_height - 8
    c.drawString(title_x, title_y, title)

    # Underline title
    c.setLineWidth(0.5)
    c.line(title_x, title_y - 2, title_x + text_width, title_y - 2)

    # === 2. Barcode ===
    barcode_width = 60 * mm
    barcode_height = 12 * mm
    barcode_x = x + (label_width - barcode_width) / 2
    barcode_y = y + label_height / 2-4
    c.drawImage(barcode_path, barcode_x, barcode_y, barcode_width, barcode_height, preserveAspectRatio=True)

    # === 4. Icons ===
    try:
        indoor_use_icon = ImageReader("indoor_use.png")
        voltage_icon = ImageReader("230v.png")
        trashCan_icon = ImageReader("trashcan.png")

        icon_size = 6 * mm
        icon_y = y + 20

        c.drawImage(indoor_use_icon, x + 50, icon_y, width=icon_size, height=icon_size, mask='auto')
        c.drawImage(voltage_icon, x + label_width - icon_size - 60, icon_y, width=icon_size, height=icon_size, mask='auto')
        c.drawImage(trashCan_icon, x + label_width - icon_size - 80, icon_y, width=icon_size, height=icon_size, mask='auto')

    except:
        pass  # Skip if icons aren't found

    # === 5. Warning Text ===
    caution_text_1 = "1) Unplug from mains before opening the device."
    caution_text_2 = "2) Unplug battery before removing/inserting SIM card"

    c.setFont("Helvetica", 6)
    c.drawString(x + 5, y + 14, caution_text_1)
    c.drawString(x + 5, y + 8, caution_text_2)

def create_labels_pdf(start=40, end=100, output_file="serial_labels_new13.pdf"):
    barcode_folder = "barcodes"
    os.makedirs(barcode_folder, exist_ok=True)

    today = date.today()
    year = today.year % 100
    week = today.isocalendar()[1]

    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4

    margin = 15 * mm
    x_spacing = 90 * mm  # Adjust spacing for 2 columns
    y_spacing = 40 * mm

    label_width = 60 * mm
    label_height = 30 * mm

    labels_per_row = 2  # Changed to 2 columns
    labels_per_col = 6  # 6 rows

    count = 0
    for i in range(start, end + 1):
        serial = generate_serial(year, week, i)
        barcode_path = generate_barcode(serial, barcode_folder)

        col = count % labels_per_row
        row = (count // labels_per_row) % labels_per_col

        x = margin + col * x_spacing
        y = page_height - margin - (row + 1) * y_spacing

        # Ensure labels don't overflow page width or height
        if x + label_width > page_width or y < margin:
            c.showPage()
            count = 0
            col = 0
            row = 0
            x = margin
            y = page_height - margin - y_spacing

        draw_label(c, x, y, serial, barcode_path)
        count += 1

        if count % (labels_per_row * labels_per_col) == 0:
            c.showPage()

    c.save()
    print(f"✅ PDF created: {output_file}")

    for file in os.listdir(barcode_folder):
        os.remove(os.path.join(barcode_folder, file))
    os.rmdir(barcode_folder)

# Run
create_labels_pdf()
