# --AUTHOR - Deepa Elizabeth Thomas-- #
# --Description : Code to extract youtube channel statistcs and snippets --#

from googleapiclient.discovery import build
import pandas as pd

class youtubeResponse:
    youtube = 0
    request = 0
    response = 0
    st =0
    sn= 0

    # Parameterized constructor
    def __init__(self, service_name, version,api_key):
        self.service_name = service_name
        self.version = version
        self.api_key = api_key
        self.videoid_list= []
        self.allVideoList= []
        self.pageCount= 0
        self.nextPageToken = 'notNull'
        self.videoStats_list_dic= []


    def responseCapture(self):
        self.youtube = build(self.service_name, self.version , developerKey=self.api_key)

# Loop through all the pages in  the response using next page token to get all video id

        while self.nextPageToken is not None:
            if self.pageCount == 0:
                self.request = self.youtube.search().list(part='id', channelId='TYGJeq4klgb398RgNh9Zpiyg',maxResults='50')
            elif self.pageCount > 0:
                self.request = self.youtube.search().list(part='id', channelId='TYGJeq4klgb398RgNh9Zpiyg',pageToken=self.nextPageToken, maxResults='50')
            self.response = self.request.execute()
            for videoList in self.response['items']:
                self.allVideoList.append(videoList)
                if videoList['id']['kind'] == 'youtube#video':
                    self.videoid_list.append(videoList['id']['videoId'])
            self.pageCount = self.pageCount + 1
            if 'nextPageToken' not in self.response:
                break
            self.nextPageToken = self.response['nextPageToken']
            # print(self.nextPageToken)

        # print(self.videoid_list)
        print(len(self.videoid_list))
        print(len(self.allVideoList))


# Get all video snippet and statistics using video id

        for videoid in self.videoid_list:
            self.request = self.youtube.videos().list(part='statistics,snippet', id=videoid)
            self.response = self.request.execute()
            # print(self.response)
            for vid_list in self.response['items']:
                # appending the videos stastics to a list
                temp = {'Video_title': str(vid_list['snippet']['title']),
                        'published at': str(vid_list['snippet']['publishedAt']),
                        'viewCount': str(vid_list['statistics']['viewCount']),
                        'FavoriteCount': str(vid_list['statistics']['favoriteCount'])}

                if ('likeCount' not in vid_list['statistics']):
                    temp['LikeCount']= '0'
                else:
                    temp['LikeCount'] = str(vid_list['statistics']['likeCount'])

                if ('commentCount' not in vid_list['statistics']):

                    temp['commentCount']= '0'
                else:
                    temp['LikeCount'] = str(vid_list['statistics']['commentCount'])

                self.videoStats_list_dic.append(temp)

# Video stats is copied to Dataframe from list

        self.df = pd.DataFrame(self.videoStats_list_dic)
        print(self.df)

    def printStats(self):
        self.df.to_csv(r'statistics.csv')
