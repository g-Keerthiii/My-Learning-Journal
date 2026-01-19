# Git Internals - Rebuilding the `.git` Directory

Date: 2026-04-01
Mood/Energy: Confused, then weirdly relieved
Estimated reading time: 8 minutes

## The "Why"
I use Git every day, but I realized I was mostly using the verbs without understanding the storage model behind them. I wanted to see what a blob, tree, and commit actually look like when I stop pretending Git is magic.

## The Exploration
This was the first topic where the mental model felt almost like archaeology. A commit is not the file itself. It is a pointer to a tree, which points to blobs, which hold the raw file contents. Once I saw that, Git stopped feeling like "version control" and started feeling like a content-addressed snapshot machine.

The shape of it made more sense when I drew it like this:

```text
commit -> tree -> blob(file contents)
        -> parent commit
```

The important part is the hash. Git does not name objects by "latest" or "final." It names them by content. That means the same content always produces the same identity, which is a very different way to think about data.

## The Code (Crucial)
The longer script is in [code/03_git_internals-example.py](../code/03_git_internals-example.py).

```python
import hashlib
import os
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
```

## The "Aha!" Moment
The click for me was that a commit is basically a signed snapshot of a tree, not a copy of every file. That explains why history is so lightweight most of the time and why branching can be cheap.

## The Struggle
I got stuck because I kept looking for files in `.git` as if they were readable text files. They are mostly compressed object blobs, so my first inspection attempts looked like nonsense. Once I used the object format directly and decompressed the files, the pieces lined up. I also tripped over the exact object header format until I realized the null byte is part of the hash input, not just a separator.

## Key Takeaways
- Git stores content as objects, not as loose file copies.
- A blob holds file content, a tree holds structure, and a commit ties them together.
- Hashes make the storage content-addressed.
- Branches are just movable references to commits.
- The `.git` folder is simpler once you stop treating it like a mystery box.

## Questions I still have
- How does Git decide when to pack objects into packfiles?
- What is the easiest way to inspect large histories without losing the structure of the DAG?
