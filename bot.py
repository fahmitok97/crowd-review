import requests
import json
import traceback
import random

from flask import Flask, request

from fetcher.fetcher import Fetcher
from crowd_review.sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)

TOKEN = "EAAYcuw9LdEMBANZAYCZAZCmNVMRlpSTXvVJTbvhkWA15iNtomikjwbB2EuKtBZCCwcGJSTpZBZAKIzTTZC4byZB7ypR2LvgNswzpkLclznZAdxdRZCoBdBBSbU0jmZA1ZB3ocZC6JVFDKuh3ls5iJnm2bxKRuIQPkaZCnZAwgkiNaCGN2JAmAZDZD"
IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/de/thumb/9/9f/Twitter_bird_logo_2012.svg/1259px-Twitter_bird_logo_2012.svg.png'
VERIFY_TOKEN = 'ini_projek_ir'
ENDPOINT_HEADER = 'https://twitter.com/comicstalks/status/'

def __get_sentiment(movie_title):

  movie_title = '#' + movie_title
  fetcher = Fetcher()

  tweets = fetcher.search_by_hashtag(movie_title, with_id=True)
  top_positive_tweet, top_negative_tweet = SentimentAnalyzer.process(tweets)

  return top_positive_tweet, top_negative_tweet

def __generate_about(sender):
    return {
        'recipient': {
            'id': sender
        },
        'message': {
            'text': 'Crowd Review Bot, real-time sentiment analysis chatbot for movie review from twitter'
        }
    }

def __generate_usage(sender):
    return {
        'recipient': {
            'id': sender
        },
        'message': {
            'text': 'Unknown command, usage :\n1. about\n2. get_review <movie-name>'
        }
    }

def __generate_review_context(sender,
                                movie_title,
                                isPositive=False):
    if isPositive :
        review_type = 'positive'
    else :
        review_type = 'negative'

    return {
        'recipient': {
            'id': sender
        },
        'message': {
            'text': 'Here\'s some {} reviews for {} movies'.format(review_type, movie_title)
        }
    }

def __generate_review_carousel(sender,
                               movie_title,
                               tweets,
                               isPositive=False):
  if isPositive :
    review_type = 'positive'
  else :
    review_type = 'negative'

  tweet_elements = [
     {
      "title": '{} Tweet-{}'.format(review_type, i + 1),
      "image_url": IMAGE_URL,
      "subtitle": tweets[i]['text'],
      "default_action": {
        "type": "web_url",
        "url": ENDPOINT_HEADER + tweets[i]['id'],
        "messenger_extensions": True,
        "webview_height_ratio": "tall",
        "fallback_url": "https://twitter.com/"
      },
      "buttons": [
        {
          "type": "web_url",
          "url": ENDPOINT_HEADER + tweets[i]['id'],
          "title":"View Tweet"
        }
      ]
    }
  for i in range(len(tweets))]

  return {
    "recipient": {
      "id": sender
    },
    "message": {
      "attachment": {
        "type":"template",
        "payload": {
          "template_type":"generic",
          "elements": tweet_elements
        }
      }
    }
  }

def __send_chat(payload):
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + TOKEN, json=payload)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data.decode('utf-8'))
      text = data['entry'][0]['messaging'][0]['message']['text']
      sender = data['entry'][0]['messaging'][0]['sender']['id']
      query = text.split(' ')

      if query[0].lower() == 'get_review':
        movie_title = ' '.join(query[1:])
        movie_title_no_space = ''.join(query[1:])
        positive_tweets, negative_tweets = __get_sentiment(movie_title_no_space)

        payload = __generate_review_context(sender, movie_title, isPositive=True)
        __send_chat(payload)
        payload = __generate_review_carousel(sender, movie_title, positive_tweets, isPositive=True)
        __send_chat(payload)
        payload = __generate_review_context(sender, movie_title, isPositive=False)
        __send_chat(payload)
        payload = __generate_review_carousel(sender, movie_title, negative_tweets, isPositive=False)
        __send_chat(payload)

      elif query[0].lower() == 'about':
        payload = __generate_about(sender)
        __send_chat(payload)
      else :
        payload = __generate_usage(sender)
        __send_chat(payload)

    except Exception as e:
      print(traceback.format_exc())

  elif request.method == 'GET':

    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
      return request.args.get('hub.challenge')

    return "Wrong Verify Token"

  return "ok"

if __name__ == '__main__':
  app.run(debug=True)
