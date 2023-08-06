def scienti_filter(table_name, data_row):
    """
    Funtion that allows to filter unwanted data from the json.
    for this case:
        * fields with "FILTRO"
        * values with the string "nan"
        * passwords
    anything can be set here to remove unwanted data.
    Parameters:
    table_name:str
        name of the table we are currently filtering
    data_row:pandas.Series
        one arrow of the current table
    Returns:
        dictionary with the clean data.

    NOTE: this is called by the funciton ukupacha.Utils.parse_table
    """
    #data_row.dropna(inplace=True)
    data = {}
    for key, value in data_row.items():
        #if "FILTRO" in key:
        #    continue
        # if value == "nan":
        #    continue
        if key == "TXT_CONTRASENA":
            continue
        data[key] = value
    return data
