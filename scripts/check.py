#!/usr/bin/env python3
"""Extract what a theorem needs into its own Lean file and compile it.

Usage (from the project root): scripts/check.py <Module> <root declaration>

Writes scripts/lean/<name>.lean, .log, .dropped.txt and, if anything had to be added
back, .keep.txt. A lemma used only by `dsimp`/`unfold`-style steps leaves no trace
in the proof term, so when the compile reports an unknown identifier the matching
declaration is added back and the extraction is retried.
"""
import re, subprocess, sys, time

mod, root = sys.argv[1:3]
base = "scripts/lean/" + root.rsplit(".", 1)[-1]
keep = set()
for attempt in range(1, 9):
    open(base + ".keep.txt", "w").write("".join(n + "\n" for n in sorted(keep)))
    with open(base + ".lean", "w") as out:
        subprocess.run([sys.executable, "scripts/extract.py", f"{mod}.lean", f"scripts/modules/{mod}.dot",
                        f"scripts/modules/{mod}.decls.tsv", root, "--keep", base + ".keep.txt",
                        "--dropped", base + ".dropped.txt"], stdout=out, check=True)
    start = time.time()
    log = subprocess.run(["lake", "env", "lean", base + ".lean"], capture_output=True, text=True)
    text = log.stdout + log.stderr
    errors = text.count(": error")
    open(base + ".log", "w").write(text)
    print(f"{base}: attempt {attempt}, {errors} errors, {time.time() - start:.0f}s, "
          f"{len(keep)} added back", flush=True)
    if not errors:
        break
    dropped = open(base + ".dropped.txt").read().split()
    new = set()
    for ident in re.findall(r"Unknown (?:identifier|constant) `([^`]+)`", text):
        new |= {d for d in dropped if d == ident or d.endswith("." + ident)}
    if not new - keep:
        break
    keep |= new
