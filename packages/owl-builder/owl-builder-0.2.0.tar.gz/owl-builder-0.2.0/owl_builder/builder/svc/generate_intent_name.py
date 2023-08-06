#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Use OpenAI to Generate Intent Names """


from typing import Optional
from openai_helper import chat

from baseblock import (
    BaseObject,
    Stopwatch,
    Enforcer,
)


class GenerateIntentName(BaseObject):
    """ Use OpenAI to Generate Intent Names """

    def __init__(self):
        """ Change Log

        Created:
            27-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/6
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _prompt(input_text: str) -> str:
        return """
Create intent definitions for each string.  Use the same format as the examples.  The intent definition should be 3 words delimited by underscores.

Examples:
WHAT_YOUR_DAY: What does a typical day in the life of you look like?
WHAT_YOUR_COLOR: I am curious to know which color holds a special place in your heart?
WHAT_YOUR_BOOK: What is your favorite book?
ARE_YOU_FEMALE: Are you a woman?
ARE_YOU_HUMAN: Are you human?
ARE_YOU_MALE: Are you a man?
DO_YOU_DATE: Will you go out on a date with me?
DO_YOU_FUN: What do you do for fun?
DO_YOU_NETFLIX: Do you watch Netflix?
GIVE_ME_HINT: Can you give me a hint?
PROPHESY_ME_FUTURE: What will I be when I grow up?

Input: #INPUT_TEXT""".replace('#INPUT_TEXT', input_text).strip()

    def process(self,
                input_text: str) -> Optional[str]:

        sw = Stopwatch()

        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        intent_name = chat(
            input_prompt=self._prompt(input_text),
            messages=None,
            remove_emojis=True)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Intent Naming Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tIntent Name: {intent_name}"]))

        return intent_name
