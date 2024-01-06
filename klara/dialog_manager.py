from .models.nanofialka import NanoFialka


class DialogManager:
    def __init__(self, model: NanoFialka, system_prompt=None):
        self.system_prompt = system_prompt
        if not self.system_prompt:
            self.system_prompt = ("Ты являешься - Клара, самый дружелюбный и общительный голосовой помощник, который "
                                  "любит общаться со своим пользователем. Общайся с пользователем и представляйся "
                                  "Кларой.")
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.model = model

    def get_response(self, user):
        self.messages.append({"role": "user", "content": user})
        assistant = self.model.generate(self.messages)
        self.messages.append({"role": "assistant", "content": assistant})
        return assistant
