import os
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # fallback to localhost

def main():
    st.title("Decision Maker Discovery System")

    # Sidebar for configuration
    st.sidebar.header("Configuration")
    target_roles = st.sidebar.multiselect(
        "Target Roles",
        ["CEO", "CTO", "COO", "CFO", "CMO", "VP of Sales", "VP of Marketing",
         "Director of Engineering", "Head of Product", "Head of HR"],
        default=["CEO", "CTO", "VP of Sales"]
    )

    # Main content
    tab1, tab2, tab3 = st.tabs(["Add Companies", "Results", "Reports"])

    with tab1:
        st.header("Add Companies to Research")

        # Single company input
        col1, col2 = st.columns([3, 1])
        with col1:
            company_name = st.text_input("Company Name")
        with col2:
            if st.button("Add", key="add_single"):
                if company_name:
                    with st.spinner(f"Processing {company_name}..."):
                        success = process_company(company_name, target_roles)
                    if success:
                        st.success(f"Added {company_name} to research queue")
                    else:
                        st.error(f"Failed to process {company_name}")
                else:
                    st.error("Please enter a company name")

        # Bulk upload
        st.subheader("Bulk Upload")
        uploaded_file = st.file_uploader("Upload CSV with company names", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)
            if st.button("Process All", key="process_bulk"):
                with st.spinner("Processing companies..."):
                    for idx, row in df.iterrows():
                        company_name = row["Company Name"]
                        process_company(company_name, target_roles)
                st.success("All companies processed!")

    with tab2:
        st.header("Decision Makers")

        # Mock data - in real implementation, fetch from Airtable
        data = {
            "Name": ["John Smith", "Sarah Johnson", "Michael Wong"],
            "Title": ["CTO", "VP Marketing", "CEO"],
            "Company": ["Acme Inc", "Acme Inc", "Tech Solutions"],
            "Email": ["john@acme.com", "sarah@acme.com", "michael@techsolutions.com"],
            "Verified": ["Yes", "Yes", "No"],
            "LinkedIn": ["linkedin.com/in/johnsmith", "linkedin.com/in/sarahjohnson", "linkedin.com/in/michaelwong"]
        }
        df = pd.DataFrame(data)

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            company_filter = st.selectbox("Filter by Company", ["All"] + list(df["Company"].unique()))
        with col2:
            title_filter = st.selectbox("Filter by Title", ["All"] + list(df["Title"].unique()))
        with col3:
            verified_filter = st.selectbox("Verified Emails Only", ["All", "Yes", "No"])

        # Apply filters
        filtered_df = df.copy()
        if company_filter != "All":
            filtered_df = filtered_df[filtered_df["Company"] == company_filter]
        if title_filter != "All":
            filtered_df = filtered_df[filtered_df["Title"] == title_filter]
        if verified_filter != "All":
            filtered_df = filtered_df[filtered_df["Verified"] == verified_filter]

        st.dataframe(filtered_df)

        if st.button("Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"decision_makers_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    with tab3:
        st.header("Reports & Analytics")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Companies", "42")
        with col2:
            st.metric("Decision Makers Found", "156")
        with col3:
            st.metric("Verified Emails", "128 (82%)")

        st.subheader("Weekly Report")
        if st.button("Generate Weekly Report"):
            with st.spinner("Generating report..."):
                # Future: Trigger Make.com webhook
                pass
            st.success("Report generated and sent!")

def process_company(company_name, target_roles):
    """Send request to backend to process a single company"""
    payload = {
        "company_name": company_name,
        "target_roles": target_roles
    }

    try:
        response = requests.post(f"{BACKEND_URL}/process_company", json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    main()