# Pip freeze > requirements.txt
# Pip install -r requirements.txt
from flask import Flask, request, jsonify
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language


app = Flask(__name__)

@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('language_detector')


@app.route('/')
def home():
    return render_template('index.html')

def language_out(id,doc):
    lan = doc._.language
    return {"Index": id, "LanguageCode": lan['language'], "Score": lan['score']}

class AppError(Exception):
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return self.message


@app.route('/language_detect', methods=['POST'])
def language_detect():
    # text = request.json['Comment']
    queries = request.json['TextList']
    lanDict = {}
    languages = []
    if len(queries) > 2:
        raise AppError("Cannot process more than 100 requests at a time")
    if len(queries) == 0:
        raise AppError("No document passed")
    try:
        if len(queries) == 1:
            doc = nlp(queries[0])
            languages.append(language_out(0, doc))
        else:
            for idx,query in enumerate(queries):
                doc = nlp(query)
                languages.append(language_out(idx,doc))
    except:
        print("No Language Detected")


    lanDict["ResultList"] = languages
    return jsonify(lanDict)

if __name__ == '__main__':
    # create_app().run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)




