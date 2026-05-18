import os
import subprocess

from llm import call_claude, call_deepseek

system_prompt = """
You are a grammar and spelling checker for academic LaTeX documents.

You will receive the full content of one or more .tex files, each prefixed with === filename ===.
Your job is to:
- Fix grammar and spelling errors in prose sections only
- Never modify LaTeX commands, environments, math, citations, or references
- Never change the meaning or style of the writing, only correct clear errors
- Return corrected_files as a dict mapping each filename to its fully corrected content
- Return a concise bullet list of what you changed across all files

If there are no grammar or spelling errors, return the original content unchanged and an empty summary list.
"""

def get_changed_tex_files() -> dict[str, str]:
    changed = subprocess.run(
        args=["git", "diff", "HEAD~1", "HEAD", "--name-only", "--diff-filter=ACM", "--", "*.tex"],
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
    tex_files = get_changed_tex_files()

    if not tex_files:
        print("No .tex files changed, skipping.")
        return

    content = "\n\n".join(f"=== {name} ===\n{body}" for name, body in tex_files.items())

    if provider == "deepseek":
        result = call_deepseek(content, system_prompt)
    elif provider == "claude":
        result = call_claude(content, system_prompt)
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
