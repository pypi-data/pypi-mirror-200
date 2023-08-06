#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import (
    List,
    Optional,
)

from pandas import DataFrame

from .builder import *
from .synonyms import *
from .relationships import *

from .keyterms import *
from .keyterms.bp import AutoTaxoOrchestrator

from .builder import generate_node
from .synonyms import generate_synonyms
from .synonyms import generate_inflections

autotaxo_orchestrator = AutoTaxoOrchestrator()


def build_ttl(input: str or DataFrame) -> Optional[List[str]]:
    """ Generate TTL Results for augmenatation of OWL model

    Args:
        input (str or DataFrame): either input text or a DataFrame
            input_text:     sent to dataframe(...) method
                Sample Input:
                    A local area network (LAN) is a computer network that interconnects computers within a limited area.
            DataFrame:      must have output format equivalent to dataframe(...) method
                Sample Input:
                    +----+---------------------------+----------------------------------+
                    |    | Parent                    | Child                            |
                    |----+---------------------------+----------------------------------+
                    |  0 | circuit                   | telecommunication circuit        |
                    |  1 | telecommunication circuit | leased telecommunication circuit |
                    |  2 | technology                | network technology               |
                    +----+---------------------------+----------------------------------+

    Sample Output:
        ###  http://graffl.ai/pathology#telecommunication_circuit
                    :telecommunication_circuit rdf:type owl:Class ;
                    rdfs:label "Telecommunication Circuit" ;
                    rdfs:subClassOf :circuit .
        ###  http://graffl.ai/pathology#circuit
                    :circuit rdf:type owl:Class ;
                    rdfs:label "Circuit" .
        ###  http://graffl.ai/pathology#leased_telecommunication_circuit
                    :leased_telecommunication_circuit rdf:type owl:Class ;
                    rdfs:label "Leased Telecommunication Circuit" ;
                    rdfs:subClassOf :telecommunication_circuit .
        ...
        ###  http://graffl.ai/pathology#token_ring
                    :token_ring rdf:type owl:Class ;
                    rdfs:label "Token Ring" ;
                    rdfs:subClassOf :ring .
        ###  http://graffl.ai/pathology#ring
                    :ring rdf:type owl:Class ;
                    rdfs:label "Ring" .

    Returns:
        Optional[List[str]]: TTL results for OWL model
    """
    return autotaxo_orchestrator.build_ttl(input)


# def generate_qa_pairs(question: str,
#                       answer: str) -> str:
#     """ Generate Additional Q&A Pairs

#     Args:
#         question (str): a sample Question
#         answer (str): a sample Answer

#     Returns:
#         str: an intent name
#     """
#     return keyterms.generate_qa_pairs(
#         question=question,
#         answer=answer)


# def generate_intent_name(input_text: str) -> str:
#     """ Generate Intent Name

#     Args:
#         input_text (str): input text of any length or description

#     Returns:
#         str: an intent name
#     """
#     return keyterms.generate_intent_name(input_text)


# def generate_intent_mapping(intent_name: str,
#                             keyterms: str) -> str:
#     """ Generate a Basic Intent Mapping

#     Args:
#         intent_name (str): the intent name
#         keyterms (str): the keyterms

#     Returns:
#         str: an intent mapping
#     """

#     intent_name = f"{intent_name.upper().strip()}#1"

#     return {
#         intent_name: [
#             {
#                 'include_all_of': keyterms
#             }
#         ],
#     }


def keyterms(input_text: str,
             use_openai: bool = False,
             use_terms: bool = False,
             use_keyterms: bool = False,
             use_ngrams: bool = False,
             use_nounchunks: bool = False) -> Optional[List[str]]:
    """ Generate KeyTerms as a simple list

    Args:
        input_text (str): input text of any length or description
        use_terms (bool, optional). Use Simple Term extraction algorithms. Default is True.
        use_keyterms (bool, optional). Use KeyTerm extraction algorithms. Default is True.
        use_ngrams (bool, optional). Use n-Gram extraction algorithms. Default is False.
        use_nounchunks (bool, optional). Use Noun Chunk extraction algorithms. Default is False.

    Sample Input:
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.

    Sample Output:
        [   'leased telecommunication circuit',
            'historical network technology',
            'large geographic distance',
            'interconnects computer',
            'local area network',
            'university campus',
            'common technology',
            'wide area network',
            'computer network',
            'office building',
            'include arcnet',
            'limited area',
            'token ring'
        ]

    Returns:
        Optional[List[str]]: list of keyterms
    """

    return autotaxo_orchestrator.keyterms(
        input_text=input_text,
        use_terms=use_terms,
        use_openai=use_openai,
        use_keyterms=use_keyterms,
        use_ngrams=use_ngrams,
        use_nounchunks=use_nounchunks)
