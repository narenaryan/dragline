import unittest
from httplib2 import Http
from dragline.request import  Request
class RequestTest(unittest.TestCase):

    def test_request(self):
        req = Http()
        content = req.request("http://www.example.org")
        reqst = Request("http://www.example.org")
        content_r = reqst.send()
        self.assertEqual(content,content_r)
    #

    def test_unique(self):
        req1 = Request("http://www.google.com", method = "POST",form_data = {"test1":"abcd","abcd":"test1"})
        req2 = Request("http://www.google.com", method = "POST",form_data = {"abcd":"test1","test1":"abcd"})
        req3 = Request("http://www.google.com", method = "POST",form_data = {"abcd":"test1","test1":"abdc"})
        self.assertEqual(req1.get_unique_id(),req2.get_unique_id())
        self.assertNotEqual(req1.get_unique_id(),req3.get_unique_id())







if __name__ == "__main__":
    unittest.main()






