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
emoji_arr = [["😄", "Smiling Face with Open Mouth and Smiling Eyes"], ["😃", "Smiling Face with Open Mouth"], ["😀", "Grinning Face"], ["😊", "Smiling Face with Smiling Eyes"], ["☺️", "White Smiling Face"], ["😉", "Winking Face"], ["😍", "Smiling Face with Heart-Shaped Eyes"], ["😘", "Face Throwing a Kiss"], ["😚", "Kissing Face with Closed Eyes"], ["😗", "Kissing Face"], ["😙", "Kissing Face with Smiling Eyes"], ["😜", "Face with Stuck-Out Tongue and Winking Eye"], ["😝", "Face with Stuck-Out Tongue and Tightly-Closed Eyes"], ["😛", "Face with Stuck-Out Tongue"], ["😳", "Flushed Face"], ["😁", "Grinning Face with Smiling Eyes"], ["😔", "Pensive Face"], ["😌", "Relieved Face"], ["😒", "Unamused Face"], ["😞", "Disappointed Face"], ["😣", "Persevering Face"], ["😢", "Crying Face"], ["😂", "Face with Tears of Joy"], ["😭", "Loudly Crying Face"], ["😪", "Sleepy Face"], ["😥", "Disappointed but Relieved Face"], ["😰", "Face with Open Mouth and Cold Sweat"], ["😅", "Smiling Face with Open Mouth and Cold Sweat"], ["😓", "Face with Cold Sweat"], ["😩", "Weary Face"], ["😫", "Tired Face"], ["😨", "Fearful Face"], ["😱", "Face Screaming in Fear"], ["😠", "Angry Face"], ["😡", "Pouting red Face"], ["😤", "Face with Look of Triumph"], ["😖", "Confounded Face"], ["😆", "Smiling Face with Open Mouth and Tightly-Closed Eyes"], ["😋", "Face Savouring Delicious Food"], ["😷", "Face with Medical Mask"], ["😎", "Smiling Face with Sunglasses"], ["😴", "Sleeping Face"], ["😵", "Dizzy Face"], ["😲", "Astonished Face"], ["🏠", "House Building"], ["🏡", "House with Garden"], ["🏫", "School"], ["🏢", "Office Building"], ["🏣", "Japanese Post Office"], ["🏥", "Hospital"], ["🏦", "Bank"], ["🏪", "Convenience Store"], ["🏩", "Love Hotel"], ["🏨", "Hotel"], ["💒", "Wedding"], ["⛪️", "Church"], ["🏬", "Department Store"], ["🏤", "European Post Office"], ["🌇", "Sunset over Buildings"], ["🌆", "Cityscape at Dusk"], ["🏯", "Japanese Castle"], ["🏰", "European Castle"], ["⛺️", "Tent"], ["🏭", "Factory"], ["🗼", "Tokyo Tower"], ["🗾", "Silhouette of Japan"], ["🗻", "Mount Fuji"], ["🌄", "Sunrise over Mountains"], ["🌅", "Sunrise"], ["🌃", "Night with Stars"], ["🗽", "Statue of Liberty"], ["🌉", "Bridge at Night"], ["🎠", "Carousel Horse"], ["🎡", "Ferris Wheel"], ["⛲️", "Fountain"], ["🎢", "Roller Coaster"], ["🚢", "Ship"], ["⛵️", "Sailboat"], ["🚤", "Speedboat"], ["🚣", "Rowboat"], ["⚓️", "Anchor"], ["🚀", "Rocket"], ["✈️", "Airplane"], ["💺", "Seat"], ["🚁", "Helicopter"], ["🚂", "Steam Locomotive"], ["🚊", "Tram"], ["🚉", "Station"], ["🐶", "Dog Face"], ["🐺", "Wolf Face"], ["🐱", "Cat Face"], ["🐭", "Mouse Face"], ["🐹", "Hamster Face"], ["🐰", "Rabbit Face"], ["🐸", "Frog Face"], ["🐯", "Tiger Face"], ["🐨", "Koala"], ["🐻", "Bear Face"], ["🐷", "Pig Face"], ["🐽", "Pig Nose"], ["🐮", "Cow Face"], ["🐗", "Boar"], ["🐵", "Monkey Face"], ["🐒", "Monkey"], ["🐴", "Horse Face"], ["🐑", "Sheep"], ["🐘", "Elephant"], ["🐼", "Panda Face"], ["🐧", "Penguin"], ["🐦", "Bird"], ["🐤", "Baby Chick"], ["🐥", "Front-Facing Baby Chick"], ["🐣", "Hatching Chick"], ["🐔", "Chicken"], ["🐍", "Snake"], ["🐢", "Turtle"], ["🐛", "Bug"], ["🐝", "Honeybee"], ["🐜", "Ant"], ["🐞", "Lady Beetle"], ["🐌", "Snail"], ["🐙", "Octopus"], ["🐚", "Spiral Shell"], ["🐠", "Tropical Fish"], ["🐟", "Fish"], ["🐬", "Dolphin"], ["🐳", "Spouting Whale"], ["🐋", "Whale"], ["🐄", "Cow"], ["🐏", "Ram"], ["🐀", "Rat"], ["🐃", "Water Buffalo"], ["🎍", "Pine Decoration"], ["💝", "Heart with Ribbon"], ["🎎", "Japanese Dolls"], ["🎒", "School Satchel"], ["🎓", "Graduation Cap"], ["🎏", "Carp Streamer"], ["🎆", "Fireworks"], ["🎇", "Firework Sparkler"], ["🎐", "Wind Chime"], ["🎑", "Moon Viewing Ceremony"], ["🎃", "Jack-o-lantern"], ["👻", "Ghost"], ["🎅", "Father Christmas"], ["🎄", "Christmas Tree"], ["🎁", "Wrapped Present"], ["🎋", "Tanabata Tree"], ["🎉", "Party Popper"], ["🎊", "Confetti Ball"], ["🎈", "Balloon"], ["🎌", "Crossed Flags"], ["🔮", "Crystal Ball"], ["🎥", "Movie Camera"], ["📷", "Camera"], ["📹", "Video Camera"], ["📼", "Videocassette"], ["💿", "Optical Disc"], ["📀", "DVD"], ["💽", "Minidisc"], ["💾", "Floppy Disk"], ["💻", "Personal Computer"], ["📱", "Mobile Phone"], ["☎️", "Black Telephone"], ["📞", "Telephone Receiver"], ["📟", "Pager"], ["📠", "Fax Machine"], ["📡", "Satellite Antenna"], ["📺", "Television"], ["📻", "Radio"], ["🔊", "Speaker with Three Sound Waves"], ["🔉", "Speaker with One Sound Wave"], ["🔈", "Speaker"], ["🔇", "Speaker with Cancellation Stroke"], ["🔔", "Bell"], ["🔕", "Bell with Cancellation Stroke"], ["1⃣", "Keycap 1"], ["2⃣", "Keycap 2"], ["3⃣", "Keycap 3"], ["4⃣", "Keycap 4"], ["5⃣", "Keycap 5"], ["6⃣", "Keycap 6"], ["7⃣", "Keycap 7"], ["8⃣", "Keycap 8"], ["9⃣", "Keycap 9"], ["0⃣", "Keycap 0"], ["🔟", "Keycap Ten"], ["🔢", "Input Symbol for Numbers"], ["#⃣", "Hash Key"], ["🔣", "Input Symbol for Symbols"], ["⬆️", "Upwards Black Arrow"], ["⬇️", "Downwards Black Arrow"], ["⬅️", "Leftwards Black Arrow"], ["➡️", "Black Rightwards Arrow"], ["🔠", "Input Symbol for Latin Capital Letters"], ["🔡", "Input Symbol for Latin Small Letters"], ["🔤", "Input Symbol for Latin Letters"], ["↗️", "North East Arrow"], ["↖️", "North West Arrow"], ["↘️", "South East Arrow"], ["↙️", "South West Arrow"], ["↔️", "Left Right Arrow"], ["↕️", "Up Down Arrow"], ["🔄", "Anticlockwise Downwards and Upwards Open Circle Arrows"], ["◀️", "Black Left-Pointing Triangle"], ["▶️", "Black Right-Pointing Triangle"], ["🔼", "Up-Pointing Small Red Triangle"], ["🔽", "Down-Pointing Small Red Triangle"], ["↩️", "Leftwards Arrow with Hook"], ["↪️", "Rightwards Arrow with Hook"], ["ℹ️", "Information Source"], ["⏪", "Black Left-Pointing Double Triangle"], ["⏩", "Black Right-Pointing Double Triangle"], ["⏫", "Black Up-Pointing Double Triangle"], ["⏬", "Black Down-Pointing Double Triangle"], ["⤵️", "Arrow Pointing Rightwards Then Curving Downwards "], ["⤴️", "Arrow Pointing Rightwards Then Curving Upwards"], ["🆗", "Squared OK"], ["🔀", "Twisted Rightwards Arrows"], ["🔁", "Clockwise Rightwards and Leftwards Open Circle Arrows"], ["🌡", "Thermometer"], ["🌢", "Black Droplet"], ["🌣", "White Sun"], ["🌤", "White Sun with Small Cloud"], ["🌥", "White Sun Behind Cloud"], ["🌦", "White Sun Behind Cloud with Rain"], ["🌧", "Cloud with Rain"], ["🌨", "Cloud with Snow"], ["🌩", "Cloud with Lightning"], ["🌪", "Cloud with Tornado"], ["🌫", "Fog"], ["🌬", "Wind Blowing Face"], ["🌶", "Hot Pepper"], ["🍽", "Fork and Knife with Plate"], ["🎔", "Heart with Tip on The Left"], ["🎕", "Bouquet of Flowers"], ["🎖", "Military Medal"], ["🎗", "Reminder Ribbon"], ["🎘", "Musical Keyboard with Jacks"], ["🎙", "Studio Microphone"], ["🎚", "Level Slider"], ["🎛", "Control Knobs"], ["🎜", "Beamed Ascending Musical Notes"], ["🎝", "Beamed Descending Musical Notes"], ["🎞", "Film Frames"], ["🎟", "Admission Tickets"], ["🏅", "Sports Medal"], ["🏋", "Weight Lifter"], ["🏌", "Golfer"], ["🏍", "Racing Motorcycle"], ["🏎", "Racing Car"], ["🏔", "Snow Capped Mountain"], ["🏕", "Camping"], ["🏖", "Beach with Umbrella"], ["🏗", "Building Construction"], ["🏘", "House Buildings"], ["🏙", "Cityscape"], ["🏚", "Derelict House Building"], ["🏛", "Classical Building"], ["🏜", "Desert"], ["🏝", "Desert Island"], ["🏞", "National Park"], ["🏟", "Stadium"], ["🏱", "White Pennant"], ["☝🏻", "White White Up Pointing Index"], ["☝🏼", "Light Brown White Up Pointing Index"], ["☝🏽", "Olive Toned White Up Pointing Index"], ["☝🏾", "Deeper Brown White Up Pointing Index"], ["☝🏿", "Black White Up Pointing Index"], ["✊🏻", "White Raised Fist"], ["✊🏼", "Light Brown Raised Fist"], ["✊🏽", "Olive Toned Raised Fist"], ["✊🏾", "Deeper Brown Raised Fist"], ["✊🏿", "Black Raised Fist"], ["✋🏻", "White Raised Hand"], ["✋🏼", "Light Brown Raised Hand"], ["✋🏽", "Olive Toned Raised Hand"], ["✋🏾", "Deeper Brown Raised Hand"], ["✋🏿", "Black Raised Hand"], ["✌🏻", "White Victory Hand"], ["✌🏼", "Light Brown Victory Hand"], ["✌🏽", "Olive Toned Victory Hand"], ["✌🏾", "Deeper Brown Victory Hand"], ["✌🏿", "Black Victory Hand"], ["🎅🏻", "White Father Christmas"], ["🎅🏼", "Light Brown Father Christmas"], ["🎅🏽", "Olive Toned Father Christmas"], ["🎅🏾", "Deeper Brown Father Christmas"], ["🎅🏿", "Black Father Christmas"], ["🏃🏻", "White Runner"], ["🏃🏼", "Light Brown Runner"], ["🏃🏽", "Olive Toned Runner"], ["🏃🏾", "Deeper Brown Runner"], ["🏃🏿", "Black Runner"], ["🏄🏻", "White Surfer"], ["🏄🏼", "Light Brown Surfer"], ["🏄🏽", "Olive Toned Surfer"], ["🏄🏾", "Deeper Brown Surfer"], ["🏄🏿", "Black Surfer"], ["🏇🏻", "White Horse Racing"], ["🏇🏼", "Light Brown Horse Racing"], ["🏇🏽", "Olive Toned Horse Racing"], ["🏇🏾", "Deeper Brown Horse Racing"], ["🏇🏿", "Black Horse Racing"], ["🏊🏻", "White Swimmer"], ["🏊🏼", "Light Brown Swimmer"], ["🏊🏽", "Olive Toned Swimmer"], ["🏊🏾", "Deeper Brown Swimmer"]]






quotes_string = '''
    There is no charge for awesomeness... or attractiveness.;Kung Fu Panda;http://www.google.co.in/search?ie=UTF-8&q=kung+fu+panda+awesomeness
    Any fool can write code that a computer can understand. Good programmers write code that humans can understand.;Martin Fowle;http://thc.org/root/phun/unmaintain.html
    He was so deadly, in fact, that his enemies would go blind from over-exposure to pure awesomeness!;Kung Fu Panda;
    One often meets his destiny on the road he takes to avoid it.;Kung Fu Panda;
    The world is moved along, not only by the mighty shoves of its heroes, but also by the aggregate of the tiny pushes of each honest worker.;Helen Keller;
    '''

r=requests.get("http://emojipedia.org/flags/")
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
    try0=[['smile','smiling'],['sad','disappointed'],['shocked','flushed']]
    k=str_var.split(',')
    for i in k:
        tosearch = i.lower()
        for try1,try2 in try0:
            if(tosearch in try1):
                return "Sir try :"+try2
        for a,b in emoji_arr:
            if tosearch in b.lower():
                arr.append(a)
                flag=1;
    if flag == 1:
        return " ".join(arr[:5])
    return "not found"
    


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
#response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":message_object})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
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