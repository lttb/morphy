"""
    Moscow Linguistics School implementation.
"""

vowels = set(['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е'])
sonors = set(['р', 'рь', 'л', 'ль', 'м', 'мь', 'н', 'нь', 'й'])
pairs = set(['б', 'п', 'в', 'ф', 'г', 'к', 'д', 'т', 'ж', 'ш', 'з', 'с'])


def split(word):
    sylls = []

    curr = ''
    i = 0
    l = len(word)

    while i < l:
        if (i + 1 < l and word[i] in sonors and word[i + 1] in pairs):
            curr = curr + word[i]
            if len(sylls):
                sylls[-1] = sylls[-1] + curr
            else:
                sylls.append(curr)
            curr = ''
        elif (i + 2 < l and word[i:i + 1] in sonors and word[i + 2] in pairs):
            curr = curr + word[i:i + 2]
            if len(sylls):
                sylls[-1] = sylls[-1] + curr
            else:
                sylls.append(curr)
            curr = ''
            i = i + 1
        elif (word[i] in vowels):
            curr = curr + word[i]
            sylls.append(curr)
            curr = ''
        else:
            curr = curr + word[i]

        i = i + 1

    if (curr):
        if (len(sylls) > 0):
            sylls[-1] = sylls[-1] + curr
        else:
            sylls.append(curr)

    return sylls
