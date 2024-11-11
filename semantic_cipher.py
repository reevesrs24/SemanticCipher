import torch
import numpy as np

from typing import List, Tuple
from prefix_mapper import PrefixMapper
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline



class SemanticCipher:
    def __init__(self, model_name: str="meta-llama/Llama-3.2-1B") -> None:
        self.prefix_mapper = PrefixMapper()
        self.model_name = model_name
        self.ascii_map = None
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def _get_next_word(self, token_prefix: str, cipher_text: str) -> str:

        if cipher_text == '':
            input_str = token_prefix.capitalize()
            next_word = input_str
        else:
            input_str = f"{cipher_text} {token_prefix}"
            next_word = token_prefix

        # Encode the input prefix and generate output
        inputs = self.tokenizer([input_str], return_tensors="pt")
        input_ids = inputs.input_ids

        while True:

            with torch.no_grad():
                outputs = self.model(input_ids=input_ids)
            
            # Get the next token
            next_token_logits = outputs.logits[0, -1, :]
            next_token_id = torch.argmax(next_token_logits).item()
            next_char = self.tokenizer.decode([next_token_id])

            # Append character to the result
            next_word += next_char
            input_ids = torch.cat([input_ids, torch.tensor([[next_token_id]])], dim=1)

            if " " in next_char:
                next_word = next_word.split(' ')[0]
                break

        return next_word.strip()

    def encode(self, plaintext: str, key: str = "") -> str:
        self.ascii_map = self.prefix_mapper.generate_mapping(key=key)

        encoded_str = ""
        for ch in plaintext:
            encoded_str += self._get_next_word(self.ascii_map[ord(ch)], encoded_str)
            encoded_str += " "

        return encoded_str

    def decode(self, ciphertext: str) -> str:
        ascii_map_reverse = {val: key for key, val in self.ascii_map.items()}
        return "".join(
            chr(ascii_map_reverse[word[:2].lower()]) for word in ciphertext.split() if word
        )



def main():    
    sc = SemanticCipher()
    ciphertext = sc.encode("0xdeadbeef", key="a")
    print(ciphertext)
    plaintext = sc.decode(ciphertext)
    print(plaintext)


if __name__ == '__main__':
    main()
    