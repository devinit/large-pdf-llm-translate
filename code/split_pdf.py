import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_dir, pages_per_split=10):
    # Check if the output directory exists; if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input PDF file
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PdfReader(input_pdf_file)
        total_pages = len(reader.pages)

        # Loop through and create new PDFs for each 10-page segment
        for start_page in range(0, total_pages, pages_per_split):
            writer = PdfWriter()
            end_page = min(start_page + pages_per_split, total_pages)

            # Add pages to the writer
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            # Save the new PDF
            output_pdf_path = os.path.join(output_dir, f'output_{start_page + 1}_to_{end_page}.pdf')
            with open(output_pdf_path, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)

            print(f'Saved: {output_pdf_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python split_pdf.py <PDF file path>")
        sys.exit(1)

    input_pdf_path = sys.argv[1]
    output_dir = "pdfs_tmp"
    split_pdf(input_pdf_path, output_dir)
