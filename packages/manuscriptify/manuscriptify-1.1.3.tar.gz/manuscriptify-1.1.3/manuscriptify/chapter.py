# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
chapter name tidier

"""
import re
from itertools import chain

from manuscriptify.functions import fragify_string
from manuscriptify.constants import ARTICLES
from manuscriptify.constants import CONJUNCTIONS
from manuscriptify.constants import PREPOSITIONS
from manuscriptify.constants import SPECIAL_PARTS


PATTERN = '|'.join([f' {c} ' for c in
                    chain(ARTICLES,
                          CONJUNCTIONS,
                          PREPOSITIONS)])


class Chapter(list):

    def __init__(self, f):
        ch_name = self._title_case(f['name'])
        if not ch_name.upper() in SPECIAL_PARTS:
            ch_num = f["description"].split('.')[-1]
            ch_name = f'Chapter {ch_num}: {ch_name}'
        chapter_logline = fragify_string(ch_name)
        super().__init__(chapter_logline)

    def _title_case(self, name):
        """properly title case the name"""
        step1 = name.title()
        pattern = re.compile(PATTERN)
        step2 = pattern.sub(self._decapitalize, step1)
        return pattern.sub(self._decapitalize, step2)

    @staticmethod
    def _decapitalize(m):
        """decaptilaise a match object"""
        return m.group(0).lower()
