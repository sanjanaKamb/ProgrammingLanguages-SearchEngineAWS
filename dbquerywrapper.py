# db wrapper for the lab2 db interaction
import sqlite3


def get_url_list_for_word(word):
    """ Returns a list of strings.
    the list will be empty if word was not found, otherwise list of urls for that search word.
    """
    # db schema comes from this
    # CREATE TABLE IF NOT EXISTS Lexicon(word_id INTEGER PRIMARY KEY, word TEXT UNIQUE);
    # CREATE TABLE IF NOT EXISTS InvertedIndex(word_id INTEGER, doc_id INTEGER);
    # CREATE TABLE IF NOT EXISTS PageRank(doc_id INTEGER PRIMARY KEY, url_rank TEXT);
    # CREATE TABLE IF NOT EXISTS DocIndex(doc_id INTEGER PRIMARY KEY, doc_url TEXT);

    # steps
    # Word >> [lexicon] >> word_id
    # word_id >> [inverted_idx] >> Doc_IDs
    # Doc_IDs >> [page_rank] >> URL_RANKS
    # probably just a python sort on url_ranks
    # sorted Doc_IDs >> [DocIdx] >> sorted URLs

    # connect to the database
    connection = sqlite3.connect('dbFile.db')
    cursor = connection.cursor()

    url_list = []
    cursor.execute('SELECT word_id FROM Lexicon WHERE word = ? ', (word,) )

    # single value tuple or None
    word_id = cursor.fetchone()
    if None == word_id:
        #print "no word id was found for " + word
        connection.close()
        return None
    #print "got " + str(word_id) + " for " + word + " type " + str(type(word_id))

    # step2, step3 and step4 combined, big thanks SQL
    cursor.execute(""" SELECT DISTINCT doc_url FROM
    (SELECT t2.url_rank, t2.doc_id, t3.doc_url
    FROM InvertedIndex t1, PageRank t2, DocIndex t3
    where t1.doc_id = t2.doc_id AND t1.doc_id = t3.doc_id AND
    t2.doc_id = t3.doc_id AND t1.word_id = ?
    ORDER BY t2.url_rank DESC)""", word_id)


    # rows is a list of tuples of strings.(the tuples only have one string in them) but there could be many tuples
    rows = cursor.fetchall()
    #print "rows: " + str(rows)

    connection.close()

    for row in rows:
        url_list.append(row[0])

    #print "url list: " + str(url_list)
    return url_list


def get_word_list_for_prefix(prefix):
    """ Returns a list of strings.
    the list will be empty if no word in the database starts with prefix,
    otherwise list of words that start with prefix.
    """
    
    # print prefix
    if None == prefix:
        return []

    prefix = str(prefix).lower()
    
    try:
        prefix = prefix.split()[0].strip()
    
    except:
        pass
    
    
    result = []

    connection = sqlite3.connect('dbFile.db')
    cursor = connection.cursor()


    cursor.execute('SELECT word FROM Lexicon WHERE word LIKE ? LIMIT 10', (prefix+"%",))


    rows = cursor.fetchall()
    #print "rows: " + str(rows)

    connection.close()

    for row in rows:
        result.append(row[0])

    return  result


if '__main__' == __name__:
    print "testing db file"
    #print get_word_list_for_prefix('ec')
    #print get_word_list_for_prefix('e')
    print get_word_list_for_prefix('to')
    
    print get_word_list_for_prefix('tor to')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    