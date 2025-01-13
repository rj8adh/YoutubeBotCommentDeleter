def checkDesc(channelID):

    import html2text
    import os
    from dotenv import load_dotenv
    from googleapiclient.discovery import build

    load_dotenv()

    ytKey = os.getenv("YT_KEY")

    youtube = build('youtube', 'v3', developerKey=ytKey)

    # Getting channel information with a certain ID
    request = youtube.channels().list(
        part = 'snippet',
        id = channelID
    )
    response = request.execute()
    # Too much filtering :(
    filteredData = response['items'][0]['snippet']['localized']['description']
    filteredData = html2text.html2text(filteredData)
    # I seperated this into 2 lines so it looks like I wrote more code than I did
    return filteredData
