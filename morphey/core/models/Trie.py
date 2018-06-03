def normalize(self, word: str) -> str:
    return word.replace('ё', 'е')


def get_grams(node):
    grams = []
    for g in node.findall('g'):
        grams.append(g.get('v'))
    return grams


class Trie:
    def __init__(self):
        self.trie = {'children': dict(), 'links': []}
        self.words = {
            'lemmas': [],
            'forms': [],
        }

    def build(self, lemmas):
        for lemma in lemmas:
            l = lemma.find('l')
            lemma_text = normalize(l.get('t'))
            base = lemma_text
            forms = lemma.findall('f')

            # base calculating
            for f in forms:
                word = normalize(f.get('t'))

                nextBase = ''
                i = 0
                baseLen = min(len(base), len(word))

                while (i < baseLen):
                    if (base[i] == word[i]):
                        nextBase = nextBase + base[i]
                    else:
                        break

                    i = i + 1

                base = nextBase

            lemmaId = len(self.words['lemmas'])
            self.words['lemmas'].append({
                'base': base,
                'word': lemma_text,
                'grams': get_grams(l)
            })

            for f in forms:
                word = normalize(f.get('t'))

                formId = len(self.words['forms'])
                self.words['forms'].append({
                    'word': word,
                    'grams': get_grams(f),
                    'lemmaId': lemmaId
                })

                chars = list(reversed(list(word)))
                curr = self.trie

                diff = len(word) - len(base)

                for i, char in enumerate(chars):
                    if (char not in curr['children']):
                        curr['children'][char] = {
                            'children': dict(),
                            'links': [],
                            'words': [],
                            'affexes': [],
                        }

                    curr = curr['children'][char]

                    curr['links'].append(formId)

                    # we should add link for the postfixes
                    # for the improved search
                    if (i == diff - 1):
                        curr['affexes'].append(formId)

                curr['words'].append(formId)
