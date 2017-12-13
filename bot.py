from flask import Flask, request
import requests
import json
import traceback
import random
app = Flask(__name__)

token = "EAAYcuw9LdEMBACtQZAI04mHAS1ezwvJBUTxW6382MziVYZAJEmQRJnbVVH484j40AqZB9zchVhMioZC0JZB9mQCOvver1vQJNeriaWTDcRfPZCWGIrwPlZCYG0j1ZBLr15QlK8aX6xT7iYE92zsKpOlhIBY7PZBSzDJBo9ZCrNZC1eItgZDZD"

def get_sentiment(movie_name):
  sentiment_result = 0.99 # Pecahan banyaknya yang nilai positif
  sample_tweets = [
    {
      'link': 'https://twitter.com/view?item=xxx',
      'image_url': 'https://petersfancybrownhats.com/company_image.png',
      'text': 'Must watch #sharknado'
    },
    {
      'link': 'https://twitter.com/view?item=xxx',
      'image_url': None,
      'text': '11/10 #sharknado2'
    }
  ]

  return sentiment_result, sample_tweets

def generate_carousel_response(sender,
                               movie_name,
                               sentiment_result,
                               sample_tweets):
  tweet_elements = [
     {
      "title": 'Sample Tweet-{}'.format(i),
      "image_url": sample_tweets[i]['image_url'],
      "subtitle": sample_tweets[i]['text'],
      "default_action": {
        "type": "web_url",
        "url": sample_tweets[i]['link'],
        "messenger_extensions": true,
        "webview_height_ratio": "tall",
        "fallback_url": "https://twitter.com/"
      },
      "buttons":[
        {
          "type":"web_url",
          "url": sample_tweets[i]['link'],
          "title":"View Tweet"
        }         
      ]      
    }
  for i in range(len(sample_tweets))]

  payload = {
    "recipient":{
      "id": sender
    },
    "message":{
      "attachment":{
        "type":"template",
        "payload":{
          "template_type":"generic",
          "elements": tweet_elements
        }
      }
    }
  }

  return payload

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      print(request.data)
      data = json.loads(str(request.data))
      text = data['entry'][0]['messaging'][0]['message']['text']
      sender = data['entry'][0]['messaging'][0]['sender']['id']

      sentiment_result, sample_tweets = get_sentiment(text) # Assume text langsung nama movie
      payload = generate_carousel_response(sender, text, sentiment_result, sample_tweets)
      
      requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
    except Exception as e:
      print(traceback.format_exc())

  elif request.method == 'GET':
    if request.args.get('hub.verify_token') == 'ini_projek_ir':
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"

  return ""

if __name__ == '__main__':
  app.run(debug=True)
