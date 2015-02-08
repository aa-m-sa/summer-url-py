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

    def test_id_conv(self):
        self.assertEqual(61, sh.to_int('9'))
        self.assertEqual('B', sh.to_text(27))
        text_id = 'a87Xjl'
        int_id = 1238
        self.assertEqual(text_id, sh.to_text(sh.to_int(text_id)))
        self.assertEqual(int_id, sh.to_int(sh.to_text(int_id)))
