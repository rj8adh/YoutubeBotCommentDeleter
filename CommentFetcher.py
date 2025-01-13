def getComments(videoLink: str, DataRows: int = 15, likeCountFilter: bool=True):

    import html2text
    import os
    from dotenv import load_dotenv
    from googleapiclient.discovery import build
    import pandas as pd

    load_dotenv()

    ytKey = os.getenv("YT_KEY")
    dataRows = DataRows

    # getting the video ID
    vidLinkSpliced = videoLink.split("?v=")
    vidLinkSpliced = vidLinkSpliced[-1].split("shorts/")

    youtube = build('youtube', 'v3', developerKey=ytKey)

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

    commentRelevDF = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'channelID', 'channelImage']) # adding headers for each column

    # formatting the comment's html text to normal text
    for i in range(0,DataRows+1):
        commentHtml[i] = html2text.html2text(commentHtml[i])
        commentHtml[i] = commentHtml[i].split('</a> ')[-1] # removes weird html formatting that got past initial filter

    commentRelevDF['commentText'] = commentHtml # adding the formmated text to the pandas dataframe

    # likeCountDF = commentRelevDF.sort_values('like_count', ascending=False) # ordering from most to least likes

    # shorten dataframes to first dataRows rows
    # likeCountDF = likeCountDF.head(dataRows) 
    commentRelevDF = commentRelevDF.head(dataRows)

    # if (likeCountFilter):
    #     return likeCountDF
    # else:
    return commentRelevDF

import pandas as pd
# pd.set_option('display.max_colwidth', 400)

print(getComments("https://www.youtube.com/watch?v=QLwIrsG0E08")['commentText'])