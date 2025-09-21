import pdfplumber
import json

pdf_path = "nevadareportcard_2024.pdf"
output = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        # Find all tables on this page
        tables = page.find_tables()
        extracted = page.extract_tables()

        for i, (t, table_data) in enumerate(zip(tables, extracted), start=1):
            x0, top, x1, bottom = t.bbox

            # Look just above the table for the title text
            title_area = (x0, max(0, top - 50), x1, top)  # 50px margin above
            title_text = page.within_bbox(title_area).extract_text()

            if title_text:
                title = " ".join(title_text.split())  # normalize whitespace
            else:
                title = f"Untitled Table {i} (Page {page_num})"

            # Build record
            record = {
                "page": page_num,
                "title": title,
                "rows": table_data
            }
            output.append(record)

# Save to JSON
with open("reportcard_tables.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(output)} tables into reportcard_tables.json")
