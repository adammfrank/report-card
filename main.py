import pdfplumber

pdf_path = "nevadareportcard_2024.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Try just the first page (change index to test others)
    page = pdf.pages[9]
    
    # Extract raw text
    text = page.extract_text()
    print("=== RAW TEXT ===")
    print(text)

    # Extract tables
    tables = page.extract_tables()
    print("\n=== TABLES FOUND ===")
    for i, table in enumerate(tables):
        print(f"\nTable {i+1}:")
        for row in table:
            print(row)
