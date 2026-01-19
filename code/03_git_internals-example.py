import hashlib
import os
import subprocess
import zlib


def write_object(repo, kind, content):
    header = f"{kind} {len(content)}\0".encode()
    data = header + content
    sha = hashlib.sha1(data).hexdigest()
    path = os.path.join(repo, ".git", "objects", sha[:2], sha[2:])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(zlib.compress(data))
    return sha


def write_ref(repo, ref, sha):
    path = os.path.join(repo, ".git", ref)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(sha + "\n")


if __name__ == "__main__":
    repo = os.getcwd()
    blob = write_object(repo, "blob", b"hello journal\n")
    tree = write_object(repo, "tree", f"100644 note.txt\0{bytes.fromhex(blob)}".encode())
    commit = write_object(repo, "commit", f"tree {tree}\nauthor me <me@example.com>\n\nfirst snapshot\n".encode())
    write_ref(repo, "refs/heads/main", commit)
    subprocess.run(["git", "cat-file", "-p", commit], check=False)
