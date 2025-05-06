"""
Frame for merging multiple PDF files.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from typing import List

from core.pdf_merger import PDFMerger


class MergeFrame(ttk.Frame):
    """Frame for the Merge PDFs functionality."""

    def __init__(self, parent):
        """
        Initialize the Merge PDFs frame.

        Args:
            parent: The parent widget
        """
        super().__init__(parent, padding=10)
        self.parent = parent
        self.pdf_files = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # PDF file list frame
        list_frame = ttk.LabelFrame(self, text="PDF Files to Merge")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # Files listbox with scrollbar
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.files_listbox.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for file management
        file_buttons_frame = ttk.Frame(self)
        file_buttons_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        add_button = ttk.Button(file_buttons_frame, text="Add Files", command=self._add_files)
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(file_buttons_frame, text="Remove Selected", command=self._remove_files)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(file_buttons_frame, text="Clear All", command=self._clear_files)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        move_up_button = ttk.Button(file_buttons_frame, text="Move Up", command=self._move_up)
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(file_buttons_frame, text="Move Down", command=self._move_down)
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        # Output file selection
        output_frame = ttk.Frame(self)
        output_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(output_frame, text="Output PDF:").pack(side=tk.LEFT, padx=5)
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(output_frame, text="Browse", command=self._browse_output)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Merge button
        merge_button = ttk.Button(self, text="Merge PDFs", command=self._merge_pdfs)
        merge_button.grid(row=3, column=0, pady=10)
    
    def _add_files(self):
        """Add PDF files to the list."""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def _remove_files(self):
        """Remove selected files from the list."""
        selected_indices = self.files_listbox.curselection()
        
        # Remove from end to start to avoid index changes
        for i in sorted(selected_indices, reverse=True):
            self.files_listbox.delete(i)
            self.pdf_files.pop(i)
    
    def _clear_files(self):
        """Clear all files from the list."""
        self.files_listbox.delete(0, tk.END)
        self.pdf_files = []
    
    def _move_up(self):
        """Move selected file up in the list."""
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices or selected_indices[0] == 0:
            return
        
        index = selected_indices[0]
        file_name = self.files_listbox.get(index)
        file_path = self.pdf_files[index]
        
        self.files_listbox.delete(index)
        self.pdf_files.pop(index)
        
        self.files_listbox.insert(index - 1, file_name)
        self.pdf_files.insert(index - 1, file_path)
        
        self.files_listbox.selection_set(index - 1)
    
    def _move_down(self):
        """Move selected file down in the list."""
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices or selected_indices[0] == self.files_listbox.size() - 1:
            return
        
        index = selected_indices[0]
        file_name = self.files_listbox.get(index)
        file_path = self.pdf_files[index]
        
        self.files_listbox.delete(index)
        self.pdf_files.pop(index)
        
        self.files_listbox.insert(index + 1, file_name)
        self.pdf_files.insert(index + 1, file_path)
        
        self.files_listbox.selection_set(index + 1)
    
    def _browse_output(self):
        """Browse for output file location."""
        file_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_var.set(file_path)
    
    def _merge_pdfs(self):
        """Merge the selected PDF files."""
        if not self.pdf_files:
            messagebox.showwarning("No Files", "Please add PDF files to merge.")
            return
        
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file.")
            return
        
        # Update status message safely
        try:
            # Try the original approach first
            app = self.parent.master
            app.set_status("Merging PDFs...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            result = PDFMerger.merge_pdfs(self.pdf_files, output_path)
            
            if result:
                try:
                    app.set_status("PDFs merged successfully.")
                except (AttributeError, NameError):
                    pass
                messagebox.showinfo("Success", f"PDFs merged successfully to:\n{output_path}")
            else:
                try:
                    app.set_status("Failed to merge PDFs.")
                except (AttributeError, NameError):
                    pass
                messagebox.showerror("Error", "Failed to merge PDFs. Check the console for details.")
        except Exception as e:
            try:
                app.set_status("Error merging PDFs.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while merging PDFs:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass    