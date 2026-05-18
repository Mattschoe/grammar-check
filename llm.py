import json
import os
from dataclasses import dataclass
from typing import cast

import anthropic
from openai import OpenAI

@dataclass
class Response:
    corrected_files: dict
    summary: list[str]

_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "corrected_files": {"type": "object"},
        "summary": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["corrected_files", "summary"]
}

def call_claude(unedited_text: str, system_prompt: str) -> Response:
    tools = [{
        "name": "submit_grammar_fixes",
        "description": "Submit the grammar fixes and summary",
        "input_schema": _TOOL_SCHEMA
    }]
    api_key = os.environ["LLM_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-opus-4-7",
        tools=tools,
        system=system_prompt,
        tool_choice={"type": "tool", "name": "submit_grammar_fixes"},
        messages=[{"role": "user", "content": unedited_text}]
    )

    result = response.content[0].input
    return Response(
        corrected_files=cast(dict, result["corrected_files"]),
        summary=cast(list[str], result["summary"])
    )

def call_deepseek(unedited_text: str, system_prompt: str) -> Response:
    tools = [{
        "type": "function",
        "function": {
            "name": "submit_grammar_fixes",
            "description": "Submit the grammar fixes and summary",
            "parameters": _TOOL_SCHEMA
        }
    }]
    api_key = os.environ["LLM_API_KEY"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "submit_grammar_fixes"}},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": unedited_text}
        ]
    )

    result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    return Response(
        corrected_files=cast(dict, result["corrected_files"]),
        summary=cast(list[str], result["summary"])
    )
