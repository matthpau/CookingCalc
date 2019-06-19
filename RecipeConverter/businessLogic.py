from num2words import num2words
import re
from .models import Converter, Conversion
from django.contrib.auth import get_user_model

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


def converter(inputs):
    """
    word_text = []
    for i in range(1, 50):
        word_text.append(num2words(i))
    print(word_text)
    """

    print(inputs)

    output_conv = []  # stores row by row information about the conversion
    output_lines = []  # stores row by row results
    output_fails = []

    replacement_text = {' 1/2': '.5',
                        '1/2': '0.5',
                        ' 1/3': '.333',
                        '1/3': '.333',
                        ' 1/4': '.25',
                        '1/4': '.25',
                        ' 1/5': '.2',
                        '1/5': '.2',
                        }

    lookupSearch = Converter.objects.all()

    for line in inputs['recipe_text'].splitlines():
        tempLine = line.strip()
        line_found = False

        if len(tempLine) == 0 or tempLine == None or tempLine == '':
            break

        elif not hasDigits(tempLine):
            output_conv.append('No numbers found, unchanged')
            output_lines.append(tempLine)
            break

        # Step 2 - find the numbers
        else:
            #Run brute force replacements
            for k, v in replacement_text.items():
                if k in tempLine:

                    tempLine = tempLine.replace(k, v)

            #Run keys search from data

            measure_found = False

            for record in lookupSearch.values():
                searchKeys = record['unit_source_keys'].split()
                searchKeys.sort(key=len, reverse=True)  # always search for the longest one first

                for key in searchKeys:
                    sub_measure_found = False
                    pos2 = tempLine.find(key)

                    if pos2 > -1:
                        measure_found = True
                        sub_measure_found = True

                        #part 2 is the found weight
                        part2 = tempLine[:pos2]
                        foundWeight = re.search(r'((?:\d*\.)?\d+)(?!.*((?:\d*\.)?\d+))', part2).group()
                        # this last part finds the last number (decimals permitted) in the first half of the instruction
                        # https://stackoverflow.com/questions/5320525/regular-expression-to-match-last-number-in-a-string

                        if foundWeight:
                            foundWeightFloat = float(foundWeight)

                            #Get part1 - the part before the weight
                            pos1 = tempLine.find(foundWeight)
                            part1 = tempLine[:pos1]
                            part1 = re.sub(r'\W*$', '', part1).strip()  # remove any non letters at end

                            # Part three is after the found unit

                            part3 = tempLine[pos2+len(key):]
                            part3 = re.sub(r'^\W*', '', part3).strip()  # remove any non letters at the beginning

                            conv_weight = str(round(foundWeightFloat * record['unit_conversion'],
                                                    3)) + ' ' + record['unit_dest_name']
                            conv_op = str(foundWeight) + ' ' + str(key) + ' to ' + str(conv_weight)
                            conv_str = conv_weight + ' ' + part3.strip()
                            if len(part1) > 0:
                                conv_str = part1 + ' ' + conv_str

                            output_conv.append(conv_op)  # stores row by row information about the conversion
                            output_lines.append(conv_str)
                            #TODO add these to the table to store results

                        else:
                            output_conv.append('Found "' + key + '", could not determine a number, unchanged')
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
    outputs = '\n'.join(output_lines)
    fails = '\n'.join(output_fails)

    m = Conversion(user=inputs['user'],
                   source_url=inputs['source_url'],
                   user_comments=inputs['comment'],
                   original_text=inputs['recipe_text'],
                   converted_ingredients=outputs,
                   converted_method=conversions,
                   converted_fails=fails)
    m.save()

    return conversions, outputs
