import yaml as pyyaml
from classes.sentiment.sentimentClass import sentimentClass
from classes.auth.yaml import Yaml

if __name__ == "__main__":
    api_keys = Yaml().readYaml('keys.yaml')
    companyNames = ['Walmart']
    sources = ['abc-news', 'al-jazeera-english', 'cnbc', 'daily-mail', 'engadget', 'cnn', \
            'the-new-york-times', 'fox-news', 'bbc-news', 'the-verge']
    for name in companyNames:
        sentimentClass(name, api_keys, sources)
