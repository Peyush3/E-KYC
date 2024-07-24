import os
import easyocr
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir,"ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")


def extract_text(image_path, confidence_threshold=0.3, languages=['en']):

    logging.info("Text Extraction Started...")
    reader = easyocr.Reader(languages)
    
    try:
        logging.info("Inside Try-Catch...")
        result = reader.readtext(image_path)
        filtered_text = "|"  
        for text in result:
            bounding_box, recognized_text, confidence = text
            if confidence > confidence_threshold:
                filtered_text += recognized_text + "|" 

        return filtered_text 
    
    except Exception as e:
        print("An error occurred during text extraction:", e)
        logging.info(f"An error occurred during text extraction: {e}")
        return ""

    