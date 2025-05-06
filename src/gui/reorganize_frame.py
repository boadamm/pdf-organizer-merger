"""
Frame for reorganizing pages in a PDF file.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from typing import List, Dict
import io

from core.page_reorganizer import PageReorganizer
from core.thumbnail import ThumbnailGenerator
from pypdf import PdfReader


class ReorganizeFrame(ttk.Frame):
    """Frame for the Reorganize Pages functionality."""

    def __init__(self, parent):
        """
        Initialize the Reorganize Pages frame.

        Args:
            parent: The parent widget
        """
        super().__init__(parent, padding=10)
        self.parent = parent
        self.input_file = None
        self.total_pages = 0
        self.thumbnails = []
        self.current_order = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Input file selection
        input_frame = ttk.LabelFrame(self, text="Input PDF")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50)
        input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_button = ttk.Button(input_frame, text="Browse", command=self._browse_input)
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        load_button = ttk.Button(input_frame, text="Load Pages", command=self._load_pages)
        load_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Page thumbnails with list
        thumbnails_frame = ttk.LabelFrame(self, text="Pages (Drag to Reorder)")
        thumbnails_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        thumbnails_frame.grid_columnconfigure(0, weight=1)
        thumbnails_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas for thumbnails with scrollbar
        self.canvas = tk.Canvas(thumbnails_frame)
        scrollbar = ttk.Scrollbar(thumbnails_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame inside canvas for thumbnails
        self.pages_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.pages_frame, anchor="nw")
        
        self.pages_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel events for scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)    # Linux scroll down
        
        # Output file selection
        output_frame = ttk.LabelFrame(self, text="Output PDF")
        output_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        output_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Save to:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_output_button = ttk.Button(output_frame, text="Browse", command=self._browse_output)
        browse_output_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        save_button = ttk.Button(button_frame, text="Save Reorganized PDF", command=self._save_pdf)
        save_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Reset Order", command=self._reset_order)
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def _on_frame_configure(self, event):
        """Configure the canvas scrollregion when the frame changes size."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Resize the frame inside the canvas when the canvas changes size."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        # Different event handling for different platforms
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
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
                self.output_var.set(os.path.join(dirname, f"{basename}_reordered.pdf"))
    
    def _browse_output(self):
        """Browse for output file location."""
        file_path = filedialog.asksaveasfilename(
            title="Save Reorganized PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_var.set(file_path)
    
    def _update_page_info(self):
        """Update the page count information for the loaded PDF."""
        if not self.input_file:
            self.total_pages = 0
            return
        
        try:
            with open(self.input_file, 'rb') as f:
                reader = PdfReader(f)
                self.total_pages = len(reader.pages)
        except Exception as e:
            self.total_pages = 0
            print(f"Error reading PDF: {str(e)}")
    
    def _load_pages(self):
        """Load PDF pages and display thumbnails for reordering."""
        input_path = self.input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an input PDF file.")
            return
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Loading PDF pages...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            # Clear existing thumbnails
            for widget in self.pages_frame.winfo_children():
                widget.destroy()
            
            self._update_page_info()
            
            # Generate thumbnails for all pages
            self.thumbnails = ThumbnailGenerator.generate_thumbnails(input_path)
            
            # Initialize the current order
            self.current_order = list(range(self.total_pages))
            
            # Display thumbnails
            self._display_thumbnails()
            
            try:
                app.set_status("PDF pages loaded successfully.")
            except (AttributeError, NameError):
                pass
        except Exception as e:
            try:
                app.set_status("Error loading PDF pages.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while loading PDF pages:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass
    
    def _display_thumbnails(self):
        """Display the thumbnails in the current order."""
        # Clear existing thumbnails
        for widget in self.pages_frame.winfo_children():
            widget.destroy()
        
        if not self.thumbnails:
            return
        
        # Display thumbnails in the current order
        for i, page_idx in enumerate(self.current_order):
            frame = ttk.Frame(self.pages_frame)
            frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            
            # Convert thumbnail to PhotoImage for display
            thumbnail = self.thumbnails[page_idx]
            photo = tk.PhotoImage(data=self._pil_to_data(thumbnail))
            
            # Store the photo to prevent garbage collection
            frame.photo = photo
            
            # Label for the page number
            ttk.Label(frame, text=f"Page {page_idx + 1}").pack(side=tk.TOP)
            
            # Thumbnail display
            label = ttk.Label(frame, image=photo)
            label.pack(side=tk.TOP)
            
            # Make the frame draggable
            label.bind("<ButtonPress-1>", lambda event, idx=i: self._on_drag_start(event, idx))
            label.bind("<B1-Motion>", self._on_drag_motion)
            label.bind("<ButtonRelease-1>", self._on_drag_release)
    
    def _pil_to_data(self, image):
        """Convert PIL image to data for Tkinter PhotoImage."""
        data = io.BytesIO()
        image.save(data, format="PNG")
        data.seek(0)
        return data.read()
    
    def _on_drag_start(self, event, idx):
        """Start dragging a thumbnail."""
        # Store the initial position and frame index
        self._drag_data = {'x': event.x, 'y': event.y, 'idx': idx}
        
        # Highlight the selected frame
        event.widget.configure(style="Selected.TLabel")
    
    def _on_drag_motion(self, event):
        """Move the dragged thumbnail."""
        # This method would be used for visual feedback during dragging
        pass
    
    def _on_drag_release(self, event):
        """Drop the dragged thumbnail at the new position."""
        if not hasattr(self, '_drag_data'):
            return
        
        # Calculate the new position based on the y-coordinate
        y = event.y_root
        new_idx = None
        
        for i, frame in enumerate(self.pages_frame.winfo_children()):
            frame_y = frame.winfo_rooty()
            frame_height = frame.winfo_height()
            
            if frame_y <= y <= frame_y + frame_height:
                new_idx = i
                break
        
        # If dropped at a valid position, update the order
        if new_idx is not None and new_idx != self._drag_data['idx']:
            idx = self._drag_data['idx']
            page_idx = self.current_order[idx]
            
            # Remove the page from its current position
            self.current_order.pop(idx)
            
            # Insert it at the new position
            self.current_order.insert(new_idx, page_idx)
            
            # Redisplay the thumbnails
            self._display_thumbnails()
        
        # Remove highlight from the selected frame
        event.widget.configure(style="TLabel")
        
        # Clear drag data
        del self._drag_data
    
    def _reset_order(self):
        """Reset the page order to the original order."""
        self.current_order = list(range(self.total_pages))
        self._display_thumbnails()
    
    def _save_pdf(self):
        """Save the reorganized PDF."""
        input_path = self.input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an input PDF file.")
            return
        
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file.")
            return
        
        if not self.current_order:
            messagebox.showwarning("No Pages", "No pages have been loaded for reordering.")
            return
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Saving reorganized PDF...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            result = PageReorganizer.reorganize_pages(input_path, output_path, self.current_order)
            
            if result:
                try:
                    app.set_status("PDF saved successfully.")
                except (AttributeError, NameError):
                    pass
                messagebox.showinfo("Success", f"Reorganized PDF saved successfully to:\n{output_path}")
            else:
                try:
                    app.set_status("Failed to save PDF.")
                except (AttributeError, NameError):
                    pass
                messagebox.showerror("Error", "Failed to save reorganized PDF. Check the console for details.")
        except Exception as e:
            try:
                app.set_status("Error saving PDF.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while saving the PDF:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass 