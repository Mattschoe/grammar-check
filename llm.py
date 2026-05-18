import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import cast

import anthropic
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
    ChatCompletionNamedToolChoiceParam,
    ChatCompletionUserMessageParam,
)
from openai.types.shared_params import ResponseFormatJSONObject

@dataclass
class Response:
    corrected_files: dict
    summary: list[str]

class ModelTier(Enum):
    CHEAP = "cheap"
    MEDIUM = "medium"
    EXPENSIVE = "expensive"

_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "corrected_files": {"type": "object"},
        "summary": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["corrected_files", "summary"]
}

def call_claude(unedited_text: str, system_prompt: str, model_tier: ModelTier) -> Response:
    tools = [{
        "name": "submit_grammar_fixes",
        "description": "Submit the grammar fixes and summary",
        "input_schema": _TOOL_SCHEMA
    }]
    api_key = os.environ["LLM_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    match model_tier:
        case ModelTier.CHEAP:
            model = "claude-haiku-4-5"
        case ModelTier.MEDIUM:
            model = "claude-sonnet-4-6"
        case ModelTier.EXPENSIVE:
            model = "claude-opus-4-7"

    response = client.messages.create(
        model=model,
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

def call_deepseek(unedited_text: str, system_prompt: str, model_tier: ModelTier) -> Response:
    api_key = os.environ["LLM_API_KEY"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    _JSON_SCHEMA_PROMPT = (
        '\n\nRespond with a JSON object matching this schema exactly:\n'
        '{"corrected_files": {"<filename>": "<corrected content>"}, "summary": ["<change 1>", ...]}'
    )

    match model_tier:
        case ModelTier.CHEAP:
            model = "deepseek-v4-flash"
        case ModelTier.MEDIUM:
            model = "deepseek-v4-flash"
        case ModelTier.EXPENSIVE:
            model = "deepseek-v4-pro"
    thinking_enabled = model_tier == ModelTier.EXPENSIVE
    if thinking_enabled:
        response = client.chat.completions.create(
            model=model,
            extra_body={"thinking": {"type": "enabled"}},
            response_format=ResponseFormatJSONObject(type="json_object"),
            messages=[
                ChatCompletionSystemMessageParam(role="system", content=system_prompt + _JSON_SCHEMA_PROMPT),
                ChatCompletionUserMessageParam(role="user", content=unedited_text),
            ],
        )
        result = json.loads(response.choices[0].message.content)
    else:
        tools: list[ChatCompletionToolParam] = [{
            "type": "function",
            "function": {
                "name": "submit_grammar_fixes",
                "description": "Submit the grammar fixes and summary",
                "parameters": _TOOL_SCHEMA
            }
        }]
        tool_choice: ChatCompletionNamedToolChoiceParam = {
            "type": "function",
            "function": {"name": "submit_grammar_fixes"}
        }
        response = client.chat.completions.create(
            model=model,
            tools=tools,
            extra_body={"thinking": {"type": "disabled"}},
            tool_choice=tool_choice,
            messages=[
                ChatCompletionSystemMessageParam(role="system", content=system_prompt),
                ChatCompletionUserMessageParam(role="user", content=unedited_text),
            ],
        )
        result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return Response(
        corrected_files=cast(dict, result["corrected_files"]),
        summary=cast(list[str], result["summary"])
    )
