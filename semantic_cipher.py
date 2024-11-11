import numpy as np

from typing import List, Tuple
from prefix_mapper import PrefixMapper
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline



class SemanticCipher:
    def __init__(self, model_name: str="meta-llama/Llama-3.2-1B") -> None:
        self.prefix_mapper = PrefixMapper()
        self.model_name = "meta-llama/Llama-3.2-3B"
        self.ascii_map = None
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def _generate_semantic_text(self, token_prefix: str, cipher_text: str) -> str:
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        inputs = self.tokenizer([f"{cipher_text} {token_prefix}"], return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=1,
            num_beams=4,
            num_return_sequences=4,
            return_dict_in_generate=True,
            output_scores=True,
        )

        transition_scores = self.model.compute_transition_scores(
            outputs.sequences, outputs.scores, normalize_logits=True
        )

        input_length = 1 if self.model.config.is_encoder_decoder else inputs.input_ids.shape[1]
        generated_tokens = outputs.sequences[:, input_length:]
        for tok, score in zip(generated_tokens[0], transition_scores[0]):
            # | token | token string | log probability | probability
            # print(f"| {tok:5d} | {self.tokenizer.decode(tok):8s} | {score.numpy():.3f} | {np.exp(score.numpy()):.2%}")
        
            return f"{token_prefix}{self.tokenizer.decode(tok).split(' ')[0]}"

    def encode(self, plaintext: str, key: str="") -> str:
        self.ascii_map = self.prefix_mapper.generate_mapping(key=key)
        ciphertext = ""

        for ch in plaintext:
            token_prefix = self.ascii_map[ord(ch)]
            ciphertext += self._generate_semantic_text(token_prefix, ciphertext)
            ciphertext += " "

        return ciphertext

    def decode(self, ciphertext: str) -> str:
        ascii_map_reverse = {val:key for key, val in self.ascii_map.items()}

        plaintext = ""

        for word in ciphertext.split(' '):
            if word != '':
                plaintext += chr(ascii_map_reverse[word[:2]])

        return plaintext



def main():    
    sc = SemanticCipher()
    ciphertext = sc.encode("0xdeadbeef")
    print(ciphertext)
    plaintext = sc.decode(ciphertext)
    print(plaintext)


if __name__ == '__main__':
    main()
    