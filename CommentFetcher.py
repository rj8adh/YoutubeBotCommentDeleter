def getComments(videoLink: str, DataRows: int = 10, likeCountFilter: bool=True):

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

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet'] # makes sure we get the top comments only
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['textDisplay'],
            comment['authorChannelId']['value'],
            comment['authorProfileImageUrl']
        ])

    # print(comment)

    commentRelevDF = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text', 'channelID', 'channelImage']) # adding headers for each column

    likeCountDF = commentRelevDF.sort_values('like_count', ascending=False) # ordering from most to least likes

    # shorten dataframes to first dataRows rows
    likeCountDF = likeCountDF.head(dataRows) 
    commentRelevDF = commentRelevDF.head(dataRows)

    if (likeCountFilter):
        return likeCountDF
    else:
        return commentRelevDF
    
print(getComments("https://www.youtube.com/watch?v=QLwIrsG0E08"))