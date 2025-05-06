"""
Unit tests for the PDF merger module.
"""
import os
import pytest
from pathlib import Path

from src.core.pdf_merger import PDFMerger
from pypdf import PdfReader


class TestPDFMerger:
    """Test cases for the PDFMerger class."""

    def test_merge_pdfs_empty_list(self, tmp_path):
        """Test merging with an empty list of PDFs."""
        output_path = tmp_path / "output.pdf"
        result = PDFMerger.merge_pdfs([], output_path)
        
        assert result is False
        assert not output_path.exists()
    
    def test_merge_pdfs(self, tmp_path, monkeypatch):
        """Test merging PDFs successfully."""
        # Mock the PdfMerger class
        class MockPdfMerger:
            def __init__(self):
                self.files = []
            
            def append(self, file_path):
                self.files.append(file_path)
            
            def write(self, output_file):
                pass
            
            def close(self):
                pass
        
        # Mock the open function
        class MockFile:
            def __init__(self, path, mode):
                self.path = path
                self.mode = mode
            
            def __enter__(self):
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
        
        # Create test files
        input_files = [tmp_path / f"input{i}.pdf" for i in range(3)]
        for file_path in input_files:
            file_path.touch()
        
        output_path = tmp_path / "output.pdf"
        
        # Apply mocks
        mock_merger = MockPdfMerger()
        
        def mock_pdf_merger():
            return mock_merger
        
        def mock_open(path, mode):
            return MockFile(path, mode)
        
        monkeypatch.setattr("pypdf.PdfMerger", mock_pdf_merger)
        monkeypatch.setattr("builtins.open", mock_open)
        
        # Test the merge function
        result = PDFMerger.merge_pdfs(input_files, output_path)
        
        assert result is True
        assert len(mock_merger.files) == 3
        assert mock_merger.files == [str(file) for file in input_files]
    
    def test_merge_pdfs_exception(self, tmp_path, monkeypatch):
        """Test merging PDFs with an exception."""
        # Create test files
        input_files = [tmp_path / f"input{i}.pdf" for i in range(3)]
        for file_path in input_files:
            file_path.touch()
        
        output_path = tmp_path / "output.pdf"
        
        # Mock the PdfMerger to raise an exception
        def mock_pdf_merger():
            raise Exception("Test exception")
        
        monkeypatch.setattr("pypdf.PdfMerger", mock_pdf_merger)
        
        # Test the merge function
        result = PDFMerger.merge_pdfs(input_files, output_path)
        
        assert result is False 