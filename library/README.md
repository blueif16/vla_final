# Library

Everything we've found that a chapter might need again: talk clips with their start times, images with their
licences, and papers and code with the numbers we've checked. Look here before searching the web, and add every new
find here the moment it's useful, so no one has to find it twice.

| File | What it holds |
|---|---|
| `clips.yaml` | Talks on YouTube, each split into sections with start times and a line on what the section covers. Which clips a chapter already embeds. Talks we found but haven't timed yet. |
| `images.yaml` | Images we've downloaded (in `docs/assets/img/`), figures we may reuse but haven't downloaded, papers whose figures we may not copy, and images we still need. |
| `environments.yaml` | Simulators, benchmarks and robots we've looked at for experiments: what each needs to run, which model we could run in it, and how close its tasks are to real life. |
| `papers.yaml` | Papers and code, with licence and the facts and numbers we've read in them. Chapters copy numbers from here. |
| `terms-zh.yaml` | The Chinese term shown next to each glossary concept, the other forms people use where usage splits, and where we checked them. |

The glossary that every web chapter shares is `docs/assets/js/glossary.js`; add a term there once and every chapter
can use it.

How the pages are built, and how to find clip times and check licences, is in the `teaching-web` skill
(`.claude/skills/teaching-web/`).
