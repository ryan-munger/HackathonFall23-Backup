__author__='Peter'
import requests
import json


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer API_KEY_HERE"}

def summarizer(text):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": text,  # Pass the input text as a string
    })

    return(output)

if __name__ == "__main__":
    text = input("Enter text to be summarized: ")
    result = summarizer(text)
    print(result)
