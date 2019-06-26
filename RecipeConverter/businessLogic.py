from num2words import num2words
import re
from .models import Converter, Conversion
from functools import partial


def has_digits(input_string):
    return bool(re.search(r'\d', input_string))


def pretty_weight(value, unit):
    """
    :param value: float, the original quantity
    :param unit: string, the destination unit type
    :return:
    """
    if unit == 'kg':
        if value < 1:
            result = str(int(value * 1000)) + ' g'
        elif value == 1:
            result = '1 kg'
        else:
            result = str(round(value, 1)) + ' ' + unit
    elif unit == 'litres' and value < 1:
        result = str(int(value * 1000)) + ' ml'
    elif unit == 'ml':
        result = str(round(value)) + ' ' + unit
    elif unit == 'quarts':
        if value == 1:
            result = '1 quart'
        else:
            result = str(round(value, 1)) + ' quarts'
    elif unit == 'grams':
        result = str(int(value)) + ' grams'
    else:
        result = str(round(value, 1)) + ' ' + unit

    return result


def find_conversion_type(text):
    """
    Given a recipe text
    :param text: the recipe
    :return: imp or met, to show which is the detected 'from' state
    this has the highest count when compared to the keys in the converter table
    """
    results = {'imp': 0, 'met': 0}

    lookupSearch = Converter.objects.filter(spoon_type=False).filter(cup_type=False)
    for record in lookupSearch.values():
        key_type = record['unit_source_type']  # "imp" or "met"
        searchKeys = record['unit_source_keys'].split(",")

        for key in searchKeys:
            if len(key) > 1:  # don't search for g, l etc
                found_count = text.count(key)
            if found_count > 0:
                text = text.replace(key, "")
                results[key_type] += found_count
                # we do this so that pounds and pound are not doubled up

    return max(results, key=results.get)


def get_temp_str(conv_type, match):
    # Called below in order to convert temperatures in the method section
    original_phrase = match.group(0)
    old_temp = int(match.group(1))
    given_type = match.group(2).lower()

    #TODO can put pretty_weight in here instead
    if conv_type == 'met' and given_type == 'c':  # from c to f
        new_temp = int((old_temp * 9 / 5) + 32)
        new_temp -= (new_temp % -10)  # round up to nearest 10
        return str(new_temp) + '°F'

    elif conv_type == 'imp' and given_type == 'f':  # from f to c
        new_temp = int((old_temp - 32) * 5 / 9)
        new_temp -= (new_temp % -10)  # round up to nearest 10
        return str(new_temp) + '°C'

    else:
        return original_phrase


def get_conv_str(record, match):
    # Called below in order to convert units in the method section
    try:
        result = pretty_weight(record['unit_conversion'] * float(match.group(1)), record['unit_dest_name'])
    except:
        result = '__problem__'
    return result


def converter(inputs):

    output_lines = []  # stores row by row results
    working_text = inputs['recipe_text']

    # Brute Force Replacements
    replacement_text = {' 1/2': '.5',
                        '1/2': '.5',
                        '½': '.5',
                        ' 1/3': '.333',
                        '1/3': '.333',
                        ' 2/3': '.666',
                        '2/3': '.666',
                        ' 1/4': '.25',
                        '1/4': '.25',
                        ' 3/4': '.75',
                        '3/4': '.75',
                        ' 1/5': '.2',
                        '1/5': '.2',
                        '1/8': '.125',
                        'half a': '0.5',
                        'half': '0.5',
                        'third of': '0.333',
                        'third': '0.333'
                        }

    # Generate dictionary of English number words and see if we can replace them
    for i in range(50):
        replacement_text[num2words(i) + ' '] = str(i)
    # TODO update this so that it uses REGEX to exclude search for text before and after.

    for k, v in replacement_text.items():
        #search for the keys above but not where they have a letter just before and just after
        s_str = '(?<![a-zA-Z])' + k + '(?![a-zA-Z])'
        prog = re.compile(r"" + s_str)

        working_text = prog.sub(v, working_text)


    # DETERMINE AUTO CONVERSION TYPE
    # if the user selected 'automatic' we need to count the instances of each measure type
    # and determine if this is metric -> imperial or imperial -> metric
    conv_auto = False
    conv_names = {'imp': 'metric', 'met': 'imperial'}

    if inputs['conversion_type'] == '1': # user selected automatic, we must determine
        conv_lookup = find_conversion_type(working_text)
        conv_auto = True
    elif inputs['conversion_type'] == '2':  # user selected 'to metric' in other word imp
        conv_lookup = 'imp'
    elif inputs['conversion_type'] == '3':  # user selected 'to metric' in other word met
        conv_lookup = 'met'

    conv_msg = 'Converting to ' + conv_names[conv_lookup]
    if conv_auto:
        conv_msg = conv_msg + ' (auto-detected)'

    #TODO need to convert 'a stick' 'a cup' into '1 stick'


    # MAKE IMPERIAL OR METRIC CUPS AND SPOONS
    # if the user has selected cups and spoons conversion, then we need to add
    # suffixes to each appearance to force correct conversion

    # Get converter table, only pick met or imperial as required
    # lookupSearch = Converter.objects.all()
    lookupSearch = Converter.objects.filter(unit_source_type=conv_lookup)

    # Remove spoons and cups if requested, if not add suitable suffixes

    # TODO could put this in a function as it is repeated
    if inputs["cups_bool"]:
        # do not search for cups
        lookupSearch = lookupSearch.filter(cup_type=False)
    else:
        # do search for cups, need to add suffix to each cup appearance
        # conv_lookup is either 'imp' or 'met'
        suffixSearch = lookupSearch.filter(cup_type=True)

        # replace each "cup" with cupimp or cupmet etc
        for record in suffixSearch.values():
            searchKeys = record['unit_source_keys'].split(',')
            searchKeys.sort(key=len, reverse=True)
            f = 0
            for key in searchKeys:
                working_text = working_text.replace(key, '__'+str(f)+"__")
                f += 1
            f = 0
            for key in searchKeys:
                working_text = working_text.replace('__'+str(f)+"__", key+conv_lookup)
                f += 1

    if inputs["spoons_bool"]:
        # do not search for spoons
        lookupSearch = lookupSearch.filter(spoon_type=False)
    else:
        # do search for spoons, need to add suffix to each cup appearance
        suffixSearch = lookupSearch.filter(spoon_type=True)
        for record in suffixSearch.values():
            searchKeys = record['unit_source_keys'].split(',')
            searchKeys.sort(key=len, reverse=True)
            f = 0
            #need to do it using 2nd key to avoid falce replacements
            for key in searchKeys:
                working_text = working_text.replace(key, '__' + str(f) + "__")
                f += 1
            f = 0
            for key in searchKeys:
                working_text = working_text.replace('__' + str(f) + "__", key + conv_lookup)
                f += 1

    # Main part of the replacement loop
    contentsFlag = False

    for line in working_text.splitlines():
        measure_found = False
        tempLine = line.strip()

        if contentsFlag:  # we have reached the first empty line, this signals the end of the ingredients list. Now just add each line
            measure_found = True
            # we have reached the method section. We need to replace temperatures here in the right direction
            # search for any digit, followed by deg, degrees,  or nothing, then a c or an F

            result = re.sub(r'(\d+)(?=\s?(?:deg|degrees|°|)\s?[cCfF])\s?(?:deg|degrees|°|)\s?([cCfF])',
                            partial(get_temp_str, conv_lookup),
                            tempLine)

            # About partial in this context
            # https://stackoverflow.com/questions/7868554/python-re-subs-replace-function-doesnt-accept-extra-arguments-how-to-avoid

            output_lines.append(result)

        elif len(tempLine) == 0 or tempLine is None or tempLine == '': #this is the first empty line
            contentsFlag = True
            measure_found = True
            output_lines.append("")

        elif not has_digits(tempLine):
            output_lines.append(tempLine)
            measure_found = True

        else:
            #Run keys search from data
            for record in lookupSearch.values():
                searchKeys = record['unit_source_keys'].split(',')
                searchKeys.sort(key=len, reverse=True)  # always search for the longest one first

                for key in searchKeys:
                    key_found = False
                    #add necessary suffixes for cups and spoons
                    if record['cup_type'] and not inputs['cups_bool']:
                        key1 = key + conv_lookup
                    elif record['spoon_type'] and not inputs['spoons_bool']:
                        key1 = key + conv_lookup
                    else:
                        key1 = key

                    #str = '((?:[\d,.]*))\s*' + key + '(?!\w)'
                    #searches for a number using any combination of digits , or . together
                    # with last one before key must be a digit
                    obj = re.compile(r'((?:[\d,.]*)(?<=\d))\s*' + key1)
                    conv_str = obj.sub(partial(get_conv_str, record),  tempLine)

                    if conv_str != tempLine:  # substitutions were made, search key was found
                        key_found = True
                        measure_found = True
                        output_lines.append(conv_str)
                        break

                if key_found:
                    break

        if not measure_found:
            output_lines.append(tempLine)


    outputs = dict()
    finished_text = '\n'.join(output_lines)

    #Final tidyup
    #1 replace any .5 with 0.5 etc
    prog = re.compile(r'(?<!\d)([\.,]\d+)')
    finished_text = prog.sub("0\g<1>", finished_text)

    #2 brute force replacements - order is important, do the long ones first

    replacement_text = {'0.5': '½',
                        '0.125': '⅛',
                        '0.25': '¼',
                        '0.75': '¾',
                        '0.375': '⅜',
                        '0.675': '⅝',
                        '0.875': '⅞',
                        '.5': '½',
                        '.125': '⅛',
                        '.25': '¼',
                        '.75': '¾',
                        '.375': '⅜',
                        '.675': '⅝',
                        '.875': '⅞',
                        }


    for k, v in replacement_text.items():
        if k in finished_text:
            finished_text = finished_text.replace(k, v)

    outputs['converted_text'] = finished_text
    outputs['conversion_msg'] = conv_msg

    m = Conversion(user=inputs['user'],
                   source_url=inputs['source_url'],
                   conversion_name=inputs['name'],
                   original_text=inputs['recipe_text'],
                   converted_text=outputs['converted_text'],
                   conversion_type=conv_msg)
    m.save()

    return m.pk, outputs
