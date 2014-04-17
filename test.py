# -*- coding: utf-8 -*-
import warc
from HTMLParser import HTMLParser
from whoosh import index
from whoosh.qparser import QueryParser
import gc
import re
import sys
import time


def striphtml(data):
    p = re.compile(r'<.*?>|/a>|&nbsp;')
    return p.sub(' ', data)

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
    	if (data != '\n' and self.skip):
    		self.content += data+' '
    		self.datalist.append(data)
    	self.skip = True

    content = ''
    skip = False
    datalist = []
    def getData(self):
    	return self.content

    def getDataList(self):
    	return self.datalist

    def kill(self):
        del self
        
def run(string):
    myindex = index.open_dir("index")
    writer = myindex.writer(procs=3,  multisegment=True, limitmb=512)
    f = None
    try:
        f = warc.open(string)
    except :
        print "Can't open this file" 
        sys.exit()

    i = 0
    print "start read record!"
    for record in f:
        i = i + 1
        
        if i >= 2:
            # parser = MyHTMLParser()
            try:    
                # parser.feed(unicode(record.payload, errors='ignore'))
                # data = parser.getData().decode('utf8')
                data = striphtml(unicode(record.payload, errors='ignore'))
                #print "write the data of %d" %(i)
                if (i % 10000) == 0:
                    print "write the data of %d" %(i)
                    print "commit now"
                    start = time.time()
                    writer.commit()
                    stop = time.time()
                    print "commit over ", (stop - start)
                    writer = myindex.writer(procs=3,  multisegment=True, limitmb=512)
                    gc.collect()
            except Exception as e:
                print "error in the data of %d" %(i)
                print e.message, e.args
                print "------------------------"
                # print data
            #parser.kill()
            writer.add_document(docId=i-1, content=data)
            # print record.header
            # print "-----------------------------------------"
            # print record.payload
            # print "-----------------------------------------"
            # print data
    print "final commit now"
    start = time.time()
    writer.commit(procs=3,  multisegment=True, limitmb=512)
    stop = time.time()
    print "final commit over", (stop - start)

# defaultString = "05.warc.gz"
# tStart = time.time()
# run(defaultString)
# tStop = time.time()

# print "Time :", tStop - tStart

# searcher = myindex.searcher()
# print len(list(searcher.lexicon("content")))


    
