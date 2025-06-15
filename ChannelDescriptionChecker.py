from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pysafebrowsing import SafeBrowsing
from googleapiclient.discovery import build
from pprint import pprint
import requests
import html2text
import json
import os

load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_KEY")

youtube = build('youtube', 'v3', developerKey=GOOGLE_KEY)
scrapingSession = requests.Session()

urlSafetyChecker = SafeBrowsing(GOOGLE_KEY)

def checkDesc(channelID: str):

    # Getting channel information with a certain ID
    request = youtube.channels().list(
        part = 'snippet',
        id = channelID
    )
    response = request.execute()
    # Too much filtering :(
    filteredData = response['items'][0]['snippet']
    # filteredData = html2text.html2text(filteredData)

    return filteredData

def checkLinks(channelURL: str):
    allLinks = {}

    params = {
        'prettyPrint': 'false',
    }

    json_data = {
        'context': {
            'client': {
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36,gzip(gfe)',
                'clientName': 'WEB',
                'clientVersion': '2.20250613.00.00',
                'originalUrl': channelURL,
                'mainAppWebInfo': {
                    'graftUrl': 'https://www.youtube.com/@cortezlabs',
                },
            },
        },
        'continuation': '4qmFsgJgEhhVQ0pqa1NiYTVXUWhsSWtxd2FHTVplWVEaRDhnWXJHaW1hQVNZS0pEWm1PVGN6WTJGaUxUQXdNREF0TWpCaVpTMWlZV1UzTFRVNE1qUXlPV1F3TkdObU9BJTNEJTNE',
    }

    channelContent = json.loads(scrapingSession.post(
        'https://www.youtube.com/youtubei/v1/browse',
        params=params,
        json=json_data,
    ).content)
    
    parsedContent = channelContent['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]
    linkData = parsedContent['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['links']

    for link in linkData:
        allLinks[link['channelExternalLinkViewModel']['title']['content']] = link['channelExternalLinkViewModel']['link']['content']

    return allLinks

def checkSecurity(websiteURL: str):
    results = urlSafetyChecker.lookup_url(websiteURL)
    return results

if __name__ == '__main__':
    # pprint(checkDesc('UCJjkSba5WQhlIkqwaGMZeYQ'))
    print(checkSecurity('https://www.youtube.com/@cortezlabs'))