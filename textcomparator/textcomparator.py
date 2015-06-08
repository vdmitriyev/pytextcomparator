# coding: utf-8

__author__ = 'Viktor Dmitriyev'
__copyright__ = 'Copyright 2015, Viktor Dmitriyev'
__credits__ = ['Viktor Dmitriyev']
__license__ = 'MIT'
__version__ = '1.1.0'
__maintainer__ = '-'
__email__   = ''
__status__  = 'dev'
__date__    = '09.03.2015'
__description__ = 'Compares two texts in various ways.'

import sys
import difflib

# importing custom libraries
try:
    from helper_directory import DirectoryHelper
except:
    import urllib
    target_path = 'https://raw.githubusercontent.com/vdmitriyev/sourcecodesnippets/master/python/helper_directory/helper_directory.py'
    target_name = 'helper_directory.py'
    urllib.urlretrieve (target_path, target_name)
    from helper_directory import DirectoryHelper
finally:
    import helper_directory
    if helper_directory.__version__ != '1.0.0':
        print 'Wrong version of the library {0}. Check the version'.format(helper_directory.__file__)

import re, math
from collections import Counter

class StopWords(object):
    """ Pocessing custom stop words from specified files """

    # configuring stop words
    SW_FOLDER = 'stopwords'
    SW_FILES = ['stop-words_english_1_en.txt',
                'stop-words_english_2_en.txt',
                'stop-words_english_3_en.txt',
                'stop-words_english_4_google_en.txt',
                'stop-words_english_5_en.txt',
                'stop-words_english_6_en.txt'
                ]

    def get_stop_words(self):
        """
            (obj) -> list

            Reading stop stop words from files.
        """

        sw = list()
        dh = DirectoryHelper()
        for sw_file in self.SW_FILES:
            sw_fullpath = self.SW_FOLDER + '\\' + sw_file
            sw_file = dh.read_file_utf8(sw_fullpath)
            for sw_single in sw_file.split('\n'):
                sw.append(sw_single[:-1])

        return sw

class ComputeCosine(object):
    """ Computing consine between two vectors of words"""

    def get_cosine(self, vec1, vec2, ignore_stopwords=False):
        """
            (obj, list, list) -> float

            Return the cosine of the vectors computed as descibed here: http://en.wikipedia.org/wiki/Cosine_similarity

        """

        vec1 = self.text_to_vector(vec1, ignore_stopwords, print_vector=False)
        vec2 = self.text_to_vector(vec2, ignore_stopwords)

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])

        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text, ignore_stopwords=False, print_vector=False):
        """
            (obj, str, boolean) -> list(int)

        """

        WORD = re.compile(r'\w+')
        words = WORD.findall(text)
        sw = StopWords().get_stop_words()

        if print_vector:
            def pp(x):
                if x[1] > 30 and x[0] not in sw:
                    print '{0} : {1}'.format(x[0], x[1])
            map(pp, Counter(words).most_common())

        if ignore_stopwords:
            counted = Counter(words)
            uniqueToListWords = list(set(words) & set(set(words) ^ set(sw)))
            _result = Counter()
            for key in uniqueToListWords:
                _result[key] = counted[key]
            return _result

        return Counter(words)

def main():
    """
        Main method that initiates all processes.
    """

    hd = DirectoryHelper()
    cc = ComputeCosine()
    try:
        filea = hd.read_file_utf8('text-a.txt').lower()
        fileb = hd.read_file_utf8('text-b.txt').lower()

        similarity = difflib.SequenceMatcher(a = filea.lower(), b = fileb.lower())

        print 'text A:\n{}\n'.format(filea)
        print 'text B:\n{}\n'.format(fileb)

        print 'similarity-diff\t\t\t : {}'.format(similarity.ratio())
        print 'similarity-cosine\t\t : {}'.format(cc.get_cosine(filea, fileb))
        print 'similarity-cosine-no-stopwords\t : {}'.format(cc.get_cosine(filea, fileb, ignore_stopwords=True))

    except Exception, ex:
        print '[i] create 2 files with texts to be compared'
        print '[e] exception: {}'.format(str(ex))


if __name__ == '__main__':

    # setting system default encoding to the UTF-8
    reload(sys)
    sys.setdefaultencoding('UTF8')

    # initiating main processing
    main()
