from imessage_reader import fetch_data
import os
import tweepy
import re
import requests
import pytesseract
from PIL import Image
import apiCred


pytesseract.pytesseract.tesseract_cmd = '/path/to/your/tesseract/executable'

# Twitter API credentials

RECIPIENT_NUMBER = "888222" 

def escape_special_characters(message):
    special_characters = {
        '\\': r'\\\\',
        '$': r'\$',
        '"': r'\"',
        # Add more special characters and their escaped representations as needed
    }

    for special_char, escaped_char in special_characters.items():
        message = message.replace(special_char, escaped_char)

    return message

def sendMessage(message):
    os.system("osascript sendMessage.applescript {} {}".format(RECIPIENT_NUMBER, escape_special_characters(message)))

def process_tweet(tweet):
    pattern = r"\b[^ ]+\b(?=\s+to\s+888222)"
    matched = re.search(pattern, tweet.text, re.IGNORECASE) 
    if matched:
        print(matched.group(0))
        sendMessage(matched.group(0))
    else:
        print(f"No code in \n \"{tweet.text}\"")
        process_media(tweet)


def process_media(tweet):
    full_tweet = api.get_status(tweet.data['id'])
    if "media" in full_tweet.entities:
        media_entities = full_tweet.extended_entities.get("media", [])
        # Download each media file
        for media_entity in media_entities:
            media_url = media_entity["media_url"]
            response = requests.get(media_url)
            if response.status_code == 200:
                # Save the media file
                file_name = media_entity["id_str"] + ".jpg"  # Or use appropriate file extension
                with open(file_name, "wb") as file:
                    file.write(response.content)
                    print(f"Media file saved: {file_name}")
                    im = Image.open(file_name)
                    im.show()
            # image = Image.open(file_name)
            # text = pytesseract.image_to_string(image)
            # print(text)
            else:
                print(f"Failed to download media: {media_url}")
    else:
        print("No media found in the tweet.")

# process_tweet("""hold my guac *drops code* Text Text V$XBFREE3S to 888222. #ChipotleFreePointer

# 300 codes avail. US only, 13+. Stnrd text & data rates may apply. Terms: http://Chipotle.com/FreePointer""")
    
# Twitter stream listener
class MyStreamingClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print("Processing")
        # print(type(tweet))
        # print(tweet.entities)
        # print(tweet.attachments)
        # print(tweet.data)
        if tweet == 420:
            #returning False in on_data disconnects the stream
            return False
        process_tweet(tweet)

# Authenticate and start streaming
auth = tweepy.OAuthHandler(apiCred.consumer_key, apiCred.consumer_secret)
auth.set_access_token(apiCred.access_token, apiCred.access_token_secret)
print("Streaming")
api = tweepy.API(auth)
print("Streaming")

streaming_client = MyStreamingClient(bearer_token=apiCred.bearer_token)

streaming_client.add_rules(tweepy.StreamRule("from:ChipotleTweets"))
print(streaming_client.get_rules().data)

print("Streaming")

streaming_client.filter()