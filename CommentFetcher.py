import html2text
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from pprint import pprint
from ChannelDescriptionChecker import checkDesc

load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_KEY")

def getComments(videoLink: str, DataRows: int = 15, likeCountFilter: bool=True, yourChannelID: str = ""):
    dataRows = DataRows
    checkChannelID = False # In the case you gave channel id, I'd want to skip your comments

    if yourChannelID:
        checkChannelID = True

    # getting the video ID
    vidLinkSpliced = videoLink.split("?v=")
    vidLinkSpliced = vidLinkSpliced[-1].split("shorts/")

    youtube = build('youtube', 'v3', developerKey=GOOGLE_KEY)

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=vidLinkSpliced[-1],
            maxResults=100,
            order='relevance'
        )
        response = request.execute()

    except:
        print("Invalid video ID")
        return "Invalid video ID"

    comments = []
    commentHtml = []

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet'] # makes sure we get the top comments only
        if checkChannelID and comment['authorChannelId']['value'] == yourChannelID:
            print("Skipped your comment")
            continue
        
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['authorChannelId']['value'],
            comment['authorProfileImageUrl']
        ])
        commentHtml.append(comment['textDisplay'])

    # print(comment)

    commentRelevDF = pd.DataFrame(comments, columns=['Author', 'Published_At', 'Updated_At', 'Like_Count', 'ChannelID', 'ChannelImage']) # adding headers for each column

    # formatting the comment's html text to normal text
    for i in range(DataRows):
        commentHtml[i] = html2text.html2text(commentHtml[i])
        commentHtml[i] = commentHtml[i].split('</a> ')[-1] # removes weird html formatting that got past initial filter

    commentRelevDF['commentText'] = commentHtml # adding the formatted text to the pandas dataframe

    # likeCountDF = commentRelevDF.sort_values('like_count', ascending=False) # ordering from most to least likes

    # shorten dataframes to first dataRows rows
    # likeCountDF = likeCountDF.head(dataRows) 
    commentRelevDF = commentRelevDF.head(dataRows)

    # if (likeCountFilter):
    #     return likeCountDF
    # else:
    return commentRelevDF

if __name__ == '__main__':

    # pd.set_option('display.max_colwidth', 400)
    comments = getComments("https://www.youtube.com/watch?v=ALgujcGrV_g", yourChannelID='UC9K44RtwiROAwCpALm1wdyQ')
    for index, comment in comments.iterrows():
        print(comment['Author'] + ': ' + comment['ChannelID'])
        print(checkDesc(comment['ChannelID']))