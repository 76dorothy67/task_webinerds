from typing import List


class GPTRequest:
    def __init__(
            self,
            context_base: str,
            best_summary: str,
            history: List[str],
            ai_msg_begin: str
    ):
        self.context_base = context_base
        self.best_summary = best_summary or ''
        self.history = [str(i) for i in history] or []
        self.ai_msg_begin = ai_msg_begin

    def __str__(self):
        return f'{self.context_base}' \
               f'\nCurrent conversation:' \
               f'\n{self.best_summary}\n' +\
               '\n'.join(self.history) +\
               f'\n{self.ai_msg_begin}'
