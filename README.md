# PDF-Tool

**PDF-Tool** is a simple tool designed to create new PDF files from existing PDFs or from image files.

## 🔧 Features

- 📄 Merge multiple PDF files into a single document  
- 🖼️ Convert one or more image files (e.g., PNG, JPG) into a PDF  
- ⚙️ Basic

## ⚙️ Usage

You can use it to:
- Combine several PDFs into one
- Turn images into PDFs 
- Rotate images or PDFs

## 📦 Requirements

You can install all dependencies with:

```bash
pip install -r requirements.txt
```

## 🚀 Run

Via command line:

```
python pdf.py
```
Or as a standalone executable (Windows):

```
pyinstaller --onefile --windowed --add-data "C:\path\to\tkinterdnd2 tkinterdnd2" pdf.py
```
> ⚠️ **Make sure to replace** `C:\path\to\tkinterdnd2` with the actual path to the `tkinterdnd2` package in your Python environment.  
>  

The generated executable will appear in the `dist` folder.
