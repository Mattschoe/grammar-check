import subprocess

from llm import call_claude

system_prompt = """
You are a grammar and spelling checker for academic LaTeX documents.

You will receive a git diff of .tex files. Your job is to:
- Fix grammar and spelling errors in prose sections only
- Never modify LaTeX commands, environments, math, citations, or references
- Never change the meaning or style of the writing, only correct clear errors
- Return the fully corrected file content and a concise bullet list of what you changed

If there are no grammar or spelling errors, return the original content unchanged and an empty summary list.
"""

def get_diff() -> str:
    """
    :return: the diff from the latest commit.
    """
    return subprocess.run(
        args=["git", "diff", "HEAD~1", "HEAD", "--", "*.tex"],
        capture_output=True,
        text=True
    ).stdout

def main():
    diff = get_diff()
    result = call_claude(diff, system_prompt)
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
