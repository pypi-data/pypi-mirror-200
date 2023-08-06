# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
manuscript generator

"""
from itertools import chain

from manuscriptify.fragment import Fragment
from manuscriptify.chapter import Chapter
from manuscriptify.parser import Parser
from manuscriptify.formatter import Formatter
from manuscriptify.filetree import FileTree
from manuscriptify.functions import progress_bar
from manuscriptify.functions import fragify_string
from manuscriptify.functions import is_chapter
from manuscriptify.constants import FOLDER_MIME, FILE_MIME
from manuscriptify.google_api.clients import Clients

TEMPLATE = '1CRtUdlrV7PZ2OwTDIBZtOKhMHT-nRHCjkaD6Q4lUFkU'


class Manuscript:
    """the manuscript generator"""

    def __init__(self, creds=None, **kwargs):
        """compose a google doc out of the assembled content"""
        docs, drive = Clients(creds).values()
        self.drive = drive
        self.kwargs = kwargs
        self.id = self._create_from_template()
        kwargs_ = {
            'documentId': self.id
        }
        doc = docs.documents().get(**kwargs_).execute()
        style = doc['documentStyle']
        kwargs['header_id'] = style['defaultHeaderId']
        kwargs['content'] = self._assemble_fragments(creds, **kwargs)
        requests = Parser(**kwargs)
        progress_bar(45)
        kwargs_['body'] = {
            'requests': requests
        }
        try:
            docs.documents().batchUpdate(**kwargs_).execute()
        except:
            kwargs_ = {
                'fileId': self.id
            }
            drive.files().delete(**kwargs_).execute()
            raise
        kwargs = {
            'header_id': style['firstPageHeaderId'],
            'wc': requests.wc
        }
        kwargs_['body'] = {
            'requests': self._wc(**kwargs)
        }
        docs.documents().batchUpdate(**kwargs_).execute()
        target = (
            'workshop drafts' if
            self.kwargs.get('workshop') or
            self.kwargs.get('selection')
            else 'manuscripts'
        )
        self.folder = self._get_outfolder(creds, target)
        kwargs = {
            'fileId': self.id,
            'addParents': self.folder,
            'body': {'name': self.kwargs['title']}
        }
        drive.files().update(**kwargs).execute()

    def _create_from_template(self):
        """copy the empty template document"""
        kwargs = {
            'fileId': TEMPLATE
        }
        file = self.drive.files().copy(**kwargs).execute()
        return file['id']

    def _assemble_fragments(self, creds, **kwargs):
        """assemble the input for the parser"""
        kwargs_ = {
            'project_folder': kwargs['project_folder'],
            'selection': kwargs.get('selection', []),
            'filter_': kwargs['workshop']
        }
        progress_bar(0)
        filetree = FileTree(creds).tree(**kwargs_)
        progress_bar(10)
        fragments = []
        ch_depth = kwargs['chapter_depth']
        chapters = ch_depth > 0
        if not chapters:
            markup = f'Chapter 0:{kwargs["title"]}%%'
            title = fragify_string(markup)
            fragments.append(title)
        for f in filetree:
            try:
                if chapters and is_chapter(f, ch_depth):
                    chapter_logline = Chapter(f)
                    fragments.append(chapter_logline)
            except KeyError:

                # single file use case
                pass

            if f['mimeType'] == FILE_MIME:
                fragment = Fragment(f['id'], creds)
                fragments.append(fragment)
        progress_bar(35)
        return list(chain(*fragments))

    @staticmethod
    def _wc(**kwargs):
        """add the word count header"""
        end_index = len(f'{kwargs["wc"]:,}') + 12
        header = [{
            'insertText': {
                'location': {
                    'segmentId': kwargs['header_id'],
                    'index': 0
                },
                'text': (f'Word count: {kwargs["wc"]:,}')
            }
        }]
        range_ = {
            'startIndex': 0,
            'endIndex': end_index,
            'segmentId': kwargs['header_id']
        }
        ts = Formatter.matter()
        header.append({
            'updateTextStyle': {
                'range': range_,
                'textStyle': ts,
                'fields': ','.join(ts.keys())
            }
        })
        st = Formatter.right()
        header.append({
            'updateParagraphStyle': {
                'range': range_,
                'paragraphStyle': st,
                'fields': ','.join(st.keys())
            }
        })
        return header

    def _get_outfolder(self, creds, target):
        """get the folder we want to put stuff in"""
        pid = self._get_project_folder_id(creds)
        queries = [
            f"mimeType = '{FOLDER_MIME}'",
            f"name = '{target}'",
            f"'{pid}' in parents",
            'trashed = false'
        ]
        kwargs = {
            'q': ' and '.join(queries),
            'pageSize': 1,
            'fields': 'files(id)'
        }
        results = self.drive.files().list(**kwargs).execute()
        if results['files']:
            f = results['files'][0]
        else:
            kwargs = {
                'body': {
                    'name': target,
                    'mimeType': FOLDER_MIME
                },
                'fields': 'id'
            }
            f = self.drive.files().create(**kwargs).execute()
            kwargs = {
                'fileId': f['id'],
                'addParents': pid
            }
            self.drive.files().update(**kwargs).execute()
        return f['id']

    def _get_project_folder_id(self, creds):
        """get the project folder id"""
        project_folder = self.kwargs['project_folder']
        writing_id = FileTree(creds).writing(project_folder)
        kwargs_ = {
            'fileId': writing_id,
            'fields': 'parents'
        }
        writing = self.drive.files().get(**kwargs_).execute()
        return writing['parents'][0]
