"""
A collection of database cursor conversion utilities.
"""
from collections import namedtuple
# todo: fix the typeing for cursor


# -------- cursor conversions --------
def to_values(cursor):
    """
    Convert a single value set of results to a list of element values
    :param cursor: database results cursor
    :return: list of values
    """
    return [
        row[0] for row in cursor.fetchall()
    ]


def to_dicts(cursor):
    """
    Convert all rows from a cursor of results as a list of dicts
    :param cursor: database results cursor
    :return: list of dicts containing field_name:value
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def to_tuples(cursor):
    """
    Convert all rows from a cursor of results as a list of tuples
    :param cursor: database results cursor
    :return: list of tuples containing field_name:value
    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

