"""
PDF Page Reorganizer module for rearranging pages in PDF files.
"""
from pathlib import Path
from typing import Union, List

from pypdf import PdfReader, PdfWriter


class PageReorganizer:
    """Class to handle reorganization of pages within PDF files."""

    @staticmethod
    def reorganize_pages(input_path: Union[str, Path], 
                         output_path: Union[str, Path],
                         new_page_order: List[int]) -> bool:
        """
        Rearrange pages in a PDF file based on the specified order.

        Args:
            input_path: Path to the PDF file to reorganize
            output_path: Path where the reorganized PDF will be saved
            new_page_order: List of page numbers in the desired order (0-indexed)
                           Example: [2, 0, 1] - places the third page first,
                           followed by the first and second pages

        Returns:
            bool: True if the reorganization was successful, False otherwise
        """
        if not new_page_order:
            return False

        try:
            reader = PdfReader(str(input_path))
            writer = PdfWriter()
            
            # Check if all requested pages are within bounds
            if any(page_num < 0 or page_num >= len(reader.pages) for page_num in new_page_order):
                return False
            
            # Add pages in the specified order
            for page_num in new_page_order:
                writer.add_page(reader.pages[page_num])
            
            # Write the reorganized PDF to the output path
            with open(str(output_path), 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Error reorganizing PDF pages: {str(e)}")
            return False 