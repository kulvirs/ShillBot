
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker
from workers.basic_worker import WorkerException


class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(ConnectionRefusedError, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read()

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)
        
    # def test_worker_add_links_in_crawled(self):
        # worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        # worker.crawled = []

        # len_to_crawl_before = len(worker.to_crawl)
        # worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        # len_to_crawl_after = len(worker.to_crawl)

        # self.assertEqual(len_to_crawl_after, len_to_crawl_before)
        
    def test_worker_crawl_links(self):
        """
        Purpose: Test if worker.to_crawl and worker.crawled are updated correctly after links are crawled
        Expectation: Once all links are crawled, len_to_crawl should be 0 and len crawled should be equal to number of links
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []
        num_links_to_crawl = len(worker.to_crawl)
        len_crawled_before = len(worker.crawled)

        self.assertRaises(ConnectionRefusedError, worker.run)
        len_to_crawl_after = len(worker.to_crawl)
        len_crawled_after = len(worker.crawled)

        self.assertEqual(len_to_crawl_after,0)
        self.assertEqual(len_crawled_before+num_links_to_crawl,len_crawled_after)
        
    def test_worker_invalid_links(self):
        """
        Purpose: Test running of Worker if it is given an invalid link to crawl (a link that returns 404).
        Expectation: WorkerException is raised.
        """
        #the following link: http://gdalskjfakl.com/ was invalid at the time this test was written
        worker = BasicUserParseWorker("http://gdalskjfakl.com/")
        self.assertRaises(WorkerException,worker.run)
        
    def test_worker_add_links_list(self):
        """
        Purpose: Test adding a list of links to worker to_crawl, with duplicate links in the list
        Expectation: The size of to_crawl increases by the size of the unique items in the list (which is 3 in this test)
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        len_to_crawl_before = len(worker.to_crawl)
        
        li = ["https://www.reddit.com/user/Chrikelnel/comments/","https://www.reddit.com/user/Chrikelnel/submitted/","https://www.reddit.com/user/Chrikelnel/gilded/","https://www.reddit.com/user/Chrikelnel/comments/"]
        worker.add_links(li);
        len_to_crawl_after = len(worker.to_crawl)
        
        self.assertEqual(len_to_crawl_before+3,len_to_crawl_after)







