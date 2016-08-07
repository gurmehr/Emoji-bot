#!/Users/gurmehrsohi/Desktop/.venv2/bin/python
# -*- coding: utf-8 -*-

import json, requests, random, re
from pprint import pprint


from django.shortcuts import render

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

quotes_string = '''
    There is no charge for awesomeness... or attractiveness.;Kung Fu Panda;http://www.google.co.in/search?ie=UTF-8&q=kung+fu+panda+awesomeness
    Any fool can write code that a computer can understand. Good programmers write code that humans can understand.;Martin Fowle;http://thc.org/root/phun/unmaintain.html
    He was so deadly, in fact, that his enemies would go blind from over-exposure to pure awesomeness!;Kung Fu Panda;
    One often meets his destiny on the road he takes to avoid it.;Kung Fu Panda;
    The world is moved along, not only by the mighty shoves of its heroes, but also by the aggregate of the tiny pushes of each honest worker.;Helen Keller;
    '''

quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
              ["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
              ["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
              ["Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference.", "Robert Frost"],
              ["I attribute my success to this: I never gave or took any excuse.", "Florence Nightingale"],
              ["You miss 100% of the shots you don’t take.", "Wayne Gretzky"],
              ["I’ve missed more than 9000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life. And that is why I succeed.", "Michael Jordan"],
              ["The most difficult thing is the decision to act, the rest is merely tenacity.", "Amelia Earhart"],
              ["Every strike brings me closer to the next home run.", "Babe Ruth"],
              ["Definiteness of purpose is the starting point of all achievement.", "W. Clement Stone"],
              ["We must balance conspicuous consumption with conscious capitalism.", "Kevin Kruse"],
              ["Life is what happens to you while you’re busy making other plans.", "John Lennon"],
              ["We become what we think about.", "Earl Nightingale"],
              ["14.Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails.  Explore, Dream, Discover.", "Mark Twain"],
              ["15.Life is 10% what happens to me and 90% of how I react to it.", "Charles Swindoll"],
              ["The most common way people give up their power is by thinking they don’t have any.", "Alice Walker"],
              ["The mind is everything. What you think you become.", "Buddha"],
              ["The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"],
              ["An unexamined life is not worth living.", "Socrates"],
              ["Eighty percent of success is showing up.", "Woody Allen"],
              ["Your time is limited, so don’t waste it living someone else’s life.", "Steve Jobs"],
              ["Winning isn’t everything, but wanting to win is.", "Vince Lombardi"],
              ["I am not a product of my circumstances. I am a product of my decisions.", "Stephen Covey"],
              ["Every child is an artist.  The problem is how to remain an artist once he grows up.", "Pablo Picasso"]]



def return_random_quote():
    random.shuffle(quotes_arr)
    return quotes_arr[0]


quotes_arr = quotes_string.split('\n')

PAGE_ACCESS_TOKEN ='EAANMgk5XWZBEBALsqxrZBGDD3SxOUxePVnvPwy2ZCB0vS7J1fdaSMZCCwGWwpwf0bZAMb0qwaznFWkqZCDqhQPeZBfRzGlCaNZBd9DUTzuaLxuCM2ZC33Gq4qdDws6B1MJhW6FovTOvSTsZAkqeokWZBQuW7JJotTnYXWrLLDZCeJUeamQZDZD'


def post_facebook_message(fbid, recevied_message):
    reply_text = recevied_message
    if(reply_text=="how r u"):
    
        try:
            user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
            user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
            user_details = requests.get(user_details_url, user_details_params).json()
            joke_text = 'Yo '+user_details['first_name']+'..! i am fine and ' + reply_text
        except:
            joke_text = 'Yo ' + reply_text
    
    else:
        try:
            user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
            user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
            user_details = requests.get(user_details_url, user_details_params).json()
            joke_text = 'Yo '+user_details['first_name']+'..! i am fine and ' + reply_text
        except:
            joke_text = 'Yo ' + reply_text

    random_quote=return_random_quote()
    joke_text=random_quote
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '8447789934':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    
    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    except:
                        return HttpResponse('Error, invalid token')
    
        return HttpResponse()


class MyQuoteBotView2(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '8447789934':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

def index(request):
    print return_random_quote()
    
    return HttpResponse("Hello World")

class MyQuoteBotView2(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World!")