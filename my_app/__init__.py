import os
import re
import io
import openai
from mastodon import Mastodon
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from bs4 import BeautifulSoup
import uuid, json, requests
from dotenv import load_dotenv
load_dotenv()


f = open("./user_token",'r')
token = f.readlines()[0]
#hashtag = "immigration"

# create and configure the app
app = Flask(__name__, instance_relative_config=True) 

# set openai api key
api_key=os.getenv("KEY",None)
#client = OpenAI(api_key=OPEN_AI_KEY)

"""
****** UPDATE ******
We do not need a database amymore, so this code is not relevant anymore.

### database configuration ###
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
migrate = Migrate(app, db) # database migrations are used to keep the database up to date 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    step1 = db.Column(db.S, unique=False, nullable=False)
    step2 = db.Column(db.Boolean, unique=False, nullable=False)
    step3 = db.Column(db.Boolean, unique=False, nullable=False)
    step4 = db.Column(db.Boolean, unique=False, nullable=False)
    step5 = db.Column(db.Boolean, unique=False, nullable=False)

    # repr method represents how one object of this datatable will look like
    def __repr__(self):
        return f"ID: {self.id}, username: {self.sername}, progress: {self.progress}"

with app.app_context():
    db.create_all() # create the database if it doesn't already exist

### end database configuration ###
"""

# HOME PAGE
@app.route('/')
@app.route('/home/')
def home():
    return render_template('about.html')

# HASHTAG_POSTS
@app.route("/immigration/discover/")
def discover():
    hashtag = request.query_string
    hashtag = str(hashtag)[2:-1]
    print(hashtag)
    number = 20
    m = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
    timeline = m.timeline_hashtag(hashtag, limit=number) # get timeline under the given hashtag
    print(timeline) # for debugging purposes, see console
    for toot in timeline: 
        content = toot['content']
        toot['content'] = str(BeautifulSoup(toot['content'],features="html.parser").get_text())
        url = toot['url']
        account = toot['account']['username']
        print(account, content, url) # for debugging purposes, see console
    
    # passing the timeline json object to the html template
    return render_template('timeline.html', timeline=timeline)

"""
def html_to_text(message):
    return str(BeautifulSoup(message,features="html.parser").get_text())
app.jinja_env.globals.update(html_to_text=html_to_text) # make the html_to_text function available to the html templates
"""


# FIND_HASHTAG (For HASHTAG_POSTS)
@app.route("/immigration/find_hashtag/", methods=('GET', 'Post'))
def find_hashtag():
    if request.method == 'POST':
        # print(request)
        hashtag = request.form['hashtag'] # get the username from the request object
        #print(hashtag) # for debugging purposes, see console
        m = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
        return redirect("/immigration/discover?"+hashtag)
        #discover(hashtag)
    
    return render_template('hashtag.html', hashtag = None)

@app.route("/immigration/news/", methods=('GET', 'Post'))
def news():
    hashtag = "immigration"
    number = 20
    m = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
    timeline = m.timeline_hashtag(hashtag, limit=number) # get timeline under the given hashtag
    print(timeline) # for debugging purposes, see console
    for toot in timeline: 
        content = toot['content']
        toot['content'] = str(BeautifulSoup(toot['content'],features="html.parser").get_text())
        url = toot['url']
        account = toot['account']['username']
        # print(account, content, url) # for debugging purposes, see console
    return render_template('news_results.html', timeline=timeline) 
        # render_template('respond.html')

    # passing the timeline json object to the html template
    return render_template('news.html', timeline=timeline)

# USERS CONNECT
@app.route("/immigration/connect/", methods=('GET', 'POST'))
def connect():
    mastodon = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
    if request.method == 'POST': # do this only if a POST request is made
        post_url = request.url # since post url is appended to current URL, get URL
        resp = request.form['resp']

        if not resp:
            flash('Response is required!')
        else: # post to Mastodon
            # find the post ID
            pattern = r"/(\d+)$"
            match = re.search(pattern, post_url)
            if match:
                in_reply_to_id = match.group(1)
            else:
                print("Post ID not found")

            # post response to Mastodon
            mastodon.status_post(
                status=resp,
                in_reply_to_id=in_reply_to_id
            )

            return render_template('success.html') # render the success page
        
    return render_template('response.html')


# UPDATE PROGRESS
@app.route("/immigration/update/", methods=('GET', 'POST'))
def update():
    if request.method == 'POST': # do this only if a POST request is made
        content = request.form['content'] # get data via the request object
        checkbox = request.form['step']
        print(checkbox)
        if not content:
            flash('Content is required!')
        else: # if both title and content are provided, post to Mastodon
            m = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
            m.toot(content + " \n#Completed" + checkbox + " #myProgressTracker")

            # add progress to database
            return render_template('success.html') # render the success page
    
    return render_template('toot.html')

@app.route("/immigration/myProgress/", methods=('GET', 'Post'))
def myProgress():
    hashtag = "myProgressTracker"
    number = 20
    m = Mastodon(access_token=token, api_base_url="https://social.cs.swarthmore.edu")
    timeline = m.timeline_hashtag(hashtag, limit=number) # get timeline under the given hashtag
    #print(timeline) # for debugging purposes, see console

    for i in range((len(timeline)-1), -1, -1):
        toot = timeline[i]
        content = toot['content']
        print(toot['content'])
        toot['content'] = str(BeautifulSoup(toot['content'], features="html.parser").get_text())
        url = toot['url']
        account = toot['account']['username']
        if account != "myercel1":
            timeline.pop(i)

       
    # passing the timeline json object to the html template
    return render_template('progress.html', timeline=timeline)

@app.route("/immigration/translate/", methods=['GET', 'POST'])
def translate():
    # Read the values from the form
    if request.method == 'POST': # do this only if a POST request is made
        original_text = request.form['text']
        target_language = request.form['language']

        if not original_text:
            flash('Text is required!')
        if not target_language:
            flash('Language is required!')
        else:
            """
            # Load the values from .env
            key = os.environ['KEY']
            endpoint = os.environ['ENDPOINT']
            location = os.environ['LOCATION']

            # Indicate that we want to translate and the API version (3.0) and the target language
            path = '/translate?api-version=3.0'
            # Add the target language parameter
            target_language_parameter = '&to=' + target_language
            #Create the full URL
            constructed_url = endpoint + path + target_language_parameter

            # Set up the header information, which includes our subscription key
            headers = {
                'Ocp-Apim-Subscription-Key': key,
                'Ocp-Apim-Subscription-Region': location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }

            # Create the body of the request with the text to be translated
            body = [{ 'text': original_text }]

            # Make the call using post
            translator_request = requests.post(constructed_url, headers=headers, json=body)
            # Retrieve the JSON response
            translator_response = translator_request.json()
            # Retrieve the translation
            translated_text = translator_response[0]['translations'][0]['text']
"""
            translated_text = translate_text(original_text, target_language)
            
    # Call render template, passing the translated text,
    # original text, and target language to the template
        return render_template(
            'results.html',
            translated_text=translated_text,
            original_text=original_text,
            target_language=target_language
        )
    return render_template('translate.html')

def translate_text(original_text, target_language):

    prompt = f"Translate the following text to {target_language}: \n\n{original_text}"
    openai.api_key=api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # get translated response from API 
    translated_text = response['choices'][0].message.content.strip()

    return translated_text

