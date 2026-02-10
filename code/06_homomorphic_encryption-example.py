from math import gcd


def lcm(a, b):
    return a * b // gcd(a, b)


def inv_mod(value, modulus):
    return pow(value, -1, modulus)


def keygen(p=7, q=11, g=12):
    n = p * q
    n_sq = n * n
    lam = lcm(p - 1, q - 1)
    mu = inv_mod(((pow(g, lam, n_sq) - 1) // n) % n, n)
    return {"n": n, "n_sq": n_sq, "g": g}, {"lambda": lam, "mu": mu}


def encrypt(public_key, message, r=2):
    n = public_key["n"]
    n_sq = public_key["n_sq"]
    g = public_key["g"]
    return (pow(g, message, n_sq) * pow(r, n, n_sq)) % n_sq


def decrypt(private_key, public_key, ciphertext):
    n = public_key["n"]
    n_sq = public_key["n_sq"]
    lam = private_key["lambda"]
    mu = private_key["mu"]
    u = pow(ciphertext, lam, n_sq)
    l_value = ((u - 1) // n) % n
    return (l_value * mu) % n


if __name__ == "__main__":
    public_key, private_key = keygen()
    left = encrypt(public_key, 2)
    right = encrypt(public_key, 5)
    summed = (left * right) % public_key["n_sq"]
    print(decrypt(private_key, public_key, summed))
