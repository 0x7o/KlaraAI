import openai


class Claude:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=api_key
        )

    def generate(self, messages: list):
        for chunk in self.client.chat.completions.create(
            model="anthropic/claude-3-haiku", messages=messages, stream=True, temperature=1.0
        ):
            yield chunk.choices[0].delta.content


if __name__ == "__main__":
    claude = Claude(
        api_key="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"
    )

    messages = [
        {"role": "system", "content": "Hello! How can I help you today?"},
        {"role": "user", "content": "Привет!"},
    ]

    for response in claude.generate(messages):
        print(response, end="")
