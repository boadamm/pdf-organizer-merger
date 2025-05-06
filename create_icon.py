"""
Script to generate a simple PDF icon for the application.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(output_path, size=(256, 256)):
    """Create a simple PDF icon."""
    # Create a new image with a white background
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a document shape
    document_color = (220, 53, 69)  # Red color
    margin = size[0] // 10
    doc_width = size[0] - 2 * margin
    doc_height = size[1] - 2 * margin
    
    # Draw document background
    draw.rectangle(
        [(margin, margin), (margin + doc_width, margin + doc_height)],
        fill=document_color
    )
    
    # Draw a folded corner
    fold_size = size[0] // 5
    fold_points = [
        (margin + doc_width - fold_size, margin),
        (margin + doc_width, margin + fold_size),
        (margin + doc_width, margin),
    ]
    draw.polygon(fold_points, fill=(180, 30, 45))
    
    # Draw PDF text
    try:
        # Try to use a font if available
        font_size = size[0] // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fall back to default font
        font_size = size[0] // 4
        font = ImageFont.load_default()
    
    text = "PDF"
    # Get text dimensions using the font object instead of ImageDraw
    # This is compatible with newer Pillow versions
    try:
        text_width, text_height = font.getsize(text)
    except AttributeError:
        # For even newer Pillow versions that don't have getsize
        bbox = font.getbbox(text)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    text_x = margin + (doc_width - text_width) // 2
    text_y = margin + (doc_height - text_height) // 2
    
    draw.text((text_x, text_y), text, fill="white", font=font)
    
    # Save the image
    img.save(output_path, "PNG")
    print(f"Icon created at {output_path}")

if __name__ == "__main__":
    assets_path = os.path.join("assets")
    icon_path = os.path.join(assets_path, "icon.png")
    
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)
    
    create_icon(icon_path) 