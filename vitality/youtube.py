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
            raise YoutubeRequestFailed(
                'Status == {}'.format(returned_value.status_code))


DEFAULT_YOUTUBE_WORKOUT_SEARCH = {'etag': 'oww2YjQMhgQkbCus-YCrHhCOLa0',
                                  'items': [{'etag': 'Gpuq22nNnxce7jTqmVdoGRgLaQo',
                                             'id': {'kind': 'youtube#video', 'videoId': 'UItWltVZZmE'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UChVRfsT_ASBZk10o0An7Ucg',
                                                         'channelTitle': 'Pamela Reif',
                                                         'description': 'Finally: a workout suitable for '
                                                         'BEGINNERS. // Werbung What makes this '
                                                         '"beginner friendly"? 1. I used BASIC '
                                                         'movements, that are not too '
                                                         'complicated or hard to ...',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2019-09-01T10:12:36Z',
                                                         'publishedAt': '2019-09-01T10:12:36Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/UItWltVZZmE/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/UItWltVZZmE/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/UItWltVZZmE/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': '20 MIN FULL BODY WORKOUT - Beginner Version '
                                                         '// No Equipment I Pamela Reif'}},
                                            {'etag': 'YGk-gsxMrm-QwKtKxQuAU5ms9bE',
                                             'id': {'kind': 'youtube#video', 'videoId': '2pLT-olgUJs'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UCCgLoMYIyP0U56dEhEL1wXQ',
                                                         'channelTitle': 'Chloe Ting',
                                                         'description': 'Abs Abs Abs! Everyone seems to be '
                                                         'asking for a QUICK and short schedule, '
                                                         'so I put together a 2 weeks schedule '
                                                         'to help you get closer to those '
                                                         'defined abs ...',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2019-08-12T11:45:00Z',
                                                         'publishedAt': '2019-08-12T11:45:00Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/2pLT-olgUJs/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/2pLT-olgUJs/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/2pLT-olgUJs/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': 'Get Abs in 2 WEEKS | Abs Workout Challenge'}},
                                            {'etag': 'z4pOk82cpA8D1vXsOpG7SzlHRPg',
                                             'id': {'kind': 'youtube#video', 'videoId': 'JkVHrA5o23o'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UCpQ34afVgk8cRQBjSJ1xuJQ',
                                                         'channelTitle': 'MadFit',
                                                         'description': 'A 20 minute APARTMENT FRIENDLY full '
                                                         'body hiit workout AT HOME! Low impact, '
                                                         'no jumping, equipment free, and NO '
                                                         'REPEAT! ⭐️SHOP MY COOKBOOKS!',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2020-03-24T13:00:15Z',
                                                         'publishedAt': '2020-03-24T13:00:15Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/JkVHrA5o23o/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/JkVHrA5o23o/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/JkVHrA5o23o/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': 'Low Impact FULL BODY HIIT Workout (No '
                                                         'Equipment + No Jumping)'}},
                                            {'etag': 'DQXmS61nI7nVM1gZR-hn398J_vo',
                                             'id': {'kind': 'youtube#video', 'videoId': 'gC_L9qAHVJ8'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UCFjc9H89-RpWuIStDqhO7AQ',
                                                         'channelTitle': 'Body Project',
                                                         'description': 'https://teambodyproject.com Create a '
                                                         'free account today. This workout is '
                                                         'part of Real Start and Real Start Plus '
                                                         '- a workout plan made for real people '
                                                         'with real ...',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2019-03-24T20:07:35Z',
                                                         'publishedAt': '2019-03-24T20:07:35Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/gC_L9qAHVJ8/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/gC_L9qAHVJ8/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/gC_L9qAHVJ8/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': '30 minute fat burning home workout for '
                                                         'beginners. Achievable, low impact results.'}},
                                            {'etag': 'wMQLWReXyXNnNF3-O33IwfdUAtE',
                                             'id': {'kind': 'youtube#video', 'videoId': 'H2U3HwAyBXg'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UCpQ34afVgk8cRQBjSJ1xuJQ',
                                                         'channelTitle': 'MadFit',
                                                         'description': 'a 20 min fat burning, full body '
                                                         'workout you can do at home without any '
                                                         'equipment! A workout designed for '
                                                         'TOTAL BEGINNERS! Wether you are just '
                                                         'getting into ...',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2020-08-13T13:47:17Z',
                                                         'publishedAt': '2020-08-13T13:47:17Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/H2U3HwAyBXg/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/H2U3HwAyBXg/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/H2U3HwAyBXg/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': '20 min FULL BODY Workout for TOTAL BEGINNERS '
                                                         '(No Equipment)'}},
                                            {'etag': 'XbPBVBQQkwFJNqHfFiNAvQKt634',
                                             'id': {'kind': 'youtube#video', 'videoId': 'ml6cT4AZdqI'},
                                             'kind': 'youtube#searchResult',
                                             'snippet': {'channelId': 'UCGiSCVGNukLqv8hwpKCsQKQ',
                                                         'channelTitle': 'SELF',
                                                         'description': 'In this high intensity cardio '
                                                         'bodyweight workout from trainer Lita '
                                                         "Lewis, you'll spike your heart rate "
                                                         'with high-knees, fast feet, and star '
                                                         'jumps; plus work your core ...',
                                                         'liveBroadcastContent': 'none',
                                                         'publishTime': '2018-05-21T16:01:33Z',
                                                         'publishedAt': '2018-05-21T16:01:33Z',
                                                         'thumbnails': {'default': {'height': 90,
                                                                                    'url': 'https://i.ytimg.com/vi/ml6cT4AZdqI/default.jpg',
                                                                                    'width': 120},
                                                                        'high': {'height': 360,
                                                                                 'url': 'https://i.ytimg.com/vi/ml6cT4AZdqI/hqdefault.jpg',
                                                                                 'width': 480},
                                                                        'medium': {'height': 180,
                                                                                   'url': 'https://i.ytimg.com/vi/ml6cT4AZdqI/mqdefault.jpg',
                                                                                   'width': 320}},
                                                         'title': '30-Minute HIIT Cardio Workout with Warm Up - '
                                                         'No Equipment at Home | SELF'}}],
                                  'kind': 'youtube#searchListResponse',
                                  'nextPageToken': 'CAYQAA',
                                  'pageInfo': {'resultsPerPage': 6, 'totalResults': 1000000},
                                  'regionCode': 'US'}

DEFAULT_YOUTUBE_DIET_SEARCH = {'etag': 'GjebS7ncm1hcm7yey5lCN3V52w4',
                               'items': [{'etag': 'Q7fao2AwqNGthYPjkJmfRIIf-_M',
                                          'id': {'kind': 'youtube#video', 'videoId': 'SWLbVHROXvg'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCr_-k8z6_RKKxkjWkt8RFvA',
                                                      'channelTitle': 'TheSeriousfitness',
                                                      'description': 'http://serious-fitness-programs.com/weightloss '
                                                      'Follow Us On Facebook: ⇨ '
                                                      'https://www.facebook.com/TheSeriousfitness '
                                                      '⇨Tools and ingredients: Olive Oil ...',
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2019-12-29T11:15:02Z',
                                                      'publishedAt': '2019-12-29T11:15:02Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/SWLbVHROXvg/default.jpg',
                                                                                 'width': 120},
                                                                     'high': {'height': 360,
                                                                              'url': 'https://i.ytimg.com/vi/SWLbVHROXvg/hqdefault.jpg',
                                                                              'width': 480},
                                                                     'medium': {'height': 180,
                                                                                'url': 'https://i.ytimg.com/vi/SWLbVHROXvg/mqdefault.jpg',
                                                                                'width': 320}},
                                                      'title': '6 Healthy Low Carb Recipes For Weight Loss'}},
                                         {'etag': 'qzanPsKtiEHPCA4aGDWspcN_5ms',
                                          'id': {'kind': 'youtube#video', 'videoId': 'GDS1OVF46UY'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCJFp8uSYCjXOMnkUyb3CQ3Q',
                                                      'channelTitle': 'Tasty',
                                                      'description': 'Check out these healthy and low carb '
                                                      'recipes! Subscribe to Tasty: '
                                                      'https://bzfd.it/2ri82Z1 About Tasty: '
                                                      'The official YouTube channel of all '
                                                      "things Tasty, the world's ...",
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2019-07-23T16:00:01Z',
                                                      'publishedAt': '2019-07-23T16:00:01Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/GDS1OVF46UY/default.jpg',
                                                                                 'width': 120},
                                                                     'high': {'height': 360,
                                                                              'url': 'https://i.ytimg.com/vi/GDS1OVF46UY/hqdefault.jpg',
                                                                              'width': 480},
                                                                     'medium': {'height': 180,
                                                                                'url': 'https://i.ytimg.com/vi/GDS1OVF46UY/mqdefault.jpg',
                                                                                'width': 320}},
                                                      'title': '7 Healthy And Low Carb Recipes • Tasty'}},
                                         {'etag': 'AgfiNXuTY33RQuRvAVSzUvL_CeA',
                                          'id': {'kind': 'youtube#video', 'videoId': 'MdarLkKDjWA'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCevU8VNx7XRwo5jkFqzrDXw',
                                                      'channelTitle': 'Sweet Peas Saffron',
                                                      'description': 'These low carb meal prep recipes will '
                                                      'help you stick to a low carb diet! '
                                                      'Whether you enjoy them for lunch or '
                                                      'dinner, you are going to be glad you '
                                                      'spent the time ...',
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2020-04-24T15:00:19Z',
                                                      'publishedAt': '2020-04-24T15:00:19Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/MdarLkKDjWA/default.jpg',
                                                                                 'width': 120},
                                                                      'high': {'height': 360,
                                                                               'url': 'https://i.ytimg.com/vi/MdarLkKDjWA/hqdefault.jpg',
                                                                               'width': 480},
                                                                      'medium': {'height': 180,
                                                                                 'url': 'https://i.ytimg.com/vi/MdarLkKDjWA/mqdefault.jpg',
                                                                                 'width': 320}},
                                                      'title': '4 LOW CARB meal prep recipes'}},
                                         {'etag': 'mdh5Y-Jbxqq_GMXVr8RRjFFz63s',
                                          'id': {'kind': 'youtube#video', 'videoId': 'mrk7YxMSzY4'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCQOQ3RxX_o-B-68wSKdcfMQ',
                                                      'channelTitle': 'The Domestic Geek',
                                                      'description': 'SAVE 50% on my 12 WEEK MEAL PLAN! Use '
                                                      "code 'EATWELL' at checkout: ...",
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2019-10-07T20:00:34Z',
                                                      'publishedAt': '2019-10-07T20:00:34Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/mrk7YxMSzY4/default.jpg',
                                                                                 'width': 120},
                                                                     'high': {'height': 360,
                                                                              'url': 'https://i.ytimg.com/vi/mrk7YxMSzY4/hqdefault.jpg',
                                                                              'width': 480},
                                                                     'medium': {'height': 180,
                                                                                'url': 'https://i.ytimg.com/vi/mrk7YxMSzY4/mqdefault.jpg',
                                                                                'width': 320}},
                                                      'title': '3 Low Carb Dinner Recipes | Quick + Easy '
                                                      'Weeknight Dinner Ideas'}},
                                         {'etag': 'JCZIjh0PqXJKyRjtSOLrUriOiqI',
                                          'id': {'kind': 'youtube#video', 'videoId': 'V1lmaPqMzAg'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCZvoUuniFzmOjfBt67lNsEQ',
                                                      'channelTitle': 'Tasty Recipes',
                                                      'description': "We're mindful of how the current "
                                                      'coronavirus outbreak might be '
                                                      'affecting your access to stores and '
                                                      'general grocery items. Please know '
                                                      'that many of these ...',
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2020-10-11T22:00:03Z',
                                                      'publishedAt': '2020-10-11T22:00:03Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/V1lmaPqMzAg/default.jpg',
                                                                                 'width': 120},
                                                                     'high': {'height': 360,
                                                                              'url': 'https://i.ytimg.com/vi/V1lmaPqMzAg/hqdefault.jpg',
                                                                              'width': 480},
                                                                     'medium': {'height': 180,
                                                                                'url': 'https://i.ytimg.com/vi/V1lmaPqMzAg/mqdefault.jpg',
                                                                                'width': 320}},
                                                      'title': '10 Easy Low-Carb Dinners • Tasty Recipes'}},
                                         {'etag': 'tLQiWqydIfnJ_VVJz9igl5BnMVc',
                                          'id': {'kind': 'youtube#video', 'videoId': 'nigbuPqz658'},
                                          'kind': 'youtube#searchResult',
                                          'snippet': {'channelId': 'UCBXV31q0rnDbCP9bnwMR7WA',
                                                      'channelTitle': 'Well Done',
                                                      'description': 'Enjoy this compilation of 18 different '
                                                      'Keto recipes - great for weeknight '
                                                      'meals or weekend gatherings. See below '
                                                      'for links to all recipes. You can also '
                                                      'use the ...',
                                                      'liveBroadcastContent': 'none',
                                                      'publishTime': '2019-02-06T22:43:36Z',
                                                      'publishedAt': '2019-02-06T22:43:36Z',
                                                      'thumbnails': {'default': {'height': 90,
                                                                                 'url': 'https://i.ytimg.com/vi/nigbuPqz658/default.jpg',
                                                                                 'width': 120},
                                                                     'high': {'height': 360,
                                                                              'url': 'https://i.ytimg.com/vi/nigbuPqz658/hqdefault.jpg',
                                                                              'width': 480},
                                                                     'medium': {'height': 180,
                                                                                'url': 'https://i.ytimg.com/vi/nigbuPqz658/mqdefault.jpg',
                                                                                'width': 320}},
                                                      'title': '18 Keto Recipes | Low Carb Super Comp | Well '
                                                      'Done'}}],
                               'kind': 'youtube#searchListResponse',
                               'nextPageToken': 'CAYQAA',
                               'pageInfo': {'resultsPerPage': 6, 'totalResults': 1000000},
                               'regionCode': 'US'}


class YoutubeRequestFailed(Exception):
    pass
