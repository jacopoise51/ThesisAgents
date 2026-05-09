# ThesisAgents

A LaTeX thesis scaffold driven by a small team of Claude Code agents
(writer, citation-manager, professor, citation-verifier, humanizer).

The repo is intentionally minimal: a `thesis.tex` main file, skeleton
chapters, a bibliography stub, and the agent definitions that automate
the drafting/review loop.

---

## What's in the repo

```
.
├── thesis.tex              # main LaTeX file (title page + \input chapters)
├── chapters/               # one .tex per chapter (00 abstract … 06 conclusion)
├── docs/                   # framing material — read by agents, never cited
│   ├── thesis-overview.md  # field, contribution, scope, deadline
│   ├── company-context.md  # NDA-cleared internship facts
│   ├── lit-review-plan.md  # themes for chapter 2
│   └── methodology-notes.md
├── references/
│   ├── bibliography.bib    # BibTeX — owned by the citation-manager agent
│   ├── papers/             # PDFs (NOT committed yet — drop yours here)
│   └── notes/              # one note file per paper, from _template.md
├── .claude/
│   ├── agents/             # the 5 agent definitions
│   └── settings.json       # tool permissions (Read/Edit/Write scopes)
├── CLAUDE.md               # project rules every agent must follow
└── TODO.md                 # next prompts to feed Claude, by user
```

---

## Prerequisites

- A TeX distribution with `latexmk`, `biber`, and the packages listed in
  `thesis.tex` (TeX Live or MiKTeX both work).
- [Claude Code](https://claude.com/claude-code) installed and signed in.

---

## Build the PDF

From the repo root:

```bash
latexmk -pdf thesis.tex
```

Or, the long way:

```bash
pdflatex thesis.tex
biber thesis
pdflatex thesis.tex
pdflatex thesis.tex
```

Clean build artefacts:

```bash
latexmk -C
```

The PDF lands at `thesis.pdf`. Whether to commit it is undecided — see
the `.gitignore` comment.

---

## Use the agents

Open Claude Code in the repo root. The five agents in `.claude/agents/`
are loaded automatically. The intended pipeline for any section:

1. **writer** drafts the section into the chapter `.tex` file. It reads
   only `references/` and `docs/`, and inserts placeholder `\cite{KEY}`
   calls or `% TODO-CITE:` flags.
2. **citation-manager** reconciles those keys with
   `references/bibliography.bib`, adding entries when a matching paper
   exists in `references/papers/` or `references/notes/`.
3. **professor** critiques the draft on argument, rigor, structure,
   sources, code fidelity, and scope. Outputs a numbered list with
   severities.
4. **writer** revises against the critique.
5. **citation-verifier** confirms every cite resolves, every cite
   matches its claim, and no claim is missing a cite.
6. **humanizer** polishes the prose last — never before review.

You don't have to invoke them by hand; describing the task ("draft the
intro", "review chapter 3") is usually enough. Be explicit if you want
to skip a step.

---

## Hard rules (lifted from `CLAUDE.md`)

- No fabricated citations. If a claim can't be sourced from
  `references/`, flag with `% TODO-CITE:` instead.
- No internship content unless it's on the cleared list in
  `docs/company-context.md`.
- LaTeX only, not Markdown. Use the project's existing macros.
- Do not delete or rewrite any `% HUMAN:` comment in `.tex` files —
  those are author notes.

---

## Where to start

New to the repo? Read in this order:

1. `CLAUDE.md` — the rules.
2. `docs/thesis-overview.md` — what the thesis is about.
3. `docs/company-context.md` — what you can and cannot say.
4. `.claude/agents/writer.md` — the agent you'll trigger most often.
5. `TODO.md` — pick the next prompt to run.
