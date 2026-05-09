# TODO — next prompts to give Claude

Living list of prompts the three of us (Gustavo, Jacopo, Matteo) can paste
into Claude Code to push the repo forward. Owners are starting suggestions,
not contracts — re-shuffle freely.

How to use: open Claude Code in the repo root, paste a prompt verbatim,
let it run, then tick the box and commit.

---

## Jacopo (thesis author — content & sources)

- [ ] **Fill in `docs/thesis-overview.md`.**
  > Read `docs/thesis-overview.md`. Ask me one question at a time to fill in
  > every `<...>` placeholder (field, one-sentence thesis statement, the 2–3
  > contributions, out-of-scope items, target audience, length, deadline).
  > Once we agree, write the file. Do NOT invent answers.

- [ ] **Fill in `docs/company-context.md` (NDA).**
  > Walk me through `docs/company-context.md` section by section. For the
  > "Cleared for thesis" and "NOT cleared" lists, prompt me for each item
  > and stop until I confirm. Then write the file. This gates everything
  > the writer agent can say about the internship — be conservative.

- [ ] **Seed `references/papers/` and write notes.**
  > I will drop ~10 PDFs into `references/papers/`. For each one: extract
  > the bib metadata, propose a citation key in `firstauthorlastnameYEAR`
  > form, and create a notes file under `references/notes/` from
  > `_template.md`. Do not edit `bibliography.bib` yet — the
  > citation-manager will do that once I've reviewed the notes.

- [ ] **Update title page in `thesis.tex`.**
  > Replace the placeholder title, author, supervisor, co-supervisor,
  > university, department, and academic year on the title page in
  > `thesis.tex` with the values I'll give you. Touch nothing else.

- [ ] **Draft Chapter 1 (Introduction).**
  > Use the `writer` agent to draft `chapters/01-introduction.tex`. It must
  > read `docs/thesis-overview.md` first and respect the `% HUMAN:` note
  > about chapter length and the closing roadmap. Stop after the draft —
  > do not run the professor or humanizer.

---

## Gustavo (review & quality)

- [ ] **Run a professor review on each drafted chapter.**
  > Once a chapter is drafted, invoke the `professor` agent on it. Pass the
  > chapter file path explicitly. Save the critique into a new file under
  > `docs/reviews/<chapter>-<YYYY-MM-DD>.md` so we have a record before the
  > writer revises.

- [ ] **Sanity-check the agent definitions against actual workflow.**
  > Read every file in `.claude/agents/` plus `CLAUDE.md`. Identify any
  > contradictions, dead references (e.g., `code/` is referenced but does
  > not exist yet), or steps that no agent owns. Report findings as a
  > bulleted list — do not edit the agent files yet.

- [ ] **Tighten the writer ↔ professor ↔ humanizer handoff.**
  > Based on your previous review of the agent definitions, propose
  > concrete edits to `.claude/agents/writer.md` and
  > `.claude/agents/professor.md` so the revision loop (steps 3–4 in
  > `CLAUDE.md`) is unambiguous. Show me the diff before applying.

- [ ] **Add a `style-guide.md` under `docs/`.**
  > Draft `docs/style-guide.md` covering: tense (past for experiments,
  > present for general truths), voice ("we" vs impersonal — pick one and
  > say where it applies), notation conventions (vectors, matrices, sets),
  > figure/table caption rules, and the IEEE citation style enforced by
  > `biblatex`. Then add a one-line pointer in `CLAUDE.md` so all agents
  > read it.

---

## Matteo (infrastructure & build)

- [ ] **Wire up a working LaTeX build.**
  > Verify the project builds. Run `latexmk -pdf thesis.tex` from the repo
  > root and report the full log. If it fails, diagnose and propose a fix
  > (do not silently install packages — list what is missing). Do not
  > commit `thesis.pdf`.

- [ ] **Add a `Makefile` (or `latexmkrc`) for one-command builds.**
  > Add a minimal `Makefile` with targets: `make`, `make clean`,
  > `make watch` (continuous build with `latexmk -pvc`). Match the
  > existing `.gitignore` so build artefacts stay ignored.

- [ ] **Create the `code/` folder + scaffolding referenced by the agents.**
  > The writer and professor agents both reference `code/` as
  > authoritative for system descriptions, but the folder does not exist.
  > Create `code/` with a short `README.md` explaining the layout we plan
  > to use (one subfolder per major component) and a `.gitkeep`. Update
  > `.claude/settings.json` to add a deny-rule for `Write(./code/**)` if
  > not already covered (it is — just confirm).

- [ ] **Add a CI check for citation integrity.**
  > Add a GitHub Actions workflow under `.github/workflows/cite-check.yml`
  > that runs on PRs: it should grep all `\cite{KEY}` calls in
  > `chapters/*.tex` and fail if any KEY is missing from
  > `references/bibliography.bib` or if any `% TODO-CITE:` comment is
  > present. Pure shell + grep — no LaTeX install needed.

- [ ] **Pre-commit hook for `% TODO-CITE` and unresolved placeholders.**
  > Add a `.githooks/pre-commit` script (and a one-line `make hooks`
  > target to install it) that blocks commits containing `% TODO-CITE:`,
  > `\todo{}`, or `<...>` placeholders inside `chapters/*.tex`. Document
  > the bypass (`git commit --no-verify`) in the README.

---

## Shared / unowned

- [ ] **Decide language: English vs Italian.** `CLAUDE.md` says English,
  `thesis.tex` comment says "change to italian if needed". Pick one and
  remove the other.
- [ ] **Decide whether `thesis.pdf` is committed.** `.gitignore` has it
  commented out. Choose and uncomment accordingly.
- [ ] **Add a `CONTRIBUTING.md`** describing the agent-driven workflow
  (writer → citation-manager → professor → writer → citation-verifier →
  humanizer) so a new collaborator can onboard without reading every
  agent file.
