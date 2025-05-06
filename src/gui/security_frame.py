"""
Frame for encrypting and decrypting PDF files.
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from core.security import PDFSecurity
from pypdf import PdfReader


class SecurityFrame(ttk.Frame):
    """Frame for the PDF Security functionality (encryption/decryption)."""

    def __init__(self, parent):
        """
        Initialize the Security frame.

        Args:
            parent: The parent widget
        """
        super().__init__(parent, padding=10)
        self.parent = parent
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Create layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create notebook for encrypt/decrypt tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create encrypt and decrypt frames
        self.encrypt_frame = ttk.Frame(self.notebook, padding=10)
        self.decrypt_frame = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.encrypt_frame, text="Encrypt PDF")
        self.notebook.add(self.decrypt_frame, text="Decrypt PDF")
        
        # Setup encrypt frame
        self._setup_encrypt_frame()
        
        # Setup decrypt frame
        self._setup_decrypt_frame()
    
    def _setup_encrypt_frame(self):
        """Set up the encrypt PDF frame."""
        # Configure grid
        self.encrypt_frame.grid_columnconfigure(1, weight=1)
        
        # Input file selection
        input_frame = ttk.LabelFrame(self.encrypt_frame, text="Input PDF")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.encrypt_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.encrypt_input_var, width=50)
        input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_button = ttk.Button(
            input_frame, 
            text="Browse", 
            command=lambda: self._browse_input(self.encrypt_input_var)
        )
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Password fields
        password_frame = ttk.LabelFrame(self.encrypt_frame, text="Encryption Settings")
        password_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        password_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="User Password:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.user_password_var = tk.StringVar()
        user_password_entry = ttk.Entry(password_frame, textvariable=self.user_password_var, show="*")
        user_password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(password_frame, text="Owner Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.owner_password_var = tk.StringVar()
        owner_password_entry = ttk.Entry(password_frame, textvariable=self.owner_password_var, show="*")
        owner_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(
            password_frame, 
            text="Leave owner password blank to use the same as user password",
            font=("", 8, "italic")
        ).grid(row=2, column=1, padx=5, sticky="w")
        
        # Show password checkboxes
        self.show_user_password = tk.BooleanVar()
        show_user_check = ttk.Checkbutton(
            password_frame, 
            text="Show", 
            variable=self.show_user_password,
            command=lambda: self._toggle_password_visibility(user_password_entry, self.show_user_password)
        )
        show_user_check.grid(row=0, column=2, padx=5)
        
        self.show_owner_password = tk.BooleanVar()
        show_owner_check = ttk.Checkbutton(
            password_frame, 
            text="Show", 
            variable=self.show_owner_password,
            command=lambda: self._toggle_password_visibility(owner_password_entry, self.show_owner_password)
        )
        show_owner_check.grid(row=1, column=2, padx=5)
        
        # Output file selection
        output_frame = ttk.LabelFrame(self.encrypt_frame, text="Output PDF")
        output_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        output_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Save to:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.encrypt_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.encrypt_output_var, width=50)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_output_button = ttk.Button(
            output_frame, 
            text="Browse", 
            command=lambda: self._browse_output(self.encrypt_output_var)
        )
        browse_output_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Encrypt button
        encrypt_button = ttk.Button(self.encrypt_frame, text="Encrypt PDF", command=self._encrypt_pdf)
        encrypt_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def _setup_decrypt_frame(self):
        """Set up the decrypt PDF frame."""
        # Configure grid
        self.decrypt_frame.grid_columnconfigure(1, weight=1)
        
        # Input file selection
        input_frame = ttk.LabelFrame(self.decrypt_frame, text="Encrypted PDF")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.decrypt_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.decrypt_input_var, width=50)
        input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_button = ttk.Button(
            input_frame, 
            text="Browse", 
            command=lambda: self._browse_input(self.decrypt_input_var, True)
        )
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Password field
        password_frame = ttk.LabelFrame(self.decrypt_frame, text="Password")
        password_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        password_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(password_frame, text="Password:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.decrypt_password_var = tk.StringVar()
        decrypt_password_entry = ttk.Entry(password_frame, textvariable=self.decrypt_password_var, show="*")
        decrypt_password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Show password checkbox
        self.show_decrypt_password = tk.BooleanVar()
        show_decrypt_check = ttk.Checkbutton(
            password_frame, 
            text="Show", 
            variable=self.show_decrypt_password,
            command=lambda: self._toggle_password_visibility(decrypt_password_entry, self.show_decrypt_password)
        )
        show_decrypt_check.grid(row=0, column=2, padx=5)
        
        # Output file selection
        output_frame = ttk.LabelFrame(self.decrypt_frame, text="Output PDF")
        output_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        output_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Save to:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.decrypt_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.decrypt_output_var, width=50)
        output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        browse_output_button = ttk.Button(
            output_frame, 
            text="Browse", 
            command=lambda: self._browse_output(self.decrypt_output_var)
        )
        browse_output_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Decrypt button
        decrypt_button = ttk.Button(self.decrypt_frame, text="Decrypt PDF", command=self._decrypt_pdf)
        decrypt_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def _toggle_password_visibility(self, entry, var):
        """Toggle password visibility."""
        if var.get():
            entry.config(show="")
        else:
            entry.config(show="*")
    
    def _browse_input(self, var, check_encrypted=False):
        """
        Browse for input PDF file.
        
        Args:
            var: The StringVar to store the file path
            check_encrypted: Whether to check if the file is encrypted
        """
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            var.set(file_path)
            
            # Check if the file is encrypted if needed
            if check_encrypted:
                try:
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        if not reader.is_encrypted:
                            messagebox.showwarning("Not Encrypted", "The selected PDF is not encrypted.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading PDF: {str(e)}")
            
            # Set default output filename
            if var == self.encrypt_input_var and not self.encrypt_output_var.get():
                dirname = os.path.dirname(file_path)
                basename = os.path.splitext(os.path.basename(file_path))[0]
                self.encrypt_output_var.set(os.path.join(dirname, f"{basename}_encrypted.pdf"))
            elif var == self.decrypt_input_var and not self.decrypt_output_var.get():
                dirname = os.path.dirname(file_path)
                basename = os.path.splitext(os.path.basename(file_path))[0]
                self.decrypt_output_var.set(os.path.join(dirname, f"{basename}_decrypted.pdf"))
    
    def _browse_output(self, var):
        """
        Browse for output file location.
        
        Args:
            var: The StringVar to store the file path
        """
        file_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            var.set(file_path)
    
    def _encrypt_pdf(self):
        """Encrypt the selected PDF."""
        input_path = self.encrypt_input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an input PDF file.")
            return
        
        output_path = self.encrypt_output_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file.")
            return
        
        user_password = self.user_password_var.get()
        if not user_password:
            messagebox.showwarning("No Password", "Please enter a user password.")
            return
        
        owner_password = self.owner_password_var.get()
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Encrypting PDF...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            result = PDFSecurity.encrypt_pdf(
                input_path, 
                output_path, 
                user_password, 
                owner_password if owner_password else None
            )
            
            if result:
                try:
                    app.set_status("PDF encrypted successfully.")
                except (AttributeError, NameError):
                    pass
                messagebox.showinfo("Success", f"PDF encrypted successfully to:\n{output_path}")
            else:
                try:
                    app.set_status("Failed to encrypt PDF.")
                except (AttributeError, NameError):
                    pass
                messagebox.showerror("Error", "Failed to encrypt PDF. Check the console for details.")
        except Exception as e:
            try:
                app.set_status("Error encrypting PDF.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while encrypting PDF:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass
    
    def _decrypt_pdf(self):
        """Decrypt the selected PDF."""
        input_path = self.decrypt_input_var.get()
        if not input_path:
            messagebox.showwarning("No Input", "Please select an encrypted PDF file.")
            return
        
        output_path = self.decrypt_output_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file.")
            return
        
        password = self.decrypt_password_var.get()
        if not password:
            messagebox.showwarning("No Password", "Please enter the password.")
            return
        
        # Get parent application to update status
        try:
            app = self.parent.master
            app.set_status("Decrypting PDF...")
        except AttributeError:
            # If that fails, just continue without status updates
            pass
        
        try:
            result = PDFSecurity.decrypt_pdf(input_path, output_path, password)
            
            if result:
                try:
                    app.set_status("PDF decrypted successfully.")
                except (AttributeError, NameError):
                    pass
                messagebox.showinfo("Success", f"PDF decrypted successfully to:\n{output_path}")
            else:
                try:
                    app.set_status("Failed to decrypt PDF.")
                except (AttributeError, NameError):
                    pass
                messagebox.showerror("Error", "Failed to decrypt PDF. Check the console for details.")
        except Exception as e:
            try:
                app.set_status("Error decrypting PDF.")
            except (AttributeError, NameError):
                pass
            messagebox.showerror("Error", f"An error occurred while decrypting PDF:\n{str(e)}")
        
        try:
            app.set_status("Ready")
        except (AttributeError, NameError):
            pass 