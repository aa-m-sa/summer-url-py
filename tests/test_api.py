import unittest
from flask import url_for
import summerurlapp
import appconfig
import types


class SummerApiTestCase(unittest.TestCase):
    """Test that the API works as intended"""

    testurl_http1 = "http://random.org"
    testurl_bad = "random.org"

    def setUp(self):
        summerurlapp.app.config.from_object(appconfig.TestConfig)
        self.app = summerurlapp.app.test_client()
        summerurlapp.init_db()

    def tearDown(self):
        summerurlapp.init_db()
        # use init_db() to clear the test db after testcase

    def post_shorten(self, link):
        return self.app.post("/api/shorten", data = dict(link = link))


    def test_shorten(self):
        resp = self.post_shorten(self.testurl_http1)
        self.assertEqual(resp.data[0], "1")

    def test_getbyid_ok(self):
        respPost = self.post_shorten(self.testurl_http1)
        respId = self.app.get('/api/' + '1')
        self.assertEqual(respId.status_code, 301)
        self.assertEqual(respId.location, self.testurl_http1)

    def test_getbyid_appendscheme(self):
        respPost = self.post_shorten(self.testurl_bad)
        respId = self.app.get('/api/' + '1')
        self.assertEqual(respId.status_code, 301)
        self.assertEqual(respId.location, "http://" + self.testurl_bad)

    def test_getbyid_noid(self):
        resp = self.app.get('/api/9000')
        self.assertEqual(resp.status_code, 404)
        resp = self.app.get('/api/nonexistentid')
        self.assertEqual(resp.status_code, 404)



