<div align="center"><img src="assets/semantic_cipher.jpeg" width="350"/></div>
  
# Semantic Cipher
Encrypt arbitrary data into semantic text

## Encode using OpenAI GPT-4o

To use OpenAI models, simply add your OpenAI API key to the `.env` file.

The `encrypt` method requires one parameter, `plaintext`, which is the textual data that is to be semantically enciphered.

Two optional parameters can be used:

* The `context` param notifies the LLM that the generated output should be relevant to the given topic.
* The `key` param shuffles the hex mapping so that the end user must know the key in order for the text to be decrypted.

There are `16!` total permutations, given that the encoding list contains all hexadecimal characters.

```python
sc = SemanticCipher(model_name="gpt-4o", key="xyz")
ciphertext = sc.encrypt(plaintext="0xdeadbeef", context="Space")

print(f"Ciphertext: {ciphertext}")

plaintext = sc.decrypt(ciphertext=ciphertext)
print(f"Plaintext: {plaintext}")
```

### Output:
```bash
Ciphertext: Launching every day, fearless astronauts will always conquer all universe. Astronauts wearing advanced technology aboard craft achieve cosmic adventures always

Plaintext: 0xdeadbeef
```

## Encode using pretrained SLM

> [!IMPORTANT]  
> - Using SLMs typically output text that is nonsensical. Next token prediction is strictly used and does not leverage the reasoning capabilities of larger models to formulate outputs.  Added as an experiment and as a template for future experiments.

```python
sc = SemanticCipher(model_name="Qwen/Qwen2.5-1.5B-Instruct", from_pretrained=True, key="xyz")

ciphertext = sc.encrypt(plaintext="0xdeadbeef")
print(f"Ciphertext: {ciphertext}")

plaintext = sc.decrypt(ciphertext=ciphertext)
print(f"Plaintext: {plaintext}")
```

### Output:
```bash
Ciphertext: Lily E. Duffin F. A. W. A. C. A. U. A. W. A. T. A. C. A. C. A. A.

Plaintext: 0xdeadbeef
```

> [!TIP]  
> - Use `requirements.txt` to install all necessary packages
> - Python version `3.10.15` was used in testing