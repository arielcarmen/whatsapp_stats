"""
Image to PDF Conversion Utilities
This module contains utility functions for converting images to PDF.
"""

from PIL import Image
import io


def validate_image_file(uploaded_file):
    """
    Validate if the uploaded file is a valid image format.
    
    Supported formats: JPG, JPEG, PNG, WEBP
    
    Args:
        uploaded_file (UploadedFile): Uploaded file via Streamlit.
        
    Returns:
        bool: True if valid image format, False otherwise.
    """
    # Include WEBP format alongside traditional image formats
    valid_formats = {'jpg', 'jpeg', 'png', 'webp'}
    file_ext = uploaded_file.name.split('.')[-1].lower()
    return file_ext in valid_formats


def convert_images_to_pdf(uploaded_files):
    """
    Convert multiple images into a single PDF file.
    
    Args:
        uploaded_files (list): List of uploaded image files via Streamlit.
        
    Returns:
        tuple: (pdf_bytes, error_message) where pdf_bytes is bytes or None if error.
    """
    if not uploaded_files:
        return None, "No images provided."
    
    images = []
    
    try:
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            # Validate file format
            if not validate_image_file(uploaded_file):
                continue
            
            # Read and convert image to RGB (required for PDF)
            try:
                image = Image.open(uploaded_file)
                
                # Convert RGBA, WEBP, or other formats to RGB for PDF compatibility
                # This handles transparency in PNG/WEBP and ensures PDF compatibility
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                images.append(image)
            except Exception as e:
                return None, f"Error processing {uploaded_file.name}: {str(e)}"
        
        if not images:
            return None, "No valid images found. Supported formats: JPG, JPEG, PNG, WEBP"
        
        # Create PDF from images
        # Use the first image as the base and append others
        pdf_bytes = io.BytesIO()
        images[0].save(
            pdf_bytes,
            format='PDF',
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
            duration=100,
            loop=0
        )
        
        pdf_bytes.seek(0)
        return pdf_bytes.getvalue(), None
        
    except Exception as e:
        return None, f"Error creating PDF: {str(e)}"


def get_image_dimensions(uploaded_file):
    """
    Get the dimensions of an uploaded image.
    
    Args:
        uploaded_file (UploadedFile): Uploaded image file via Streamlit.
        
    Returns:
        tuple: (width, height) in pixels, or None if error.
    """
    try:
        image = Image.open(uploaded_file)
        return image.size
    except Exception:
        return None


def estimate_pdf_size(uploaded_files):
    """
    Estimate the size of the resulting PDF.
    
    Args:
        uploaded_files (list): List of uploaded image files via Streamlit.
        
    Returns:
        str: Human-readable estimated size (e.g., "2.5 MB").
    """
    total_size = 0
    
    for uploaded_file in uploaded_files:
        if validate_image_file(uploaded_file):
            total_size += uploaded_file.size
    
    # Rough estimate: PDF is typically 70-80% of original images size
    estimated_bytes = int(total_size * 0.75)
    
    if estimated_bytes < 1024:
        return f"{estimated_bytes} B"
    elif estimated_bytes < 1024 * 1024:
        return f"{estimated_bytes / 1024:.1f} KB"
    else:
        return f"{estimated_bytes / (1024 * 1024):.1f} MB"
