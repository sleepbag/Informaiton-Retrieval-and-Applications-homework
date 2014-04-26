from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring


myindex = index.open_dir("index")
searcher = myindex.searcher(weighting=scoring.TF_IDF())

qp = QueryParser("content", schema=myindex.schema)
q = qp.parse(u"Nokia")
results = searcher.search(q, limit=None)

#for x in results:
	#print "docId = %5r , score = %r" %(x['docId'], x.score)
a = 0
for contents in searcher.lexicon("content"):
	print contents
