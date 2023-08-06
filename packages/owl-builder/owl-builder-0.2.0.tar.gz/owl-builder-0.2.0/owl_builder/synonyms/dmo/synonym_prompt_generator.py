#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate Synonym Prompts """


from typing import Optional

from baseblock import BaseObject

from openai_helper import chat

from owl_builder.synonyms.dto import OpenAICache


class SynonymPromptGenerator(BaseObject):
    """ Generate Synonym Prompts """

    def __init__(self):
        """
        Created:
            29-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/10
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                entity_name: str,
                entity_context: Optional[str] = None,
                desired_synonym_size: Optional[str] = None) -> str:

        prompt_1 = f"Generate all the near English synonyms for '{entity_name}'"

        if not entity_context and not desired_synonym_size:
            return f"{prompt_1}."

        prompt_2 = f"where the synonym would make sense in the context '{entity_context}'."

        if entity_context and not desired_synonym_size:
            return f"{prompt_1} {prompt_2}"

        def get_size_prompt() -> str:

            if desired_synonym_size == 'unigram':
                return "Each synonym must be a unigram."

            if desired_synonym_size == 'bigram':
                return "Each synonym must be a bigram or smaller."

            if desired_synonym_size == 'trigram':
                return "Each synonym must be a trigram or smaller."

            raise NotImplementedError(desired_synonym_size)

        prompt_3 = get_size_prompt()

        if not entity_context and desired_synonym_size:
            return f"{prompt_1}. {prompt_3}"

        return f"{prompt_1} {prompt_2} {prompt_3}"
