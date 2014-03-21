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
import pytz
from math import floor
from BeautifulSoup import BeautifulSoup

settings = {
    'prefix': "!",              # command prefix
    'host': "irc.iotek.org",    # irc server address
    'port': 6667,               # irc server port
    'nick': "obot",             # nickname
    'user': "o",                # username
    'real': "OSRICbot",         # realname
    'ssl' : True,               # use SSL?
#    'ssl' : False,              # use SSL?
    'chans': [ '#d20' ],        # channels to join on connect
    'ns_pass': "",              # set to None for no auth
}

def proc_cmd (c, e):

    cmd =  e.arguments[0][1:]
    t   = (e.arguments[0].encode)

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
