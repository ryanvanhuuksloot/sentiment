import yaml as pyyaml
from classes.sentiment.sentimentClass import sentimentClass
from classes.auth.yaml import Yaml
import os

if __name__ == "__main__":
    api_keys = Yaml().readYaml('keys.yaml')
    companyNames = ['ICE']
    # ?companyNames = [
    #     'Microsoft',
    #     'Apple iCloud',
    #     'Pixar',
    #     'Ebay',
    #     'Travelocity',
    #     'Boeing',
    #     'EasyJet',
    #     'Samsung',
    #     'Xerox',
    #     '3M',
    #     'NFL',
    #     'Diebold',
    #     'NBC',
    #     'Mazda',
    #     'GE Healthcare',
    #     'General Dynamics',
    #     'Fujitsu',
    #     'Alaska Airlines',
    #     'Aston Martin',
    #     'BMW',
    #     'LG',
    #     'Trek bikes',
    #     'Symantec',
    #     'NetApp',
    #     'Dell',
    #     'Flipkart',
    #     'Heineken',
    #     'Merrillynch',
    #     'AccuWeather',
    #     'Halliburton',
    #     'ICE']
    sources = ['abc-news', 'al-jazeera-english', 'cnbc', 'daily-mail', 'engadget', 'cnn', \
            'the-new-york-times', 'fox-news', 'bbc-news', 'the-verge']

    sentimentObjects = {}
    for name in companyNames:
        sentimentObjects[name] = sentimentClass(name, api_keys, sources)

    sentimentObjects2 = {}
    for name in companyNames:
        sentimentObjects2[name] = sentimentClass(name, api_keys, sources, from_param='2018-04-21', dateUntil='2018-04-23')

    try:
        os.remove('fileout.yaml')
    except OSError:
        pass

    if not os.path.exists('fileouts'):
        os.makedirs('fileouts')

    for name in companyNames:
        with open('./fileouts/' + name + '.yaml', 'a') as fileout:
            dictionary = {}
            dictionarySingle = {}
            dictionarySingle['urls'] = sentimentObjects[name].urls
            dictionarySingle['articles'] = sentimentObjects[name].articles
            dictionarySingle['sentimentScore'] = sentimentObjects[name].sentimentScore
            dictionarySingle['articleCount'] = sentimentObjects[name].articleCount
            dictionary['2017'] = dictionarySingle
            dictionarySingle = {}
            dictionarySingle['urls'] = sentimentObjects2[name].urls
            dictionarySingle['articles'] = sentimentObjects2[name].articles
            dictionarySingle['sentimentScore'] = sentimentObjects2[name].sentimentScore
            dictionarySingle['articleCount'] = sentimentObjects2[name].articleCount
            dictionary['2018'] = dictionarySingle
            #pyyaml.dump(dictionary, fileout, default_flow_style=False)

        with open('./fileouts/' + name + '.csv', 'a') as csvout:
            csvout.write(name + ',' + str(sentimentObjects[name].articleCount/330) + ',' + str(sentimentObjects[name].sentimentScore) \
                        + ',' + str(sentimentObjects2[name].articleCount/3) + ',' + str(sentimentObjects2[name].sentimentScore))
