__author__ = 'Nick'

import os
from openai import OpenAI
from .math_string import getMathStringAnswer


def ask_word_problem():
    question= input("Enter the word problem: ")
    return answer_word_problem(question)


def answer_word_problem(question: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    query = "Get the mathematical string of how to solve the following word problem:" + question + "Do not use an equal sign, do not put a question mark at the end, do not use words."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system", "content": "You only give numbers and operations that are used to solve a word problem. You never include an equal sign or a question mark as the answer. You always only give one expression. You want it in the form like these: 2 + 2 or 10 - 7 or .05 * 15"
                },
                {
                    "role": "user", "content": query
                },
        ],
    )

    math_string = response.choices[0].message.content 
    print(math_string)
    
    clean_math_str = clean_math_string(math_string)
    print(clean_math_str)

    answer = getMathStringAnswer(clean_math_str, 10).result
    return answer

def clean_math_string(math_str):
    clean_string = math_str
    alphabet = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    number = set("1234567890")
   
   #remove everything after the equal sign
    if "=" in clean_string:
        clean_string = clean_string.split("=")[0]
    
    #remove every character in alphabet
    for i in clean_string:
        if i in alphabet:
            clean_string = clean_string.replace(i, "")
    
    return clean_string

def main():
    print(ask_word_problem())

if __name__ == "__main__":
    main() 



 


