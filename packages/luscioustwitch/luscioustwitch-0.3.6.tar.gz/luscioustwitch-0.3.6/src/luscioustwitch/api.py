from .saferequests import *
from .websocket import *
from .events import *

from typing import Callable, Tuple

import time

TWITCH_API_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class TwitchAPI:
  API_URL = "https://api.twitch.tv/helix"
  OAUTH_URL = "https://id.twitch.tv/oauth2"
  CLIENT_ID = ""
  CLIENT_SECRET = ""
  ACCESS_TOKEN = ""
  DEFAULT_HEADERS = {}
  rlrequests = RateLimitedRequests(400, 60)
  TWITCH_WEBSOCKET = None
  
  def __add_parameters(self, url : str, params : dict):
    """Add parameters to an API request URL.

    Args:
        url (string): API endpoint
        params (string): Dictionary of parameters. See function descriptions for valid params.

    Returns:
        string: URL with params.
    """
    separator = "?"
    for k, v in params.items():
      url += f"{separator}{k}={v}"
      separator = "&"
    return url
  
  def __raise_req_error(self, response : requests.Response):
    raise Exception(f'Status {response.status_code}: {response.content}')

  def __init__(self, credentials : dict, override_api_url : str = "", override_oauth_url : str = ""):
    """Constructor for TwitchAPI. Must pass in credentials in the form of a dictionary.

    Args:
        credentials (dict): API Credentials. "CLIENT_ID" and "CLIENT_SECRET" should be in the dict.
    """
    if override_api_url != "":
      self.API_URL = override_api_url
      
    if override_oauth_url != "":
      self.OAUTH_URL = override_oauth_url
    
    self.CLIENT_ID = credentials["CLIENT_ID"]
    
    if 'ACCESS_TOKEN' in credentials:
      self.ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    else:
      self.CLIENT_SECRET = credentials["CLIENT_SECRET"]
    
      r = requests.post(f'{self.OAUTH_URL}/token?client_id={self.CLIENT_ID}&client_secret={self.CLIENT_SECRET}&grant_type=client_credentials', headers = {'Content-Type': 'application/x-www-form-urlencoded'})
    
      try:
        self.ACCESS_TOKEN = r.json()['access_token']
      except:
        raise Exception("Failed to create access token. Invalid credentials.")
    
    self.DEFAULT_HEADERS = { "Authorization": f"Bearer {self.ACCESS_TOKEN}", "Client-Id": self.CLIENT_ID }
    
  def refresh_access_token(self, refresh_token : str) -> dict:
    url = f'{self.OAUTH_URL}/token'
    post_params = {
      'client_id': self.CLIENT_ID,
      'client_secret': self.CLIENT_SECRET,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token
    }
    url = self.__add_parameters(url, post_params)
    
    r : requests.Response = self.rlrequests.post(url = url, headers = { 'Content-Type': 'application/x-www-form-urlencoded' })
    
    try:
      self.ACCESS_TOKEN = r.json()['access_token']
    except:
      raise Exception(f"{r.status_code}: {r.content}.\nFailed to refresh access token.")
    
    self.DEFAULT_HEADERS = { "Authorization": f"Bearer {self.ACCESS_TOKEN}", "Client-Id": self.CLIENT_ID }
    
    return r

  def get_user_id(self, login : str = "") -> str:
    """Get user ID from username.

    Args:
        username (string): Username

    Returns:
        string: User ID
    """
    if login == "":
      url = f'{self.API_URL}/users'
    else:
      url = f"{self.API_URL}/users?login={login}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()["data"][0]["id"]
    else:
      self.__raise_req_error(r)
      
  def get_user_info(self, id : str) -> dict:
    """Get user information

    Args:
        id (str): user ID

    Returns:
        dict: user information
    """
    
    """Get user ID from username.

    Args:
        username (string): Username

    Returns:
        string: User ID
    """
    url = f"{self.API_URL}/users?id={id}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()["data"][0]
    else:
      self.__raise_req_error(r)
  
  def get_channel_info(self, user_id : str) -> dict:
    """Get Channel Information.

    Args:
        user_id (string): User ID

    Returns:
        dict: Channel information
    """
    url = f"{self.API_URL}/channels?broadcaster_id={user_id}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data'][0]
    else:
      self.__raise_req_error(r)
      
  def get_category_info(self, category_name : str) -> dict:
    """Get category information from category name

    Args:
        category_name (string): Category name

    Returns:
        dict: Category information
    """
    url = f"{self.API_URL}/games?name={category_name}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()["data"][0]
    else:
      self.__raise_req_error(r)
      
  def get_category_id(self, category_name : str) -> str:
    """Get category ID

    Args:
        category_name (str): _description_

    Returns:
        str: _description_
    """
    return self.get_category_info(category_name)['id']

  def get_clip(self, clip_id : str) -> dict:
    """Get info for one clip from ID.

    Args:
        clip_id (string): Video ID

    Returns:
        dict: clip info
    """
    url = f"{self.API_URL}/clips?id={clip_id}"
    r: requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data'][0]
    else:
      self.__raise_req_error(r)

  def get_clips(self, params : dict) -> Tuple[list, str]:
    """Get clips based on params.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Clip ID
            broadcaster_id (string): Broadcaster ID
            game_id (string): Game/Category ID
            started_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            ended_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            first (int): fetch the first n clips
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of clip info
    """
    url = f"{self.API_URL}/clips"
    url = self.__add_parameters(url, params)
    
    r : requests.Response = self.rlrequests.get(url = url, headers=self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      try:
        return r.json()['data'], r.json()['pagination']['cursor']
      except:
        return r.json()['data'], ""
    else:
      self.__raise_req_error(r)

  def get_all_clips(self, params : dict) -> list:
    """Get all clips based on params (auto-pagination).

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Clip ID
            broadcaster_id (string): Broadcaster ID
            game_id (string): Game/Category ID
            started_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            ended_at (string): RFC3339 format, use TWITCH_API_TIME_FORMAT from this library
            first (int): fetch the first n clips
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of clip info
    """
    all_clips = []
    while True:
      clips, cursor = self.get_clips(params)

      for clip in clips:
        all_clips.append(clip)
      
      if cursor == "":
        return all_clips
      else:
        params["after"] = cursor

  def get_video(self, video_id : str) -> dict:
    """Get info for one video from ID.

    Args:
        video_id (string): Video ID

    Returns:
        dict: Video info
    """
    url = f"{self.API_URL}/videos?id={video_id}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data'][0]
    else:
      self.__raise_req_error(r)

  def get_videos(self, params : dict) -> Tuple[list, str]:
    """Get videos based on params.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Video ID
            user_id (string): User ID
            game_id (string): Game/Category ID
            language (string): ISO 639-1
            period (string): "all", "day", "month", or "week"
            sort (string): "time", "trending", or "views"
            type (string): "all", "archive", "highlight", or "upload"
            first (int): fetch the first n videos
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of video info
        string: Pagination cursor
    """
    url = f"{self.API_URL}/videos"
    url = self.__add_parameters(url, params)
    
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      try:
        return r.json()['data'], r.json()['pagination']['cursor']
      except:
        return r.json()['data'], ""
    else:
      self.__raise_req_error(r)

  def get_all_videos(self, params : dict) -> list:
    """Get all videos based on params (auto-pagination).

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            id (string): Video ID
            user_id (string): User ID
            game_id (string): Game/Category ID
            language (string): ISO 639-1
            period (string): "all", "day", "month", or "week"
            sort (string): "time", "trending", or "views"
            type (string): "all", "archive", "highlight", or "upload"
            first (int): fetch the first n videos
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of video info
    """
    all_clips = []
    while True:
      vids, cursor = self.get_videos(params)

      for vod in vids:
        all_clips.append(vod)
      
      if cursor == "":
        return all_clips
      else:
        params["after"] = cursor

  def get_streams(self, params : dict) -> dict:
    """Get a list of streams.

    Args:
        params (dict): Dictionary of parameters for the API request. The valid params are:
            user_id (string): User ID
            user_login (string): Username
            game_id (string): Game/Category ID
            type (string): "all" or "live"
            language (string): ISO 639-1
            first (int): fetch the first n streams
            before (string): reverse pagination
            after (string): forward pagination

    Returns:
        list: list of stream info
    """
    url = f"{self.API_URL}/streams/"
    url = self.__add_parameters(url, params)
    
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data']
    else:
      self.__raise_req_error(r)

  def is_user_live(self, user_id : str) -> bool:
    stream_info = self.get_streams({ "user_id": user_id })
    return (len(stream_info) > 0)
  
  def get_emotes(self, user_id : str) -> list:
    """Get Channel Emotes

    Args:
        user_id (string): User ID

    Returns:
        list: List of emote information.
    """
    url = f"{self.API_URL}/chat/emotes?broadcaster_id={user_id}"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data']
    else:
      self.__raise_req_error(r)
  
  def get_global_emotes(self) -> list:
    """Get Global Emotes.

    Returns:
        list: List of global emote information.
    """
    url = f"{self.API_URL}/chat/emotes/global"
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data']
    else:
      self.__raise_req_error(r)
    
  def get_custom_rewards(self, params : dict) -> list:
    """Get a list of custom rewards for a channel.

    Args:
        params (dict): dictionary of parameters for the request
          broadcaster_id (int): The ID of the broadcaster whose custom rewards you want to get
          id (string): Rewards ID
          only_manageable_rewards (bool): only get custom rewards that the app may manage

    Returns:
        _type_: _description_
    """
    url = f"{self.API_URL}/channel_points/custom_rewards"
    url = self.__add_parameters(url, params)
    
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data']
    else:
      self.__raise_req_error(r)
    
  def create_custom_reward(self, broadcaster_id : str, reward_params : dict) -> dict:
    url = f"{self.API_URL}/channel_points/custom_rewards?broadcaster_id={broadcaster_id}"
    
    r : requests.Response = self.rlrequests.post(url = url, headers = self.DEFAULT_HEADERS, json = reward_params)
    
    if r.status_code == 200:
      return r.json()['data'][0]
    else:
      self.__raise_req_error(r)
    
  def setup_websocket(self, url_override = None):
    """Connect to the Twitch WebSockets interface for subscribing to events.

    Args:
        url_override (str, optional): Pass a different websockets url for testing purposes. Defaults to None.
    """
    self.TWITCH_WEBSOCKET = TwitchWebSocket(url_override)
    
  def websocket_session_id(self) -> str:
    return self.TWITCH_WEBSOCKET.SESSION_ID
    
  def join_websocket_thread(self):
    self.TWITCH_WEBSOCKET.THREAD.join()
    
  def _add_subscription(self, params : dict) -> bool:
    if not self.TWITCH_WEBSOCKET.CONNECTED:
      print("WebSocket is not connected.")
      return False
    
    url = f'{self.API_URL}/eventsub/subscriptions'
    
    r : requests.Response = self.rlrequests.post(url = url, headers = self.DEFAULT_HEADERS, json=params)
    
    if r.status_code == 202:
      return r.json()['data'][0]['status'] == 'enabled'
    else:
      return False
    
  def get_active_subscriptions(self) -> list:
    """Get active subscriptions in current WebSocket instance.

    Returns:
        list: list of active subscriptions
    """
    url = f'{self.API_URL}/eventsub/subscriptions'
    r : requests.Response = self.rlrequests.get(url = url, headers = self.DEFAULT_HEADERS)
    
    if r.status_code == 200:
      return r.json()['data']
    else:
      self.__raise_req_error(r)
    
  def add_subscription(self, event : TwitchEvent, callback) -> bool:
    """Add a subscription to the WebSocket interface.

    Args:
        event (TwitchEvent): Desired subscription event type
        callback (function): Callback for handling notifications matching this subscription

    Returns:
        bool: Success.
    """
    self.TWITCH_WEBSOCKET.add_callback(event.notification_type(), callback)
    return self._add_subscription(event.params())
  
  def subscribe_to_updates(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(UpdateEvent(user_id, self.websocket_session_id()), callback)
    
  def subscribe_to_follows(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(FollowEvent(user_id, self.websocket_session_id()), callback)
    
  def subscribe_to_subscriptions(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(SubscribeEvent(user_id, self.websocket_session_id()), callback)
    
  def subscribe_to_gifted_subscriptions(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(SubscriptionGiftEvent(user_id, self.websocket_session_id()), callback)
    
  def subscribe_to_subscription_messages(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(SubscriptionMessageEvent(user_id, self.websocket_session_id()), callback)
  
  def subscribe_to_cheers(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(CheerEvent(user_id, self.websocket_session_id()), callback)
  
  def subscribe_to_raids(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(RaidEvent(user_id, self.websocket_session_id()), callback)
  
  def subscribe_to_bans(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(BanEvent(user_id, self.websocket_session_id()), callback)
  
  def subscribe_to_unbans(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(UnbanEvent(user_id, self.websocket_session_id()), callback)
  
  def subscribe_to_reward_redemption(self, user_id : str, callback : Callable[[object, str], None], reward_id : str = None) -> bool:
    return self.add_subscription(CustomRewardRedemptionAddEvent(user_id, self.websocket_session_id(), reward_id), callback)
    
  def subscribe_to_stream_online(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(StreamOnlineEvent(user_id, self.websocket_session_id()), callback)
    
  def subscribe_to_stream_offline(self, user_id : str, callback : Callable[[object, str], None]) -> bool:
    return self.add_subscription(StreamOfflineEvent(user_id, self.websocket_session_id()), callback)