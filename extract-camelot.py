import camelot
import time

tables = camelot.read_pdf('nevadareportcard_2024.pdf', pages="all", flavor="lattice", strip_text="\n")
tables.export('reportcard.csv', f='csv', compress=False)
