"""
Script to convert PNG icon to ICO format for Windows executables.
"""
from PIL import Image
import os

def png_to_ico(png_path, ico_path):
    """Convert PNG to ICO format"""
    try:
        # Open PNG and convert to ICO
        img = Image.open(png_path)
        img.save(ico_path, format="ICO")
        print(f"ICO file created at {ico_path}")
        return True
    except Exception as e:
        print(f"Error converting PNG to ICO: {str(e)}")
        return False

if __name__ == "__main__":
    # Paths
    assets_path = os.path.join("assets")
    png_path = os.path.join(assets_path, "icon.png")
    ico_path = os.path.join(assets_path, "icon.ico")
    
    # Check if PNG exists
    if not os.path.exists(png_path):
        print(f"Error: PNG icon not found at {png_path}")
    else:
        # Convert to ICO
        if png_to_ico(png_path, ico_path):
            print("Conversion successful!")
        else:
            print("Conversion failed.") 