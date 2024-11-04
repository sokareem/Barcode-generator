import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import re
import textwrap

def sanitize_label(label):
    # Replace underscores with spaces
    label = label.replace('_', ' ')
    
    # Use regex to find price at the end of the string
    match = re.search(r'(-?\d+\.\d{2})$', label)
    if match:
        price = match.group(0)
        # Convert price to float to remove any negative sign or extra hyphens
        formatted_price = f"$ {abs(float(price)):,.2f}"
        # Remove price from the label for further formatting
        label = label[:match.start()].strip()
    else:
        # If no price found, set formatted price as an empty string
        formatted_price = ""
    
    # Capitalize each word and join the text with formatted price
    sanitized_label = ' '.join([word.capitalize() for word in label.split()])
    
    # Append formatted price with a colon
    if formatted_price:
        sanitized_label += f": {formatted_price}"
    
    return sanitized_label

def wrap_text(text, max_width, font_name, font_size, canvas_obj):
    """Helper function to wrap text within a specified width."""
    wrapped_text = []
    words = text.split()
    line = ""
    for word in words:
        # Try adding the next word to the line
        test_line = f"{line} {word}".strip()
        # Check the width of the line
        text_width = canvas_obj.stringWidth(test_line, font_name, font_size)
        if text_width <= max_width:
            line = test_line
        else:
            # If adding the word exceeds max width, add the line and start a new one
            wrapped_text.append(line)
            line = word
    # Add any remaining text in the last line
    if line:
        wrapped_text.append(line)
    
    return wrapped_text

def create_barcode_pdf(input_dir='barcodes', output_pdf='optimized_barcodes.pdf', image_width=2*inch, image_height=1*inch):
    # Initialize PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    page_width, page_height = A4
    margin = 0.5 * inch
    min_font_size = 6  # Minimum font size to keep text readable
    max_font_size = 10  # Starting font size

    # Calculate number of images that can fit in a row and column based on specified dimensions
    images_per_row = int((page_width - 2 * margin) // image_width)
    images_per_column = int((page_height - 2 * margin) // (image_height + 0.4 * inch))  # Adding extra space for labels

    # Get list of image files in the input directory
    image_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.png')])
    
    x_position = margin  # Starting x position for the first image
    y_position = page_height - margin - image_height  # Starting y position for the first image

    for index, image_file in enumerate(image_files):
        # Full path to the image
        image_path = os.path.join(input_dir, image_file)
        
        # Load image filename (without extension) for labeling
        image_label = sanitize_label(os.path.splitext(image_file)[0])

        # Define max width for text wrapping
        max_text_width = image_width

        # Dynamically adjust font size and wrap text
        font_size = max_font_size
        wrapped_text = wrap_text(image_label, max_text_width, "Helvetica", font_size, c)
        
        # If font size is too large for wrapping, reduce it
        while len(wrapped_text) > 2 and font_size > min_font_size:  # Limit to max 2 lines
            font_size -= 1
            wrapped_text = wrap_text(image_label, max_text_width, "Helvetica", font_size, c)

        # Draw image on PDF
        c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height)
        
        # Draw wrapped text below the image
        c.setFont("Helvetica", font_size)
        for line_index, line in enumerate(wrapped_text[:2]):  # Draw only up to 2 lines
            label_x_position = x_position + (image_width - c.stringWidth(line, "Helvetica", font_size)) / 2
            label_y_position = y_position - (font_size + 5) * (line_index + 1)
            c.drawString(label_x_position, label_y_position, line)

        # Update x_position for the next image in the row
        x_position += image_width + 0.2 * inch  # Add some space between images
        
        # If we reach the end of the row, reset x_position and move down to the next row
        if (index + 1) % images_per_row == 0:
            x_position = margin
            y_position -= (image_height + 0.5 * inch)  # Move down by image height + space for label and margin
            
            # If y_position goes too low, start a new page
            if y_position < margin + image_height:
                c.showPage()
                y_position = page_height - margin - image_height  # Reset y_position for new page

    # Save the PDF
    c.save()
    print(f"PDF created successfully: {output_pdf}")

# Usage example
create_barcode_pdf()