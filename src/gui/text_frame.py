"""
Frame for extracting text from PDF files.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
from typing import List, Dict

from core.text_extractor import TextExtractor
from pypdf import PdfReader


class TextFrame(ttk.Frame):
    """Frame for the Extract Text functionality."""

    def __init__(self, parent):
        """
        Initialize the Extract Text frame.

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
        
        ttk.Label(
            pages_frame, 
            text="Format: 1,3,5-7 (leave empty for all pages)",
            font=("", 8, "italic")
        ).grid(row=1, column=1, padx=5, sticky="w")
        
        # Page info
        self.page_info_var = tk.StringVar()
        self.page_info_var.set("Total pages: 0")
        page_info_label = ttk.Label(pages_frame, textvariable=self.page_info_var)
        page_info_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Action buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        extract_button = ttk.Button(button_frame, text="Extract Text", command=self._extract_text)
        extract_button.pack(side=tk.LEFT, padx=5)
        
        save_button = ttk.Button(button_frame, text="Save to File", command=self._save_text)
        save_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_text)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Text display area
        text_frame = ttk.LabelFrame(self, text="Extracted Text")
        text_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=80, height=20)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
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
    
    def _parse_page_ranges(self, page_range_str: str) -> List[int]:
        """
        Parse page range string into a list of page numbers.

        Args:
            page_range_str: String containing page ranges (e.g., "1,3,5-7")

        Returns:
            List of page indices (0-indexed)
        """
        if not page_range_str.strip():
            return None  # Empty string means all pages
        
        page_indices = []
        
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
                    
                    page_indices.extend(range(start_idx, end_idx + 1))
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
                    
                    page_indices.append(page_idx)
                except ValueError:
                    messagebox.showwarning("Invalid Format", f"Invalid page number: {part}")
                    return []
        
        return page_indices
    
    def _extract_text(self):
        """Extract text from the PDF based on the selected pages."""
        input_path = self.input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an input PDF file.")
            return
        
        # Parse page ranges
        page_ranges_str = self.pages_var.get()
        page_indices = self._parse_page_ranges(page_ranges_str)
        # Empty list means there was an error, None means all pages
        if page_indices == []:
            return
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Extracting text...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            # Clear the text area
            self.text_area.delete(1.0, tk.END)
            
            if page_indices is None:
                # Extract all text
                text = TextExtractor.extract_all_text(input_path)
                self.text_area.insert(tk.END, text)
            else:
                # Extract text from specified pages
                text_dict = TextExtractor.extract_text_from_pages(input_path, page_indices)
                
                # Display the extracted text
                for page_num in sorted(text_dict.keys()):
                    # Convert back to 1-indexed for display
                    self.text_area.insert(tk.END, f"Page {page_num + 1}:\n")
                    self.text_area.insert(tk.END, text_dict[page_num])
                    self.text_area.insert(tk.END, "\n\n")
            
            try:
                app.set_status("Text extracted successfully.")
            except (AttributeError, NameError):
                pass
        except Exception as e:
            try:
                app.set_status("Error extracting text.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while extracting text:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass
    
    def _save_text(self):
        """Save the extracted text to a file."""
        if not self.text_area.get(1.0, tk.END).strip():
            messagebox.showwarning("No Text", "There is no text to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Extracted Text As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Text saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the text:\n{str(e)}")
    
    def _clear_text(self):
        """Clear the text area."""
        self.text_area.delete(1.0, tk.END) 