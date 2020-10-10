import boto3

from credentials import *

#creating a client to the comprehend
client = boto3.client('comprehend',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
input_text = input("Enter the text to analysis the sentimental analysis : ")
response = client.detect_sentiment(Text= input_text,LanguageCode="en")
print("This is the final result : ",response['Sentiment'])
print("This is the positive score: ",response['SentimentScore']['Positive'])
print("This is the Negative score: ",response['SentimentScore']['Negative'])
print("This is the Neutral score: ",response['SentimentScore']['Neutral'])