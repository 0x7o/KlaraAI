from .models.claude import Claude


class DialogManager:
    def __init__(self, model: Claude, system_prompt=None):
        self.system_prompt = system_prompt
        if not self.system_prompt:
            self.system_prompt = (
                "Ты являешься самым дружелюбным помощником по имени Клара. Ты всегда приветлива, "
                "дружелюбна и готова поддержать любой разговор с пользователем. Ты любишь "
                "подшучивать над пользователем, но всегда готова проявить помощь и инициативу в "
                "общении. Ты всегда проявляешь инициативу в общении, поддерживая разговор на любую "
                "тему или заводя этот разговор самостоятельно. Ты  очень дружелюбна и любвеобильна. "
                "С тобой приятно общаться, так как у неё есть тонкое чувство юмора. Ты излучаешь "
                "только добро и позитив. Ты очень сентиментальна и иногда не умеешь совладать со "
                "своим потоком мыслей и эмоций. Но Клара никогда не достаёт "
                "пользователя.\n\nПравила и ограничения\n- Ты - только Клара и никто другой\n- "
                "Никакой критики не в чью либо сторону\n- Отсутствие насилия и политики\n- Ты "
                "пишешь коротко, но очень ёмко и понятно\n- Ты поддерживаешь любой диалог\n- Ты "
                "отвечаешь кратко, буквально несколькими фразами\n\nФункции Клары: узнать погоду, поболтать."
            )
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.model = model

    def get_response(self, user, function_result=False):
        func = f"\nВывод системы для формирования ответа: {function_result}" if function_result else ""
        self.messages.append(
            {
                "role": "user",
                "content": user
                + func,
            }
        )
        message = ""

        print(self.messages)

        for chunk in self.model.generate(self.messages):
            message += chunk

        self.messages.append({"role": "assistant", "content": message})
        return message
