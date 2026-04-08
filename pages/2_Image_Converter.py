"""
Image to PDF Converter Page
This page allows users to convert multiple images into a single PDF file.
"""

import streamlit as st
from utils.image_converter import convert_images_to_pdf, estimate_pdf_size, validate_image_file

# Configure page metadata
st.set_page_config(
    page_title="Image to PDF Converter",
    layout="wide"
)

st.title("Image to PDF Converter")
st.write("Convert multiple images into a single PDF file. Each image will be placed on its own page.")

st.divider()

# Instructions section
with st.expander("How to Use", expanded=False):
    st.write(
        """
        1. Select multiple images from your device (JPG, JPEG, PNG, or WEBP format)
        2. You can mix different image formats in a single upload
        3. Images will be processed in alphabetical order
        4. Each image will be placed on a separate page in the PDF
        5. Click 'Convert to PDF' to generate the file
        6. Download your PDF file
        
        Supported formats: JPG, JPEG, PNG, WEBP
        """
    )

st.divider()

# File uploader
st.subheader("Upload Images")
st.write("Select one or more images to convert:")

uploaded_files = st.file_uploader(
    "Choose image files",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    help="You can select multiple images at once (supports JPG, JPEG, PNG, and WEBP formats)"
)

if uploaded_files:
    st.divider()
    
    # Display preview of selected files
    st.subheader("Selected Files")
    
    valid_files = []
    invalid_files = []
    
    for file in uploaded_files:
        if validate_image_file(file):
            valid_files.append(file)
        else:
            invalid_files.append(file)
    
    # Show file list
    col1, col2 = st.columns(2)
    
    with col1:
        if valid_files:
            st.write(f"Valid images: {len(valid_files)}")
            for file in valid_files:
                st.write(f"• {file.name}")
    
    with col2:
        if invalid_files:
            st.warning(f"Invalid files: {len(invalid_files)}")
            for file in invalid_files:
                st.write(f"• {file.name}")
    
    # Show estimated size
    if valid_files:
        estimated_size = estimate_pdf_size(valid_files)
        st.info(f"Estimated PDF size: {estimated_size}")
    
    st.divider()
    
    # Conversion button
    if valid_files:
        if st.button("Convert to PDF", use_container_width=True, type="primary"):
            with st.spinner("Converting images to PDF..."):
                pdf_bytes, error = convert_images_to_pdf(valid_files)
                
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success("PDF created successfully!")
                    
                    st.divider()
                    
                    # Download button
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name="converted_images.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
    else:
        st.warning("Please ensure you have selected at least one valid image file.")
