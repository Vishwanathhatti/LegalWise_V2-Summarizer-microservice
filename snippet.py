import requests
import fitz # PyMuPDF
import json
import time
import os
import base64
from PIL import Image
import io

# API configuration
# Leave apiKey as an empty string. The Canvas environment will provide it at runtime.
API_KEY = ""
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_backoff_delay(attempt: int) -> int:
    """
    Calculates the exponential backoff delay for API retries.
    """
    return min(1000 * (2 ** attempt), 60000)

def call_gemini_api_with_retry(payload: dict, max_retries: int = 3) -> str:
    """
    Makes a robust API call with exponential backoff.
    
    Args:
        payload: The complete JSON payload to send to the Gemini API.
        max_retries: The maximum number of retry attempts.

    Returns:
        The text response from the API.
    """
    headers = {'Content-Type': 'application/json'}

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json()
            if result.get('candidates') and result['candidates'][0].get('content'):
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "No summary was generated."

        except requests.exceptions.RequestException as e:
            if response and response.status_code == 429 and attempt < max_retries:
                delay = get_backoff_delay(attempt) / 1000  # Delay in seconds
                print(f"API rate limit exceeded. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"API call failed after {attempt} attempts: {e}")
                return f"Error: Failed to get summary. Please check the console for details."
    
    return "Failed to get a response from the API after multiple retries."

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file, first from the text layer.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The extracted text as a single string.
    """
    if not os.path.exists(file_path):
        return f"Error: The file '{file_path}' was not found."

    try:
        doc = fitz.open(file_path)
        full_text = ""
        
        # Try to get text from the PDF's text layer first
        for page in doc:
            full_text += page.get_text()

        doc.close()
        return full_text
    except Exception as e:
        return f"Error: Failed to extract text from PDF. Details: {e}"

def extract_images_and_summarize(file_path: str, word_count: int) -> str:
    """
    Extracts images from a PDF and uses the Gemini API's multimodal
    capabilities to summarize the content.

    Args:
        file_path: The path to the PDF file.
        word_count: The desired word count for the summary.

    Returns:
        The summary text from the API.
    """
    try:
        doc = fitz.open(file_path)
        payload_parts = []
        
        # Add the text prompt to the payload first
        prompt_text = f"Please summarize the following document in approximately {word_count} words."
        payload_parts.append({"text": prompt_text})

        # Process each page as an image
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            
            payload_parts.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": base64_img
                }
            })
        doc.close()
        
        # Construct the full payload
        payload = {
            "contents": [{"parts": payload_parts}]
        }

        return call_gemini_api_with_retry(payload)
    except Exception as e:
        return f"Error during image extraction and summarization: {e}"

if __name__ == "__main__":
    # The PDF file is expected to be named 'demo.pdf' and located in the same directory.
    pdf_path = 'PS4.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found in the current directory.")
    else:
        # Get the desired word count from the user
        word_count = input("Enter the desired summary word count (e.g., 200): ")

        # Validate word count input
        try:
            word_count = int(word_count)
        except ValueError:
            print("Invalid word count. Using default of 200.")
            word_count = 200

        # Extract text from the PDF
        print("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(pdf_path)

        if extracted_text.strip():
            print("Text layer found. Summarizing...")
            prompt = f"Please summarize the following document in approximately {word_count} words. \n\nDocument:\n{extracted_text}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            summary = call_gemini_api_with_retry(payload)
        else:
            print("No text layer found. Sending images for multimodal analysis...")
            summary = extract_images_and_summarize(pdf_path, word_count)
            
        print("\n--- Summary ---")
        print(summary)
