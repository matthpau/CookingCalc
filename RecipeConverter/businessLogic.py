from num2words import num2words
import re
from .models import Converter

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

    output_lines = []
    replacement_text = {' 1/2': '.5',
                        '1/2': '0.5',
                        ' 1/3': '.333',
                        '1/3': '.333',
                        ' 1/4': '.25',
                        '1/4': '.25',
                        ' 1/5': '.2',
                        '1/5': '.2',
                        }

    replacement_res = {''}

    lookupSearch = Converter.objects.all()
    print(lookupSearch.values())

    for line in inputs['recipe_text'].splitlines():
        tempLine = line.strip()
        print(len(tempLine))

        if len(tempLine) == 0:
            break

        # Step 1 - if there are no digits at all, this is not an ingredient that can be converted
        elif not hasDigits(tempLine):
            output_lines.append(tempLine)

        # Step 2 - find the numbers
        else:
            #Run brute force replacements
            for k, v in replacement_text.items():
                if k in tempLine:
                    print('Doing a replace', k, v)
                    tempLine = tempLine.replace(k, v)

            #Run keys search from data
            for record in lookupSearch.values():
                searchKeys = record['unit_source_keys'].split()  # always search for the longest one first
                searchKeys.sort(key=len, reverse=True)

                found = False
                for key in searchKeys:
                    pos2 = tempLine.find(key)

                    print()
                    print('searching for', key)
                    if pos2 > -1:
                        print('Found', key, ' in ', tempLine, 'position', pos2)

                        #part 2 is the found weight
                        part2 = tempLine[:pos2]
                        foundWeight = re.search(r'((?:\d*\.)?\d+)(?!.*((?:\d*\.)?\d+))', part2).group()
                        # this last part finds the last number (decimals permitted) in the first half of the instruction
                        # https://stackoverflow.com/questions/5320525/regular-expression-to-match-last-number-in-a-string

                        if foundWeight:
                            found = True
                            print('Found a number for a weight!!!!')

                            foundWeightFloat = float(foundWeight)
                            print('float of foundWeight', foundWeight, foundWeightFloat)

                            #Get part1 - the part before the weight
                            pos1 = tempLine.find(foundWeight)
                            # no need to test, was found above
                            part1 = tempLine[:pos1]

                            # Part three is after the found unit

                            part3 = tempLine[pos2+len(key):]
                            part3 = re.sub(r'^\W*', '', part3)  # remove any non letters at the beginning


                            print('Part1', part1)
                            print('Part2', part2)
                            print('pos2', pos2, key, len(key))
                            print('FoundWeight', foundWeight)
                            print('part3', part3)

                        else:
                            print('Found a measure, but could not determine a number')

                    else:
                        print('Could not find', key)

        output_lines.append('found a number: ' + tempLine)

        print()

    outputs = '\n'.join(output_lines)

    #print(outputs)

    return outputs
