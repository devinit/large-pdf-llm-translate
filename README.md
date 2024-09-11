# large-pdf-llm-translate
Chunk and translate large PDFs using LLMs

## Installation

```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## To run

```
rm -rf pdfs_tmp
rm -rf output
python3 code/split_pdf.py pdfs/240607021743.pdf
python3 translate_pdfs.py
```