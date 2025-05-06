"""
PDF Splitter module for extracting specific pages or page ranges from PDF files.
"""
from pathlib import Path
from typing import List, Union, Tuple

from pypdf import PdfReader, PdfWriter


class PDFSplitter:
    """Class to handle splitting PDF files into smaller documents."""

    @staticmethod
    def split_pdf(input_path: Union[str, Path], output_path: Union[str, Path], 
                  page_ranges: List[Union[int, Tuple[int, int]]]) -> bool:
        """
        Extract specified pages from a PDF file and save as a new PDF.

        Args:
            input_path: Path to the PDF file to split
            output_path: Path where the split PDF will be saved
            page_ranges: List of page numbers or ranges to extract
                         Single page: 0 (first page)
                         Page range: (0, 3) (pages 1-4, inclusive)
                         Note: Page numbers are 0-indexed

        Returns:
            bool: True if the split was successful, False otherwise
        """
        if not page_ranges:
            return False

        try:
            reader = PdfReader(str(input_path))
            writer = PdfWriter()
            
            # Process each page range
            for page_range in page_ranges:
                if isinstance(page_range, int):
                    # Extract a single page
                    if 0 <= page_range < len(reader.pages):
                        writer.add_page(reader.pages[page_range])
                elif isinstance(page_range, tuple) and len(page_range) == 2:
                    # Extract a range of pages
                    start, end = page_range
                    if 0 <= start <= end < len(reader.pages):
                        for i in range(start, end + 1):
                            writer.add_page(reader.pages[i])
            
            # Write the split PDF to the output path
            with open(str(output_path), 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Error splitting PDF: {str(e)}")
            return False 