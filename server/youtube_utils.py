
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from io import *
import json

DEVELOPER_KEY = "AIzaSyBuyUD1YN9SQ0mjjcyrH8q9vzXth0g67ok"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    videos = []
    channels = []
    playlists = []
    saved_video = False;
    
    # Get related json file
    with open(query[0].upper()+'.json', 'r') as read_file:
        data = json.load(read_file)
        
    # Chack query against data
    for item in data:
        if query.upper() == item['query']:
            saved_video = True;
            item['query'] = ""
            videos.append(item)
    
    
    # Check to see if the query passed is a direct link
    if 'https://www.youtube.com/watch?v=' in query:
        #Get unique video id from link
        video_id = query.split('=')[1]
        
        videos.append({
                "query": "",
                "title": "Direct Url Request",
                "id": video_id,
                "uploader": "Direct Url Request",
                "description": "Direct Url Request",
                "thumbnail": "https://static.wikia.nocookie.net/pokemon/images/d/d6/Jessie_Mimikyu.png/revision/latest?cb=20170915045921",
                "url": query,
                "autoplay_url": query + "?autoplay=1"})
        })
    
    elif saved_video == True:
        pass
    else:
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=50
        ).execute()

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append({
                    "query": query.upper(),
                    "title": search_result["snippet"]["title"],
                    "id": search_result["id"]["videoId"],
                    "uploader": search_result["snippet"]["channelTitle"],
                    "description": search_result["snippet"]["description"],
                    "thumbnail": search_result["snippet"]["thumbnails"]["high"],
                    "url": "https://www.youtube.com/embed/" + search_result["id"]["videoId"],
                    "autoplay_url": "https://www.youtube.com/embed/" + search_result["id"]["videoId"] + "?autoplay=1"

                })

    return videos


def search_related_videos(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)


    search_response = youtube.search().list(
        part="id,snippet",
        relatedToVideoId=video_id,
        maxResults=50,
        type="video"
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append({
                "title": search_result["snippet"]["title"],
                "id": search_result["id"]["videoId"],
                "uploader": search_result["snippet"]["channelTitle"],
                "description": search_result["snippet"]["description"],
                "thumbnail": search_result["snippet"]["thumbnails"]["high"],
                "url": "https://www.youtube.com/embed/" + search_result["id"]["videoId"],
                "autoplay_url": "https://www.youtube.com/embed/" + search_result["id"]["videoId"] + "?autoplay=1"

            })

    return videos



def get_video(yt_id, query):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    response = youtube.videos().list(
        part="id,snippet,contentDetails",
        id=yt_id
    ).execute()

    #print(response)

    response = response.get("items", [None])[0]

    if not response:
        return None

    video = {
        "query": query.upper()
        "title": response["snippet"]["title"],
        "id": response["id"],
        "uploader": response["snippet"]["channelTitle"],
        "description": response["snippet"]["description"],
        "thumbnail": response["snippet"]["thumbnails"]["high"],
        "url": "https://www.youtube.com/embed/" + response["id"],
        "autoplay_url": "https://www.youtube.com/embed/" + response["id"] + "?autoplay=1",
        "duration": response["contentDetails"]["duration"]
    }
    
    #TODO: Implement save video to json here
    if video['query'] != "":
        with open(query[0].upper()+'.json', 'w+') as data_file:
            json.dump(video)
    #print(video)
    else:
        Pass
    return video


