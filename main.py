import os
import subprocess

from llm import call_claude, call_deepseek, ModelTier

system_prompt = """
You are a grammar and spelling checker for prose documents.

You will receive the full content of one or more files, each prefixed with === filename ===.
Your job is to:
- Fix grammar and spelling errors in prose only
- Never modify markup, commands, code, math, citations, or references (e.g. LaTeX commands and environments, Markdown syntax, code blocks, inline code)
- Never change the meaning or style of the writing, only correct clear errors
- Return corrected_files as a dict mapping each filename to its fully corrected content
- Return a concise bullet list of what you changed across all files

If there are no grammar or spelling errors, return the original content unchanged and an empty summary list.
"""


def parse_globs() -> list[str]:
    raw = os.environ["FILE_EXTENSIONS"]
    globs = [f"*.{ext.strip().lstrip('.')}" for ext in raw.split(",") if ext.strip().lstrip(".")]
    if not globs:
        raise ValueError(f"FILE_EXTENSIONS must list at least one extension, got: {raw!r}")
    return globs


def get_changed_files() -> dict[str, str]:
    before = os.environ["BEFORE_SHA"]
    after = os.environ["AFTER_SHA"]
    globs = parse_globs()
    changed = subprocess.run(
        args=["git", "diff", before, after, "--name-only", "--diff-filter=ACM", "--", *globs],
        capture_output=True,
        text=True
    ).stdout.strip()

    if not changed:
        return {}

    files = {}
    for path in changed.splitlines():
        with open(path) as f:
            files[path] = f.read()
    return files

def main():
    provider = os.environ["LLM_PROVIDER"]
    model_tier = ModelTier(os.environ.get("LLM_TIER", "").strip().lower() or "medium")
    files = get_changed_files()

    if not files:
        print("No matching files changed, skipping.")
        return

    content = "\n\n".join(f"=== {name} ===\n{body}" for name, body in files.items())

    if provider == "deepseek":
        result = call_deepseek(content, system_prompt, model_tier)
    elif provider == "claude":
        result = call_claude(content, system_prompt, model_tier)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider!r}")
    print(result)

    if not result.summary:
        print("No grammar issues found, skipping PR.")
        return

    #Write files to disk
    for filename, content in result.corrected_files.items():
        with open(filename, "w") as file:
            file.write(content)

    #Write PR description
    with open("pr_description.md", "w") as file:
        file.write("## Grammar Fixes\n\n")
        file.write("\n".join(f"- {point}" for point in result.summary))


if __name__ == "__main__":
    main()
