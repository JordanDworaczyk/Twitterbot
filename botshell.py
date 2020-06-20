#!/usr/bin/env python
import cmd, sys
from pprint import pprint
from twitterbot import *

class BotShell(cmd.Cmd):

    intro = 'Welcome to the twitterbot shell. Type help or ? to list commands.\n'    
    prompt = '(twitterbot) ' 
    file = None

    def do_connect(self, arg):
        """Link to your twitter account: CONNECT 
        
        You will be sent to Twitter so that you can log in and verify your 
        account. After you verify with Twitter you will be given a verification
        code which you will enter into the prompt.

        If you have not already entered in your consumer keys and secrets, 
        then you will be prompted to do so.
        """
        self.bot = TwitterBot() 
    
    def do_download(self, arg):
        """Download all followers: DOWNLOAD 
        
        Can download up to 75,000 followers every 15 minutes. So, if you 
        have ~210,000 followers, then it should take about 45 minutes or 
        less to download.
        """
        try:
            self.bot.download_all_followers()
        except AttributeError:
            print("Error! Bot is not connected/loaded. Nothing to download.")
            return False

    def do_rank(self, arg):
        """Rank by some criteria: RANK <options>
        
        options
        ========
        <recently_followed>      rank by who most recently followed you
        <followers_count>        rank by who has the most followers
        <created_at>             rank by who has the oldest twitter account
        <friends_count>          rank by who followers the most people
        <statuses_count>         rank by who has the most total tweets
        <verified>               rank by who is verified and who isnt

        Ex: 
            rank followers_count statuses_count friends_count

        will rank your followers by how many followers they have, the amount
        of statuses they have, and the amount of people that they follow.
        """
        try:
            if len(self.bot.followers) == 0:
                print("Error! No followers downloaded.")
                return False
            self.bot.rank(parse(arg))
        except AttributeError:
            print("Error! Bot is not connected/loaded. Nothing to rank.")
            return False

    def do_limits(self, arg):
        "Get current API limits: LIMITS"
        try:
            pprint(self.bot.api_limits(*parse(arg)))
        except AttributeError:
            print("Error! Bot is not connected/loaded. No limits to fetch.")
            return False

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def do_exit(self, arg):
        """Close the twitter bot window, and exit: EXIT
        
        Note that it is highly recommended to save before exiting.
        SEE save command.
        """
        print('Thank you for using twitter bot')
        self.close()
        return True

    def do_followers(self, arg):
        "Lists the IDs of the people who are following you: FOLLOWERS"
        try:
            if len(self.bot.followers) == 0:
                print("Error! No followers downloaded.")
                return False
            pprint([follower.id for follower in self.bot.followers])
        except AttributeError:
            print("Error! Bot is not connected/loaded. No followers to fetch.")
            return False

    def do_priority(self, arg):
        "Lists the IDs of people who are priority based on rankings: PRIORITY"
        try:
            if len(self.bot.followers) == 0:
                print("Error! No followers downloaded.")
                return False
            if len(self.bot.priority_followers) == 0:
                print("Error! No priority. You need to rank your followers.")
                return False
            pprint([follower.id for follower in self.bot.priority_followers])
        except AttributeError:
            print("Error! Bot is not connected/loaded. No priorities.")
            return False

    def do_send(self, arg):
        """Sends direct message to priority followers: SEND <quantity>
        
        <quantity>: the amount of messages you would like the bot 
        to send out. 

        Ex:

            >>> send 15

        Will send the message to 15 of your priority followers. Starting 
        with the highest of priority.

        NOTE: currently not been tested.
        """
        try:
            text = input("Message you wish to send: ")
            temp = parse(arg)
            if len(temp) == 1:
                qty = int(temp[0])
                self.bot.send(text, qty)
            else:
                print("Error! Did not specify the quantity of messages.")
                return False
        except AttributeError:
            print("Error! Bot is not connected/loaded. No priorities.")
            return False

    def do_save(self, arg):
        """Saves current session: SAVE
        
        Save your current session's data. This is HIGHLY RECOMENDED. All data
        will be saved including the followers you have already contacted as 
        well as your Twitter verification credentials. 

        Next time you use the Twitterbot app be sure to load your session 
        that you saved before exiting. SEE load command.
        """
        try:
            self.bot.save(*parse(arg))
        except AttributeError:
            print("Error! Bot is not connected/loaded. Nothing to save.")
            return False

    def do_load(self, arg):
        """Loads previous session: LOAD
        
        Loading reloads your last session that you saved. Everything from
        who you consider your priority followers to the followers that you 
        have already contacted will be loaded back into the twitterbot.

        Avoid having to reconnect reverify your Twitter account by loading
        your last session. Loading your previous session, and saving your 
        current session is highly recomended. SEE save command.
        """
        try:
            self.bot = load(*parse(arg))
        except FileNotFoundError:
            print("Error! Nothing to load.")

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    BotShell().cmdloop()
