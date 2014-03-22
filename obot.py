#!/usr/bin/python2
# OSRICbot barebone

"""                 IOTek in-house solution for DnD & Neckbearding

                    Brought to you by dami-ooooh <dami0@iotek.org>

                                   Based on batcot

                              There is in fact, a spoon

"""

import sys
import time
import ssl
import irc.client
import urllib2
import json
import datetime
import random
#import pytz
from math import floor
#from BeautifulSoup import BeautifulSoup

settings = {
    'prefix': "!",              # command prefix
    'dicepre' : ".",            # dice prefix
    'host': "irc.iotek.org",    # irc server address
    'port': 6667,               # irc server port
    'nick': "obot",             # nickname
    'user': "o",                # username
    'real': "OSRICbot",         # realname
#    'ssl' : True,               # use SSL?
    'ssl' : False,              # use SSL?
    'chans': [ '#d20' ],        # channels to join on connect
    'ns_pass': "",    # set to None for no auth
}

class play_char:
    'This is the class for the player characters'
    player_count = 0

    def __init__(self, name, clas, algn, race, xp, hp, ac, lvl, age, hght, wght,
            sex, attr)
        self.name = name
        self.clas = clas
        self.algn = algn
        self.race = race
        self.xp   = xp
        self.hp   = hp
        self.ac   = ac
        self.lvl  = lvl
        self.age  = age
        self.hght = hght
        self.wght = wght
        self.sex  = sex
        self.attr = attr


def proc_die (c, e):

    if e.target == '#nixers': return
    
    msg  = ""
    cmd  = e.arguments[0][1:]
    t    = (e.arguments[0].encode("ascii", "ignore")).split(' ')
    t[0] = t[0][1:]
    nick = e.source.nick.encode("ascii", "ignore")
    random.seed()

    if 4 > len(t) > 0:
        wins = 0; rolls = []
        t = extract(t)
        print(t)
        if t == None: return
        for x in range(0, t[2]):
            rolls.append(random.randint(1, t[0]))
            if rolls[-1] >= t[1]: wins += 1
        rolls = ', '.join(str(x) for x in rolls)
        if t[1] > 0:
            if   t[2] == 1 and wins == 1: msg = "Success; "
            elif t[2] == 1 and wins == 0: msg =  "Fail; "
            elif t[2] > 1: msg = str(wins) + " successes; "
        msg = msg + rolls

    if msg: 
        msg = nick + ": " + msg
        c.privmsg(e.target, msg)

def extract (raw):
    try:
        stuff = []
        print(raw)
        for lmnt in raw:
            if len(lmnt) > 0: stuff.append(int(lmnt))
        print("stuff: " + ', '.join(str(x) for x in stuff))
        if len(stuff) < 2: stuff.append(0)
        if len(stuff) < 3: stuff.append(1)
        if stuff[1] < 0: stuff[1] = 0
        if stuff[1] > stuff[0]: return None
        if stuff[2] < 0: stuff[2] = 1
        return stuff
    except: return None


def on_connect (c, e):

    if settings['ns_pass']:
        c.privmsg("NickServ", "IDENTIFY %s" % settings['ns_pass'])
        print("nickserv pass")
        time.sleep(3)
    for chan in settings['chans']:
        print("[JOIN] %s" % chan)
        c.join(chan)

def on_disconnect (c, e):

    c.reconnect()

def on_pubmsg (c, e) :

    if e.arguments[0].startswith(settings['prefix']):
        proc_cmd(c, e)
    elif e.arguments[0].startswith(settings['dicepre']):
        proc_die(c, e)

if (__name__ == '__main__'):
    # ssl?
    ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket) if (
    settings['ssl']) else None
    client = irc.client.IRC()
    server = client.server()
    server.buffer_class.errors = 'replace'

    try:
        if ssl_factory:
            c = server.connect(
                settings['host'],
                settings['port'],
                settings['nick'],
                username=settings['user'],
                ircname=settings['real'],
                connect_factory=ssl_factory,
                )
        else:
            c = server.connect(
                settings['host'],
                settings['port'],
                settings['nick']
                )
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("welcome", on_connect)
#    c.add_global_handler("privmsg", on_privmsg)
    c.add_global_handler("pubmsg",  on_pubmsg)
    c.add_global_handler("disconnect", on_disconnect)
    # other handlers

    client.process_forever()
