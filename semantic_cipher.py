import os
import json
import torch
import numpy as np

from typing import List, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SemanticCipher:
    def __init__(self, model_name: str="meta-llama/Llama-3.2-1B") -> None:
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.hex_map = {
                        '0': 'E',
                        '1': 'T',
                        '2': 'A',
                        '3': 'O',
                        '4': 'I',
                        '5': 'N',
                        '6': 'S',
                        '7': 'H',
                        '8': 'R',
                        '9': 'D',
                        'A': 'L',
                        'B': 'C',
                        'C': 'U',
                        'D': 'M',
                        'E': 'W',
                        'F': 'F'
                    }
        self.llm_model = 'gpt-4o'
        self.api_key = os.getenv("OPENAI_API_KEY")

    def _query_llm(self, encoded_str: str, context: str=""):
        client = OpenAI(api_key=self.api_key)

        prompt = f"""
                Task: Generate a sentence where each word begins with the corresponding character in the provided list of characters. The sentence must be logical, semantically correct, and follow these constraints:

                1. Each word must begin with the corresponding character in the list, in order.
                2. The output must contain a word for every character in the list, with no omissions or extra words. 

                Input format: A string of characters, e.g., `"abcd"`.  
                Output format: A sentence where each word starts with the corresponding character, e.g., `"Always before continuing downward"`.

                Example 1:  
                - Input: `"abcdefg"`  
                - Output: `"Always before continuing downward, expect failing guardrails"`

                Example 2:  
                - Input: `"ruendbg"`  
                - Output: `"Running under everything now, beyond glad"`  

                Now, using the above guidelines, process the input and generate the output.
                
                
            """
        if context != "":
            prompt += f"The context of the sentence should be {context}."

        prompt += f"Use these following characters to construct the output: {encoded_str}"

        prompt += """
                Return the response in JSON format.
                Use the follwing format:
                {
                    "text": <generated_output>
                }
            """

        content = [
            {
                "type": "text",
                "text": prompt,
            },
        ]


        completion = client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            response_format={"type": "json_object"}
        )

        output = completion.choices[0].message.content
        output = json.loads(output)
        return output.get('text', '')

    def _get_next_word(self, token_bigram: str, cipher_text: str) -> str:

        if cipher_text == '':
            input_str = token_bigram.capitalize()
            next_word = input_str
        else:
            input_str = f"{cipher_text}{token_bigram.lower()}"
            next_word = token_bigram.lower()

        # Encode the input bigram and generate output
        inputs = self.tokenizer([input_str], return_tensors="pt")
        input_ids = inputs.input_ids

        print(input_str)

        while True:
            with torch.no_grad():
                outputs = self.model(input_ids=input_ids)

            # Get the next token
            next_token_logits = outputs.logits[0, -1, :]
            next_token_id = torch.argmax(next_token_logits).item()
            next_char = self.tokenizer.decode([next_token_id])

            # Append character to the result
            input_ids = torch.cat([input_ids, torch.tensor([[next_token_id]])], dim=1)

            if next_char[0] == " ":
                next_word = next_word.split(' ')[0].replace('\n', '')
                break
            
            next_word += next_char

        return next_word.strip()

    def _string_to_hex(self, text: str):
        # Convert each character to hexadecimal and join them
        return ''.join(format(ord(char), '02x') for char in text)
    
    def _hex_to_string(self, hex_text: str):
        # Split hex text into pairs of two characters, convert to char, and join them
        return ''.join(chr(int(hex_text[i:i+2], 16)) for i in range(0, len(hex_text), 2))

    def _checksum(self, cipher_chunk, chunk):
        decoded_cipher_chunk = self.decode(cipher_chunk)
        decoded_cipher_chunk_2 = self._hex_to_string(chunk)
        return False if decoded_cipher_chunk != decoded_cipher_chunk_2 else True

    def encode(self, plaintext: str, key: str = "") -> str:
        ciphertext = ""
        encoded_plaintext = self._string_to_hex(plaintext)

        chunks = [encoded_plaintext[i:i+10] for i in range(0, len(encoded_plaintext), 10)]

        for chunk in chunks:
            encoded_str = [self.hex_map[ch.upper()] for ch in chunk]
            # print(encoded_str)
            text = self._query_llm(encoded_str, "space")
            count = 0
            while not self._checksum(text, chunk) and count < 10:
                print("no match")
                text = self._query_llm(encoded_str, "space")
                count += 1
            print()
            ciphertext += text + ". "

        return ciphertext


    def decode(self, ciphertext: str) -> str:
        hex_map_reverse = {val: key for key, val in self.hex_map.items()}
        print(ciphertext.split(' '))
        return self._hex_to_string("".join(
            hex_map_reverse[word[0].upper()] for word in ciphertext.split(' ') if word != ''
        ))


def main():    
    sc = SemanticCipher()
    ciphertext = sc.encode("Analis Reeves", key="")
    print(ciphertext)
    plaintext = sc.decode(ciphertext)
    print(plaintext)


if __name__ == '__main__':
    main()
    