#This app will scrape a website and suggest and then build an email campaign for the user. 
#It uses streamilt, openai and beautifulsoup libraries.

import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
import myemail

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")


def scrape_website(url):
    """Scrape website content from the given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting text from the webpage; this might need adjustments
        # depending on the website's structure
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        return text
    except Exception as e:
        return f"An error occurred: {e}"
    

def summarize_text(text, purpose):
    """Summarize the given text to a specified maximum word length using OpenAI."""
    response = openai.chat.completions.create(
    model="gpt-4-1106-preview",  # or another suitable model
        messages=[
        {   "role": "system",
        "content" : "You are the best digital marketing agency. You are helping your client to create the most effective email campaign",
            "role":"user",
        "content": f"Based on the client's website {text} and the purpose of the email campaign is {purpose}, create the most effective email campaign for the client. Need to create a series of emails",
        
        }
    ]
    )
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title('Email Campaign Generator')
    content = ""    
    summary = ""
    # User choice for input type
    name = st.text_input("Enter your company name")
    website_url = st.text_input("Enter the website URL to summarize:")
    if website_url:
        with st.spinner('Scraping website content...'):
            content = scrape_website(website_url)
            if not content:
                st.error("Failed to scrape the website or the website is empty.")

    purpose = st.text_area("Enter what you are trying to achieve with this email campaign:")

    if st.button('Generate Email Campaign'):
        if content and content.strip():
            with st.spinner('Email Campaign content generation...'):
                summary = summarize_text(content, purpose)
            st.success("Summary generated successfully!")
            st.write(summary)
        else:
            st.error("Please enter a valid URL or text to summarize.")
            
        if summary and summary.strip():
            myemail.send_email(summary)
        else:
            st.error("Failed to generate email content.")


if __name__ == "__main__":
    main()