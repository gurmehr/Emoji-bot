#!/Users/gurmehrsohi/Desktop/.venv2/bin/python
# -*- coding: utf-8 -*-

import json, requests, random, re
from pprint import pprint
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
import webbrowser
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
              ]

img_url=""

def return_random_quote():
    random.shuffle(quotes_arr)
    return quotes_arr[0][0]

def quote_search(str_var):
    tosearch = str_var.lower()
    random.shuffle(quotes_arr)
    for quote_text,quote_author in quotes_arr:
        if tosearch in quote_author.lower():
            return quote_text

    return return_random_quote()

def scrape_generic():
    url ="http://www.iemoji.com/"
    
#quotes_arr = quotes_string.split('\n')

PAGE_ACCESS_TOKEN ='EAANMgk5XWZBEBALsqxrZBGDD3SxOUxePVnvPwy2ZCB0vS7J1fdaSMZCCwGWwpwf0bZAMb0qwaznFWkqZCDqhQPeZBfRzGlCaNZBd9DUTzuaLxuCM2ZC33Gq4qdDws6B1MJhW6FovTOvSTsZAkqeokWZBQuW7JJotTnYXWrLLDZCeJUeamQZDZD'


def post_facebook_message(fbid, recevied_message):
    
    reply_text = recevied_message
   
    
    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
        user_details = requests.get(user_details_url, user_details_params).json()
        joke_text = 'Yo '+user_details['first_name']+'..! i am fine and ' + reply_text
    except:
        joke_text = 'Yo ' + reply_text
    

    joke_text=quote_search(recevied_message)

    message_object = {
        "attachment":{
            "type":"image",
                "payload":{
                    #"url":"http://thecatapi.com/api/images/get?format=src&type=png"
                    "url" : "http://worldversus.com/img/ironman.jpg"
                    }
        }
    }
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":message_object})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    webbrowser.open("https://www.google.com")
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