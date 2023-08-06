# manuscriptify
# Compile google docs into a manuscript
# Copyright (c) 2022 Manuscriptify
# Open source, MIT license: http://www.opensource.org/licenses/mit-license.php
"""
main app logic

"""
from googleapiclient.errors import HttpError

from manuscriptify.manuscript import Manuscript
from manuscriptify.functions import run_with_shell_args
from manuscriptify.functions import progress_bar
from manuscriptify.exceptions import InconvenientResults


@run_with_shell_args
def manuscriptify(**kwargs):
    try:
        Manuscript(**kwargs)
        progress_bar(100)
        print(kwargs['title'], 'compiled successfully')
    except AttributeError as e:
        app_errors = [InconvenientResults]
        if type(e) in app_errors:
            pass
        else:
            raise
    except HttpError as e:
        print(e)
        raise


manuscriptify('dummy_arg')
