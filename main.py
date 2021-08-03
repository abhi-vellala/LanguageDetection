# pip freeze > requirements.txt
# pip install -r requirements.txt
# pip list --format=freeze > requirements.txt
# pip install -U spacy
# pip install spacy-langdetect
# python -m spacy download en_core_web_sm
from flask import Flask, request, jsonify, render_template
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import pandas as pd


app = Flask(__name__)

@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('language_detector')

df = pd.read_csv("language_codes_spacy.csv", sep=";")

@app.route('/')
def home():
    return render_template('index.html')

def language_out(doc):
    lan = doc._.language
    return {"LanguageCode": lan['language'], "Score": lan['score']}

class AppError(Exception):
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return self.message


@app.route('/language_detect', methods=['POST'])
def language_detect():
    # text = request.json['Comment']
    # queries = request.json['TextList']
    queries = request.form
    # lanDict = {}
    # languages = []
    # if len(queries) > 2:
    #     raise AppError("Cannot process more than 100 requests at a time")
    # if len(queries) == 0:
    #     raise AppError("No document passed")
    doc = nlp(queries['document'])
    langDict = doc._.language
    lang = list(df['language'].loc[df['code'] == langDict['language']])[0]
    score = round(langDict['score'] *100,5)
    return render_template('index2.html', document= queries['document'],prediction_text='The Language Detected is {} with {}% probability'.format(lang,score))


if __name__ == '__main__':
    # create_app().run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=8080)




