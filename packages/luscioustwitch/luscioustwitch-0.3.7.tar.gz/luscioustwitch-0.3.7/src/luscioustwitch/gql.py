import os
import urllib
from .saferequests import *
    
class TwitchGQL_API:
  API_URL = "https://gql.twitch.tv/gql"
  CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
  DEFAULT_HEADERS = { "Client-ID": CLIENT_ID }
  REQ = RateLimitedRequests(400, 60)
    
  def get_clip(self, clip_id):
    """Get clip information from Twitch's GQL API.

    Args:
        clip_id (string): Clip ID

    Returns:
        dict: Clip info
    """
    content = [
      {
        "operationName": "VideoAccessToken_Clip",
        "variables": {
          "slug": f"{clip_id}"
        },
        "extensions": {
          "persistedQuery": {
            "version": 1,
            "sha256Hash": "36b89d2507fce29e5ca551df756d27c1cfe079e2609642b4390aa4c35796eb11"
          }
        }
      }
    ]
    r = self.REQ.post(url = self.API_URL, headers = self.DEFAULT_HEADERS, json = content)
    
    try:
      return r.json()[0]['data']['clip']
    except:
      return None
    
  def get_video(self, video_id):
    """Get video info.

    Args:
        video_id (string): Video ID

    Returns:
        dict: Video information
    """
    content = {
      "query": "query{video(id:\"" + video_id + "\"){title,thumbnailURLs(height:180,width:320),createdAt,lengthSeconds,owner{id,displayName}}}",
      "variables": {}
    }
    r = self.REQ.post(url = self.API_URL, headers = self.DEFAULT_HEADERS, json = content)
    
    try:
      return r.json()['data']['video']
    except:
      return None

  def download_clip(self, clip_id, filename, saveover = False):
    """Download a Twitch clip.

    Args:
        clip_id (string): Clip ID
        filename (string): Filename
        saveover (bool, optional): Overwrite existing files with the same name. Defaults to False.

    Returns:
        bool: Download succeeded/failed.
    """
    if (not saveover and os.path.exists(filename)):
      print(f"Skipping {clip_id} because the filename '{filename}' is taken.")
      return True
    
    info = self.get_clip(clip_id)
    
    url = info["videoQualities"][0]["sourceURL"]
    signature = info["playbackAccessToken"]["signature"]
    token = urllib.parse.quote(info["playbackAccessToken"]["value"])
    full_url = f"{url}?sig={signature}&token={token}"
    
    try:
      r = requests.get(full_url)
      with open(filename, 'wb') as outfile:
        outfile.write(r.content)
        return True
    except:
      return False
    
  def get_video_chapters(self, video_id):
    content = {
      "extensions" : { 
        "persistedQuery": {
          "sha256Hash": "8d2793384aac3773beab5e59bd5d6f585aedb923d292800119e03d40cd0f9b41",
          "version": 1
        }
      },
      "operationName": "VideoPlayer_ChapterSelectButtonVideo",
      "variables": {
        "videoID": video_id
      }
    }
    r = self.REQ.post(url = self.API_URL, headers = self.DEFAULT_HEADERS, json = content)
    try:
      return r.json()['data']['video']['moments']['edges']
    except:
      return []
    
  def __fetch_all_chat(self, video_id):
    """Fetches the chat messages without checking uniqueness or sorting.

    Args:
        video_id (string): Video ID

    Returns:
        list: List of chat messages
    """
    content = [
      {
        "operationName": "VideoCommentsByOffsetOrCursor",
        "variables": {
          "videoID": video_id,
          "contentOffsetSeconds": 0
        },
        "extensions": {
          "persistedQuery": {
            "version": 1,
            "sha256Hash": "b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044aa76adf6a"
          }
        }
      }
    ]
    
    comments = []
    while True:
      r = self.REQ.post(url = self.API_URL, headers = self.DEFAULT_HEADERS, json = content)
      
      try:
        commentlist = r.json()[0]['data']['video']['comments']['edges']
      except KeyError:
        print("Improper response format.")
        return comments
      
      cursor = None
      for commentdata in commentlist:
        comment = commentdata['node']
        comments.append(comment)
        cursor = commentdata['cursor']
        
      try:
        has_next_page = r.json()[0]['data']['video']['comments']['pageInfo']['hasNextPage']
      except KeyError:
        print("Issue with comment list. Missing pageInfo or hasNextPage.")
        return comments
      
      if has_next_page:
        if "contentOffsetSeconds" in content[0]['variables']:
          content[0]['variables'].pop("contentOffsetSeconds")
        content[0]['variables']['cursor'] = cursor
      else:
        return comments
      
  def get_chat_messages(self, video_id):
    """Get all chat messages and remove duplicates, sort by timestamp

    Args:
        video_id (string): Video ID

    Returns:
        list: List of chat messages
    """
    raw_chat = self.__fetch_all_chat(video_id)
    
    processed_chat = [i for n, i in enumerate(raw_chat) if i not in raw_chat[n + 1:]]
    
    processed_chat.sort(key=lambda a: a['contentOffsetSeconds'])
    return processed_chat
      