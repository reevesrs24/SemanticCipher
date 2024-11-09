import random

from collections import defaultdict
from typing import List, Tuple
from datasets import load_dataset

class PrefixMapper:
    def __init__(self) -> None:
        # Initialize a default dictionary to store the count of prefixes
        self.prefix_map: defaultdict[str, int] = defaultdict(int)
        self.prefix_list: List[int]
        self.ascii_map: defaultdict[str, str]

    def generate_mapping(self, key: str) -> None:
        self._generate_prefix_map()
        self._map_prefixes_to_ascii(key)

    def _map_prefixes_to_ascii(self, key: str) -> None:
        random.seed(key)
        random.shuffle(self.prefix_list)

        self.ascii_map = {x:prefix for x, prefix in zip(range(0, 256), self.prefix_list)}

    def _generate_prefix_map(self) -> None:
        """
        Creates a prefix map from the 'wikitext-2-v1' dataset.
        The map counts occurrences of 1-character and 2-character
        alphabetical prefixes (lowercase, where the second character is also lowercase).
        """
        # Load the dataset
        dataset = load_dataset("ag_news", split="train")
        
        # Iterate over each text entry in the dataset
        for raw_text_iter in dataset['text']:
            # Split text into words and convert to lowercase
            words: List[str] = raw_text_iter.lower().split()
            
            for word in words:
                # Check if the first character is alphabetical
                if word[0].isalpha():
                    # Increment count for 1-character prefix
                    self.prefix_map[word[:1]] += 1
                    # If the word has a second lowercase alphabetical character, increment for 2-character prefix
                    if len(word) >= 2 and word[1].isalpha() and word[1].islower():
                        self.prefix_map[word[:2]] += 1

        # Sort the prefixes by their count in descending order and get the top 2 most frequent
        self.prefix_map: List[Tuple[str, int]] = sorted(self.prefix_map.items(), key=lambda x: x[1], reverse=True)[:256]
        self.prefix_list = [x[0] for x in self.prefix_map]
        

def main():    
    pm = PrefixMapper()
    pm.generate_mapping(key="abcde")

if __name__ == '__main__':
    main()
    