import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
# getting the api key from the environment
gemini_api_key = os.getenv("GOOGLE_API_19jan_key1")
# Let's configure the model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",
                               api_key=gemini_api_key,
                               temperature=0.7)
# Design the UI of the application
st.title(":orange[Healthify Me:] :blue[your personal health assistant]")
st.markdown("##### Ask any health-related questions and get instant personalised answers!")
st.write('''
Follow these steps,
* Enter your details in the sidebar and click on the submit button first before proceeding.
* Then, ask any health-related question in the text area and click 'Generate Report' and relax!!!.
''')

# Design the sidebar for all the user parameters
st.sidebar.header(":red[ENTER YOUR DETAILS]")
name = st.sidebar.text_input('Enter your Name')
gender = st.sidebar.selectbox('Select your Gender', ['Male', 'Female', 'Other'])
age = st.sidebar.number_input('Enter your Age', min_value=1, max_value=120)
weight = st.sidebar.text_input('Enter your Weight (in kg)')
height = st.sidebar.text_input('Enter your Height (in cm)')
bmi = pd.to_numeric(weight) / ((pd.to_numeric(height) / 100) ** 2)
active = st.sidebar.slider('Rate your activity[0 - 5]',0,5,1)
fitness = st.sidebar.slider('Rate your fitness level[0 - 5]',0,5,1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, Your BMI is: {round(bmi,2)} Kg/m^2")
# Lets use gemini model to generate the report
user_input = st.text_area("Enter your health-related question here:")
prompt = f'''<Role> You are an expert in health and wellness and has 10+ years experience in guiding people.
<Goal> Generate the customised report addressing the problem the user has asked. 
Here, is the question that user has asked :{user_input}.
<Context>Here are the details that the user has provided.
name = {name}
age = {age}
height = {height}
weight = {weight}
gender = {gender}
bmi = {bmi}
activity rating (0-5) = {active}
fitness rating (0-5) = {fitness}
<format> Following should be the outline in the sequence provided,
* Start with the 2-3 line of comment on the details that the user has provided.
* Explain what the real problem could be on the basis of input the user has provided.
* Suggest the possible reasons for the problem.
* What are the possible solutions.
* Mention the doctor from which specialisation can be visited if required.
* Mention any change in the diet which is required.
* At last, create a final brief summary of all the points that has ben discussed in the report.
<Instruction> 
* Use bullet points wherever required.
* Create tables to represent any data wherever possible.
* Strictly do not advice any medicine.'''
if st.button('Generate Report'):
    response = model.invoke(prompt)
    st.write(response.content)
 
