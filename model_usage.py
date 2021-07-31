import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import pandas as pd

@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


def usage():
    text = input('Text:')
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe('language_detector')
    doc = nlp(text)
    lan = doc._.language
    return lan

# if __name__ == '__main__':
#     df = pd.read_csv('/Users/abhi/Desktop/Envigo-Vicinus/Projects/languages_dataset.csv')
#     nlp = spacy.load("en_core_web_sm")
#     nlp.add_pipe('language_detector')
#     for idx,row in df[20:27].iterrows():
#         print(row.Text[:75])
#         print(f'Original Language: {row.language}')
#         doc = nlp(row.Text)
#         print(f'Predicted:{doc._.language}')

# if __name__ == '__main__':
#     language = usage()
#     print(language)


