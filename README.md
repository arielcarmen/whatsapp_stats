# Whatsapp Stats

A professional multi-page Streamlit application for analyzing WhatsApp chat exports and converting images to PDF.

## Features

**WhatsApp Message Counter**
- Count messages per user and analyze user activity
- Search for specific keywords or phrases in chat history
- Filter messages within specific date ranges
- Identify most active members
- Export analysis results as text files

**Image to PDF Converter**
- Convert multiple images into a single PDF file
- Support for JPG, JPEG, and PNG formats
- Preserve image quality and order
- Generate downloadable PDF documents
- Batch conversion with progress tracking

## Project Structure

```
whatsapp_stats/
├── main.py                          # Home page (entry point)
├── pages/
│   ├── __init__.py
│   ├── whatsapp_counter.py         # WhatsApp message counter page
│   └── image_converter.py                       # Image to PDF Converter page
├── utils/
│   ├── __init__.py
│   ├── analyzer.py                 # WhatsApp analysis functions
│   └── image_converter.py          # Image conversion functions
├── requirements.txt
├── Dockerfile
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd whatsapp_stats
   ```

2. **Create a virtual environment**
   ```bash
   # macOS / Linux
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Once installed, launch the Streamlit app:

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## Pages Overview

### Home Page (`main.py`)
- Welcome message and application overview
- Feature descriptions for both tools
- Step-by-step usage guides
- Frequently asked questions
- Technical information and privacy details
- Navigation guide to other pages

### WhatsApp Message Counter (`pages/whatsapp_counter.py`)
- Upload WhatsApp chat export files
- View extracted group information
- Filter messages by date range
- Search for specific keywords
- View detailed user statistics
- Download analysis results as text files

### Image to PDF Converter (`pages/pd.py`)
- Upload multiple image files (JPG, PNG)
- Preview selected files before conversion
- View estimated PDF file size
- Convert to single PDF document
- Download generated PDF files

## How to Use

### WhatsApp Message Counter

1. Export your WhatsApp chat:
   - **iPhone**: Open chat → Contact info → Export Chat → Without Media
   - **Android**: Open chat → Menu → More → Export Chat → Without Media

2. Navigate to "WhatsApp Message Counter"
3. Upload your .txt export file
4. View group information
5. Set optional filters:
   - Date range (start and end dates)
   - Keyword search (optional)
6. Click "Generate Statistics"
7. Review results and download if needed

### Image to PDF Converter

1. Prepare your image files (JPG, JPEG, or PNG)
2. Navigate to "Image to PDF Converter"
3. Upload one or more images
4. Review the file list and estimated PDF size
5. Click "Convert to PDF"
6. Download the generated PDF file

## Architecture & Code Quality

### Modular Design

**utils/analyzer.py** - WhatsApp analysis functions
- `extract_group_details()`: Extract group name and creation info
- `get_date_range()`: Get min/max dates from messages
- `analyze_messages()`: Analyze messages with filtering
- `generate_analysis_report()`: Generate formatted reports

**utils/image_converter.py** - Image conversion functions
- `validate_image_file()`: Check if file is valid image
- `convert_images_to_pdf()`: Convert images to single PDF
- `get_image_dimensions()`: Get image dimensions
- `estimate_pdf_size()`: Estimate resulting PDF size

### Best Practices
- Clean, well-documented code with docstrings
- Modular structure for easy maintenance
- Separation of concerns (UI vs. logic)
- Proper error handling and user feedback
- Professional interface without visual clutter
- Memory-efficient image processing

## Dependencies

- **streamlit**: Web framework for building data apps
- **Pillow**: Image processing library
- **Python Standard Library**: Collections, re (regex), datetime

## Docker Support

The application includes a Dockerfile for containerized deployment.

To build and run with Docker:

```bash
docker build -t whatsapp-stats .
docker run -p 8501:8501 whatsapp-stats
```

## Usage Examples

### WhatsApp Counter
1. Export a WhatsApp group chat as .txt
2. Upload to "WhatsApp Message Counter"
3. Leave dates as default for full analysis
4. Enter keyword (e.g., "hello") or leave empty
5. Click "Generate Statistics"
6. Download the report

### Image Converter
1. Select 5-10 images from your device
2. Go to "Image to PDF Converter"
3. Upload all images at once
4. Verify the file list
5. Click "Convert to PDF"
6. Download your merged PDF

## File Processing Details

### WhatsApp Counter
- Parses standard WhatsApp export format
- Extracts timestamps, usernames, messages
- Filters by date range (optional)
- Searches keywords (whole word match)
- Calculates statistics per user
- Generates formatted report

### Image Converter
- Validates image format (JPG, PNG)
- Converts all to RGB if needed
- Preserves aspect ratio
- Creates single PDF document
- Maintains file order (alphabetical)

## Limitations

**WhatsApp Counter:**
- Only supports .txt export format from WhatsApp
- Requires standard export format (DD/MM/YYYY HH:MM)
- Searches use whole-word matching

**Image Converter:**
- Supports JPG, JPEG, PNG only
- Images processed in alphabetical order by filename

## Privacy & Security

- No data storage or logging
- No external uploads or API calls
- All processing done locally
- Files not retained after use
- GDPR and privacy compliant

## Version & Updates

**Version**: 2.1 (Image Converter Edition)  
**Last Updated**: April 2026

**Recent Updates:**
- Added Image to PDF Converter feature
- Replaced placeholder page with functional utility
- Expanded Home page with comprehensive guides
- Improved error handling and user feedback

## Contributing

Feel free to fork, create issues, or submit pull requests for improvements!

## License

This project is open source and available under the MIT License.

---

Made with care using Streamlit
