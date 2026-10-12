import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_parser import extract_text_from_pdf

file_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "sample_cv.pdf"
)

text = extract_text_from_pdf(file_path)

print("\n----- CV TEXT -----\n")
print(text)