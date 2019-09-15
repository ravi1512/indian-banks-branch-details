"""This module provides utility function to branch-details app"""


def row2dict(row):
    """Converts query result rows into a Python dict"""
    result = {}
    for column in row.__table__.columns:
        result[column.name] = str(getattr(row, column.name))
    return result


def prepare_results(rows):
    """Creates a list of dicts from query results"""
    results = []
    for row in rows:
        branch_details = row2dict(row[0])
        branch_details["bank_name"] = row[1].name
        results.append(branch_details)
    return results
