## Migration and Mastodon: LAMA's Web App

## Overview
Immigration into the United States is an extremely long and complicated process. First and foremost, there are a plethora of ways to immigrate to the US, and there are many steps and documentation involved in each process that can seem daunting.
 
In order to develop a platform that promotes community whilst providing assistance regarding the legal process of immigration, we expanded upon the Mastodon API. We developed a web app that is connected to Mastodon in multiple ways to ensure a seamless user experience between the two social computing systems. 

## Structure
```my_app``` folder contains the flask python file that contains our web-app and the HTML templates that are rendered by the web-app.

```.env``` file contains the openAI API key for accessting ChatGPT for our translation feature.

```user_token``` file contains a Mastodon user's account token to be able to access the Mastodon API.

## Features
We have a Home that outlines the norms and guidelines for individuals using our web app. In Discover and News, individuals are able to look up specific hashtags or see posts using the immigration hashtag, respectively. Additionally, users are able to track their progress in the green card application process via posting on Mastodon, after which their completion status on the web app is updated. By updating their status via the Update section, a toot is posted to Mastodon. They are able to see the steps they have completed in the process and the next steps to take via the myProgress section on the web app. Lastly, we have a Translate feature that allows users to copy and paste text in any language that they find on our web app (or Mastodon) and have it displayed in any other language. 

In summary, our main features include daily news, updating and tracking green card application progress, and a translation feature.

## How to run this code
At this moment, our platform is only able to support one user at a time, specifically for the tooting and progress tracking featutes. In order to be able to run this app, the "KEY" variable in the _.env_ file needs to be set to a valid openAI API key, and the user_token file needs to contain a valid Mastodon user's token. The _Connect_ and _Update_ pages will toot to Mastodon from this user's account, and the _myProgress_ page will pull toots regarding immigration progress from this person's account as well. 

We recommend running this app in a virtual environment by following these instructions:
- Install virtualenv: ```pip3 install virtualenv```
- Create your virtual environment: ```virtualenv venv```
- Activate your virtual environment: ```source venv/bin/activate```
- Install Mastodon: ```pip3 install Mastodon.py```
- Install Flask: ```pip3 install flask```

Then, copy and paste the given https link into a web browser and enjoy your web-app!
