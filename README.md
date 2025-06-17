# 🏷️ Barcode Label Generator for A4 Sheets

This project is a Python-based barcode label generator that creates printable PDF files with custom serial numbers and barcodes. It places each barcode onto a user-provided label design (PNG image) and arranges the labels on A4-sized pages.

---

## 📦 Features

- ✅ Generate **Code128** barcodes with custom serial numbers
- ✅ Insert each barcode into a customizable **background label design**
- ✅ Supports any number of serials (auto pagination over A4 sheets)
- ✅ Adjustable **label size**, number of **columns** and **rows**
- ✅ Automatically cleans up temporary barcode images
- ✅ Outputs a clean, print-ready **PDF**

---

## 📄 Output

Generates a `PDF` (default: `final_labels.pdf`) that contains barcode labels arranged on an A4 sheet. Each label includes a barcode and serial number on your custom background.

---

## 🛠️ Requirements

Before running the script, install the required Python libraries:

```bash
pip install python-barcode reportlab pillow

How It Works
Serial numbers are generated in the format:

nginx
Copy
Edit
YYWWXXXX
YY → Last two digits of the year

WW → ISO week number

XXXX → Serial index (e.g., 0040, 0041...)

Barcodes are generated using python-barcode

Each barcode is temporarily saved and drawn over the label background image (PNG)

Labels are placed in a grid (configurable rows and columns) on each A4 page

Once the PDF is created, all temporary barcode images are deleted

🖼️ Label Template
You can use any PNG image as your label background.

✅ The default image used is bg_new.png.
📌 Ensure your image fits the label dimensions defined in the script.

✏️ Customization
You can modify key settings in the script:

Function Call
python
Copy
Edit
create_final_label_pdf(
    start=40,              # Start serial number (index)
    end=119,               # End serial number (index)
    bg_image="bg_new.png", # Your label background image
    output_pdf="final_labels.pdf" # Output PDF file name
)
Layout & Sizing
Inside the script:

python
Copy
Edit
cols, rows = 4, 10          # Number of columns and rows per A4 page
lw, lh = 50 * mm, 24 * mm   # Width and height of each label
mx, my = 5 * mm, 10 * mm    # Margins from left and top
sx, sy = lw + 0.5 * mm, lh + 0.5 * mm  # Spacing between labels
You can tweak these to fit your label sheet dimensions or sticker layout.

Example Usage
Replace bg_new.png with your own label design (if desired).

Run the script:

bash
Copy
Edit
python label_generator.py
Open final_labels.pdf – it will contain your barcode labels.

    🌟 Support
If you find this project useful, feel free to give it a ⭐ on GitHub!

yaml
Copy
Edit

---

Let me know if you’d like me to also:

- Generate a sample `label_generator.py` to go with it  
- Add GitHub badges (e.g., license, Python version)  
- Include a visual template preview in the `README`

🙌 Author
Created with ❤️ by Ravindu Dariju
