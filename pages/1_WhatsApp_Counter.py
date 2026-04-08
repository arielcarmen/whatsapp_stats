"""
WhatsApp Message Counter Page
This page allows users to analyze their WhatsApp chat exports.
"""

import streamlit as st
from utils.analyzer import (
    extract_group_details,
    get_date_range,
    analyze_messages,
    generate_analysis_report
)

# Configure page metadata
st.set_page_config(
    page_title="WhatsApp Counter",
    layout="wide"
)

st.title("WhatsApp Message Counter")
st.write("Analyze your WhatsApp chat exports and get detailed statistics about message counts by user.")

st.divider()

# File upload section
st.subheader("Upload Your Chat Export")
st.write("Export your WhatsApp chat as a text file (.txt) and upload it here.")

file = st.file_uploader("Choose your WhatsApp chat export file:", type=["txt"])

# Process the uploaded file
if file is not None:
    st.success("File uploaded successfully!")
    st.divider()
    
    # Extract group details
    group_infos, group_name = extract_group_details(file)
    
    if group_infos:
        st.subheader("Group Information")
        st.info(f"{group_infos}")
    else:
        group_name = "WhatsApp Group"
    
    st.divider()
    
    # Get available date range
    date_min, date_max = get_date_range(file)
    
    if date_min and date_max:
        st.subheader("Filter Messages")
        
        col1, col2 = st.columns(2)
        with col1:
            date_start = st.date_input(
                "Start date",
                value=date_min,
                min_value=date_min,
                max_value=date_max
            )
        with col2:
            date_end = st.date_input(
                "End date",
                value=date_max,
                min_value=date_min,
                max_value=date_max
            )
        
        # Keyword search
        keyword = st.text_input(
            "Keyword search (leave empty for overall statistics)",
            "",
            help="Search for a specific word or phrase"
        )
        
        st.divider()
        
        # Analysis button
        if st.button("Generate Statistics", use_container_width=True, type="primary"):
            with st.spinner("Analyzing messages..."):
                # Analyze messages
                results, timestamps = analyze_messages(file, keyword, date_start, date_end)
                
                if results:
                    # Generate report
                    report = generate_analysis_report(results, group_name, keyword, timestamps)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    st.text(report)
                    
                    # Download button
                    st.download_button(
                        label="Download Report as TXT",
                        data=report,
                        file_name=f"{group_name}_export.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.warning("No messages found with the specified filters.")
    else:
        st.error("Could not extract date range from the file. Please ensure it's a valid WhatsApp export.")
else:
    st.info("Please upload a WhatsApp chat export file to get started.")
