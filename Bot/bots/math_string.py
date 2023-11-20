__author__ = 'Ryan'
import requests
import json

class Answer(object):
    def __init__(self, result, error):
        self.result = result
        self.error = error

# usage: pass in array of mathematical equations and/or conversions
# outputs an answer object, get the answer using the .result property
def getMathStringAnswer(questions, precision):
    url = 'http://api.mathjs.org/v4'
    reqObj = {'expr': questions, 'precision': precision}

    response = requests.post(url, json = reqObj)
    res = response.text
    j = json.loads(res)
    ans = Answer(**j)
    return ans

def main():
    question = ""
    questions = []

    while (question != "exit"):
        questions.append(question)
        question = input("Please enter your expression or conversion below. \nExamples: a = 1.2 * sin(13), or 32 miles in km \nType 'exit' to stop.\n")
    questions.pop(0)

    precision = input("What is the desired precision (how many digits in output): ")

    ans = getMathStringAnswer(questions, precision)

    print("\n")
    if (ans.error == None):
        for i in range(len(questions)):
            print(f'{questions[i]:30} ==> {ans.result[i]:30}')
    print("\n")

# main()