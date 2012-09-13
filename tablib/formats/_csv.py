# -*- coding: utf-8 -*-

""" Tablib - CSV Support.
"""

from tablib.compat import is_py3, csv, StringIO


title = 'csv'
extensions = ('csv',)


DEFAULT_ENCODING = 'utf-8'

def get_delimiter(dataset):
    try:
        delimiter = dataset.delimiter
    except AttributeError:
        delimiter = ','
    return delimiter


def export_set(dataset):
    """Returns CSV representation of Dataset."""
    stream = StringIO()

    delimiter = get_delimiter(dataset)

    if is_py3:
        _csv = csv.writer(stream, delimiter=delimiter)
    else:
        _csv = csv.writer(stream, encoding=DEFAULT_ENCODING, delimiter=delimiter)

    for row in dataset._package(dicts=False):
        _csv.writerow(row)

    return stream.getvalue()


def import_set(dset, in_stream, headers=True):
    """Returns dataset from CSV stream."""

    dset.wipe()
    delimiter = get_delimiter(dset)

    if is_py3:
        rows = csv.reader(in_stream.splitlines(), delimiter=delimiter)
    else:
        rows = csv.reader(in_stream.splitlines(), encoding=DEFAULT_ENCODING, delimiter=delimiter)
    for i, row in enumerate(rows):

        if (i == 0) and (headers):
            dset.headers = row
        else:
            dset.append(row)


def detect(stream):
    """Returns True if given stream is valid CSV."""
    try:
        csv.Sniffer().sniff(stream, delimiter=delimiter)
        return True
    except (csv.Error, TypeError):
        return False
