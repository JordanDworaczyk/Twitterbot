# Twitterbot
Download your followers and sort them by some criteria so that you may 
contact your priority followers.

## Download Followers
Download your followers from Twitter so that you can sort them for priority
contact. Using Twitter's API via [tweepy](http://www.tweepy.org/) we can 
download up to 75,000 followers every 15 minutes. 

## Message by Priority
Rank your followers so that you can message each by their priority. You can 
sort your followers into ranks by the following criteria

* recently followed
* followers count 
* oldest twitter account
* who follows the most people
* who has the most total tweets
* who is verified

## Contact Followers
You can direct message up to 1000 followers each day. Twitterbot stores state
so that you know who you messaged in the past, so that you don't recontact
them by accident. You can try it out by sending test messages to a few accounts
before you decide to send a message to 1000 followers each day. 

## Getting Started
First, install Python 3:
https://www.python.org/downloads/

Then set up a virtual environment. 
```
$ python -m venv twitterbot
$ source twitterbot/bin/activate
```

Next you need to install the python dependencies. 
```
(twitterbot) $ pip install tweepy
```
Next download the source code using Git
```
(twitterbot) $ git clone https://github.com/JordanDworaczyk/Twitterbot.git 
```
Now that we have installed the dependencies. Navigate to the project folder.
We can use Twitterbot by the command line interface. Use the following command
```
(twitterbot) $ python botshell.py
```
to run the Twitterbot. You can use the `help` command to learn about the 
various commands that the Twitterbot offers.

Next, you will need to connect to Twitter using your consumer key and 
consumer secret. You can get one of these keys by registering a developer
app through Twitter. See [here](https://developer.twitter.com/en) to 
register app. You will need your consumer key and consumer secret to use
the Twitterbot.

Connect Twitterbot to your Twitter account using the `connect` command. Type
`help connect` for more details. Once you have connected your Twitterbot, use
the `save` command to save your verification details, so that you will not
need to use the `connect` command again. Once your credentials are saved, you
can reload the Twitterbot from the previous session using the `load` command.
See `help load` for more details. This `load` command comes in handy if you
exit the Twitterbot because you can load a saved session and still have 
all the previous data from before.

Now you should be connected to Twitter and good to go!
