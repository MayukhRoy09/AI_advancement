"""
RAG Pipeline Module

Handles:
1. Formatting retrieved attendance information into context.
2. Sending prompts to Anthropic Claude.
"""

import anthropic

import config


def build_context_block(results) -> str:
    """
    Convert knowledge base results into a text context block.

    Args:
        results: Retrieved data from knowledge_base.py

    Returns:
        Formatted context string for the LLM.
    """

    if not results:
        return "No relevant attendance information found."

    context_parts = []

    # Handle dictionary-based retrieval results
    if isinstance(results, dict):

        documents = results.get("documents", [])

        if documents:
            for document in documents:

                if isinstance(document, list):
                    context_parts.extend(document)

                else:
                    context_parts.append(str(document))

    # Handle list-based retrieval results
    elif isinstance(results, list):

        for item in results:
            context_parts.append(str(item))

    # Handle plain text results
    else:
        context_parts.append(str(results))

    return "\n\n".join(context_parts)


def _call_llm(prompt: str) -> str:
    """
    Send a prompt to Anthropic Claude.

    Args:
        prompt: Final AI prompt containing attendance context.

    Returns:
        Claude generated response.
    """

    if not config.ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY is missing. "
            "Add it to your .env file."
        )

    client = anthropic.Anthropic(
        api_key=config.ANTHROPIC_API_KEY
    )

    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=1000,
        system="""
You are an AI assistant for an attendance tracker system.

Rules:
- Answer only using the provided attendance context.
- Do not create fake attendance records.
- If information is unavailable, say that it is not available.
- Keep answers clear and concise.
""",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.content[0].text
