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
begin=0;
# Create your views here.




emoji_arr=[]

img_arr=[]
quotes_string = '''
    There is no charge for awesomeness... or attractiveness.;Kung Fu Panda;http://www.google.co.in/search?ie=UTF-8&q=kung+fu+panda+awesomeness
    Any fool can write code that a computer can understand. Good programmers write code that humans can understand.;Martin Fowle;http://thc.org/root/phun/unmaintain.html
    He was so deadly, in fact, that his enemies would go blind from over-exposure to pure awesomeness!;Kung Fu Panda;
    One often meets his destiny on the road he takes to avoid it.;Kung Fu Panda;
    The world is moved along, not only by the mighty shoves of its heroes, but also by the aggregate of the tiny pushes of each honest worker.;Helen Keller;
    '''
bigdata_list=['http://emojipedia.org/people/','http://emojipedia.org/food-drink/','http://emojipedia.org/nature/','http://emojipedia.org/activity/','http://emojipedia.org/travel-places/','http://emojipedia.org/objects/','http://emojipedia.org/flags/','http://emojipedia.org/birthday/']
r1=requests.get("http://emojipedia.org/facebook/messenger/")
soup1 = BeautifulSoup(r1.text,"html.parser")
p1=soup1.find('ul',{'class':'emoji-grid'})
list_fb=p1.find_all('img')
for l in list_fb:
    a=[l.get('src'),l.get('alt')]
    img_arr.append(a)

for start in bigdata_list:
    r=requests.get(start)
    soup = BeautifulSoup(r.text,"html.parser")
    p=soup.find('ul',{'class':'emoji-list'})
    list_flags=p.find_all('li')
    flags_list=[]
    flags_name=[]
    for list in list_flags:
        flags_list.append(list.find('span').text)
        flags_name.append(list.text)
    final_list=[]
    k=0
    for i in flags_list:
        a=[flags_list[k],flags_name[k]]
        k=k+1
        emoji_arr.append(a)

pprint(emoji_arr[0][0])

#url=a.text;
quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
              ["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
              ["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
              ]



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


def get_emoji(str_var):
    flag=0
    arr=[]
    
    if str_var.lower() in "*,random,anything":
        random.shuffle(emoji_arr)
        return emoji_arr[0][0]
            # arr.append("Emojis:")
    try0=[['smile','smiling'],['sad','disappointed'],['shocked','flushed'],['potty','poo'],['tatti','poo']]
    
    k=str_var.split(' ')
    for i in k:
        
        if(i.lower() in "help,rules,?,hi,hello,wassup,hey,howdy,hola".split(',')):
            return "intro"
        tosearch = i.lower()
        for try1,try2 in try0:
            if(tosearch in try1):
                return "Sir try "+try2
        for a,b in emoji_arr:
            if tosearch in b.lower():
                arr.append(a)
                flag=1;

    if flag == 1:
        return " ".join(arr[:5])
    return "Sorry not found!!!"
    


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
    

# joke_text=quote_search(recevied_message)
    joke_text=get_emoji(recevied_message)
    if joke_text=="intro":
        joke_text="Hello " +user_details['first_name'] + ",this is a chatbot created to help you find emojis.Just send a text and i will search an emoji that matches it."
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    message_object = {
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":joke_text,
                "buttons":[
                           {
                           "type":"postback",
                           "title":"Copy",
                           "payload":"USER_DEFINED_PAYLOAD"
                           }
                           ]
            }
    }
    }
    message_object2 = {
        "attachment":{
            "type":"image",
            "payload":{
                "url":"https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg"
        }
    }
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":message_object})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":message_object2})
#response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":message_object})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
# status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
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