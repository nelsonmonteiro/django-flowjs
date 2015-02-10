import os
import datetime
import mimetypes
from settings import FLOWJS_PATH, FLOWJS_EXPIRATION_DAYS


def chunk_upload_to(instance, filename):
    """
    Save chunk to the right path and filename based in is number
    """
    return os.path.join(FLOWJS_PATH, instance.filename)


def guess_mimetype(url):
    """
    Return the mimetype of a file
    """
    mimetype = mimetypes.guess_type(url)
    if not mimetype or not mimetype[0]:
        name, ext = os.path.splitext(url)

        # Ubuntu 14.04 LTS didn't recognized by default,
        # and this was created to fix that problem instead install
        # more libraries
        mimetypes_dict = {
            '.m4v': ['video/x-m4v'],
            '.m4a': ['audio/x-m4a'],
        }
        mimetype = mimetypes_dict.get(ext, ['unknown/unknown'])
    return mimetype[0]


def guess_filetype(url):
    """
    Return the file type of a file ('audio', 'video', 'etc')
    """
    return guess_mimetype(url).split('/')[0]


def remove_expired_files():
    """
    Remove non completed uploads
    """
    from models import FlowFile
    FlowFile.objects.filter(
        state__in=[FlowFile.STATE_UPLOADING, FlowFile.STATE_UPLOAD_ERROR],
        updated__lte=datetime.datetime.date() - datetime.timedelta(days=FLOWJS_EXPIRATION_DAYS)
    ).delete()