# Document to Mindmap Converter

A Flask-based web application that converts text documents into interactive mindmaps using Google's Gemini AI. The application processes various document formats and generates visual hierarchical representations of their content.

## Features

The Document to Mindmap Converter offers several powerful capabilities:

- Supports multiple document formats including TXT, PDF, and DOCX files
- Generates interactive, zoomable mindmaps using D3.js visualization
- Processes documents using Google's Gemini AI for intelligent content structuring
- Provides an intuitive web interface for document uploads
- Implements automatic file cleanup after processing
- Includes built-in error handling and user feedback

## Prerequisites

Before running the application, ensure you have the following:

- Python 3.7 or higher
- A Google Gemini API key
- Flask secret key for session management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abcxyz91/Mindmap_Summary
cd Mindmap_Summary
```

2. Install the required dependencies:
```bash
pip install flask google-generativeai python-dotenv PyPDF2 python-docx
```

3. Create a `.env` file in the project root directory with the following variables:
```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a document (supported formats: .txt, .pdf, .docx)

4. The application will process your document and display an interactive mindmap

## Technical Details

### Components

- **Frontend**: HTML, CSS, and D3.js for visualization
- **Backend**: Flask web framework
- **AI Processing**: Google Gemini AI API
- **Document Processing**: PyPDF2 and python-docx libraries

### File Structure

- `app.py`: Main Flask application file containing route handlers and document processing logic
- `index.html`: Frontend template with D3.js visualization implementation
- `uploads/`: Temporary directory for file processing (automatically created)

### Security Features

The application implements several security measures:

- File extension validation
- Maximum file size limit (16MB)
- Automatic file cleanup after processing
- Environment variable protection for sensitive keys

## Limitations

- Maximum file size: 16MB
- Supported file formats: .txt, .pdf, .docx only
- Requires active internet connection for AI processing

## Error Handling

The application includes comprehensive error handling for:

- Invalid file formats
- Missing files in requests
- JSON parsing errors
- File processing failures
- API communication issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for document processing
- D3.js for visualization capabilities
- Flask framework for web implementation