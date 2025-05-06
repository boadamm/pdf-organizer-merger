"""
PDF Merger module for combining multiple PDF files into a single document.
"""
from pathlib import Path
from typing import List, Union

from pypdf import PdfMerger


class PDFMerger:
    """Class to handle merging of multiple PDF files into a single document."""

    @staticmethod
    def merge_pdfs(input_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> bool:
        """
        Merge multiple PDF files into a single PDF document.

        Args:
            input_paths: List of paths to the PDF files to merge
            output_path: Path where the merged PDF will be saved

        Returns:
            bool: True if the merge was successful, False otherwise
        """
        if not input_paths:
            return False

        try:
            merger = PdfMerger()
            
            # Add each PDF to the merger
            for pdf_path in input_paths:
                merger.append(str(pdf_path))
            
            # Write the merged PDF to the output path
            with open(str(output_path), 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            return True
        except Exception as e:
            print(f"Error merging PDFs: {str(e)}")
            return False 