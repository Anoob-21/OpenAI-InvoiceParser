# Description: This file contains  code for streamlit  application which is used to extract invoice data from pdf files.
import streamlit as st
from dotenv import load_dotenv
from utils import *


def main():
    load_dotenv()

    st.set_page_config(page_title="Invoice Parser Agent")
    st.title("Invoice Extraction Bot 🤖")
    st.subheader("I can help you in extracting invoice data")
    

    # Upload the Invoices (pdf files)
    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)
    

    submit=st.button("Extract Data")

    if submit:
        with st.spinner('Wait for extraction to complete...🔄'):
            df=create_docs(pdf)
            st.write(df.head())

            data_as_csv= df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV", 
                data_as_csv, 
                "ConsolidatedInvoices.csv",
                "text/csv",
                key="ConsolidatedInvoices-csv",
            )
        st.success("Extraction complete")


#Invoking main function
if __name__ == '__main__':
    main()
