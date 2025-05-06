"""
Frame for splitting a PDF file by extracting specific pages.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import re
from typing import List, Tuple, Union

from core.pdf_splitter import PDFSplitter
from pypdf import PdfReader


class SplitFrame(ttk.Frame):
    """Frame for the Split PDF functionality."""

    def __init__(self, parent):
        """
        Initialize the Split PDF frame.

        Args:
            parent: The parent widget
        """
        super().__init__(parent, padding=10)
        self.parent = parent
        self.input_file = None
        self.total_pages = 0
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Input file selection
        input_frame = ttk.LabelFrame(self, text="Input PDF")
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50)
        input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_button = ttk.Button(input_frame, text="Browse", command=self._browse_input)
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Page selection
        pages_frame = ttk.LabelFrame(self, text="Page Selection")
        pages_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        pages_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(pages_frame, text="Pages:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.pages_var = tk.StringVar()
        pages_entry = ttk.Entry(pages_frame, textvariable=self.pages_var)
        pages_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        hint_label = ttk.Label(
            pages_frame, 
            text="Format: 1,3,5-7 (page numbers start from 1)",
            font=("", 8, "italic")
        )
        hint_label.grid(row=1, column=1, padx=5, sticky="w")
        
        # Page info
        self.page_info_var = tk.StringVar()
        self.page_info_var.set("Total pages: 0")
        page_info_label = ttk.Label(pages_frame, textvariable=self.page_info_var)
        page_info_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Output file selection
        output_frame = ttk.LabelFrame(self, text="Output PDF")
        output_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        output_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Save to:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_output_button = ttk.Button(output_frame, text="Browse", command=self._browse_output)
        browse_output_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Split button
        split_button = ttk.Button(self, text="Split PDF", command=self._split_pdf)
        split_button.grid(row=3, column=0, pady=10)
    
    def _browse_input(self):
        """Browse for input PDF file."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.input_var.set(file_path)
            self.input_file = file_path
            self._update_page_info()
            
            # Set default output filename
            if not self.output_var.get():
                dirname = os.path.dirname(file_path)
                basename = os.path.splitext(os.path.basename(file_path))[0]
                self.output_var.set(os.path.join(dirname, f"{basename}_split.pdf"))
    
    def _browse_output(self):
        """Browse for output file location."""
        file_path = filedialog.asksaveasfilename(
            title="Save Split PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_var.set(file_path)
    
    def _update_page_info(self):
        """Update the page count information for the loaded PDF."""
        if not self.input_file:
            self.page_info_var.set("Total pages: 0")
            self.total_pages = 0
            return
        
        try:
            with open(self.input_file, 'rb') as f:
                reader = PdfReader(f)
                self.total_pages = len(reader.pages)
                self.page_info_var.set(f"Total pages: {self.total_pages}")
        except Exception as e:
            self.page_info_var.set("Error reading PDF")
            self.total_pages = 0
            print(f"Error reading PDF: {str(e)}")
    
    def _parse_page_ranges(self, page_range_str: str) -> List[Union[int, Tuple[int, int]]]:
        """
        Parse page range string into a list of page numbers and ranges.

        Args:
            page_range_str: String containing page ranges (e.g., "1,3,5-7")

        Returns:
            List of page indices (0-indexed) and tuples representing ranges
        """
        if not page_range_str.strip():
            return []
        
        page_ranges = []
        
        # Split by comma
        parts = page_range_str.split(',')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check if it's a range (contains '-')
            if '-' in part:
                try:
                    start, end = part.split('-')
                    # Convert from 1-indexed (user input) to 0-indexed (internal)
                    start_idx = int(start.strip()) - 1
                    end_idx = int(end.strip()) - 1
                    
                    if start_idx < 0 or end_idx >= self.total_pages or start_idx > end_idx:
                        messagebox.showwarning(
                            "Invalid Range", 
                            f"Page range {part} is out of bounds (1-{self.total_pages})."
                        )
                        return []
                    
                    page_ranges.append((start_idx, end_idx))
                except ValueError:
                    messagebox.showwarning("Invalid Format", f"Invalid page range format: {part}")
                    return []
            else:
                # Single page
                try:
                    # Convert from 1-indexed (user input) to 0-indexed (internal)
                    page_idx = int(part) - 1
                    
                    if page_idx < 0 or page_idx >= self.total_pages:
                        messagebox.showwarning(
                            "Invalid Page", 
                            f"Page {part} is out of bounds (1-{self.total_pages})."
                        )
                        return []
                    
                    page_ranges.append(page_idx)
                except ValueError:
                    messagebox.showwarning("Invalid Format", f"Invalid page number: {part}")
                    return []
        
        return page_ranges
    
    def _split_pdf(self):
        """Split the PDF based on the selected pages."""
        input_path = self.input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an input PDF file.")
            return
        
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file.")
            return
        
        page_ranges_str = self.pages_var.get()
        if not page_ranges_str:
            messagebox.showwarning("No Pages", "Please specify pages to extract.")
            return
        
        # Parse page ranges
        page_ranges = self._parse_page_ranges(page_ranges_str)
        if not page_ranges:
            return
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Splitting PDF...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            result = PDFSplitter.split_pdf(input_path, output_path, page_ranges)
            
            if result:
                try:
                    app.set_status("PDF split successfully.")
                except (AttributeError, NameError):
                    pass
                messagebox.showinfo("Success", f"PDF split successfully to:\n{output_path}")
            else:
                try:
                    app.set_status("Failed to split PDF.")
                except (AttributeError, NameError):
                    pass
                messagebox.showerror("Error", "Failed to split PDF. Check the console for details.")
        except Exception as e:
            try:
                app.set_status("Error splitting PDF.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while splitting PDF:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass 