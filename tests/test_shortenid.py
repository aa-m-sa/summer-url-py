import unittest
import string
import shortenid as sh

class ShortenIdTestCase(unittest.TestCase):
    """Test module shortenid (converting integer ids to text ids and vice versa)"""

    def test_char_conv(self):
        for x in range(0, 62):
            self.assertEqual(x, sh.str2int(sh.int2str(x)))
        for x in string.ascii_letters:
            self.assertEqual(x, sh.int2str(sh.str2int(x)))
