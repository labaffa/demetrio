from datetime import date


def is_today(test_date):
    """Return True if a given date is today"""
    if test_date == date.today():
        return True
    return False


def get_row(linear_index, matrix_columns):
    """
    From a matrix of given columns return the row index
    corresponding to a given linear index
    """
    index = linear_index
    columns = matrix_columns
    return int(index/columns)


def get_column(linear_index, matrix_columns):
    """
    From a matrix of given columns return the column index
    corresponding to a given linear index
    """
    index = linear_index
    columns = matrix_columns
    return int(index) - int(index/columns)*int(columns)
