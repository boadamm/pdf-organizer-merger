# PDF Organizer & Merger

An all-in-one desktop tool for everyday PDF management built with Python and Tkinter.

## Features

- **Merge PDFs**: Combine multiple PDF documents into a single file
- **Split PDFs**: Extract specific pages or ranges from a PDF
- **Text Extraction**: Extract and display searchable text from any PDF
- **Rearrange Pages**: Modify the page order of existing PDFs
- **Encryption/Decryption**: Protect your PDFs with password-based encryption

## Installation

### Requirements
- Python 3.12 or higher

### Setup

1. Clone this repository
   ```
   git clone https://github.com/yourusername/pdf-tool.git
   cd pdf-tool
   ```

2. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python src/main.py
```

## Building Executable

To create a standalone executable:
```
pyinstaller --onefile --windowed src/main.py
```

The executable will be available in the `dist` directory.

## Technologies Used

- **Python 3.12**: Core programming language
- **Tkinter + ttk**: GUI framework
- **pypdf**: PDF merging, splitting, and page reordering
- **pdfplumber**: Text extraction
- **cryptography**: Encryption/decryption functionality
- **Pillow**: Image handling for thumbnails
- **PyInstaller**: Packaging
- **pytest**: Testing

## License

MIT 