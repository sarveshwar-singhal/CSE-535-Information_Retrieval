
from flask import Flask, render_template, request as flreq
import urllib.request
import json
from preprocess import Preprocessor

app = Flask(__name__)
EC2_IP = '18.118.18.237'
CORE_NAME = 'IRF21P1'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    user_query = ""
    user_query = "This is sample English query"
    user_query = "इस वाक्य को हिंदी में परिवर्तित करें"
    user_query = 'convierte esta oración a español'
    pp = Preprocessor()
    solr_query = pp.get_query(user_query)
    print(solr_query)
    inurl = 'http://' + EC2_IP + ':8983/solr/' + CORE_NAME + '/select?q='
    inurl += 'text_en:' + solr_query + '%20OR%20text_de:' + solr_query + '%20OR%20text_ru:' + solr_query
    inurl += '&fl=id%2Cscore&wt=json&indent=true&rows=20'
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['data']
    print(docs)


def main():
    user_query = ""
    user_query = "This is sample English query"
    user_query = "इस वाक्य को हिंदी में परिवर्तित करें"
    user_query = 'convierte esta oración a español'
    user_query = 'consumo'
    pp = Preprocessor()
    solr_query = pp.get_query(user_query)
    print(solr_query)
    inurl = 'http://' + EC2_IP + ':8983/solr/' + CORE_NAME + '/select?q='
    inurl += 'tweet_text:' + solr_query
    # + '%20OR%20text_ru:' + solr_query
    # + '%20OR%20text_de:' + solr_query
    inurl += '&fl=id%2Cscore%2Ctweet_text&wt=json&indent=true&rows=20'
    print(inurl)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    print(docs)



if __name__ == '__main__':
    main()
    # app.run(debug=True)