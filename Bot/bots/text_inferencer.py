__author__ = 'Ryan'
import requests
import json

class Answer(object):
    def __init__(self, score, start, end, answer):
        self.score = score
        self.start = start
        self.end = end
        self.result = answer

API_URL = "https://api-inference.huggingface.co/models/Falconsai/question_answering_v2"
headers = {"Authorization": f"Bearer API_KEY_HERE"}

# USAGE: pass in what you are looking for and the text you are looking in
# returns an answer object. to get the answer it self use the .result property
def inferencer(question, context):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": {
            "question": question,
            "context": context
        },
    })

    # j = json.loads(output)
    ans = Answer(**output)
    return(ans)

def main():
    print(inferencer('Where was President Taft Born?', 'William Howard Taft (September 15, 1857 - March 8, 1930) was an American politician and lawyer who was the 27th president of the United States (1909-1913) and the tenth chief justice of the United States (1921–1930), the only person to have held both offices. Taft was elected president in 1908, the chosen successor of Theodore Roosevelt, but was defeated for reelection in 1912 by Woodrow Wilson after Roosevelt split the Republican vote by running as a third-party candidate. In 1921, President Warren G. Harding appointed Taft to be chief justice, a position he held until a month before his death. Taft was born in Cincinnati, Ohio, in 1857. His father, Alphonso Taft, was a U.S. attorney general and secretary of war. Taft attended Yale and joined the Skull and Bones, of which his father was a founding member. After becoming a lawyer, Taft was appointed a judge while still in his twenties. He continued a rapid rise, being named solicitor general and a judge of the Sixth Circuit Court of Appeals. In 1901, President William McKinley appointed Taft civilian governor of the Philippines. In 1904, Roosevelt made him Secretary of War, and he became Roosevelt\'s hand-picked successor. Despite his personal ambition to become chief justice, Taft declined repeated offers of appointment to the Supreme Court of the United States, believing his political work to be more important. With Roosevelt\'s help, Taft had little opposition for the Republican nomination for president in 1908 and easily defeated William Jennings Bryan for the presidency in that November\'s election. In the White House, he focused on East Asia more than European affairs and repeatedly intervened to prop up or remove Latin American governments. Taft sought reductions to trade tariffs, then a major source of governmental income, but the resulting bill was heavily influenced by special interests. His administration was filled with conflict between the Republican Party\'s conservative wing, with which Taft often sympathized, and its progressive wing, toward which Roosevelt moved more and more. Controversies over conservation and antitrust cases filed by the Taft administration served to further separate the two men. Roosevelt challenged Taft for renomination in 1912. Taft used his control of the party machinery to gain a bare majority of delegates and Roosevelt bolted the party. The split left Taft with little chance of reelection, and he took only Utah and Vermont in Wilson\'s victory.').result)
    print(inferencer('What was the magician\'s name?', 'There was a magic show ran by the great magicain Mr. Peter Arvanitis!').result)

# main()