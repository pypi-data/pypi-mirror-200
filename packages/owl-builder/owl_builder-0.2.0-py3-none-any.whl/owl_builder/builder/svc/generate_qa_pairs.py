#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate Additional QA Pairs from a Given Example """


from functools import lru_cache
from typing import List

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from openai_helper import chat


class GenerateQAPairs(BaseObject):
    """ Generate Additional QA Pairs from a Given Example """

    def __init__(self):
        """
        Created:
            28-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/5
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    @lru_cache
    def _prompt(question: str,
                answer: str) -> str:
        prompt = """I will give you a question and answer pair.  Please generate 10 more.  You may rephrase both the Question and the Answer, but don't change the meaning of either the Question or the Answer.
----------------------------------
Question: #QUESTION
Answer: #ANSWER
----------------------------------""".strip()

        prompt = prompt.replace('#QUESTION', question)
        prompt = prompt.replace('#ANSWER', answer)

        return prompt

    def process(self,
                question: str,
                answer: str) -> List[str]:

        sw = Stopwatch()

        if self.isEnabledForDebug:
            Enforcer.is_str(question)
            Enforcer.is_str(answer)

        results = chat(
            input_prompt=self._prompt(
                question=question,
                answer=answer),
            messages=None,
            remove_emojis=True)

        qa_pairs = [
            x for x in results.split('Question:')
            if x and len(x)
        ]

        qa_pairs = [
            [
                y.strip() for y in x.split('Answer:')
                if y and len(y)
            ]
            for x in qa_pairs
        ]

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "QA Pair Generation Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tQA Pairs: {qa_pairs}"]))

        return qa_pairs
