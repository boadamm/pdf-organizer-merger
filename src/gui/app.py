"""
Main application window for the PDF Tool.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from gui.merge_frame import MergeFrame
from gui.split_frame import SplitFrame
from gui.text_frame import TextFrame
from gui.reorganize_frame import ReorganizeFrame
from gui.security_frame import SecurityFrame


class PDFToolApp:
    """Main application class for the PDF Tool."""

    def __init__(self, root):
        """
        Initialize the main application window.

        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("PDF Organizer & Merger")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Set the application icon (if available)
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                    "assets", "icon.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error setting icon: {str(e)}")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for each feature
        self.merge_frame = MergeFrame(self.notebook)
        self.split_frame = SplitFrame(self.notebook)
        self.text_frame = TextFrame(self.notebook)
        self.reorganize_frame = ReorganizeFrame(self.notebook)
        self.security_frame = SecurityFrame(self.notebook)
        
        # Add the frames to the notebook
        self.notebook.add(self.merge_frame, text="Merge PDFs")
        self.notebook.add(self.split_frame, text="Split PDF")
        self.notebook.add(self.text_frame, text="Extract Text")
        self.notebook.add(self.reorganize_frame, text="Rearrange Pages")
        self.notebook.add(self.security_frame, text="Security")
        
        # Add status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor=tk.W, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create a menu
        self._create_menu()
    
    def _create_menu(self):
        """Create the application menu."""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def _show_about(self):
        """Show the about dialog."""
        messagebox.showinfo(
            "About PDF Organizer & Merger",
            "PDF Organizer & Merger\n\n"
            "A desktop application for managing and manipulating PDF files.\n\n"
            "Features:\n"
            "- Merge multiple PDFs\n"
            "- Split PDFs by pages\n"
            "- Extract text\n"
            "- Rearrange pages\n"
            "- Encrypt/decrypt PDFs"
        )
    
    def set_status(self, message):
        """
        Update the status bar message.

        Args:
            message: The message to display
        """
        self.status_var.set(message)
        self.root.update_idletasks()


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main() 