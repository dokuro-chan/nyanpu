#!/usr/bin/env python

# @author: William B.
# @github: https://github.com/dokuro-chan
# @description: Cute minimal IRC bot for fun.
# @contact: w^x@0nl1ne.cc (elmo@irc.rizon.net #nyanya)

# @note: This bot was inspired by a twitch bot a friend of mine wrote awhile back.

import re, sys, time
import socket, random

class NyanRC:
  def __init__(self):
    # main settings
    self.debg = 1 # enable debugging
    self.nya = None # fd for socket
    self.port = 6667 # irc server port
    self.user = "nya" # bot username
    self.oper = "elmo" # bot owner/operator
    self.nick = "nyan" # bot nick
    self.name = "nyanya" # bot real name
    self.chan = "#nyanya" # irc channel
    self.pswd = "********" # bot password
    self.serv = "irc.rizon.net" # irc server
    
  # quit in a neat manner
  def nyanquit(self):
    self.nya.close()
    self.nya = None
    exit(0)
    
  # show help
  def nyanhelp(self, c):
    self.nya.send("PRIVMSG %s :List of available commands...\r\n" % (c))
    self.nya.send("PRIVMSG %s :- !o | give user op status\r\n" % (c))
    self.nya.send("PRIVMSG %s :- syntax: !o <#channel> <nick>\r\n" % (c))
    self.nya.send("PRIVMSG %s :- !j | make bot join channel\r\n" % (c))
    self.nya.send("PRIVMSG %s :- syntax: !j <#channel>\r\n" % (c))
    self.nya.send("PRIVMSG %s :- !p | make bot part channel\r\n" % (c))
    self.nya.send("PRIVMSG %s :- syntax: !p <#channel>\r\n" % (c))
    self.nya.send("PRIVMSG %s :- !q | quit/kill bot\r\n" % (c))
    self.nya.send("PRIVMSG %s :- !h | show this help message\r\n" % (c))
    
  # reply to pings
  # def nyanpong(self, m):
  #   self.nya.send("PONG %s\r\n" % (m))
    
  # join channel
  def nyanjoin(self, c):
    self.nya.send("JOIN %s\r\n" % (c))
    
  # part channel
  def nyanpart(self, c):
    self.nya.send("PART %s\r\n" % (c))
    
  # send message
  def nyansend(self, c, m):
    self.nya.send("PRIVMSG %s :%s\r\n" % (c, m))
    
  # connect and login
  def first(self):
    self.nya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.nya.settimeout(14)
    
    try: self.nya.connect((self.serv, self.port))
    except: self.nyanquit()
    
    self.nya.settimeout(None)
    
    # authenticate and join channel
    self.nya.send("USER %s %s %s :%s\r\n" % (self.user, self.user, self.user, self.user))
    self.nya.send("NICK %s\r\n" % (self.nick))
    self.nya.send("PRIVMSG NickServ :IDENTIFY %s\r\n" % (self.pswd))
    self.nya.send("JOIN %s\r\n" % (self.chan))
    
    while(1):
      print(self.nya.recv(1024))
      data = self.nya.recv(1024)
      data = data.rstrip()
      data = data.split()
      
      # show some help
      if data[3].startswith(":!h"):
        cnl = data[2]
        self.nyanhelp(cnl)
        
      # op user
      if data[3].startswith(":!o"):
        cn = data[4]
        ta = data[5]
        self.nya.send("MODE %s +o %s\r\n" % (cn, ta))
        
      # join channel
      if data[3].startswith(":!j"):
        cnl = data[4]
        self.nyanjoin(cnl)
        
      # leave channel
      if data[3].startswith(":!p"):
        cnl = data[4]
        self.nyanpart(cnl)
        
      # quit/exit
      if data[3].startswith(":!q"):
        self.nyanquit()
        
nyan = NyanRC()
nyan.first()
