"""
Thumbnail generator for creating image previews of PDF pages.
"""
from pathlib import Path
from typing import Union, List, Tuple, Optional
import io

from PIL import Image
import pdfplumber


class ThumbnailGenerator:
    """Class to handle generation of thumbnail images from PDF pages."""

    @staticmethod
    def generate_thumbnail(input_path: Union[str, Path], 
                          page_number: int,
                          size: Tuple[int, int] = (200, 200)) -> Optional[Image.Image]:
        """
        Generate a thumbnail image for a specific page of a PDF file.

        Args:
            input_path: Path to the PDF file
            page_number: Page number to generate thumbnail for (0-indexed)
            size: Tuple of (width, height) for the thumbnail size

        Returns:
            PIL.Image or None: Thumbnail image or None if generation failed
        """
        try:
            with pdfplumber.open(str(input_path)) as pdf:
                if 0 <= page_number < len(pdf.pages):
                    page = pdf.pages[page_number]
                    
                    # Convert the page to an image
                    img = page.to_image()
                    pil_img = img.original
                    
                    # Resize the image to the requested size while maintaining aspect ratio
                    pil_img.thumbnail(size, Image.LANCZOS)
                    
                    return pil_img
                return None
        except Exception as e:
            print(f"Error generating thumbnail: {str(e)}")
            return None

    @staticmethod
    def generate_thumbnails(input_path: Union[str, Path], 
                           page_numbers: Optional[List[int]] = None,
                           size: Tuple[int, int] = (200, 200)) -> List[Image.Image]:
        """
        Generate thumbnail images for multiple pages of a PDF file.

        Args:
            input_path: Path to the PDF file
            page_numbers: List of page numbers to generate thumbnails for (0-indexed)
                          If None, generate thumbnails for all pages
            size: Tuple of (width, height) for the thumbnail size

        Returns:
            List[PIL.Image]: List of thumbnail images
        """
        thumbnails = []
        
        try:
            with pdfplumber.open(str(input_path)) as pdf:
                # If no page numbers provided, generate thumbnails for all pages
                if page_numbers is None:
                    page_numbers = list(range(len(pdf.pages)))
                
                # Generate thumbnail for each page
                for page_num in page_numbers:
                    if 0 <= page_num < len(pdf.pages):
                        thumbnail = ThumbnailGenerator.generate_thumbnail(
                            input_path, page_num, size
                        )
                        if thumbnail:
                            thumbnails.append(thumbnail)
            
            return thumbnails
        except Exception as e:
            print(f"Error generating thumbnails: {str(e)}")
            return thumbnails
            
    @staticmethod
    def save_thumbnail(image: Image.Image, 
                      output_path: Union[str, Path], 
                      format: str = "PNG") -> bool:
        """
        Save a thumbnail image to disk.

        Args:
            image: PIL Image object to save
            output_path: Path where the image will be saved
            format: Image format (e.g., "PNG", "JPEG")

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            image.save(str(output_path), format=format)
            return True
        except Exception as e:
            print(f"Error saving thumbnail: {str(e)}")
            return False 