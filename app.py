# A field to put job description
# upload pdf
# pdf to image --> processing --> Google Gemini Pro
# Prompt template 

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(prompt, pdf_content, input):
    model = genai.GenerativeModel('gemini-pro-vision')

    response = model.generate_content([prompt, pdf_content[0], input])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Converting the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Converting the image to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format='JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(image_byte_arr).decode() 
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError('No File Uploaded')
    
# Streamlit app
st.set_page_config(page_title='ATS')
st.header('Applicant Tracking System')
input_text = st.text_area('Job Description:',key='input')

uploaded_file = st.file_uploader('Upload Your Resume(in PDF format)',type=['pdf'])

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit1 = st.button('Percentage Match (Resume Score)')
submit2 = st.button('What are the important keywords that are missing in the resume')

input_prompt1 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. The ouput should consist the percentage sccore only.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. The ouput should contain both the percentage score and the keywords that are missing. 
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader('Response:')
        st.write(response)
    else:
        st.write('Please upload the resume')

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader('Response:')
        st.write(response)
    else:
        st.write('Please upload the resume')



