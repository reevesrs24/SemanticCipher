# SemanticCipher
Encode arbitrary data into semantic text

## Encode using OpenAI GPT-4o

To use OpenAI models, simply add your OpenAI API key to the `.env` file.

The `encode` method requires one parameter, `plaintext`, which is the textual data that is to be semantically enciphered.

Two optional parameters can be used:

* The `context` param notifies the LLM that the generated output should be relevant to the given topic.
* The `key` param shuffles the hex mapping so that the end user must know the key in order for the text to be decoded.

There are `16!` total permutations, given that the encoding list contains all hexadecimal characters.

```python
sc = SemanticCipher(model_name="gpt-4o")
ciphertext = sc.encode(plaintext="0xdeadbeef", context="Space", key="xyz")
print(f"Ciphertext: {ciphertext}")
plaintext = sc.decode(ciphertext)
print(f"Plaintext: {plaintext}")
```

Output:
```bash
Ciphertext: Launching every day, fearless astronauts will always conquer all universe. Astronauts wearing advanced technology aboard craft achieve cosmic adventures always
Plaintext: 0xdeadbeef
```

## Encode using pretrained SLM

> [!IMPORTANT]  
> - Using SLMs typically output text that is erroneous and/or illogical. Next token prediction is strictly used and does not leverage the reasoning capabilities of larger models to formulate outputs.  Added as an experiment and as a template for future experiments.

```python
sc = SemanticCipher(model_name="Qwen/Qwen2.5-1.5B-Instruct", from_pretrained=True)
ciphertext = sc.encode("0xdeadbeef", key="xyz")
print(f"Ciphertext: {ciphertext}")
plaintext = sc.decode(ciphertext)
print(f"Plaintext: {plaintext}")
```

Output:
```bash
Ciphertext: Lily E. Duffin F. A. W. A. C. A. U. A. W. A. T. A. C. A. C. A. A.
Plaintext: 0xdeadbeef
```

> [!TIP]  
> - Use `requirements.txt` to install all necessary packages
> - Python version `3.10.15` was use in testing