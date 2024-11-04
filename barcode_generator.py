import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import re

def sanitize_filename(filename):
    # Replace any character that is not alphanumeric or underscore with an underscore
    return re.sub(r'[^\w\-_\.]', '_', filename)

def generate_barcodes_from_csv(csv_path, output_dir='barcodes'):
    # Load CSV file
    data = pd.read_csv(csv_path)
    print("Columns= ", data.columns)
    
    # Check if required columns are in CSV
    required_columns = {'SKU', 'Item Name', 'Token', 'Price'}
    if not required_columns.issubset(data.columns):
        missing_cols = required_columns - set(data.columns)
        return f"Missing columns in CSV: {', '.join(missing_cols)}"
    
    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over each row and generate a barcode
    for index, row in data.iterrows():
        sku = row['SKU']
        product_name = row['Item Name']
        product_id = row['Token']
        price = row['Price']
        
        # Sanitize filename by removing invalid characters
        filename = f"{output_dir}/{sanitize_filename(product_name)}-{sanitize_filename(price)}"
        
        # Generate barcode with SKU and save as PNG
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(sku, writer=ImageWriter())
        barcode_instance.save(filename)

    return f"Barcodes generated and saved in '{output_dir}' directory."

# Usage example (after placing CSV file in the same directory)
result = generate_barcodes_from_csv('Mama Africas Inventory - Items.csv')
print(result)