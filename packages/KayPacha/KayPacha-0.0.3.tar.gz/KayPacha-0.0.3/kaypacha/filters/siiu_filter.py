def siiu_filter(table_name, data_row):
    """
    Funtion that replaces na values by None,
    otherwise the created JSON gets corrupted for having
    null values it does not recognize,
    for this case the na values are the ones recognized
    by pandas as such.
    
    Parameters:
    table_name:str
        name of the table we are currently filtering
    data_row:pandas.Series
        one arrow of the current table
    Returns:
        dictionary with the clean data.
    NOTE: this is called by the funciton ukupacha.Utils.parse_table
    """
    return data_row.astype(object).where(data_row.notna(), None)
