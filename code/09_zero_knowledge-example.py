import hashlib
import secrets


PRIME = 2**127 - 1
GENERATOR = 5


def hash_int(*parts):
    data = b"|".join(part if isinstance(part, bytes) else str(part).encode() for part in parts)
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % PRIME


def derive_verifier(salt, password):
    x = hash_int(salt, password)
    return pow(GENERATOR, x, PRIME)


def server_challenge():
    return secrets.randbelow(PRIME - 2) + 2


def client_proof(verifier, challenge):
    return hash_int(verifier, challenge)


def server_verify(verifier, challenge, proof):
    return proof == hash_int(verifier, challenge)


if __name__ == "__main__":
    salt = b"user-salt"
    password = b"correct horse battery staple"
    verifier = derive_verifier(salt, password)
    challenge = server_challenge()
    proof = client_proof(verifier, challenge)
    print(server_verify(verifier, challenge, proof))
