#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate an Ontology Graph Node in TTL Format """


from typing import List
from typing import Optional
from functools import partial

from datetime import datetime
from baseblock import BaseObject
from baseblock import TextUtils

from owl_builder.synonyms.svc import GenerateEnglishSynonyms
from owl_builder.synonyms.svc import GenerateEnglishInflections

from rdflib.graph import Graph
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS, XSD


class GenerateTTLNode(BaseObject):
    """ Generate an Ontology Graph Node in TTL Format """

    def __init__(self,
                 model_name: str = "gpt-4"):
        """ Change Log

        Created:
            28-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/8

        model_name (str, optional). defaults to "GPT-4"
        """
        BaseObject.__init__(self, __name__)
        self._model_name = model_name

        self._generate_synonyms = partial(
            GenerateEnglishSynonyms().process,
            desired_synonym_size="trigram")

        self._generate_inflections = partial(
            GenerateEnglishInflections().process,
            model=self._model_name)

    @staticmethod
    def _to_identifier(entity_name: str) -> str:

        entity_name = entity_name.upper().strip()
        entity_name = entity_name.replace(' ', '_')

        for item in ["'"]:
            entity_name = entity_name.replace(item, "").strip()

        return entity_name

    def _version(self) -> str:
        text = "Generated on #TIME using #MODEL"

        text = text.replace('#TIME', str(datetime.now())[:-10])
        text = text.replace('#MODEL', self._model_name.upper().strip())

        return text

    def _synonyms(self,
                  entity_name: str,
                  entity_context: Optional[str] = None) -> Optional[List[str]]:

        master = set()

        def update(results: Optional[List[str]]):
            if results:
                [master.add(x) for x in results]

        update(self._generate_synonyms(
            entity_name=entity_name,
            entity_context=entity_context))

        update(self._generate_inflections(
            input_text=entity_name))

        if not len(master):
            return None

        return sorted(master, key=len, reverse=True)

    def process(self,
                entity_name: str,
                entity_context: Optional[str] = None,
                namespace: Optional[str] = "http://graffl.ai/test") -> str:

        entity_id = self._to_identifier(entity_name)
        entity_label = TextUtils.title_case(entity_name)

        g = Graph()

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            RDF.type,
            OWL.Class
        ))

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            RDFS.label,
            Literal(entity_label, datatype=XSD.string)
        ))

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            OWL.versionInfo,
            Literal(self._version(), datatype=XSD.string)
        ))

        synonyms = self._synonyms(
            entity_name=entity_name,
            entity_context=entity_context)

        if synonyms and len(synonyms):
            for synonym in synonyms:
                g.add((
                    URIRef(f"{namespace}/{entity_id}"),
                    RDFS.seeAlso,
                    Literal(synonym, datatype=XSD.string)
                ))

        result = g.serialize(format="turtle")

        normalized = [
            f"### {namespace}/{entity_id}"
        ]

        lines = result.split('\n')

        lines = [
            line.strip() for line in lines
            if line and len(line)
        ]

        lines = [
            line for line in lines
            if not line.startswith('@prefix')
        ]

        for line in lines:

            if line.startswith('<http:'):
                line = f":{entity_label} rdf:type owl:Class ;"

            if line.startswith("rdfs:") or line.startswith("owl:"):
                line = f"  {line}"
            elif line.startswith('"'):
                line = f"     {line}"

            normalized.append(line)

        return '\n'.join(normalized)
