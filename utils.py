from os import write
from langchain.llms import OpenAI
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
import pandas as pd
import re
import streamlit as st
from langchain.prompts import PromptTemplate

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#Function to extract data from text
def extracted_data(pages_data):

    template = """ 
        Remove any $ symbols.
        Extract  the following values  in a JSON format : Invoice,Date, Description, Quantity, 
        Unit Price , Amount, Total, Email and Phone Number  from this data: {pages}.
        
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)
    llm = OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))
    
    #print("Full Response")
    #print(full_response)
    
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    
    
    df = pd.DataFrame({'Invoice': pd.Series(dtype='str'),
                       'Description': pd.Series(dtype='str'),
		               'Date': pd.Series(dtype='str'),
                       'Quantity': pd.Series(dtype='str'),
                       'Unit Price': pd.Series(dtype='str'),
                       'Amount': pd.Series(dtype='int'),
                       'Total': pd.Series(dtype='str'),
                       'Email': pd.Series(dtype='str'),
                       'Phone Number': pd.Series(dtype='str')
                        
                    })
    
    for filename in user_pdf_list:
        
        print("filename")
        print(filename)
        raw_data=get_pdf_text(filename)
        #st.write("RAWDATA:..."+raw_data)
        #print("extracted raw data")
        #print(raw_data)
        
        llm_extracted_data=extracted_data(raw_data)
        #st.write("LLMDATA..."+llm_extracted_data)
        # Write code to append the extracted data to the dataframe
       # df = df.append(llm_extracted_data, ignore_index=True)
        #print("DF start")
       # print(df)
        
        print("llm extracted data")
        #Adding items to our list - Adding data & its metadata
        print(llm_extracted_data)
        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
             # Escape quotes in the extracted text
            #extracted_text = extracted_text.replace('"', '\\"').replace("'", "\\'")
            # Converting the extracted text to a dictionary
            # Remove line continuation characters
            #extracted_text = extracted_text.replace('\\', '')
            #print("********************Extracted Text***************")
            #print(extracted_text)
            
            #print("********************Data Dict***************")
            data_dict = eval('{' + extracted_text + '}')
            #print(data_dict)
            #Convert data_dict to a dataframe
           # df = pd.DataFrame.from_dict(data_dict, orient='index').T
            #print("********************Data Dict End***************")
           
        else:
            print("No match found.")
            data_dict = {}
            
        #print("********************DF Final start***************")       
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
        #print(df)
        #print("********************DF Final End***************")
    #df = pd.concat([df, pd.DataFrame.from_dict(data_dict)])
    #df= pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)
    #df = pd.concat([df, pd.DataFrame.from_dict(data_dict, orient='columns', index=[0])])
    #df = pd.concat([df, pd.DataFrame({k: [v] for k, v in data_dict.items()})])
       
    
        # Create a DataFrame from the dictionary
        # If the dictionary values are not lists, convert them to lists
        
        #df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head()
    return df