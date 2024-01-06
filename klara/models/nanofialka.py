from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class NanoFialka:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("0x7194633/nanoFialka-v1")
        self.model = AutoModelForCausalLM.from_pretrained("0x7194633/nanoFialka-v1")

    def generate(self, messages, repetition_penalty=1.1, temperature=0.7):
        first_message = messages[0]
        last_messages = messages[-10:]
        first_message_tokens = self.tokenizer.encode(f"<|{first_message['role']}|>\n{first_message['content']}</s>\n")
        last_messages_tokens = [self.tokenizer.encode(f"<|{message['role']}|>\n{message['content']}</s>\n") for message
                                in last_messages]
        total_tokens = len(first_message_tokens) + sum(len(tokens) for tokens in last_messages_tokens)
        while total_tokens > 1500:
            last_messages_tokens.pop(0)
            total_tokens = len(first_message_tokens) + sum(len(tokens) for tokens in last_messages_tokens)
        prompt = self.tokenizer.decode(first_message_tokens)
        for tokens in last_messages_tokens:
            prompt += self.tokenizer.decode(tokens)
        prompt += "<|assistant|>\n"
        input_tokens = self.tokenizer.encode(prompt, return_tensors='pt')
        with torch.no_grad():
            output_tokens = self.model.generate(input_tokens, max_length=512, do_sample=True,
                                                repetition_penalty=repetition_penalty, temperature=temperature)
        return self.tokenizer.decode(output_tokens[0]).replace(prompt, "").replace("</s>", "")

