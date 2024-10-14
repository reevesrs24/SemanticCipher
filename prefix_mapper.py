from collections import defaultdict
from datasets import load_dataset

class PrefixMapper:
    def __init__(self) -> None:
        pass

    def create_prefix_map(self):
        
        prefix_map = defaultdict(int)

        dataset = load_dataset("wikitext", 'wikitext-2-v1', split="train")

        for raw_text_iter in dataset['text']:
            for word in raw_text_iter.lower().split(' '):
                if len(word) >= 1 and word[:1][0].isalpha():
                    prefix_map[word[:1]] += 1
                if len(word) >= 2 and word[:2][0].isalpha() and word[:2][1].isalpha() and not word[:2][1].isupper():
                    prefix_map[word[:2]] += 1

        prefix_map = sorted(prefix_map.items(), key=lambda x: x[1], reverse=True)
        print(prefix_map)


def main():    
    pm = PrefixMapper()
    pm.create_prefix_map()

if __name__ == '__main__':
    main()
    