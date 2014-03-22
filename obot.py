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

def proc_die (c, e):

    msg  = ""
    cmd  = e.arguments[0][1:]
    t    = (e.arguments[0].encode("ascii", "ignore")).split(' ')
    t[0] = t[0][1:]
    nick = e.source.nick.encode("ascii", "ignore")
    random.seed()

    if 'd' in t[0] and 3 > len(t):
        wins = 0; rolls = []
        t = extract(t)
        print(t)
        if t == None: return
        for x in range(0, t[0]):
            rolls.append(random.randint(1, t[1]))
            if rolls[-1] >= t[2]: wins += 1
        rolls = ', '.join(str(x) for x in rolls)
        if   t[0] == 1 and wins == 1: msg = "Success; "
        elif t[0] == 1 and wins == 0: msg =  "Fail; "
        elif t[0] > 1: msg = str(wins) + " successes; "
        if   t[2] == 0: msg = rolls
        msg = msg + rolls + "."

    if msg: c.privmsg(e.target, msg)

def extract (raw):
    try:
        stuff = []
        i = raw[0].split('d')[0]
        if len(i) > 0: stuff.append(int(i))
        elif len(i) < 1 or int(i) < 1: stuff.append(1) 
        raw[0] = raw[0].split('d')[1]
        if raw[0] < 1: return
        stuff.append(int(raw[0]))
        if len(raw) > 1:
            if raw[1] < 0: raw[1] = 0
            if raw[1] > raw[0]: return
            if raw[1]: stuff.append(int(raw[1]))
        else: stuff.append(0)
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
