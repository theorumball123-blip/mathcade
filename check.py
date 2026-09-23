"""Mathcade consistency check. Run from anywhere:

    python3 tools/check.py

1. Every inline <script> block in every page parses (node --check).
2. The shared modules (Save, MathEngine, Quiz, Results) are byte-identical
   in every page that has them.
3. The shared stylesheet (index.html's <style>) starts the first <style>
   block of every game that uses it, unchanged. Game CSS goes after it.
4. No name is declared twice across a page's script blocks. Each block
   parses on its own, so a whole block pasted in twice only shows up as
   "already been declared" once the browser runs it.

Exits non-zero if anything is wrong.
"""
import re, subprocess, pathlib, sys, hashlib, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODS = ["Save", "MathEngine", "Quiz", "Results"]
SHARED_CSS = ["index.html", "prism-rush.html", "nitro-cup.html", "mage-run.html", "tower-guard.html", "astro-blast.html", "admin.html"]
bad = 0
pages = sorted(ROOT.glob("*.html"))

print("1. Does every script parse?")
with tempfile.TemporaryDirectory() as tmpdir:
    for f in pages:
        html = f.read_text(encoding="utf-8")
        blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
        for i, code in enumerate(blocks, 1):
            tmp = pathlib.Path(tmpdir) / f"{f.stem}-{i}.js"
            tmp.write_text(code, encoding="utf-8")
            r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
            if r.returncode:
                bad += 1
                print(f"   {f.name} block {i}: SYNTAX ERROR")
                print("     ", "\n      ".join(r.stderr.strip().splitlines()[:4]))
print("   done")

print("2. Are the shared modules identical?")
def grab(html, name):
    m = re.search(r"^const %s = \(\(\) => \{.*?^\}\)\(\);" % name, html, re.S | re.M)
    return m.group(0) if m else None
for mod in MODS:
    seen = {}
    for f in pages:
        body = grab(f.read_text(encoding="utf-8"), mod)
        if body:
            seen[f.name] = hashlib.sha256(body.encode()).hexdigest()[:10]
    same = len(set(seen.values())) <= 1
    bad += not same
    print(f"   {mod:11} in {len(seen)} page(s): {'identical' if same else 'DIFFERENT: ' + str(seen)}")

print("3. Is the shared stylesheet identical?")
# index.html's stylesheet is the master copy. Other pages must start their
# first <style> block with exactly that (Mage Run adds its own rules after it
# in the same block; the others use a second block).
first = lambda name: re.search(r"<style[^>]*>(.*?)</style>", (ROOT / name).read_text(encoding="utf-8"), re.S).group(1)
master = first("index.html").rstrip()
for name in SHARED_CSS[1:]:
    ok = first(name).startswith(master)
    bad += not ok
    print(f"   {name:18} {'matches' if ok else 'DIFFERENT from index.html'}")

print("4. Is anything declared twice in one page?")
# node --check reads one block at a time, so a block that got pasted in
# twice still parses. The browser is the one that complains.
for f in pages:
    html = f.read_text(encoding="utf-8")
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    count = {}
    for code in blocks:
        for name in {m.group(1) for m in re.finditer(r"^(?:const|let|class|function)\s+([A-Za-z_$][\w$]*)", code, re.M)}:
            count[name] = count.get(name, 0) + 1
    twice = sorted(n for n, c in count.items() if c > 1)
    if twice:
        bad += 1
        print(f"   {f.name:18} DECLARED TWICE: {', '.join(twice[:8])}")
print("   done")

print("\n" + ("ALL GOOD" if not bad else f"{bad} PROBLEM(S)"))
sys.exit(1 if bad else 0)
