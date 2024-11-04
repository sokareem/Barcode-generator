# Barcode-generator
Generates barcode from a CSV file containing Product name, Price and SKU

# Barcode Generator and PDF Creator

This project provides two Python scripts to generate barcodes from a CSV file and compile them into a PDF:

	1.	barcode_generator.py: Generates barcode images from product information in a CSV file.
	2.	create_barcode_pdf.py: Creates a PDF containing the generated barcode images with labels.

Table of Contents

	•	Prerequisites
	•	Installation
	•	Usage
	•	1. Prepare the CSV File
	•	2. Generate Barcodes
	•	3. Create the Barcode PDF
	•	Customization
	•	Troubleshooting
	•	Contributing
	•	License

Prerequisites

	•	Python: Version 3.6 or higher
	•	pip: Python package installer

Installation

	1.	Clone or Download the Repository
If you have not already, clone the repository or download the script files into a directory on your machine.
	2.	Navigate to the Project Directory
Open your terminal or command prompt and navigate to the directory containing the scripts.
	3.	Create a Virtual Environment (Optional but Recommended)

python -m venv venv

Activate the virtual environment:
	•	On Windows:

venv\Scripts\activate


	•	On macOS/Linux:

source venv/bin/activate


	4.	Install Required Python Packages
Install the necessary packages using pip:

pip install pandas python-barcode pillow reportlab

Alternatively, if a requirements.txt file is provided:

pip install -r requirements.txt



Usage

1. Prepare the CSV File

Ensure you have a CSV file containing the following columns:

	•	SKU: The SKU code for the product (used for barcode generation).
	•	Item Name: The name of the product.
	•	Token: A unique identifier (not used in barcode generation but required by the script).
	•	Price: The price of the product.

Example CSV (products.csv):

SKU,Item Name,Token,Price
123456789012,Organic Honey,token123,19.99
987654321098,African Coffee,token456,29.99

Place this CSV file in the same directory as the Python scripts.

2. Generate Barcodes

Run the barcode_generator.py script to generate barcode images:

python barcode_generator.py

What the Script Does:

	•	Reads the CSV file Mama Africas Inventory - Items.csv.
	•	Validates the presence of required columns.
	•	Generates Code128 barcodes using the SKU values.
	•	Saves barcode images in the barcodes directory with filenames based on the product name and price.

Customizing the CSV Filename:

If your CSV file has a different name, modify the last line in barcode_generator.py:

result = generate_barcodes_from_csv('your_csv_file.csv')

3. Create the Barcode PDF

Run the create_barcode_pdf.py script to compile the barcodes into a PDF:

python create_barcode_pdf.py

What the Script Does:

	•	Reads barcode images from the barcodes directory.
	•	Formats labels by sanitizing filenames and formatting prices.
	•	Arranges images and labels on an A4-sized PDF.
	•	Saves the PDF as optimized_barcodes.pdf in the current directory.

Customizing the Output PDF Filename:

To change the output PDF filename, modify the function call at the end of create_barcode_pdf.py:

create_barcode_pdf(output_pdf='your_output_filename.pdf')

Customization

Adjusting Image Sizes

You can adjust the size of the barcode images in the PDF by modifying the image_width and image_height parameters:

create_barcode_pdf(image_width=2*inch, image_height=1*inch)

Changing Page Size

To change the page size (e.g., to Letter size), modify the pagesize parameter when initializing the canvas:

from reportlab.lib.pagesizes import letter

c = canvas.Canvas(output_pdf, pagesize=letter)

Font Settings

Adjust the min_font_size and max_font_size in create_barcode_pdf.py to change the label font sizes:

min_font_size = 6
max_font_size = 10

Troubleshooting

	•	Missing Dependencies
Ensure all required packages are installed. Re-run the installation commands if necessary.
	•	CSV File Errors
	•	Verify the CSV file is correctly formatted and contains all required columns.
	•	Ensure there are no typos in the column headers.
	•	Barcode Generation Issues
	•	Check that the SKU values are valid and properly formatted.
	•	Ensure the barcode package supports the barcode type you are generating.
	•	PDF Creation Issues
	•	Confirm that the barcodes directory contains the generated PNG files.
	•	Check for any error messages when running the scripts.
	•	Font or Encoding Errors
	•	If you encounter encoding issues, ensure your text data is UTF-8 encoded.
	•	Install any missing fonts or adjust font settings in the script.

Contributing

Contributions are welcome! Please follow these steps:

	1.	Fork the Repository
	2.	Create a New Branch

git checkout -b feature/your-feature-name


	3.	Commit Your Changes

git commit -am 'Add a feature'


	4.	Push to the Branch

git push origin feature/your-feature-name


	5.	Open a Pull Request

License

This project is licensed under the MIT License. See the LICENSE file for details.

Happy coding!
