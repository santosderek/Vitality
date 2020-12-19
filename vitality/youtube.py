import requests

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


class Youtube:

    def __init__(self, developerKey):
        self.developerKey = developerKey

    def search_topic(self, topic: str):

        returned_value = requests.get(YOUTUBE_SEARCH_URL,
                                      headers={
                                          'Accept': 'application/json'
                                      },
                                      params={
                                          'part': "snippet",
                                          'maxResults': 6,
                                          'q': topic,
                                          'key': self.developerKey
                                      })

        if returned_value.status_code == 200:
            return returned_value.json()
        else:
           raise YoutubeRequestFailed('Status == {}'.format(returned_value.status_code))


DEFAULT_FALL_BACK_WORKOUT_DICT = {'kind': 'youtube#searchListResponse', 'etag': 'h1FYP32fQ1WpzTrG218-R5U2WOE', 'nextPageToken': 'CAYQAA', 'regionCode': 'US', 'pageInfo': {'totalResults': 1000000, 'resultsPerPage': 6}, 'items': [{'kind': 'youtube#searchResult', 'etag': '_z-mApBYzZK4CpjH8kitCBUsU5s', 'id': {'kind': 'youtube#video', 'videoId': 'cC9r0jHF-Fw'}, 'snippet': {'publishedAt': '2016-11-09T17:00:07Z', 'channelId': 'UCI-Ho-GaKYbtMzXJWmWAsrg', 'title': '2 Hours of Beautiful Coral Reef Fish, Relaxing Ocean Fish, &amp; Stunning Aquarium Relax Music', 'description': 'Enjoy 2 hours of relaxing coral reef aquarium. This video features beautiful coral reef fish and relaxing music that is ideal for sleep, study and meditation.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/cC9r0jHF-Fw/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/cC9r0jHF-Fw/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/cC9r0jHF-Fw/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Cat Trumpet', 'liveBroadcastContent': 'none', 'publishTime': '2016-11-09T17:00:07Z'}}, {'kind': 'youtube#searchResult', 'etag': '8Z34-YmyQ1GvrF8HItUF4bfAfAg', 'id': {'kind': 'youtube#video', 'videoId': '0gT8Ty0ClHc'}, 'snippet': {'publishedAt': '2020-10-04T16:13:03Z', 'channelId': 'UCj8f0ZLB8gML9iHDxWDne4g', 'title': 'Betta Koi Pleco Snail Carp Fish Goldfish Angelfish Guppy Guppies Catfish animals Videos', 'description': 'Betta Koi Pleco Snail Carp Fish Goldfish Angelfish Guppy Guppies Catfish animals Videos #betta #fish #goldfish #koi #koifish #snail #carps #carp #guppy ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/0gT8Ty0ClHc/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/0gT8Ty0ClHc/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/0gT8Ty0ClHc/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'The Animals Around Us', 'liveBroadcastContent': 'none', 'publishTime': '2020-10-04T16:13:03Z'}}, {'kind': 'youtube#searchResult', 'etag': '8RqhHygcDhICyiN4azvZu086n_0', 'id': {'kind': 'youtube#channel', 'channelId': 'UC7MCFUG5oKKsfVDl7gT7BRA'}, 'snippet': {'publishedAt': '2016-04-06T06:35:52Z', 'channelId': 'UC7MCFUG5oKKsfVDl7gT7BRA', 'title': 'Catch Em All Fishing', 'description': 'Stories Fade, but REEL LEGENDS NEVER DIE! My Apparel Store is Available Online https://reellegendsneverdie.com/ RAW WILD REAL FOOTAGE AND ...', 'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnhie2Wl8buLx7ONTQQRa7ARxXiZH0c225TuCVa6rA=s88-c-k-c0xffffffff-no-rj-mo'}, 'medium': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnhie2Wl8buLx7ONTQQRa7ARxXiZH0c225TuCVa6rA=s240-c-k-c0xffffffff-no-rj-mo'}, 'high': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnhie2Wl8buLx7ONTQQRa7ARxXiZH0c225TuCVa6rA=s800-c-k-c0xffffffff-no-rj-mo'}}, 'channelTitle': 'Catch Em All Fishing', 'liveBroadcastContent': 'upcoming', 'publishTime': '2016-04-06T06:35:52Z'}}, {'kind': 'youtube#searchResult', 'etag': 'YtS4Np2RaPVZzWS5FQxpKWWBghc', 'id': {'kind': 'youtube#video', 'videoId': 'ilqbT-uaaVg'}, 'snippet': {'publishedAt': '2020-12-15T08:00:14Z', 'channelId': 'UCYU6l9Ws7ciniwyJtODjong', 'title': 'Survival Skills: Primitive Couple Unique Hand Fishing Catch Big Fish - Cooking Delicous Fish', 'description': 'Survival Skills: Primitive Couple Unique Hand Fishing Catch Big Fish - Cooking Delicous Fish #PrimitiveCookingKT #SurvivalSkills #CookingFish ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/ilqbT-uaaVg/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/ilqbT-uaaVg/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/ilqbT-uaaVg/hqdefault.jpg', 'width': 480, 'height'Result', 'etag': 'Gqu28yZB7tfnOrcnv6UmjvwvzC8', 'id': {'kind': 'youtube#video', 'videoId': 'vA-FizFqXV8'}, 'snippet': {'publishedAt': '2020-12-11T22:57:25Z', 'channelId': 'UCZdNPWAwux7zPVODRguoYMg', 'title': 'Trained Colorful Aquarium Fish Feed From My hand!!', 'description': 'instagram - https://www.instagram.com/franklinseeber/ Rawwfam Merch -https://www.rawwfishing.com/shop.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/vA-FizFqXV8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/vA-FizFqXV8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/vA-FizFqXV8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'RAWWFishing', 'liveBroadcastContent': 'none', 'publishTime': '2020-12-11T22:57:25Z'}}, {'kind': 'youtube#searchResult', 'etag': 'K_Cc5GwdZ8cIadxQNT6wwqmDYHg', 'id': {'kind': 'youtube#video', 'videoId': 'POLneoshHUI'}, 'snippet': {'publishedAt': '2020-12-13T20:57:10Z', 'channelId': 'UC7MCFUG5oKKsfVDl7gT7BRA', 'title': 'CATCHING GIANT Rare WHITE LIGHTNING FISH!', 'description': 'Catching rare giant white lightning blue talapia. CATCH EM GEAR is HERE: https://catchemfishing.com/ Check out my Inmedium': {'url': 'https://i.ytimg.com/vi/POLneoshHUI/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/POLneoshHUI/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Catch Em All Fishing', 'liveBroadcastContent': 'none', 'publishTime': '2020-12-13T20:57:10Z'}}]}
class YoutubeRequestFailed(Exception):
    pass
