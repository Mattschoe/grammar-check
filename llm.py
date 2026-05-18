import os
from dataclasses import dataclass
from typing import cast

import anthropic

@dataclass
class Response:
    corrected_files: dict
    summary: list[str]

def call_claude(unedited_text: str, system_prompt: str) -> Response:
    """
    :param unedited_text: The unedited text that Claude should grammar check
    :param system_prompt: The system prompt given to Claude
    :return: the edited text corrected for grammar.
    """
    tools = [{
        "name": "submit_grammar_fixes",
        "description": "Submit the grammar fixes and summary",
        "input_schema": {
            "type": "object",
            "properties": {
                "corrected_files": {"type": "object"},
                "summary": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["corrected_files", "summary"]
        }
    }]
    model="claude-opus-4-7"
    api_key = os.environ["LLM_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        tools=tools,
        system=system_prompt,
        tool_choice={"type": "tool", "name": "submit_grammar_fixes"}, #Forces Claude to use this tool
        messages=[
            {"role": "user", "content": unedited_text}
        ]
    )

    result = response.content[0].input
    return Response(
        corrected_files=cast(dict, result["corrected_content"]),
        summary=cast(list[str], result["summary"])
    )
