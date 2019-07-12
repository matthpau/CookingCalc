import re

def nice_address(*args):
    result = ', '.join(args)
    for arg in args:
        if arg not in ('', None):
            break
        else:
            return ''
    # Get rid of any double or triple commas
    char = ", "
    pattern = '(' + char + '){2,}'
    result = re.sub(pattern, char, result)
    
    return result