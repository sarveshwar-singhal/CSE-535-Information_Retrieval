# encoding= utf-8
import pickle
import time

from flask import Flask, render_template, request as flreq, json, jsonify
import urllib.request, urllib.parse
from preprocess import Preprocessor
import numpy as np, pandas as pd

app = Flask(__name__)
EC2_IP = '3.17.16.7'
CORE_NAME = 'Project4'

LANG = {'English':'en', 'Hindi':'hi', 'Spanish':'es'}

QUERY_RESULT = pd.DataFrame()
SEARCH_TYPE = 0
SELECTED_LANGUAGE = ''
POI = ''

@app.route('/')
def index():
    return render_template('index1.html')


def solr_search(query):
    global QUERY_RESULT
    inurl = 'http://' + EC2_IP + ':8983/solr/' + CORE_NAME + '/select?q='
    inurl += 'tweet_text:*' + query + '*'
    # + '%20OR%20text_ru:' + solr_query
    # + '%20OR%20text_de:' + solr_query
    field = '*'
    # inurl += '%20AND%20type:r'
    # inurl += '%20&%20type:r'
    # inurl += '%20%26%20type:r'
    inurl += '&fl=' + field + '&wt=json&indent=true&rows=1000'
    print(inurl)
    # exit(10)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    QUERY_RESULT = pd.json_normalize(docs)
    # QUERY_RESULT.drop('_version_', axis=1, inplace=True)
    QUERY_RESULT.drop(['id','text_en','text_es','text_hi','poi_id','_version_'],axis=1, inplace=True)
    # print(QUERY_RESULT.columns)
    # print(QUERY_RESULT)
    # print(docs)
    # return docs


@app.route('/search', methods=["POST", "GET"])
def search():
    pp = Preprocessor()
    global QUERY_RESULT
    global SEARCH_TYPE
    global SELECTED_LANGUAGE
    global POI

    QUERY_RESULT = pd.DataFrame()
    SEARCH_TYPE = 0
    SELECTED_LANGUAGE = ''
    POI = ''

    # user_query = "इस वाक्य को हिंदी में परिवर्तित करें"
    # user_query = 'convierte esta oración a español'
    input_data = json.loads(flreq.data.decode())
    # searchkey = json.jsonify(input_data)
    # print(input_data)
    SEARCH_TYPE = input_data['val']
    if input_data['val'] == 1:
        user_query = input_data['basic']
    else:
        user_query = input_data['adsearch']
    # user_query = input_data['basic']
    solr_query = pp.get_query(user_query)
    print(solr_query)
    solr_search(solr_query)
    result = QUERY_RESULT
    result = result[result['type'] == 'r']
    if input_data['val'] == 2:
        if input_data['languageselected']['name'] != 'Choose..':
            result = result[result['tweet_lang'] == LANG[input_data['languageselected']['name']]]
            SELECTED_LANGUAGE = LANG[input_data['languageselected']['name']]
            print(SELECTED_LANGUAGE)
        if input_data['poiselected']['name'] != 'Choose..':
            result = result[result['poi_name'] == input_data['poiselected']['name']]
            POI = input_data['poiselected']['name']
            print(POI)
    # QUERY_RESULT.to_excel('query_result.xlsx', index=False)
    # formatted_docs = format_data_for_search(docs)
    # print(formatted_docs)
    # print(result)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    # return_json['queryresult'] = pd.DataFrame.to_json(QUERY_RESULT)
    # with open('table-data1.json', 'w') as fp:
    #     json.dump(return_json, fp)
    # with open('data.pickle','wb') as fp:
    #     pickle.dump(formatted_docs, fp, protocol=pickle.HIGHEST_PROTOCOL)
    # return render_template('search.html', docs=formatted_docs)
    # print(return_json)
    return jsonify(return_json)


@app.route('/api/get-news-result', methods=["POST", "GET"])
def news():
    # time.sleep(5)
    global QUERY_RESULT
    global SEARCH_TYPE
    global SELECTED_LANGUAGE
    # print(input_data)
    result = QUERY_RESULT
    result = result[result['type'] == 'n']
    if SEARCH_TYPE == 2:
        if SELECTED_LANGUAGE != '':
            result = result[result['tweet_lang'] == SELECTED_LANGUAGE]
    # QUERY_RESULT.to_excel('query_result.xlsx', index=False)
    # formatted_docs = format_data_for_search(docs)
    # print(formatted_docs)
    # print(result)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    # return_json['queryresult'] = pd.DataFrame.to_json(QUERY_RESULT)
    # print(return_json)
    return jsonify(return_json)


@app.route('/api/get-general-result', methods=["POST","GET"])
def general():
    global QUERY_RESULT
    global SELECTED_LANGUAGE
    result = QUERY_RESULT
    result = result[result['type'] == 're']
    if SELECTED_LANGUAGE != '':
        result = result[result['tweet_lang'] == SELECTED_LANGUAGE]
    print(result)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    return jsonify(return_json)


@app.route('/api/get-chart-result')
def chart1():
    # time.sleep(5)
    global QUERY_RESULT
    global SEARCH_TYPE
    global POI
    global SELECTED_LANGUAGE
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    poi = result[result['type'] == 'r']
    print(poi)
    if POI != '':
        poi = poi[poi['poi_name'] == POI]
    if SELECTED_LANGUAGE != '':
        poi = poi[poi['tweet_lang'] == SELECTED_LANGUAGE]
    li = []
    for i in poi['sentiment']:
        # print(type(i))
        li.append(round(float(i), 5))
        # print(round(float(i), 5))
    # poi['sentiment'] = li
    # poi.loc[:,'sentiment'] = li
    poi = poi.assign(sentiment=li)
    # print(poi)
    ind = poi.groupby('poi_name').describe().index
    print(ind)
    graph_data = []
    for i in ind:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['poi_name'] == i]
        data['poi_name'] = i
        data['count'] = temp['sentiment'].mean()
        # print(data)
        graph_data.append(data)
    print(graph_data)
    return jsonify(graph_data)


@app.route('/api/get-chart-result1')
def chart2():
    global QUERY_RESULT
    global SELECTED_LANGUAGE
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    poi = result[result['type'] == 'r']
    if SELECTED_LANGUAGE != '':
        poi = poi[poi['tweet_lang'] == SELECTED_LANGUAGE]
    # poi = result
    # print(poi)
    lang = poi.groupby('tweet_lang').describe().index
    graph_data = []
    for i in lang:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['tweet_lang'] == i]
        data['language'] = i
        data['count'] = int(temp['tweet_lang'].count())
        # print(data)
        graph_data.append(data)
    # print(graph_data)
    return jsonify(graph_data)


@app.route('/api/get-chart-result2')
def chart3():
    global QUERY_RESULT
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    # poi = result[result['type'] == 'r']
    # print(poi)
    poi = result
    lang = poi.groupby('country').describe().index
    graph_data = []
    for i in lang:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['country'] == i]
        data['country'] = i
        data['count'] = int(temp['country'].count())
        # print(data)
        graph_data.append(data)
    # print(graph_data)
    return jsonify(graph_data)


def format_data_for_search(data):
    final_li = []
    for i in range(len(data)):
        temp_dic = data[i]
        temp_dic.pop('id')
        final_li.append(temp_dic)
    return final_li


def main():
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


@app.route('/advance_search', methods=["POST"])
def advance_search():
    lang = flreq.form.get('lang')
    poi = flreq.form.get('poi')
    user_query = flreq.form.get("search")
    other_param = ''
    if not lang:
        other_param += '&tweet_lang='+lang
    if not poi:
        other_param += '&poi_name='+poi
    pp = Preprocessor()
    solr_query = pp.get_query(user_query)
    docs = solr_search(solr_query, other_param)
    return render_template('search.html', docs=docs)


def temp_chart1():
    # time.sleep(5)
    searchkey = flreq.args.get('searchkey')
    global QUERY_RESULT
    print("inside chart1")
    print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    gk = result[result['type'] == 'r'].groupby('poi_name')
    print(gk.describe()['sentiment'].columns)
    # print(gk.describe()['sentiment']['count']/gk.describe()['sentiment']['freq'])
    g1 = gk.describe()['sentiment']['mean']
    g1 = g1.reset_index()
    graph_data = []
    d1 = {}
    for i in range(len(g1)):
        d1['poi_name'] = g1.iloc[i, 0]
        d1['count'] = g1.iloc[i, 1]
        graph_data.append(d1)
    print(graph_data)
    return jsonify(graph_data)

def save_file():
    li = [{'id': '1453227473668296722', 'tweet_text': 'RT @mansukhmandviya: आज मैं राज्यों के स्वास्थ्य मंत्रियों से मिल रहा हूं। कोविड टीकाकरण, इमरजेंसी कोविड पैकेज व अन्य मुद्दों पर विस्तार से…', 'score': 3.7479284},
          {'id': '1426926048499798019', 'tweet_text': 'कोविड से आज़ाद होंगे हम।\n\n#Unite2FightCorona https://t.co/WjGOZy7V3E', 'score': 3.6021595},
          {'id': '1459038035866124292', 'tweet_text': 'RT @OfficeOf_MM: प्रधानमंत्री जी ने कभी नहीं कहा कि कोविड-19 चला गया है। उन्होंने हमेशा यह कहा कि कोविड-19 नियंत्रण में है, इसलिए हमें साव…', 'score': 3.5865898},
          {'id': '1401412953967050755', 'tweet_text': 'ब्लू टिक के लिए मोदी सरकार लड़ रही है-\nकोविड टीका चाहिए तो आत्मनिर्भर बनो!\n\n#Priorities', 'score': 3.1287215},
          {'id': '1463380065748668417', 'tweet_text': 'कांग्रेस पार्टी की दो माँग हैं-\n1. कोविड मृतकों के सही आँकड़े बताए जायें।\n2. अपने प्रियजनों को कोविड में खो चुके परिवारों को चार लाख हरजाना दिया जाए।\n\nसरकार हो तो जनता का दुख दूर करना होगा,\nहरजाना मिलना चाहिए, #4LakhDenaHoga https://t.co/aEPO7XVxyJ', 'score': 3.0318995},
          {'id': '1453227040694542336', 'tweet_text': "आज मैं राज्यों के स्वास्थ्य मंत्रियों से मिल रहा हूं। कोविड टीकाकरण, इमरजेंसी कोविड पैकेज व अन्य मुद्दों पर विस्तार से चर्चा होगी।\n\nहाल ही में प्रधानमंत्री @NarendraModi जी द्वारा लॉंच की गयी 'PM आयुष्मान भारत हेल्थ इंफ्रास्ट्रक्चर मिशन' योजना पर भी बात होगी।", 'score': 3.0318995},
          {'id': '1426195379293278210', 'tweet_text': '8 जुलाई को कैबिनेट द्वारा घोषित ₹23,123 करोड़ के ‘इमरजेंसी कोविड रिस्पांस पैकेज’-ECRP II के तहत राज्यों एवं UTs को 50% अग्रिम भुगतान का अनुमोदन किया गया।\n\nइस राशि से राज्यों एवं UTs को कोविड संबंधित सुविधाओं को सुदृढ़ करने में मदद मिलेगी\n\nhttps://t.co/Q6ZSgxSVja', 'score': 2.9777198},
          {'id': '1388080831009333248', 'tweet_text': 'कोविड की दूसरी लहर\nका चौथा सप्ताह \n2 लाख से ज़्यादा मृतक\nजवाबदेही ज़ीरो\n\nकर दिया सिस्टम ने ‘आत्मनिर्भर’!', 'score': 2.9618845}, {'id': '1434804595696422915', 'tweet_text': 'सुरक्षा उनकी, जो हमें सुरक्षित रखते है।\n\nकच्छ में तैनात सुरक्षा बलों का पूर्ण टीकाकरण एवं उनके परिवार को कोविड से बचाव के लिये वैक्सीन की पहली डोज़ लगाई जा चुकी है।\n\nकोविड महामारी के विरुद्ध लड़ाई में सरकार ने यह महत्वपूर्ण उपलब्धि हासिल की है। https://t.co/yPq5Okinqb', 'score': 2.9254427},
          {'id': '1382907374063738883', 'tweet_text': 'केंद्र सरकार की कोविड रणनीति-\n\nस्टेज 1- तुग़लक़ी लॉकडाउन लगाओ।\n\nस्टेज 2- घंटी बजाओ।\n\nस्टेज 3- प्रभु के गुण गाओ।', 'score': 2.9101574},
          {'id': '1406883733630644224', 'tweet_text': 'आज गांधीनगर लोकसभा क्षेत्र में कोविड टीकाकरण केंद्रों का निरीक्षण किया। प्रदेश सरकार द्वारा सभी केंद्रों पर कोविड प्रोटोकॉल के तहत समुचित व्यवस्थाएं की गई है। मैं सभी से वैक्सीन लगवाने की अपील करता हूँ।\n\nमोदी सरकार देश के सभी नागरिकों के नि:शुल्क टीकाकरण के लिए कृतसंकल्प है। https://t.co/ETqc7eJHiq', 'score': 2.8749695},{'id': '1466711613965160450', 'tweet_text': 'RT @OfficeOf_MM: कोविड के दौरान जरूरी प्रोटोकॉल मेडिसिन उपलब्ध कराने के लिए सरकार ने रात-दिन काम किया है : डॉ @MansukhMandviya', 'score': 2.8602057},{'id': '1304647836886327296', 'tweet_text': "कोविड के ख़िलाफ़ मोदी सरकार की 'सुनियोजित लड़ाई' ने भारत को मुसीबतों की खाई में धकेल दिया:\n\n1. GDP में 24% की ऐतिहासिक कमी\n2. 12 करोड़ नौकरियाँ खोयीं\n3. 15.5 लाख करोड़ अतिरिक्त तनावग्रस्त क़र्ज़\n4. विश्व में कोविड के सर्वाधिक दैनिक केस-मौतें\n\nलेकिन GOI व मीडिया कहें ‘सब चंगा सी’।", 'score': 2.8262086},{'id': '1430881563894452228', 'tweet_text': 'विषम परिस्थितियों, कठिन रास्तों और प्रतिकूल वातावरण के कारण जहां टीकाकरण कठिन था, उन क्षेत्रों में क्लस्टर आधारित नीति बनाने से टीकाकरण की गति में तेजी आई है।\n\nकोविड से सुरक्षा देने के लिये अपने इन कोविड वॉरियर्स के प्रति मैं ह्रदय से आभार और धन्यवाद व्यक्त करता हूँ। https://t.co/3T8uMAGXlu', 'score': 2.8262086},{'id': '1466725763495854084', 'tweet_text': 'RT @sansad_tv: "भारत दुनिया का सबसे बड़ा #VaccinationDrive चला रहा है-  सबको वैक्सीन, मुफ्त वैक्सीन"\n\n#LokSabha में नियम 193 के अधीन कोविड-…', 'score': 2.8119402},{'id': '1462019419979145222', 'tweet_text': 'RT @COVIDNewsByMIB: #IndiaFightsCorona \n\n📍क्या #कोविड19 टीकाकरण पुरुषों और महिलाओं में संतानहीनता का कारण बन सकता है ❓\n\n➡️कोविड वैक्सीन से…', 'score': 2.8119402},{'id': '1461263161714118657', 'tweet_text': 'RT @mansukhmandviya: मम्मी पापा भूल न जाना\nकोविड टीके का दूसरा डोज जरूर लगवाना! \n\nटीकाकरण हेतु जागरूकता फैलाने का innovative तरीक़ा\n\n#HarGh…', 'score': 2.8119402},{'id': '1457956242886836227', 'tweet_text': 'RT @mansukhmandviya: बिहार के सिवान ज़िले में #HarGharDastak अभियान के तहत किसानों को खेतों में ही कोविड टीके लगाए गये। हमारे स्वास्थ्यक…', 'score': 2.8119402},{'id': '1450802327875506182', 'tweet_text': 'RT @MoHFW_INDIA: #LargestVaccineDrive \n\nकोविड महामारी के दौरान कई ऐसे साहसिक चेहरे सामने आए हैं जिनकी मदद से घर-घर तक वैक्सीन लगवाने सम्बं…', 'score': 2.7652764},{'id': '1467802678071676934', 'tweet_text': 'RT @narendramodi: बहुत-बहुत बधाई @jairamthakurbjp जी। कोविड के खिलाफ लड़ाई में हिमाचलवासियों ने पूरे देश के सामने एक अनुकरणीय उदाहरण पेश कि…', 'score': 2.7652764}]
    with open('data.pickle', 'wb') as fp:
        pickle.dump(li, fp, protocol=pickle.HIGHEST_PROTOCOL)

def garbage_solr_search(query, other_param = None, type_query = None):
    inurl = 'http://' + EC2_IP + ':8983/solr/' + CORE_NAME + '/select?q='
    inurl += 'tweet_text:' + '"' + query + '"'
    # + '%20OR%20text_ru:' + solr_query
    # + '%20OR%20text_de:' + solr_query
    field = 'id%2Cpoi_name%2Ccountry%2Ctweet_text%2Ctweet_lang%2Chashtags%2Ctweet_urls%2Ctweet_date'
    # field = '*'
    # inurl += '%20AND%20type:r'
    # inurl += '%20&%20type:r'
    # inurl += '%20%26%20type:r'
    if type_query:
        inurl += ',%0Atype:"' + type_query + '"'
    if other_param or other_param != '':
        # other_param = urllib.parse.quote(other_param)
        inurl += other_param
        inurl += '&q.op=AND'
    inurl += '&fl=' + field + '&wt=json&indent=true&rows=100'
    print(inurl)
    # exit(10)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    # print(docs)
    return docs


if __name__ == '__main__':
    # main()
    app.run(debug=True)