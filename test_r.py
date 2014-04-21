# -*- coding: utf-8 -*-
import warc
from HTMLParser import HTMLParser
from whoosh import index
from whoosh.qparser import QueryParser
import gc
import re
import sys
import time
from createIndex import *


def striphtml(data):
    # get only the body content
    # remove the newlines
    # print data
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
   
    # replace consecutive spaces into a single one
    data = " ".join(data.split())   

    x = re.search('(<body[^<>]*?>.*?</body>)', data, re.DOTALL)
    if x == None:
        x = re.search('(<body[^<>]*?>.*/)', data, re.DOTALL)
        if x == None:
            #print data
            return None
        else:
            data = x.groups()[0]
    else:
        data = x.groups()[0]

    #print data

    # now remove the java script
    p = re.compile(r'<script[^<>]*?>.*?</script>')
    data = p.sub('', data)
   
    # remove the css styles
    p = re.compile(r'<style[^<>]*?>.*?</style>')
    data = p.sub('', data)

    # remove the css styles
    p = re.compile(r'<!-.*?->')
    data = p.sub('', data)
    
    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)
   
    # remove all the tags
    p = re.compile(r'<[^<]*?>|&.*?;')
    data = p.sub(' ', data)    
    
    return data      

def run(string):
    f = None
    try:
        f = warc.open(string)
    except :
        print "Can't open this file" 
        sys.exit()

    i = 0
    error = 0
    print "start read record!"
    for record in f:
        i = i + 1
        if i > 2:
            data1 = striphtml(unicode(record.payload, errors='ignore'))
            if data1 == None:
                error = error + 1
            if (i % 1000) == 0 :
                print error
                print i
    print error
            

defaultString = "05.warc.gz"
tStart = time.time()
run(defaultString)
tStop = time.time()






    
