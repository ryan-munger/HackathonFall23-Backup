__author__='Peter'
import language_tool_python

def correct_grammar(input_text):
    tool = language_tool_python.LanguageTool('en-US')

    # Check for grammatical errors
    matches = tool.check(input_text)

    # If there are errors, correct them
    if matches:
        corrected_text = tool.correct(input_text)
        return corrected_text
    else:
        return "No grammatical errors found."

if __name__ == "__main__":
    user_input = input("Enter a sentence: ")
    corrected_sentence = correct_grammar(user_input)
    print("Corrected Sentence:")
    print(corrected_sentence)