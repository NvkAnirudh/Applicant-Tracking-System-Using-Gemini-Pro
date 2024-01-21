# A field to put job description
# upload pdf
# pdf to image --> processing --> Google Gemini Pro
# Prompt template 

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import json
import PyPDF2 as pdf
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(input)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    else:
        raise FileNotFoundError('No File Uploaded')
    
# Streamlit app
st.set_page_config(page_title='ATS')
st.text("Improve your Resume")
st.header('Applicant Tracking System')
jd = st.text_area('Job Description:',key='input')

uploaded_file = st.file_uploader('Upload Your Resume(in PDF format)',type=['pdf'],help='Please upload the required pdf')

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit = st.button('Submit')

input_prompt = """
Hey, can you act like a skilled or very experienced ATS(Application Tracking System) with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide 
best assistance for improving the resume. Assign the percentage Matching based on job description and the missing technical keywords from job description with high accuracy
resume:{text}
description:{jd}

I want the response in the following structure:
"JD Match":"%"
"MissingKeywords:[]"
"Profile Summary":""
"""

if submit:
    if uploaded_file is not None:
        text = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader('Response:')
        st.write(response)
    else:
        st.write('Please upload the resume')



