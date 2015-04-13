# -*- coding: utf-8 -*-

from cwr.file import FileTag
from cwr.grammar.field import special
from data.accessor import CWRConfiguration
from cwr.grammar.factory.field import DefaultFieldFactory


"""
CWR file name grammar.

This stores grammar for parsing the CWR file name.

As the file name is a very precise type of string, this parsing will be lossless, meaning that all the information
from the file name will be always parsed into the resulting object.

CWR file names follow the pattern CWyynnnnsss_rrr.Vxx, where each section means the following:
CW - Header indicating it is a CWR file.
yy - Year.
nnnn - Sequence. This was originally 2 numbers, later changed to 4.
sss - Sender. 2 or 3 digits.
rrr - Receiver. 2 or 3 digits.
xx - Version of the CWR standard (version x.x).

There are two parsing patterns offered, one for the new format and one for the old.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

# Acquires data sources
_config = CWRConfiguration()
_filename_factory = DefaultFieldFactory(_config.load_field_config('filename'))

"""
Filename patterns.

This the grammatical structure for the old and new filename templates.
"""

# CWR filename patterns
cwr_filename_old = special.lineStart + \
                   _filename_factory.get_field('header', compulsory=True).suppress() + \
                   _filename_factory.get_field('year', compulsory=True) + \
                   _filename_factory.get_field('sequence_n_old', compulsory=True) + \
                   _filename_factory.get_field('sender', compulsory=True) + \
                   _filename_factory.get_field('delimiter_ip', compulsory=True).suppress() + \
                   _filename_factory.get_field('receiver', compulsory=True) + \
                   ((_filename_factory.get_field('delimiter_version', compulsory=True).suppress() +
                     _filename_factory.get_field('version', compulsory=True)) |
                    _filename_factory.get_field('delimiter_zip', compulsory=True)) + \
                   special.lineEnd
cwr_filename = special.lineStart + \
               _filename_factory.get_field('header', compulsory=True).suppress() + \
               _filename_factory.get_field('year', compulsory=True) + \
               _filename_factory.get_field('sequence_n_new', compulsory=True) + \
               _filename_factory.get_field('sender', compulsory=True) + \
               _filename_factory.get_field('delimiter_ip', compulsory=True).suppress() + \
               _filename_factory.get_field('receiver', compulsory=True) + \
               ((_filename_factory.get_field('delimiter_version', compulsory=True).suppress() +
                 _filename_factory.get_field('version', compulsory=True)) |
                _filename_factory.get_field('delimiter_zip', compulsory=True)) + \
               special.lineEnd

"""
Parsing actions for the patterns.

Both the old and new filename will be parsed into a FileTag instance.
"""

cwr_filename.setParseAction(lambda p: _to_filetag(p))
cwr_filename_old.setParseAction(lambda p: _to_filetag(p))

# TRANSFORMATION METHODS

"""
Parsing methods.

These are the methods which transform nodes into instances of classes.
"""


def _to_filetag(parsed):
    """
    Transforms the final parsing result into a FileTag instance.

    :param parsed: result of parsing a file name
    :return: a FileTag created from the file name
    """
    return FileTag(parsed.year, parsed.sequence_n, parsed.sender, parsed.receiver, parsed.version)