#!/usr/bin/env python3
"""Sanity checks for art/ before building the font.

Catches the failure modes we actually hit:
  * two files with identical content (a batch writing the same image twice)
  * duplicate codepoints in the manifest
  * manifest entries whose file is missing / art files not in the manifest
  * sequence components that are not covered by the manifest
"""
import json, os, sys, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ART = os.path.join(ROOT, "art")


def main():
    man = json.load(open(os.path.join(ART, "manifest.json")))
    seq_path = os.path.join(ART, "sequences.json")
    seq = json.load(open(seq_path)) if os.path.exists(seq_path) else {}
    problems = []

    cps = collections.Counter(man.values())
    for cp, n in cps.items():
        if n > 1:
            problems.append(f"duplicate codepoint {cp}: {[f for f,v in man.items() if v==cp]}")

    for fname in man:
        if not os.path.exists(os.path.join(ART, fname)):
            problems.append(f"missing art: {fname}")

    listed = set(man) | set(seq)
    for f in sorted(os.listdir(ART)):
        if f.endswith(".png") and f not in listed:
            problems.append(f"art not in manifest: {f}")

    hashes = collections.defaultdict(list)
    for f in sorted(listed):
        p = os.path.join(ART, f)
        if os.path.exists(p):
            hashes[hashlib.sha256(open(p, "rb").read()).hexdigest()].append(f)
    for h, files in hashes.items():
        if len(files) > 1:
            problems.append(f"identical content: {files}")

    covered = {int(v[2:], 16) for v in man.values()}
    for fname, s in seq.items():
        for part in s.split():
            cp = int(part, 16)
            if cp in (0x200D, 0xFE0F):
                continue
            if cp not in covered:
                problems.append(f"sequence {fname}: component U+{cp:04X} not in manifest")

    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"ok: {len(man)} codepoints + {len(seq)} sequences, no duplicates, all files present")


if __name__ == "__main__":
    main()
