import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from tqdm import tqdm


load_dotenv()
CLIENT = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

MODEL_DICT = {
    'gpt-3.5-turbo': {
        'api_name': 'gpt-3.5-turbo-0125',
        'context_window': 16385,
        'max_output': 4096,
        'token_input_cost': 0.5,
        'token_output_cost': 1.5,
        'token_cost_per': 1000000,
        'sleep_time': 5,
    },
    'gpt-4o': {
        'api_name': 'gpt-4o-2024-05-13',
        'context_window': 30000, # 128000, but we're rate limited to 30,000 per minute
        'max_output': 4096,
        'token_input_cost': 5,
        'token_output_cost': 15,
        'token_cost_per': 1000000,
        'sleep_time': 60,
    },
    'gpt-4o-mini': {
        'api_name': 'gpt-4o-mini-2024-07-18',
        'context_window': 128000,
        'max_output': 4096,
        'token_input_cost': 0.15,
        'token_output_cost': 0.60,
        'token_cost_per': 1000000,
        'sleep_time': 60,
    },
}

# Folder paths
input_folder = "pdfs_tmp"
output_folder = "output"
output_file = os.path.join(output_folder, "output.txt")


def pdf_full_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text_list = list()
    for page in pdf_reader.pages:
        text_list.append(page.extract_text())
    return '\n'.join(text_list).replace('\x00','')


# Function to read and translate PDFs
def translate_pdfs(input_folder, output_file):
    system_prompt = """
    Please translate the entire contents of user text from Nepali to English.
    Return only the translated text.
    """
    model_attributes = MODEL_DICT["gpt-4o-mini"]
    all_translations = []

    # Check if output directory exists; if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all PDF files in the input folder
    for filename in tqdm(os.listdir(input_folder)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            
            # Read the PDF content
            full_text = pdf_full_text(pdf_path)

            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": full_text
                }
            ]
            response = CLIENT.chat.completions.create(
                model=model_attributes['api_name'],
                messages=messages
            )
            translation = response.choices[0].message.content
            all_translations.append(translation)
            time.sleep(model_attributes['sleep_time'])

    # Concatenate all translations and save to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("\n\n".join(all_translations))

    print(f"All translations have been saved to {output_file}")

# Run the translation function
translate_pdfs(input_folder, output_file)
