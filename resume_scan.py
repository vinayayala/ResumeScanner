import os
import re
import docx
import fitz  # PyMuPDF

# Function to extract text from DOCX files
def extract_text_from_docx(doc_path):
    doc = docx.Document(doc_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to filter likely certification and training names based on patterns
def filter_certifications(text):
    # Define regex patterns to match certification and training lines
    cert_pattern = re.compile(r'\b(certified|certification|certifications|certificate|cert|notary|training|course|program|workshop|completed|received)\b', re.IGNORECASE)
    section_pattern = re.compile(r'\b(certifications and education|certifications)\b', re.IGNORECASE)
    exclude_pattern = re.compile(r'\b(is|was|am|are|were|be|been|being|provide|provided|manage|managed|develop|developed|track|tracked|facilitate|facilitated|coordinate|coordinated|maintain|maintained|assist|assisted|engaged|created|obtained|initiated|implemented|oversaw|maintained|created|including|but|not|limited|strategy|objectives|principles|strategy)\b', re.IGNORECASE)

    lines = text.split('\n')
    seen_lines = set()
    certifications = []

    for line in lines:
        # Skip section titles
        if section_pattern.search(line):
            continue
        # Check for certification-related keywords and filter out short lines and non-relevant content
        if cert_pattern.search(line) and len(line.split()) > 2:
            # Additional check to filter out lines with verbs indicating job responsibilities
            if not exclude_pattern.search(line):
                clean_line = line.strip()
                if len(clean_line.split()) > 30:
                    # Split long lines into shorter sentences
                    sentences = re.split(r'[.!?]', clean_line)
                    for sentence in sentences:
                        if cert_pattern.search(sentence) and len(sentence.split()) > 2:
                            short_sentence = sentence.strip()
                            if short_sentence not in seen_lines:
                                seen_lines.add(short_sentence)
                                certifications.append(short_sentence)
                else:
                    if clean_line not in seen_lines:
                        seen_lines.add(clean_line)
                        certifications.append(clean_line)

    return certifications

# Function to process each file and extract certifications
def extract_certifications(file_path):
    if file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        return ["Unsupported file format"]

    # Filter entities based on likely certification patterns
    certifications = filter_certifications(text)

    return certifications

# Function to process all resumes in the folder
def process_resumes_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Certifications in {file_path}:")
            certifications = extract_certifications(file_path)
            if certifications:
                for cert in certifications:
                    print(f"- {cert}")
            else:
                print("No certifications found.")
            print("\n")

# Path to the folder containing the resumes
folder_path = '/Users/vinayayala/Desktop/Zen/Resumes 2023'

# Process the resumes in the specified folder
process_resumes_in_folder(folder_path)
