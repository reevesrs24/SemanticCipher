<div align="center"><img src="assets/semantic_cipher.jpeg" width="350"/></div>
  
# Semantic Cipher
Encrypt arbitrary data into semantic text

## Index
1. [How it Works](#how-it-works)
   - [Encryption](#encryption)
     - [Step 1: Convert Plaintext to Hexadecimal Format](#step-1-convert-plaintext-to-hexadecimal-format)
     - [Step 2: Create Hexadecimal Mapping](#step-2-create-hexadecimal-mapping)
     - [Step 3: Map Each Corresponding Hexadecimal Value to English Word](#step-3-map-each-corresponding-hexadecimal-value-to-english-word)
   - [Decryption](#decryption)
     - [Step 1: Parse the Ciphertext and Extract First Character of Each Word](#step-1-parse-the-ciphertext-and-extract-first-character-of-each-word)
     - [Step 2: Map the Hexadecimal Characters to Their Corresponding Values](#step-2-map-the-hexadecimal-characters-to-their-corresponding-values)
2. [Encrypt Using OpenAI Models](#encrypt-using-openai-models)
3. [Encrypt Using Pretrained SLM](#encrypt-using-pretrained-slm)

## How it Works
### Encryption
**Step 1.  Convert Plaintex to Hexadecimal Format**
* The plaintext is converted into a hexadecimal representation  
    * Input: `Hello`
        - **H** → ASCII: 72  → Hex: `0x48`
        - **e** → ASCII: 101 → Hex: `0x65`
        - **l** → ASCII: 108 → Hex: `0x6C`
        - **l** → ASCII: 108 → Hex: `0x6C`
        - **o** → ASCII: 111 → Hex: `0x6F`

       Output: `0x48656C6C6F21`  

**Step 2.  Create Hexadecimal Mapping**

* Each of the 16 hexadecimal characters are mapped to one of the 16 highest frequency English characters.  These characters are `E`, `T`, `A`, `O`, `I`, `N`, `S`. `H`, `R`, `D`, `L`, `C`, `U`, `M`, `W` and `F`.  
* If a `key` is a chosen the hex mapping will be "scrambled" in such a way that only the key can be used to restructure the hex mapping to retrieve the semantically encrypted text.
* Hex mapping when `key=""`
```python
self.hex_map = {'0': 'U', '1': 'H', '2': 'T', '3': 'I', '4': 'L', '5': 'R', '6': 'A', '7': 'F', '8': 'E', '9': 'N', 'A': 'M', 'B': 'C', 'C': 'S', 'D': 'O', 'E': 'D', 'F': 'W'}
```
* Hex mapping when `key="abc"`
```python
self.hex_map = {'0': 'L', '1': 'T', '2': 'H', '3': 'D', '4': 'S', '5': 'F', '6': 'R', '7': 'O', '8': 'E', '9': 'I', 'A': 'A', 'B': 'M', 'C': 'U', 'D': 'N', 'E': 'C', 'F': 'W'}
```

**Step 3.  Map Each Corresponding Hexadecimal Value to English Word**

*  For each hexadecimal character in the hexadecimal representaion of `Hello` (`48656C6C6F`) lookup the corresponding value and semantically generate the next most probabilistic word.  The LLM/SLM will be "forced" to output the next most logical word given the prior words that start with the corresponding character.  

    * Input: `48656C6C6F` and`Key=""`
        - **0x4** → Value: `L` → Learning
        - **0x8** → Value: `E` → every
        - **0x6** → Value: `A` → aspect
        - **0x5** → Value: `R` → requires
        - **0x6** → Value: `A` → a
        - **0xC** → Value: `S` → strong
        - **0x6** → Value: `A` → analytical
        - **0xC** → Value: `S` → skill
        - **0x6** → Value: `A` → and
        - **0xF** → Value: `W` → willpower

    Output: `Learning every aspect requires a strong analytical skill and willpower`

### Decryption
**Step 1.  Parse the Ciphertext and Extract First Character of Each Word**  

* Input: `Learning every aspect requires a strong analytical skill and willpower` and `Key=""`  
  - **Learning** → Value: `L` → Hex: `0x4`
  - **every** → Value: `E` → Hex: `0x8`
  - **aspect** → Value: `A` → Hex: `0x6`
  - **requires** → Value: `R` → Hex: `0x5`
  - **a** → Value: `A` → Hex: `0x6`
  - **strong** → Value: `S` → Hex: `0xC`
  - **analytical** → Value: `A` → Hex: `0x6`
  - **skill** → Value: `S` → Hex: `0xC`
  - **and** → Value: `A` → Hex: `0x6`
  - **willpower** → Value: `W` → Hex: `0xF`

  Output: `0x48656C6C6F21` 

**Step 2.  Map the Hexadecimal Characters to Their Correpsonding Values**

* Input: `0x48656C6C6F21` and `Key=""`  
    - **Hex: `0x48`** → Character: `H`
    - **Hex: `0x65`** → Character: `e`
    - **Hex: `0x6C`** → Character: `l`
    - **Hex: `0x6C`** → Character: `l`
    - **Hex: `0x6F`** → Character: `o`

    Output: `Hello`

## Encrypt Using OpenAI Models

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

## Encrypt Using Pretrained SLM

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