"""
Unit tests for the PDF splitter module.
"""
import os
import pytest
from pathlib import Path

from src.core.pdf_splitter import PDFSplitter
from pypdf import PdfReader, PdfWriter


class TestPDFSplitter:
    """Test cases for the PDFSplitter class."""

    def test_split_pdf_empty_list(self, tmp_path):
        """Test splitting with an empty list of page ranges."""
        input_path = tmp_path / "input.pdf"
        input_path.touch()  # Create an empty file
        
        output_path = tmp_path / "output.pdf"
        result = PDFSplitter.split_pdf(input_path, output_path, [])
        
        assert result is False
        assert not output_path.exists()
    
    def test_split_pdf(self, tmp_path, monkeypatch):
        """Test splitting PDF successfully."""
        # Mock the PdfReader class
        class MockPdfReader:
            def __init__(self, path):
                self.path = path
                self.pages = [MockPage(i) for i in range(10)]
        
        class MockPage:
            def __init__(self, index):
                self.index = index
        
        # Mock the PdfWriter class
        class MockPdfWriter:
            def __init__(self):
                self.pages = []
            
            def add_page(self, page):
                self.pages.append(page)
            
            def write(self, output_file):
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
        
        # Create test file
        input_path = tmp_path / "input.pdf"
        input_path.touch()
        
        output_path = tmp_path / "output.pdf"
        
        # Apply mocks
        mock_writer = MockPdfWriter()
        
        def mock_pdf_reader(path):
            return MockPdfReader(path)
        
        def mock_pdf_writer():
            return mock_writer
        
        def mock_open(path, mode):
            return MockFile(path, mode)
        
        monkeypatch.setattr("pypdf.PdfReader", mock_pdf_reader)
        monkeypatch.setattr("pypdf.PdfWriter", mock_pdf_writer)
        monkeypatch.setattr("builtins.open", mock_open)
        
        # Test the split function with a mix of single pages and ranges
        page_ranges = [1, 3, (5, 7)]
        result = PDFSplitter.split_pdf(input_path, output_path, page_ranges)
        
        assert result is True
        assert len(mock_writer.pages) == 5  # Pages 1, 3, 5, 6, 7
        assert mock_writer.pages[0].index == 1
        assert mock_writer.pages[1].index == 3
        assert mock_writer.pages[2].index == 5
        assert mock_writer.pages[3].index == 6
        assert mock_writer.pages[4].index == 7
    
    def test_split_pdf_exception(self, tmp_path, monkeypatch):
        """Test splitting PDF with an exception."""
        # Create test file
        input_path = tmp_path / "input.pdf"
        input_path.touch()
        
        output_path = tmp_path / "output.pdf"
        
        # Mock the PdfReader to raise an exception
        def mock_pdf_reader(path):
            raise Exception("Test exception")
        
        monkeypatch.setattr("pypdf.PdfReader", mock_pdf_reader)
        
        # Test the split function
        result = PDFSplitter.split_pdf(input_path, output_path, [1, 2, 3])
        
        assert result is False 