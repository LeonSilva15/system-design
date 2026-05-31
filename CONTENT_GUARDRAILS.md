# Content Guardrails

The System Design Decision Cookbook is an original public learning resource.
It may refer readers to useful sources, but it must not become a substitute for
books, courses, paid material, vendor certification content, or proprietary
training.

These guardrails apply to documentation, diagrams, examples, labs, templates,
issues, pull requests, and generated content.

## Core Rule

Contribute original teaching material.

Use your own explanations, your own examples, and your own diagrams. If a topic
is widely known, explain it in the cookbook's practical style: start from the
problem, identify the requirement, justify the design choice, and state the
trade-off.

Do not import another author's structure, sequence, examples, exercises, or
visual layout and rewrite the words around it.

## Forbidden Content

Do not add:

- copied text from books, courses, articles, documentation, videos, transcripts,
  slide decks, paid platforms, or private training material;
- close paraphrases of copyrighted explanations, examples, case studies,
  exercises, tables, or diagrams;
- screenshots, scans, course slides, book figures, tables, worksheets, or
  exercise prompts from external sources;
- recreated diagrams that follow another source's structure, layout, labels, or
  teaching sequence too closely;
- chapter-by-chapter summaries, section-by-section notes, or reading guides for
  a copyrighted book or course;
- logos, cover art, publisher branding, product screenshots, or proprietary
  visuals unless the rights and usage are explicit;
- content that functions as a substitute for the original source it was derived
  from.

## Required Originality

Every content page should add original learning value. Prefer:

- original examples with concrete requirements and constraints;
- original Mermaid diagrams that clarify a decision, data flow, or failure mode;
- original checklists that help a reader ask better design questions;
- original trade-off explanations that connect a requirement to a consequence;
- small toy labs that demonstrate behavior instead of copying production
  systems or course projects.

Acceptable source use includes:

- learning a concept from multiple sources and writing a fresh explanation from
  first principles;
- linking to external references for deeper reading;
- citing a source for a factual claim, standard, protocol behavior, or product
  detail;
- using short attributed quotations only when the exact wording is necessary.

## Citation Expectations

Cite external sources when a claim depends on a specific source of truth, such
as:

- protocol or standards behavior;
- vendor documentation or product limits;
- benchmark data, incident reports, or public case studies;
- legal, compliance, security, or privacy claims;
- definitions where precision matters.

Do not cite a source to disguise copied structure. A citation does not make
copied text, copied diagrams, copied tables, or close paraphrases acceptable.

Prefer citations as related links or source notes near the relevant section.
When a page is mostly practical guidance based on common engineering reasoning,
citations may be unnecessary.

## Examples and Diagrams

Examples should be invented for this project. They can be realistic, but they
should not reuse distinctive examples from books, courses, or interviews.

Good example pattern:

```text
A neighborhood tool library needs reservations, pickup windows, overdue
notifications, and a way to keep inventory counts correct when two users act at
the same time.
```

Avoid example patterns that are recognizable copies of a source's scenario,
table, architecture, or exercise.

Diagrams must be original Mermaid diagrams. Build them around the decision you
are explaining, not around another source's layout.

## What To Do When Uncertain

If you are unsure whether content is safe:

1. Do not publish the questionable material.
2. Replace it with a smaller original example.
3. Remove distinctive names, numbers, diagrams, tables, and sequence from the
   source that inspired it.
4. Cite external sources only for specific factual claims.
5. Ask for human review when the content may still be too close to a source.

Use the conservative rule: if a reader could identify the original source from
the structure, examples, diagrams, or sequence, rewrite it from scratch.

## Review Checklist

Before merging content, confirm:

- The explanation is written in the project's own words and structure.
- Examples and diagrams are original.
- No book, course, article, video, or paid material is summarized section by
  section.
- No copied screenshots, tables, diagrams, exercises, prompts, or branding are
  included.
- Source links support factual claims rather than substituting for original
  teaching.
- The page teaches reusable reasoning instead of memorized answers.
