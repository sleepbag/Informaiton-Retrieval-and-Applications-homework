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

    # remove the css styles
    p = re.compile(r'<a [^<>]*?>.*?</a>')
    data = p.sub('', data)    
    
    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)
   
    # remove all the tags
    p = re.compile(r'<[^<].*?>|&.*?;')
    data = p.sub(' ', data)

    return data

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if (tag == 'body'):
            self.skip = True
        if (tag == 'script'):
            self.skipScript = False
        else:
            self.skipScript = True

    def handle_data(self, data):
        if (data != '\n' and self.skip and self.skipScript):
            self.content += data+' '

    content = ''
    skip = False
    skipScript = True
    def getData(self):
        return self.content

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
    count = 1
    datalist = []
    print "start read record!"
    for record in f:
        i = i + 1
        
        if i >= 2:
            # parser = MyHTMLParser()
            try:    
                
                # data = striphtml(unicode(record.payload, errors='ignore'))
                # datalist.append(data)

                # if data == None :
                    # print i
                parser = MyHTMLParser()
                parser.feed(unicode(record.payload, errors='ignore'))
                data = parser.getData().decode('utf8')
                # datalist.append(data2)
                parser.kill()

                if (i % 15000) == 0:
                    print "write the data of %d" %(i)
                    # for x in datalist:
                    #     writer.add_document(docId=count, content=x)
                    #     count += 1
                    print "commit now"
                    start = time.time()
                    writer.commit()
                    stop = time.time()
                    print "commit over ", (stop - start)
                    writer = myindex.writer(procs=3,  multisegment=True, limitmb=512)
                    datalist = []
                    gc.collect()
            except Exception as e:
                print "error in the data of %d" %(i)
                print e.message, e.args
                print "------------------------"
                # print data
            #parser.kill()
            writer.add_document(docId=i-1, content=data)
    # for x in datalist:
    #     writer.add_document(docId=count, content=x)
    #     count += 1
    print "final commit now"
    start = time.time()
    writer.commit()
    stop = time.time()
    print "final commit over", (stop - start)

defaultString = "05.warc.gz"
#run(defaultString)


    
