# Contributing to Cairn

Cairn is open source (MIT) and authored by **Mohammed Nasher** ([@mhd-nasher](https://github.com/mhd-nasher)).
Contributions are welcome — Cairn gets stronger the more real-world stacks and failure modes it covers.

## Good contributions

- **New stack profiles** in `reference/stack-profiles.md` (APPLY/SUPPRESS + default boundary level).
- **Sharper guardrails** in `reference/over-engineering-guardrails.md`.
- **More evals** in `evals/` — especially new failure modes Cairn doesn't yet defend against.
- **Worked examples** in `examples/`.
- **Plain-language / translation** improvements so more beginners can use it.

## How to contribute

1. Fork [github.com/mhd-nasher/cairn](https://github.com/mhd-nasher/cairn).
2. Make your change. Keep `SKILL.md` frontmatter minimal (`name`, `description`, `license` only).
3. Follow the skill-TDD loop in `evals/README.md`: add/adjust an eval, watch it fail without your change,
   confirm it passes with it.
4. Open a pull request describing the change and the failure mode it addresses.

## Ground rules

- Keep Cairn **stack-aware** — never add a rule without saying when to suppress it.
- Honor the **Anti-Over-Engineering Law** in the docs themselves: don't add a file or section that doesn't
  earn its place.
- Be honest about scope: Cairn produces structure, not security guarantees.

By contributing, you agree your contribution is licensed under the project's [MIT License](LICENSE).
