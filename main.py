"""
Whatsapp Stats - Multi-Page Streamlit Application
Main entry point and home page of the application.
"""

import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="Whatsapp Stats",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom sidebar header
st.sidebar.markdown("""
---
### Tools
---
""")

# Page title and welcome message
st.title("Whatsapp Stats")
st.markdown("### Your All-in-One Utility Application")

st.divider()

# Introduction section
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Welcome to Whatsapp Stats")
    st.write(
        """
        Whatsapp Stats is a comprehensive utility application designed to help you with two primary tasks:
        
        1. **Analyze WhatsApp chat exports** and generate detailed statistics about message counts and user activity
        2. **Convert multiple images** into a single, organized PDF document
        
        Whether you're managing group conversations or organizing digital documents, 
        this application provides simple, efficient tools for your needs.
        """
    )

with col2:
    st.info(
        """
        **Quick Navigation:**
        
        Use the sidebar to access:
        - WhatsApp Message Counter
        - Image to PDF Converter
        
        Or continue reading for more information about each feature.
        """
    )

st.divider()

# Features section
st.header("Available Features")

# Feature 1: WhatsApp Message Counter
st.subheader("1. WhatsApp Message Counter")

feat_col1, feat_col2 = st.columns([1, 1])

with feat_col1:
    st.write(
        """
        **What it does:**
        Analyze your WhatsApp chat exports and get detailed statistics about message counts by user.
        
        **Key capabilities:**
        - Count total messages per user
        - Search for specific keywords or phrases
        - Filter messages by date range
        - Identify most active members
        - Export results as text files
        """
    )

with feat_col2:
    st.write(
        """
        **Supported functionality:**
        - Parse WhatsApp text exports
        - Preserve message timestamps
        - Track first message of each user
        - Sort users by activity level
        - Download formatted reports
        
        **Perfect for:**
        - Group chat analytics
        - Finding specific conversations
        - Understanding participation patterns
        - Archiving statistics
        """
    )

st.divider()

# Feature 2: Image to PDF Converter
st.subheader("2. Image to PDF Converter")

feat_col3, feat_col4 = st.columns([1, 1])

with feat_col3:
    st.write(
        """
        **What it does:**
        Convert multiple image files into a single, organized PDF document in seconds.
        
        **Key capabilities:**
        - Upload multiple images at once
        - Automatic format conversion (JPG, PNG to PDF)
        - Preserve image quality
        - Control image ordering
        - Enable easy sharing and storage
        """
    )

with feat_col4:
    st.write(
        """
        **Supported formats:**
        - JPG / JPEG files
        - PNG files
        - Single or multiple images
        
        **Perfect for:**
        - Scanning document collections
        - Creating photo albums
        - Organizing receipts or invoices
        - Preparing documents for printing
        - Merging multiple scans
        """
    )

st.divider()

# How to use section
st.header("Getting Started")

col_howto1, col_howto2 = st.columns(2)

with col_howto1:
    st.subheader("WhatsApp Message Counter")
    with st.expander("Step-by-step guide", expanded=False):
        st.write(
            """
            **Step 1: Export your chat**
            - On iPhone: Open chat → Contact info → Export Chat → Without Media
            - On Android: Open chat → Menu → More → Export Chat → Without Media
            
            **Step 2: Navigate to the feature**
            - Click "WhatsApp Message Counter" in the sidebar
            
            **Step 3: Upload and configure**
            - Upload your .txt export file
            - View group information
            - Set date range (optional)
            - Enter keyword to search (optional)
            
            **Step 4: Analyze**
            - Click "Generate Statistics" button
            - Review the results
            - Download the report if needed
            """
        )

with col_howto2:
    st.subheader("Image to PDF Converter")
    with st.expander("Step-by-step guide", expanded=False):
        st.write(
            """
            **Step 1: Prepare images**
            - Gather images in JPG or PNG format
            - Keep them in desired order (alphabetical or numbered)
            
            **Step 2: Navigate to the feature**
            - Click "Image to PDF Converter" in the sidebar
            
            **Step 3: Upload**
            - Click file uploader
            - Select one or more image files
            - Images will be listed for verification
            
            **Step 4: Convert**
            - Review estimated PDF size
            - Click "Convert to PDF" button
            - Download the generated PDF file
            """
        )

st.divider()

# FAQ Section
st.header("Frequently Asked Questions")

faq_col1, faq_col2 = st.columns(2)

with faq_col1:
    st.subheader("WhatsApp Counter FAQ")
    
    with st.expander("What formats are supported?"):
        st.write("Only .txt files exported directly from WhatsApp are supported.")
    
    with st.expander("Can I search for multiple keywords?"):
        st.write("Currently, you can search for one keyword at a time. Leave empty for overall statistics.")
    
    with st.expander("Is my data stored?"):
        st.write("No. All data is processed locally and immediately discarded after analysis.")

with faq_col2:
    st.subheader("Image Converter FAQ")
    
    with st.expander("What image formats work?"):
        st.write("JPG, JPEG, and PNG formats are supported. Other formats will be skipped.")
    
    with st.expander("What's the file size limit?"):
        st.write("There's no strict limit, but very large files may take longer to process.")
    
    with st.expander("How is image order determined?"):
        st.write("Images are processed in alphabetical order of filename by default.")

st.divider()

# Technical Information
st.header("Technical Information")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.subheader("Architecture")
    st.write(
        """
        - Multi-page Streamlit application
        - Modular utility structure
        - Clean separation of concerns
        - Optimized for performance
        """
    )

with tech_col2:
    st.subheader("Data Privacy")
    st.write(
        """
        - No data storage
        - No external uploads
        - Local processing only
        - Files not retained
        - GDPR compliant
        """
    )

with tech_col3:
    st.subheader("Technologies")
    st.write(
        """
        - Streamlit (web framework)
        - Pillow (image processing)
        - Python 3.8+
        - Pure Python implementation
        """
    )

st.divider()

# Footer
st.write("")
st.markdown(
    """
    ---
    **Whatsapp Stats** | Multi-purpose Utility Application  
    Version 2.1 | April 2026
    """
)

# Sidebar footer
st.sidebar.markdown(
    """
    ---
    **Version:** 2.1  
    **Built with:** Streamlit  
    **Privacy:** Local processing only
    """
)
