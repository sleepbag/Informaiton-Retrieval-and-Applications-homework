# -*- coding: utf-8 -*-
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in
from shutil import *

# 重複建立Index會清除現有之Index
def createIndex(path):
	schema = Schema(docId=NUMERIC(int, 64, signed=False, stored=True), content=TEXT)
	if not os.path.exists(path):
	    os.mkdir(path)
	myIndex = create_in(path, schema)

def deleteIndex(path):
	rmtree(path, ignore_errors=True)


# deleteIndex(u"index")
# createIndex(u"index")