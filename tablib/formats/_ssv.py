# -*- coding: utf-8 -*-

""" Tablib - SSV (Semicolon Separated Values) Support.
"""

from tablib.compat import is_py3, csv, StringIO



title = 'ssv'
extensions = ('ssv',)

DEFAULT_ENCODING = 'utf-8'

def export_set(dataset):
    """Returns a SSV representation of Dataset."""

    stream = StringIO()

    if is_py3:
        _ssv = csv.writer(stream, delimiter=';')
    else:
        _ssv = csv.writer(stream, encoding=DEFAULT_ENCODING, delimiter=';')

    for row in dataset._package(dicts=False):
        _ssv.writerow(row)

    return stream.getvalue()


def import_set(dset, in_stream, headers=True):
    """Returns dataset from SSV stream."""

    dset.wipe()

    if is_py3:
        rows = csv.reader(in_stream.split('\r\n'), delimiter=';')
    else:
        rows = csv.reader(in_stream.split('\r\n'), delimiter=';',
                          encoding=DEFAULT_ENCODING)

    for i, row in enumerate(rows):
        # Skip empty rows
        if not row:
            continue

        if (i == 0) and (headers):
            dset.headers = row
        else:
            dset.append(row)


def detect(stream):
    """Returns True if given stream is valid SSV."""
    try:
        csv.Sniffer().sniff(stream, delimiters=';')
        return True
    except (csv.Error, TypeError):
        return False
