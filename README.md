# grammar-check

A GitHub Action that runs an LLM over your repo's `.tex` files on every push, fixes grammar and spelling, and opens a PR with the changes. Supports Claude and DeepSeek.

## Usage

Drop this into `.github/workflows/grammar.yml` in your repo:

```yaml
name: Grammar Check
on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  grammar:
    runs-on: ubuntu-latest
    steps:
      - uses: Mattschoe/grammar-check@v1
        with:
          provider: claude
          api-key: ${{ secrets.LLM_API_KEY }}
```

That's the whole consumer-side config. The action handles checkout, dependency install, running the checker, and opening the PR.

### Optional: filter to `.tex` pushes

If you'd rather not invoke the action on pushes that don't touch any `.tex` files, add a `paths` filter to the trigger:

```yaml
on:
  push:
    branches: [main]
    paths: ['**.tex']
```

The action is a no-op when there are no changed `.tex` files, so this is purely an optimization.

## Inputs

| Input      | Required | Default  | Description                                       |
|------------|----------|----------|---------------------------------------------------|
| `provider` | yes      | —        | `claude` or `deepseek`                            |
| `api-key`  | yes      | —        | API key for the chosen provider                   |
| `tier`     | no       | `medium` | `cheap`, `medium`, or `expensive` — model size    |

## Why the workflow needs a `permissions:` block

GitHub Actions does not let a composite action elevate the consumer's `GITHUB_TOKEN` on its own. The action's final step opens a PR using `gh`, which requires `contents: write` and `pull-requests: write`. Without those, you'll see a 403 from `gh pr create`. This is a platform constraint, not something the action can paper over.

## Provider notes

- **Claude** — `api-key` is your Anthropic API key. Tiers map to Haiku / Sonnet / Opus.
- **DeepSeek** — `api-key` is your DeepSeek key. `expensive` enables extended thinking.
