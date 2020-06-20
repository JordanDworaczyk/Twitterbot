import webbrowser           # for opening twitter to verify connection to api 
import time                 # for waiting when API limit reaches max
import tweepy               # for talking to twitter API
import pickle               # for saving data
from pprint import pprint   # makes output pretty

class TwitterBot():

    def __init__(self, consumer_key=None, consumer_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # get key from user if key is none
        if self.consumer_key is None:
            self.consumer_key = input("Enter consumer key: ")

        if self.consumer_secret is None:
            self.consumer_secret = input("Enter consumer secret: ")

        self.api = self.connect()       # connect to twitter API
        self.followers_ids = []
        self.followers = []
        self.priority_followers = []
        self.called = []

    def connect(self):
        """Connect to twitter API. 

        User will be redirected to Twitter for authenticating info. The user
        will be given a verification code from Twitter.
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        try: 
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
            return False
        
        print("Redirecting you to Twitter for authorization...")
        webbrowser.open(redirect_url)
        print("Verify your twitter account")
        verifier = input('Verify Code: ')
    
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Error! Failed to get access token.')
            return False
    
        auth.set_access_token(auth.access_token, auth.access_token_secret)
        
        try: 
            self.api = tweepy.API(auth)
            print("Success! We connected to your twitter account.")
            return self.api
        except tweepy.TweepError:
            print("We couldn't connect. Try again.")
            return False
    
    def rank(self, rules):
        """Rank your followers based on criteria. 
        
        Sort your followers into ranks by the following criterias: 
            
            recently_followed: rank by who most recently
            followed you.

            followers_count: rank by who has the most followers.

            created_at: rank by who has the oldest twitter account.

            friends_count: rank by who followers the most people.

            statuses_count: rank by who has the most total tweets.

            verified: rank by who is verified and who isnt. (verified useres get
            higher priority than those who are not verified.)
        """
        self.priority_followers = []

        # Note that reverse=True makes sorted() sort from greatest to smallest
        for rule in rules:
            print(f"Ranking by {rule}...")
            if rule == 'recently_followed':
                self.priority_followers = self.followers
            elif rule == 'followers_count':
                user = lambda user: user.followers_count
                temp = sorted(self.followers, key=user, reverse=True)
                self.priority_followers = temp
            elif rule == 'created_at':
                user = lambda user: user.created_at
                self.priority_followers = sorted(self.followers, key=user)
            elif rule == 'friends_count':
                user = lambda user: user.friends_count
                temp = sorted(self.followers, key=user, reverse=True)
                self.priority_followers = temp 
            elif rule == 'statuses_count':
                user = lambda user: user.statuses_count
                temp = sorted(self.followers, key=user, reverse=True)
                self.priority_followers = temp
            elif rule == 'verified':
                user = lambda user: user.verified
                temp = sorted(self.followers, key=user, reverse=True)
                self.priority_followers = temp
            else:
                print(f"Your ranking criteria <{rule}> is invalid.")
                return False

        print("All your followers have been ranked!")
    
    def download_all_followers(self):
        """Download all of your followers. 

        Downloads your followers. Can download up to 75,000 followers every
        15 minutes. So, if you have ~210,000 followers, then it should take
        about 45 minutes or less to download.
        """
        follower_book = []
        print("Downloading...")
    
        # first get follower's @ 5000 IDs per call we have ~75000 calls 
        # every 15 minutes. So, we have an average of 5000 IDs per minute.
        try: 
            for pg in tweepy.Cursor(self.api.followers_ids, count=5000).pages():
                follower_book.append(pg)
        except tweepy.RateLimitError:
            # wait 15 minutes for API limit to reset
            print("Rate Limit Exceeded: will resume in 15 minutes...") 
            time.sleep(15 * 60)
    
        # flatten follower IDs from pages to 1D list where one elmement is 
        # one User()
        self.followers_ids = [user for pg in follower_book for user in pg]

        # get full user profiles by using users/lookup @ 100 users per call
        # we have 900 calls every 15 minutes. So, we have 6000 users per minute
        # on average
        try: 
            # get chunks of 100 users per call
            # the max limit for twitter API users/lookup is 100 per call
            for i in range(0, len(self.followers_ids), 100):
                chunk = self.followers_ids[i:i+100]
                # call API and get full users info
                for user in self.api.lookup_users(chunk):
                    self.followers.append(user)
        except tweepy.RateLimitError:
            # wait 15 minutes until API limits are reset
            print("Rate Limit Exceeded: will resume in 15 minutes...") 
            time.sleep(15 * 60)
            return False

        print("We downloaded all of your followers!")
        print(f"Total Followers: {len(self.followers_ids)}")
        return self.followers 
    
    def api_limits(self, keyword=None):
        """Returns your current twitter API allowence.

            Returns in json format. Use keyword to navigate limits. 

            Ex: to get followers limits use 

                >>> bot.api_limits('followers')
        """
        if keyword:
            try: 
                return self.api.rate_limit_status()['resources'][keyword]
            except KeyError:
                print("Error! Wrong key. Key entered is not found.")
                return False 
        return self.api.rate_limit_status()

    def send(self, text, qty=1):
        """Send priority followers a direct message.

        NOTE: Currently not been tested.
        """
        count = 0
        if qty > 1000:
            print("Qty given is more than max! Please retry.")
            return False
            
        call_sheet = self.priority_followers 
        if len(call_sheet) == 0: 
            print("Error! You need to rank your followers first!")
            return False 

        print("Send message to the following users.")
        for follower in call_sheet:
            if len(text) < 10000:
                if follower not in self.called:
                    try:
                        self.api.send_direct_message(follower.id, text)
                    except tweepy.RateLimitError:
                        # wait 15 minutes until API limits are reset
                        print("Rate Limit Exceeded: will resume in 15 minutes.")
                        time.sleep(15 * 60)
                        return False
                    print("ID: ", follower.id)
                    print("NAME: ", follower.name)
                    self.called.append(follower)
                    count = count + 1
                    if count == qty: 
                        break
            else:
                print("Error! Your message is too long! Try again.")
                return False
        print()
        self.save('session')    # save after changing data

    def save(self, name='session'):
        "Saves current instance of object as pickle."
        print("Saving data...")
        with open(name+'.pickle', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print(f"{name} is saved!")

def load(name='session'):
    "Loads a pickled object."
    print("Loading...")
    with open(name+'.pickle', 'rb') as f:
        data = pickle.load(f)
        print("Loaded data from previous session!")
        return data
