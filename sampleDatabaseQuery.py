import sqlite3 as lite

con = lite.connect("dbFile.db")
cur = con.cursor()

cur.execute('SELECT * FROM Lexicon')
data = cur.fetchall()
print 'Lexicon: ' + str(data)

cur.execute('SELECT * FROM DocIndex')
data = cur.fetchall()
print 'DocIndex: ' + str(data)

cur.execute('SELECT DISTINCT word_id,doc_id FROM InvertedIndex WHERE word_id=1') #To get distinct tuple values as the table contains duplicates
data = cur.fetchall()
print 'InvertedIndex: ' + str(data)

cur.execute('SELECT * FROM PageRank')
data = cur.fetchall()
print 'PageRank: ' + str(data)

con.close()