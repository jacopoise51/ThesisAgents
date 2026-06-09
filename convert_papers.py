#!/usr/bin/env python3
"""Convert PDF papers to Markdown using markitdown.

Usage:
    python convert_papers.py [--papers-dir PATH] [--notes-dir PATH] [--force]

LLM for OCR is configured via .env (LLM + LLM_MODEL + the matching API key).
The --llm flag overrides the model name from .env if needed.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def build_converter(model_override: str | None):
    from markitdown import MarkItDown

    provider = os.environ.get("LLM", "").strip().lower()
    model = model_override or os.environ.get("LLM_MODEL", "").strip()

    if not provider or not model:
        return MarkItDown()

    try:
        import openai
    except ImportError:
        print("WARNING: openai package not installed. Falling back to no-LLM mode.", file=sys.stderr)
        return MarkItDown()

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            print("WARNING: LLM=gemini but GEMINI_API_KEY is not set in .env. Falling back to no-LLM mode.", file=sys.stderr)
            return MarkItDown()
        client = openai.OpenAI(api_key=api_key, base_url=GEMINI_BASE_URL)
        print(f"Using Gemini model: {model}")

    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            print("WARNING: LLM=openai but OPENAI_API_KEY is not set in .env. Falling back to no-LLM mode.", file=sys.stderr)
            return MarkItDown()
        client = openai.OpenAI(api_key=api_key)
        print(f"Using OpenAI model: {model}")

    else:
        print(f"WARNING: Unknown LLM provider '{provider}' in .env (expected 'gemini' or 'openai'). Falling back to no-LLM mode.", file=sys.stderr)
        return MarkItDown()

    return MarkItDown(llm_client=client, llm_model=model)


def convert_papers(papers_dir: Path, notes_dir: Path, model_override: str | None, force: bool):
    pdfs = sorted(papers_dir.glob("*.pdf"))

    if not pdfs:
        print(f"No PDF files found in {papers_dir}")
        return

    notes_dir.mkdir(parents=True, exist_ok=True)
    md = build_converter(model_override)

    skipped = 0
    converted = 0
    failed = 0

    for pdf in pdfs:
        out = notes_dir / (pdf.stem + ".md")

        if out.exists() and not force:
            skipped += 1
            continue

        print(f"Converting: {pdf.name} ...", end=" ", flush=True)
        try:
            result = md.convert(str(pdf))
            out.write_text(result.text_content, encoding="utf-8")
            print("done")
            converted += 1
        except Exception as exc:
            print(f"FAILED ({exc})")
            failed += 1

    total = len(pdfs)
    print(
        f"\nDone. {converted} converted, {skipped} skipped (already exist), "
        f"{failed} failed — {total} total PDFs."
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--papers-dir",
        type=Path,
        default=Path("references/papers"),
        help="Directory containing PDF files (default: references/papers)",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=Path("references/md"),
        help="Output directory for .md files (default: references/md)",
    )
    parser.add_argument(
        "--llm",
        metavar="MODEL",
        default=None,
        help="Override the LLM_MODEL from .env for this run",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-convert files even if .md already exists",
    )
    args = parser.parse_args()

    if not args.papers_dir.is_dir():
        print(f"Error: papers directory not found: {args.papers_dir}", file=sys.stderr)
        sys.exit(1)

    convert_papers(args.papers_dir, args.notes_dir, args.llm, args.force)


if __name__ == "__main__":
    main()
