__author__ = 'Ryan'

import pycountry
import requests

api_key='3544201f69bc484fa17a1cee77af8263'

class News:
    def __init__(self, source, author, title, description, url, urlToImage, publishedAt, content):
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt
        self.content = content

# usage: returns a json string of articles that match the search keyword
def searchNewsByKeyword(searchWord):
    url = 'https://newsapi.org/v2/everything'
    response = requests.get(url, params={"q": searchWord, "apiKey": api_key})
    return response.json()

# usage: returns a json string of articles that match a given country and category
# note: countries are searched for by code, category must be business, entertainment, general, health, science, sports, or technology
def searchNewsByArea(country, category):
    country = findCountryCode(country)
    url = 'https://newsapi.org/v2/top-headlines'
    response = requests.get(url, params={"country": country, "category": category, "apiKey": api_key})
    return response.json()

def findCountryCode(input):
    mapping = {country.name: country.alpha_2 for country in pycountry.countries}
    return mapping.get(input)

# print(searchNewsByArea('United States', 'Technology'))
# print(searchNewsByKeyword('Apple'))

