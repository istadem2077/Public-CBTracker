def stripresult(string):
    string = string.split()
    string = string[2]
    string = string.split("(")
    string = string[1].split(")")
    string.pop(1)
    string = string[0]
    return string


    """
    It's specific for 'View your (N) search results' string. Do not you for anything ELSE!

    """
