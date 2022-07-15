# --AUTHOR - Deepa Elizabeth Thomas-- #
# --Date - 6/30/2022-- #
# --Description : Code to extract Matrox youtube channel statistcs and snippets --#

from youtube_api import youtubeResponse
import os
from dotenv import load_dotenv


if __name__ == '__main__':

 # Environment data variable load
    load_dotenv()
    api_key = os.getenv('apikey')
    service_name= os.getenv('service_name')
    version = os.getenv('version')

#Capture Youtube API Response
    resp = youtubeResponse(service_name,version,api_key)
    resp.responseCapture()

 # Print Video stats
    resp.printStats()


