"""
PDF Security module for encrypting and decrypting PDF files.
"""
from pathlib import Path
from typing import Union

from pypdf import PdfReader, PdfWriter


class PDFSecurity:
    """Class to handle encryption and decryption of PDF files."""

    @staticmethod
    def encrypt_pdf(input_path: Union[str, Path], 
                   output_path: Union[str, Path], 
                   user_password: str,
                   owner_password: str = None) -> bool:
        """
        Encrypt a PDF file with a password.

        Args:
            input_path: Path to the PDF file to encrypt
            output_path: Path where the encrypted PDF will be saved
            user_password: Password required to open the PDF
            owner_password: Password for full permissions (defaults to user_password if None)

        Returns:
            bool: True if encryption was successful, False otherwise
        """
        try:
            reader = PdfReader(str(input_path))
            writer = PdfWriter()
            
            # Add all pages to the writer
            for page in reader.pages:
                writer.add_page(page)
            
            # Use user_password as owner_password if not provided
            if owner_password is None:
                owner_password = user_password
            
            # Encrypt the PDF with the AES-256 algorithm
            writer.encrypt(user_password=user_password, 
                          owner_password=owner_password,
                          use_128bit=False)  # False = use AES-256
            
            # Write the encrypted PDF to the output path
            with open(str(output_path), 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Error encrypting PDF: {str(e)}")
            return False

    @staticmethod
    def decrypt_pdf(input_path: Union[str, Path], 
                   output_path: Union[str, Path], 
                   password: str) -> bool:
        """
        Decrypt a password-protected PDF file.

        Args:
            input_path: Path to the encrypted PDF file
            output_path: Path where the decrypted PDF will be saved
            password: Password to decrypt the PDF

        Returns:
            bool: True if decryption was successful, False otherwise
        """
        try:
            reader = PdfReader(str(input_path))
            writer = PdfWriter()
            
            # Check if the PDF is encrypted
            if reader.is_encrypted:
                # Try to decrypt with the provided password
                if not reader.decrypt(password):
                    print("Incorrect password")
                    return False
            else:
                print("PDF is not encrypted")
                return False
            
            # Add all pages to the writer
            for page in reader.pages:
                writer.add_page(page)
            
            # Write the decrypted PDF to the output path
            with open(str(output_path), 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Error decrypting PDF: {str(e)}")
            return False 