import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, redirect, url_for
from PyPDF2 import PdfReader
from docx import Document
import os
import json

# Load the environment variables and validate the API key
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is missing or invalid")
else:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Setup SYSTEM PROMPT and model
SYSTEM_PROMPT = """
Create a hierarchical mindmap structure from the following text. 
You must always respond with valid JSON that strictly follows this structure:
    {
        "central_topic": "Main Topic",
        "branches": [
            {
                "topic": "Subtopic 1",
                "children": [
                    {"topic": "Point 1"},
                    {"topic": "Point 2"}
                ]
            }
        ]
    }
Rules:
1. Always return raw JSON data only
2. Do not include any explanatory text
3. Do not use markdown formatting
4. The response should be parseable by json.loads() in Python
5. Do not include ```json or ``` markers 
"""

model = genai.GenerativeModel("gemini-2.0-flash-exp",system_instruction=SYSTEM_PROMPT)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") # Secret key for flash messages
app.config["UPLOAD_PATH"] = "uploads" # Upload directory
app.config["MAX_CONTENT_LENGTH"] = 16* 1024 * 1024 # 16MB limit
app.config["UPLOAD_EXTENSIONS"] = [".txt", ".docx", ".pdf"] # Allowed file extensions
os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True) # Create the upload directory if it doesn't exist

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        # Check if key "file" is in request.files dictonary
        if "file" not in request.files:
            flash("No file part")
            return redirect(url_for("home"))
        file = request.files["file"]
        # Check if user uploads an empty file
        if file.filename == "":
            flash("No selected file")
            return redirect(url_for("home"))
        
        # Check if the POST request has the allowed file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            flash("File extension not allowed")
            return redirect(url_for("home"))
        
        # Save the uploaded file
        file_path = os.path.join(app.config["UPLOAD_PATH"], file.filename)
        file.save(file_path)

        # Read the uploaded file based on the file extension
        try:
            if file_ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            elif file_ext == ".docx":
                text = text_from_docx(file_path)
            elif file_ext == ".pdf":
                text = text_from_pdf(file_path)

            # Summarize by Gemini and generate the mindmap structure
            response = model.generate_content(text)
            # Clean the response by removing markdown code blocks
            cleaned_response = cleaned_response(response.text)
            
            try:
                mindmap_data = json.loads(cleaned_response) # Parse the JSON response
                return render_template("index.html", mindmap_data=json.dumps(mindmap_data))
            except json.JSONDecodeError:
                flash("Error: Invalid JSON response")
                return redirect(url_for("home"))

        # Clean up the uploaded file even if error happens
        except Exception as e:
            flash(f"error: {str(e)}")
            return redirect(url_for("home"))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

def text_from_docx(file_path):
    # Combine all paragraphs into a single string separated by newline
    document = Document(file_path)
    text = "\n".join([p.text for p in document.paragraphs])
    return text


def text_from_pdf(file_path):
    # Combine all paragraphs into a single string separated by newline
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    return text


def cleaned_response(response):
    # Remove starting ```json or ``` and ending ```
    cleaned_response = response.strip()
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.split("\n", 1)[1]  # Remove first line
        cleaned_response = cleaned_response.rsplit("\n", 1)[0]  # Remove last line
        cleaned_response = cleaned_response.strip()
    return cleaned_response


if __name__ == "__main__":
    app.run(debug=True)
