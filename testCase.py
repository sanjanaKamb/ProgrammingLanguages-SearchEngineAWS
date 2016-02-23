import unittest
from crawler import crawler
import sqlite3 as lite

class testCase(unittest.TestCase):
  con = lite.connect("dbFileTest.db")
  cur = con.cursor()

  #The webpage in testOneLink.txt contains a link to a sample webpage with no links
  bot = crawler(con, "testOneLink.txt")
  bot.crawl(depth=1)

  con.close()

  #Test for total number of words in both webpages
  def test_number_of_words(self):
     expectedNumWords = 89
     self.assertEqual(expectedNumWords,len(crawler.lexicon))

  #Test for total number of urls
  def test_number_of_urls(self):
      expectedNumUrls = 2
      self.assertEqual(expectedNumUrls,len(crawler.document_url))

  #Test that the word 'paragraph' is present for both urls in resolved_inverted_index
  def test_resolved_inverted_index(self):
      word = 'paragraph'
      expectedNumUrls = 2
      expectedUrl1  = 'http://www.ecf.utoronto.ca/~kambalap/'
      expectedUrl2 = 'http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm'
      self.assertEqual(expectedNumUrls, len(crawler.resolved_inverted_index[word]))
      self.assertTrue(expectedUrl1 in crawler.resolved_inverted_index[word])
      self.assertTrue(expectedUrl2 in crawler.resolved_inverted_index[word])

  #Test that word IDs for 'webpage' matches url IDs in inverted index
  def test_inverted_index(self):
      expectedWord = 'webpage'
      expectedUrl1  = 'http://www.ecf.utoronto.ca/~kambalap/'
      expectedUrl2 = 'http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm'
      word_id = 2
      url1_id = 1
      url2_id = 2
      #Test lexicon has the correct word_id for 'webpage'
      self.assertEqual(expectedWord,crawler.lexicon[word_id])
      #Test document_url has correct url IDs
      self.assertEqual(expectedUrl1,crawler.document_url[url1_id])
      self.assertEqual(expectedUrl2,crawler.document_url[url2_id])
      #Test inverted_index contains correct url_ids to word_id
      self.assertTrue(url1_id in crawler.inverted_index[word_id])
      self.assertTrue(url2_id in crawler.inverted_index[word_id])

  #Test that the word ID for 'sample' is present only in one url
  def test_inverted_index_false(self):
      expectedWord = 'sample'
      expectedUrl1  = 'http://www.ecf.utoronto.ca/~kambalap/'
      expectedUrl2 = 'http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm'
      word_id = 1
      url1_id = 1
      url2_id = 2
      #Test lexicon has the correct word_id for 'sample'
      self.assertEqual(expectedWord,crawler.lexicon[word_id])
      #Test in inverted_index that 'sample' is present only in one url
      self.assertTrue(url1_id in crawler.inverted_index[word_id])
      self.assertFalse(url2_id in crawler.inverted_index[word_id])

  #Test that all words are mapped correctly in doc_index for url 'http://www.ecf.utoronto.ca/~kambalap/'
  def test_doc_index(self):
      expectedWords = ['sample','webpage','with','one','link','word','-','paragraph','link']
      url_id = 1
      for word_id_tuple in crawler.doc_index[url_id]:
          word = crawler.lexicon[word_id_tuple[0]]
          self.assertTrue(word in expectedWords)

  #Test page rank structure is as expected for url 'http://www.ecf.utoronto.ca/~kambalap/'
  def test_page_rank(self):
      expected_page_rank =  {1: 0.15000000000000002}
      self.assertEqual(expected_page_rank,crawler.call_pagerank())

   #Test link_state structure is as expected for url 'http://www.ecf.utoronto.ca/~kambalap/'
  def test_page_rank(self):
      expected_link_database =  [(1, 2)]
      self.assertEqual(expected_link_database ,crawler.get_link_database())


if __name__ == '__main__':
    unittest.main()