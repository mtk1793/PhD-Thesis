#!/usr/bin/env python3
"""Render LaTeX equations (matplotlib mathtext) to high-resolution PNGs for the thesis docx."""
import os, re, sys, glob, json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CACHE = os.path.join(os.path.dirname(__file__), "..", "eq_cache")
os.makedirs(CACHE, exist_ok=True)

# Replacements to make raw agent LaTeX mathtext-compatible
REPLACEMENTS = [
    (r"\\mathrm", r"\\mathdefault"),   # mathtext has no \mathrm
    (r"\\displaystyle", ""),
    (r"\\left", ""), (r"\\right", ""),
    (r"\\quad", r"\\;\\;"), (r"\\qquad", r"\\;\\;\\;\\;"),
    (r"\\operatorname\{([a-zA-Z]*)\}", r"\\mathdefault{\\mathrm{\\1}}"),
    (r"\\top", r"T"),
    (r"\\le([^a-zA-Z])", r"\\leq\1"), (r"\\ge([^a-zA-Z])", r"\\geq\1"),
    (r"\\iff", r"\;\\Leftrightarrow\;"), (r"\\implies", r"\;\\Rightarrow\;"),
    (r"\\prec", r"\\precq") if False else (r"\\wedge", r"\\;\\mathrm{and}\\;"),
    (r"\\le$", r"\\leq"), (r"\\ge$", r"\\geq"),
    (r"\\argmin", r"\\mathrm{arg\\,min}"),
    (r"\\argmax", r"\\mathrm{arg\\,max}"),
    (r"\\text\{([^}]*)\}", r"\\mathrm{\\1}"),
    (r"\\!{", "{"), (r"\\!", ""),
    (r"\\;\\;\\;\\;\\;\\;\\;\\;", r"\\;\\;\\;\\;"),
]

def sanitize(latex: str) -> str:
    s = latex.strip().rstrip(",").strip()
    s = s.replace(r"^\top", "^{T}")
    for a, b in REPLACEMENTS:
        s = re.sub(a, b, s)
    # remove unsupported unicode
    s = s.replace("⟨", r"\langle ").replace("⟩", r"\rangle ")
    s = s.replace("−", "-").replace("–", "-")
    return s

def render(latex: str, tag: str, dpi: int = 400) -> str:
    """Render one equation; return path to PNG. Raises on failure."""
    s = sanitize(latex)
    fig = plt.figure(figsize=(0.1, 0.1))
    txt = fig.text(0, 0, f"${s}$", fontsize=13)
    path = os.path.join(CACHE, f"eq_{tag}.png")
    try:
        fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.04, facecolor="white")
    except Exception as e:
        plt.close(fig)
        raise RuntimeError(f"mathtext failed for {tag}: {e}\nLaTeX: {s}")
    plt.close(fig)
    return path

def eq_fences(md_path: str):
    """Yield (number, latex) pairs from a markdown file."""
    text = open(md_path, encoding="utf-8").read()
    # strip ONLY plain/text code fences so ```text blocks with # comments are ignored
    text = re.sub(r"```text\n.*?\n```", "", text, flags=re.S)
    for m in re.finditer(r"```eq\n%%([\d\.]+)\n(.*?)\n```", text, flags=re.S):
        yield m.group(1), m.group(2).strip()

def main():
    chapters = sorted(
        glob.glob(os.path.join(os.path.dirname(__file__), "..", "chapters_md", "*.md"))
    )
    failures, ok = [], 0
    for ch in chapters:
        for num, latex in eq_fences(ch):
            tag = num.replace(".", "_")
            try:
                render(latex, tag)
                ok += 1
            except Exception as e:
                failures.append((num, str(e)[:200]))
    print(f"rendered {ok} equations, {len(failures)} failures")
    for num, err in failures:
        print("FAIL", num, err)
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
