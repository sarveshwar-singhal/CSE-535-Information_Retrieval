from flask import Flask
from guess_language import guess_language
import time
import numpy as np
from nltk.stem import PorterStemmer
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

def main():
    # print(guess_language("this is a sentence for sample text detection and see how this works"))
    ps = PorterStemmer()
    t1 = time.time()
    li = np.random.randint(65, 122, 10)
    text = "महिला, महिलाएं"
    sent = text.split(" ")
    for word in sent:
        print(ps.stem(word, to_lowercase=True))
    text = text.encode("ascii", "replace")
    # print("text after encoding:",text)
    text = text.decode()
    print(text)
    # print(ps.stem("महिला, महिलाएं"))
    # print(ps.stem("woman, women"))
    # for num in li:
    #     print(type(li))
    # print(li)
    print(guess_language("एक एक एक एक")=='UNKNOWN')
    # print(guess_language("después"))
    # print(guess_language("this"))


if __name__ == '__main__':
    main()