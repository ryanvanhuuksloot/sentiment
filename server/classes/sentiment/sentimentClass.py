import requests
from newsapi import NewsApiClient
from aylienapiclient import textapi
import classes.sentiment.exceptions
from classes.sentiment.logging import logger

LOGGER = logger(__name__).getLogger()

class sentimentClass:
    """
    Responsible for all the methods for each company
    """

    def __init__(self, companyName: str, api_keys: dict, sources: list, language: str = 'en', from_param: str = '2017-01-01', dateUntil: str = '2018-12-01'):
        """
        Initialize the object

        Parameters
        ----------
        companyName : str
            name of the company you want to do sentiment on
        api_keys : dict
            a dictionary containing all the api keys you need
        """
        self.companyName = companyName
        self._api_keys = api_keys
        self.sources = ','.join(map(str, sources))
        self.language = language
        self.dateUntil = dateUntil
        self.from_param = from_param
        self.urls = []
        self.articles = []
        self.sentimentScore = 0
        self.articleCount = 0

        self.retrieveNews
        self.retrieveTextFromURL
        self.retrieveSentiment

    @property
    def retrieveNews(self) -> list:
        """
        Retrieve less than 100 news urls from a list of sources provided using the newsapi library

        Parameters
        ----------
        None

        Returns
        -------
        urls : list[str]
            a list of less than 100 article urls from the sources provided
        """
        newsapi = NewsApiClient(api_key=self._api_keys['newsapi'])
        pageNumber = 1

        LOGGER.info("Retrieving urls for " + self.companyName)
        while (len(self.urls) < 100):
            all_articles = newsapi.get_everything(q=self.companyName,
                                            sources=self.sources,
                                            from_param=self.from_param,
                                            to=self.dateUntil,
                                            language=self.language,
                                            sort_by='relevancy',
                                            page_size=100,
                                            page=pageNumber)

            self.articleCount += all_articles['totalResults'] 
            for article in all_articles['articles']:
                self.urls.append(article['url'])

            pageNumber += 1
        
        return self.urls

    @retrieveNews.deleter
    def retrieveNews(self):
        LOGGER.warning("Deleting all the urls for " + self.companyName)
        self.urls = []
        LOGGER.warning("Deleting all the articles in tandom")
        del self.retrieveTextFromURL

    @property
    def retrieveTextFromURL(self) -> list:
        """
        Get the text from each url retrieved from retrieveNews

        Parameters
        ----------
        None

        Returns
        -------
        articles : list[str]
            a plain text of all the articles
        """
        # Check URLS
        if len(self.urls) == 0:
            raise URLException('Error has occured retrieving news URLs')

        # Create the client
        client = textapi.Client(self._api_keys['textapi']['applicationId'], self._api_keys['textapi']['applicationKey'])

        count = 0
        for url in self.urls:
            extract = client.Extract({'url': url})
            self.articles.append(extract['article'])
            count += 1

            if count == 5:
                break

        return self.articles

    @retrieveTextFromURL.deleter
    def retrieveTextFromURL(self) -> None:
        LOGGER.warning("Deleting all the articles for " + self.companyName)
        self.articles = []

    @property
    def retrieveSentiment(self) -> None:
        """
        Determine the sentiment for each block of text from each url from retrieveTextFromURL

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if len(self.articles) == 0:
            raise ArticleException('Error in retrieving the text from the URLs')

        sentiment = 1
        count = 0
        id = 0
        sentimentRequest = {'documents': [] }


        for article in self.articles:
            document = {}
            document['id'] = id
            document['language'] = 'en'
            document['text'] = article
            sentimentRequest['documents'].append(document)
            id += 1

        header = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self._api_keys['Ocp-Apim-Subscription-Key'],
        }

        microsoftUrl = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

        sentiments = requests.post(microsoftUrl, headers=header, json=sentimentRequest)
        sentiments = sentiments.json()
        sentimentCount = 0

        for sentiment in sentiments['documents']:
            if 'score' in sentiment:
                self.sentimentScore += sentiment['score']
                sentimentCount += 1

        if sentimentCount:
            self.sentimentScore = self.sentimentScore / sentimentCount
        else:
            self.sentimentScore = -1


