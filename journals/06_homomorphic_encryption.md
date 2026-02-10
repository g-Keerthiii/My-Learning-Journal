# Homomorphic Addition with Paillier

Date: 2026-05-14
Mood/Energy: Frustrated until the math clicked
Estimated reading time: 8 minutes

## The "Why"
I had heard the phrase "compute on encrypted data" a lot, and it sounded almost impossible in a practical sense. I wanted to see one real example instead of just repeating the slogan back to myself.

## The Exploration
Paillier is the first cryptography topic here that made me slow down and write the math out by hand. The big idea is that the encryption scheme preserves addition in a weird indirect way. I do not decrypt each value, add them in plaintext, and re-encrypt. I combine ciphertexts and get a ciphertext that decrypts to the sum.

My simplified picture was:

```text
encrypt(a) + encrypt(b) -> encrypt(a + b)
```

That is obviously not how ordinary encryption behaves, which is why the property feels so powerful. The catch, of course, is that this is only partially homomorphic. It supports addition well, but not arbitrary general-purpose math.

## The Code (Crucial)
The longer Python example lives in [code/06_homomorphic_encryption-example.py](../code/06_homomorphic_encryption-example.py).

```python
a = encrypt(public_key, 2)
b = encrypt(public_key, 5)
combined = (a * b) % public_key.n_sq
print(decrypt(private_key, combined))  # 7
```

## The "Aha!" Moment
The thing that finally clicked was that the ciphertext space is doing the arithmetic for me. I do not need to reveal the numbers to make the sum happen. I just need the algebraic structure to line up in the right way.

## The Struggle
I kept getting lost in the notation because I wanted the algorithm to feel like a normal API call. It is not. The modular arithmetic is the whole point, and I had to stop skipping over the ugly parts of the formula. Once I tested a tiny example with small primes and wrote out each step, the structure became easier to trust.

## Key Takeaways
- Homomorphic encryption lets us compute on ciphertexts.
- Paillier supports addition, not full general computation.
- Modular arithmetic is not a side detail; it is the mechanism.
- Small worked examples are the only way I could keep the math straight.
- The privacy benefit comes from never exposing plaintext during the operation.

## Questions I still have
- How do systems choose parameters that are both secure and practical?
- What does a real-world pipeline look like when homomorphic operations are only one step in a larger workflow?
