# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
 
    def get_guid(self):
        return self.guid
        
    def get_title(self):
        return self.title
     
    def get_description(self):
        return self.description
        
    def get_link(self):
        return self.link
        
    def get_pubdate(self):
        return self.pubdate
    
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ', '.join(sb)
 
    def __repr__(self):
        return self.__str__()
        
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ', '.join(sb)
 
    def __repr__(self):
        return self.__str__() 

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger, NewsStory):
    def __init__(self, argument, phrase):
        self.argument = argument
        self.phrase = phrase
        
    def is_phrase_in(self, argument):
        phrase_str, argument_str = self.phrase.lower(), self.argument.lower()
        remove = re.compile('[^a-zA-Z]')
        phrase_str = remove.sub(' ', phrase_str)
        phrase_str = " ".join(phrase_str.split())

        if argument_str in phrase_str:
            f, l = phrase_str.index(argument_str[0]), phrase_str.rindex(argument_str[-1])+2
            phrase_str = phrase_str[f:l].strip()
            return argument_str == phrase_str
        else:
            return False
        
            
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, argument):
        self.argument = argument
        
    def evaluate(self, story):
        self.phrase = story.get_title()
        return self.is_phrase_in(self.argument)

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger): 
    def __init__(self, argument):
        self.argument = argument

    def evaluate(self, story):
        self.phrase = story.get_description()
        return self.is_phrase_in(self.argument)
        
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger, NewsStory):
    def __init__(self, EST):
        self.EST = datetime.strptime(EST, '%d %b %Y %H:%M:%S')
    
    def fix_pubdate(self, story):
        self.pubdate = story.get_pubdate()
        return self.pubdate.replace(tzinfo=None)
        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        self.pubdate = self.fix_pubdate(story)
        return self.pubdate < self.EST
        
class AfterTrigger(TimeTrigger): 
    def evaluate(self, story):
        self.pubdate = self.fix_pubdate(story)
        #print(self.pubdate, self.EST)
        return self.pubdate > self.EST

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger, NewsStory):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)
        
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger, NewsStory):
    def __init__(self, trig1, trig2):
        self.trig1, self.trig2 = trig1, trig2
    
    def evaluate(self, story):
        #print('AND',self.trig1.evaluate(story), self.trig2.evaluate(story))
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger, NewsStory):
    def __init__(self, trig1, trig2):
        self.trig1, self.trig2 = trig1, trig2
    
    def evaluate(self, story):
        #print('OR', self.trig1.evaluate(story), self.trig2.evaluate(story))
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_list = []

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_list.append(story)
            else:
                continue
            
    return filtered_list



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
            
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
        
    trigger_dict = {'TITLE': TitleTrigger,
                   'DESCRIPTION': DescriptionTrigger,
                   'AFTER': AfterTrigger,
                   'BEFORE': BeforeTrigger,
                   'NOT': NotTrigger,
                   'AND': AndTrigger,
                   'OR': OrTrigger,
                   'PHRASE': PhraseTrigger}
   
 
    broken_lines = []
    for line in lines:
        broken_lines.append(line.split(','))
        
    trig_dic = dict()
    triggerlist = []
    
    for line in broken_lines: 
        var_name, trig = line[0], line[1]  
        if var_name == 'ADD':
            for t in line[1:]: triggerlist.append(trig_dic[t])      
        elif trig == 'AND' or trig == 'OR':
            arg_one, arg_two = trig_dic[line[2]], trig_dic[line[3]]
            trig_dic.update({var_name: trigger_dict[trig](arg_one, arg_two)})
        else:
            str_arg =   ' '.join(line[2:])
            trig_dic.update({var_name: trigger_dict[trig](str_arg)})
            
    return triggerlist

    

SLEEPTIME = 60 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("London")
#        t2 = DescriptionTrigger("Terror")
#        t3 = DescriptionTrigger("attack")
#        t5 = AfterTrigger("18 Jun 2017 17:00:10")
#        t6 = AndTrigger(t1, t5)
#        t4 = AndTrigger(t2, t3)
#        triggerlist = [t6, t4]
    
        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')

        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

