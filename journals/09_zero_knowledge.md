# Zero-Knowledge Password Proof

Date: 2026-06-10
Mood/Energy: Skeptical, then impressed
Estimated reading time: 8 minutes

## The "Why"
I wanted to understand the part of password authentication that happens before the server ever sees a real secret. The idea sounded almost too good, so I decided to trace the flow and see what is actually stored and exchanged.

## The Exploration
This topic made me appreciate the difference between "never storing plaintext" and "never transmitting anything useful." Zero-knowledge password proofs try to prove knowledge of a password without sending the password itself or a reusable hash.

My rough mental model was:

```text
client knows secret
client proves knowledge
server verifies proof
server never learns secret
```

The key thing I had to keep repeating to myself is that the server stores a verifier, not the password. That verifier is enough for verification, but not enough to reconstruct the secret.

## The Code (Crucial)
The longer Python example lives in [code/09_zero_knowledge-example.py](../code/09_zero_knowledge-example.py).

```python
salt = b"user-salt"
password = b"correct horse battery staple"
verifier = derive_verifier(salt, password)
challenge = server_challenge()
proof = client_proof(verifier, challenge)
assert server_verify(verifier, challenge, proof)
```

## The "Aha!" Moment
The thing that clicked was that authentication can be about proving possession, not revealing the thing itself. That shifted the whole problem from "send me the secret" to "show me evidence that you know it."

## The Struggle
I got stuck because I kept mentally collapsing SRP into ordinary salted hashing. They are related, but not the same. The proof exchange matters, and the server-side verifier is not a password hash in the usual sense. Once I separated those ideas, the flow became much less confusing.

## Key Takeaways
- The server should not need plaintext passwords.
- A verifier can be enough for authentication.
- Zero-knowledge style protocols prove knowledge, not identity by disclosure.
- The challenge-response flow is the part that blocks replay.
- Password storage and password proof are related but different problems.

## Questions I still have
- How do real clients handle safe recovery when a verifier is lost?
- What are the practical tradeoffs between SRP-style flows and newer passwordless options?
