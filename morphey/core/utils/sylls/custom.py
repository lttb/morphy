"""
    Custom syllables splitting implementation for Russian,
    simply based on idea of phonemic similarity.

    сода -> ['с', 'од', 'а']
    мода -> ['м', 'од', 'а']
    лайнер -> ['л', 'ай', 'н', 'ер']
    майнер -> ['м', 'ай', 'н', 'ер']
    злость -> ['з', 'лос', 'ть']
    трость -> ['т', 'рос', 'ть']
    мальчик -> ['м', 'аль', 'ч', 'ик']
    пальчик -> ['п', 'аль', 'ч', 'ик']
    графини -> ['г', 'раф', 'ин', 'и']
    княгини -> ['к', 'няг', 'ин', 'и']
"""

vowels = set(['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е'])
marks = set(['й', 'ь'])


def split(word):
    sylls = []

    curr = ''
    i = 0
    l = len(word)

    while i < l:
        if (i + 1 < l and word[i] in marks and word[i + 1] in vowels):
            if (curr != ''):
                sylls.append(curr)

            curr = word[i:i + 1]
            i + 1
        elif (word[i] in vowels):
            if (curr != ''):
                sylls.append(curr)

            curr = word[i]

        elif (
            i - 1 > 0 and (word[i] not in vowels)
            and (word[i - 1] not in vowels) and (word[i] not in marks)
        ):
            if (curr != ''):
                sylls.append(curr)

            curr = word[i:i + 1]
        elif (
            i - 1 >= 0 and (word[i] not in vowels)
            and (word[i - 1] not in vowels) and (word[i] not in marks)
        ):
            if (curr != ''):
                sylls.append(curr)

            curr = word[i:i + 2]
            i = i + 1
        else:
            curr = curr + word[i]

        i = i + 1

    if (curr != ''):
        sylls.append(curr)

    return sylls
