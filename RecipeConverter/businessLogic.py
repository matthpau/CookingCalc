from num2words import num2words
import re
from .models import Converter, Conversion

"""
re.findall(r'\d+\.?\d*', '3.5 pounds rump roast')
['3.5']

re.search(r'\d+\.?\d*', '3.5 pounds rump roast')
<re.Match object; span=(0, 3), match='3.5'>

re.search(r'\d+\.?\d*', '3.5 pounds rump roast').group(0)
'3.5'
"""

def hasDigits(inputString):
    return bool(re.search(r'\d', inputString))


def prettyWeight(value, unit):
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
    elif unit == 'quart':
        if value == 1:
            result = '1 quart'
        else:
            result = str(round(value, 1)) + ' quarts'
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
            found_count = text.count(key)
            if found_count > 0:
                text = text.replace(key, "")
                results[key_type] += found_count
                # we do this so that pounds and pound are not doubled up

    return max(results, key=results.get)


def converter(inputs):

    output_conv = []  # stores row by row information about the conversion
    output_lines = []  # stores row by row results
    output_fails = []

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
                        }

    # Generate dictionary of English number words and see if we can replace them
    for i in range(50):
        replacement_text[num2words(i) + ' '] = str(i)

    working_text = inputs['recipe_text']

    for k, v in replacement_text.items():
        if k in working_text:
            working_text = working_text.replace(k, v)
        if k.capitalize() in working_text:
            working_text = working_text.replace(k.capitalize(), v)

    #Single letter replacements
    #these are problematic in conversions
    #make sure they appear here, and that there are no single letter search keys in the converters model
    single_replace = {'l': 'litres'}

    for k, v in single_replace.items():
        # replace standalone versions with spaces on both sides
        working_text = working_text.replace(' ' + k + ' ', ' ' + v + ' ')  # ' l ' becomes ' litres'
        #Search for any single letter in list with a digit in front and a space after it
        working_text = re.sub(r'(?<=\d)' + k + '(?=\s)', ' ' + v, working_text) # '5l ' becomes '5 litres'


    # DETERMINE AUTO CONVERSION TYPE
    # if the user selected 'automatic' we need to count the instances of each measure type
    # and determine if this is metric -> imperial or imperial -> metric
    conv_auto = False
    conv_names = {'imp': 'imperial', 'met': 'metric'}

    if inputs['conversion_type'] == '1': # user selected automatic, we must determine
        conv_lookup = find_conversion_type(working_text)
        conv_auto = True
    elif inputs['conversion_type'] == '2':  # user selected 'to metric' in other word imp
        conv_lookup = 'imp'
    elif inputs['conversion_type'] == '3':  # user selected 'to metric' in other word met
        conv_lookup = 'met'

    conv_msg = 'Converting from ' + conv_names[conv_lookup]
    if conv_auto:
        conv_msg = conv_msg + ' (autodetected)'

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
            output_conv.append("Method")
            output_lines.append(tempLine)
            measure_found = True

            #TODO need to use regex now to find celcius or farenheit numbers and convert depending on conv_lookup value
            """
            Examples: find 350 C or 350 c
            print(re.search(r'\d+(?=\s[cC])', '350 C').group()) # find 350 C or 350 c
            print(re.search(r'\d+(?=\sdeg\s[cC])', '350 deg C').group()) # find 350 deg C or 350 deg c
            print(re.search(r'\d+(?=\sdeg\s[cC])\sdeg\s[cC]', '350 deg C').group()) #  includes the deg C as well if you want it
            """

        elif len(tempLine) == 0 or tempLine is None or tempLine == '': #this is the first empty line
            contentsFlag = True
            measure_found = True
            output_conv.append("")
            output_lines.append("")

        elif not hasDigits(tempLine):
            output_conv.append('No digits found, unchanged')
            output_lines.append(tempLine)
            measure_found = True

        else:
            #Run keys search from data
            for record in lookupSearch.values():
                searchKeys = record['unit_source_keys'].split(',')
                searchKeys.sort(key=len, reverse=True)  # always search for the longest one first

                for key in searchKeys:
                    sub_measure_found = False

                    #add necessary suffixes for cups and spoons
                    if record['cup_type'] and not inputs['cups_bool']:
                        key1 = key + conv_lookup
                    elif record['spoon_type'] and not inputs['spoons_bool']:
                        key1 = key + conv_lookup
                    else:
                        key1 = key

                    pos2 = tempLine.find(key1)

                    if pos2 > -1:
                        measure_found = True
                        sub_measure_found = True

                        #part 2 is the found weight
                        part2 = tempLine[:pos2]
                        foundWeight1 = re.search(r'((?:\d*\.)?\d+)(?!.*((?:\d*\.)?\d+))', part2)

                        # this last part finds the last number (decimals permitted) in the first half of the instruction
                        # https://stackoverflow.com/questions/5320525/regular-expression-to-match-last-number-in-a-string

                        if foundWeight1:
                            foundWeight = foundWeight1.group()
                            foundWeightFloat = float(foundWeight)

                            #Get part1 - the part before the weight
                            pos1 = tempLine.find(foundWeight)
                            part1 = tempLine[:pos1]
                            part1 = re.sub(r'\W*$', '', part1).strip()  # remove any non letters at end
                            # Part3 is after the found unit
                            part3 = tempLine[pos2+len(key1):]
                            part3 = re.sub(r'^\W*', '', part3).strip()  # remove any non letters at the beginning

                            conv_weight_value = foundWeightFloat * record['unit_conversion']
                            conv_weight = prettyWeight(conv_weight_value, record['unit_dest_name'])

                            conv_op = str(foundWeight) + ' ' + str(key1) + ' to ' + str(conv_weight)
                            conv_str = conv_weight + ' ' + part3.strip()
                            if len(part1) > 0:
                                conv_str = part1 + ' ' + conv_str

                            output_conv.append(conv_op)  # stores row by row information about the conversion
                            output_lines.append(conv_str)

                        else:
                            output_conv.append('Found "' + key1 + '", but could not determine a number, unchanged')
                            output_fails.append(tempLine)
                            output_lines.append(tempLine)

                    if sub_measure_found:
                        break

                if measure_found:
                    break

        if not measure_found:
            output_conv.append('No measures found, unchanged')
            output_lines.append(tempLine)

    conversions = '\n'.join(output_conv)
    fails = '\n'.join(output_fails)

    outputs = dict()
    outputs['converted_text'] = '\n'.join(output_lines)
    outputs['conversion_msg'] = conv_msg

    m = Conversion(user=inputs['user'],
                   source_url=inputs['source_url'],
                   conversion_name=inputs['name'],
                   original_text=inputs['recipe_text'],
                   converted_text=outputs['converted_text'],
                   conversion_type=conv_msg,
                   converted_method=conversions,
                   converted_fails=fails)
    m.save()

    return conversions, outputs
