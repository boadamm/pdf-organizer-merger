"""
PDF Text Extractor module for extracting text content from PDF files.
"""
from pathlib import Path
from typing import Union, List, Dict, Optional

import pdfplumber


class TextExtractor:
    """Class to handle extraction of text from PDF files."""

    @staticmethod
    def extract_text_from_pages(input_path: Union[str, Path], 
                               page_numbers: Optional[List[int]] = None) -> Dict[int, str]:
        """
        Extract text content from specified pages of a PDF file.

        Args:
            input_path: Path to the PDF file
            page_numbers: List of page numbers to extract text from (0-indexed)
                          If None, extract text from all pages

        Returns:
            Dict[int, str]: Dictionary mapping page numbers to extracted text
        """
        result = {}
        
        try:
            with pdfplumber.open(str(input_path)) as pdf:
                # If no page numbers provided, extract from all pages
                if page_numbers is None:
                    page_numbers = list(range(len(pdf.pages)))
                
                # Extract text from each specified page
                for page_num in page_numbers:
                    if 0 <= page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        result[page_num] = page.extract_text() or ""
            
            return result
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return result

    @staticmethod
    def extract_all_text(input_path: Union[str, Path]) -> str:
        """
        Extract all text content from a PDF file and return as a single string.

        Args:
            input_path: Path to the PDF file

        Returns:
            str: Extracted text from all pages
        """
        try:
            with pdfplumber.open(str(input_path)) as pdf:
                text = ""
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n\n"
                return text
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return "" 