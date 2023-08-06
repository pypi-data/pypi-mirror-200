# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
fragment assembler

"""
from bisect import bisect, bisect_left

from manuscriptify.exceptions import InconvenientResults
from manuscriptify.exceptions import SortKeyError
from manuscriptify.functions import sort_key
from manuscriptify.constants import FOLDER_MIME
from manuscriptify.google_api.clients import Clients

FIELDS = 'id, name, description, parents, mimeType'


class FileTree:

    def __init__(self, creds=None):
        self.drive = Clients(creds)['drive']

    def tree(self, project_folder, selection=[], filter_=''):
        """all the relevant files, in their proper order"""
        writing_folder = self.writing(project_folder)
        folder_tree = self._expand(writing_folder)
        files = self._files(folder_tree)
        if selection:
            files = self._select(files, selection)
        elif filter_:
            files = self._filter(files, filter_)
        return tuple(files)

    def writing(self, project_folder):
        """get source folder"""
        all_folders = self._all_folders()
        project_folders = [
            f['id'] for f in all_folders if
            any(f[key] == project_folder
                for key in ('name', 'id'))
        ]
        writing_folders = [
            f['id'] for f in all_folders if
            f['name'] == 'writing' and
            any(p in f['parents'] for
                p in project_folders)
        ]
        if len(writing_folders) == 1:
            return writing_folders[0]
        else:
            raise InconvenientResults(writing_folders)

    def _all_folders(self):
        """get all folders in drive"""
        mime_type = FOLDER_MIME
        queries = [
            f"mimeType = '{mime_type}'",
            "'me' in owners",
            'trashed = false'
        ]
        kwargs = {
            'api_method': self.drive.files().list,
            'q': ' and '.join(queries),
            'pageSize': 100,
            'fields': f'nextPageToken, files({FIELDS})'
        }
        all_folders = self.get_all_results(**kwargs)
        return [
            f for f in all_folders
            if 'parents' in f
        ]

    def _expand(self, writing_folder):
        """get folders in source tree"""
        parents = [writing_folder]
        all_folders = self._all_folders()
        descendants = []
        while True:
            next_gen = [
                f['id'] for f in all_folders if
                any(a in f['parents'] for
                    a in parents)
            ]
            if not next_gen:
                break
            descendants.extend(next_gen)
            parents = next_gen
        return [writing_folder] + descendants

    def _files(self, folder_tree):
        """get files in folder tree"""
        query = [f"'{folder_id}' in parents"
                 for folder_id in folder_tree]
        queries = [
            f"({' or '.join(query)})",
            'trashed = false'
        ]
        kwargs = {
            'api_method': self.drive.files().list,
            'q': ' and '.join(queries),
            'pageSize': 100,
            'fields': f'nextPageToken, files({FIELDS})'
        }
        results = self.get_all_results(**kwargs)
        prioritized = self._prioritize(results)
        try:
            files = sorted(prioritized, key=sort_key)
        except (ValueError, KeyError):
            raise SortKeyError(prioritized)
        return files

    @staticmethod
    def get_all_results(api_method, list_key='files', **kwargs):
        """chain paginated results"""
        all_results = []
        page_token = None
        while True:
            if page_token:
                kwargs['pageToken'] = page_token
            results = api_method(**kwargs).execute()
            all_results.extend(results[list_key])
            if 'nextPageToken' not in all_results:
                break
            page_token = results['nextPageToken']
        return all_results

    @staticmethod
    def _prioritize(results):
        """add ancestor priorities"""
        for i, result in enumerate(results):
            while True:
                desc = results[i].get('description') or '99'
                parents = [r for r in results if
                           r['id'] in result['parents']]
                if not parents:
                    results[i]['description'] = desc
                    break
                priorities = [
                    parents[0].get('description') or '99',
                    desc
                ]
                results[i]['description'] = '.'.join(priorities)
                result = parents[0]
        return results

    @staticmethod
    def _select(files, selection):
        """get subset of files for workshopping - api"""
        fragments = [
            f for f in files if
            f['id'] in selection or
            any(child['description'].split('.')[0]
                == f.['description'] for
                child in files if
                child['id'] in selection)
        ]
        for f in fragments:
            if f['id'] not in selection:
                f['name'] += '~~'
        return fragments

    @staticmethod
    def _filter(files, filter_):
        """get subset of files for workshopping - ce"""
        results = []
        for range_ in filter_.split(','):
            bounds = range_.split('-')
            if len(bounds) == 1:
                bounds += bounds
            lower, upper = [
                list(map(int, x)) for x in
                [b.split('.') for b in bounds]
            ]
            i = bisect_left(files, lower, key=sort_key)
            j = bisect(files, upper + [99], key=sort_key)
            if len(lower) > 1:
                chapter_frag = next(
                    f for f in files if
                    f['description'] == str(lower[0])
                )
                chapter_frag['name'] += '~~'
                results.append(chapter_frag)
            results += files[i:j]
        return results
