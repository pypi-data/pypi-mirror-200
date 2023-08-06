from typing import List

import openai

from ai_git_commit.config import ICommitMessage
from ai_git_commit.prompts import prompts

openai.api_key = ""


def generate_commit_messages(
    diff: str,
    num_of_commit_messages: int = 1,
    model: str = "text-davinci-002",
    max_tokens: int = 1024,
    max_retries: int = 3,
    retry_delay: int = 500,
):
    if len(diff) == 0:
        raise ValueError("No diff provided")

    selected_prompt = prompts[5]
    prompt = selected_prompt["prompt"](
        diff=diff, num_of_commit_messages=num_of_commit_messages
    )

    for current_retry in range(max_retries, 0, -1):
        response = openai.Completion.create(
            engine=model, prompt=prompt, max_tokens=max_tokens, temperature=0.35
        )
        return response
