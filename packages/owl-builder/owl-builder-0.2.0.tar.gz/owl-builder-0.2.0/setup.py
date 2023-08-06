# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owl_builder',
 'owl_builder.builder',
 'owl_builder.builder.dmo',
 'owl_builder.builder.svc',
 'owl_builder.keyterms',
 'owl_builder.keyterms.bp',
 'owl_builder.keyterms.dmo',
 'owl_builder.keyterms.dto',
 'owl_builder.keyterms.svc',
 'owl_builder.recipes',
 'owl_builder.relationships',
 'owl_builder.relationships.bp',
 'owl_builder.relationships.svc',
 'owl_builder.synonyms',
 'owl_builder.synonyms.bp',
 'owl_builder.synonyms.dmo',
 'owl_builder.synonyms.dto',
 'owl_builder.synonyms.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock',
 'networkx==2.8.8',
 'nltk==3.8.1',
 'openai>=0.27.0,<0.28.0',
 'openai_helper',
 'pandas>=1.4.0,<2.0.0',
 'rdflib>=6.1.1,<7.0.0',
 'regex==2022.7.9',
 'scipy==1.9.2',
 'spacy==3.5.0',
 'tabulate',
 'textacy==0.12.0',
 'textblob>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'owl-builder',
    'version': '0.2.0',
    'description': 'Tools for Automating the Construction of an Ontology (OWL)',
    'long_description': '# Ontology Builder (owl-builder)\n\n##\n\n## Key Term Extraction\n```python\nfrom owl_builder import keyterms\n\ninput_text = """\nA local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.\n\nBy contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.\n\nEthernet and Wi-Fi are the two most common technologies in use for local area networks.\n\nHistorical network technologies include ARCNET, Token Ring, and AppleTalk.\n"""\n\nresults = keyterms(\n    input_text=input_text,\n    use_openai=False,\n    use_terms=True,\n    use_keyterms=True,\n    use_ngrams=False,\n    use_nounchunks=False)\n```\n\nThe results are\n```json\n[\n   "leased telecommunication circuit",\n   "historical network technology",\n   "large geographic distance",\n   "interconnects computer",\n   "local area network",\n   "university campus",\n   "common technology",\n   "wide area network",\n   "computer network",\n   "office building",\n   "include arcnet",\n   "limited area",\n   "token ring"\n]\n```\n\nIf `use_openai` is set to `True`, then the following environment variables must be set:\n```python\nos.environ[\'USE_OPENAI\'] = "True"\nos.environ[\'OPENAI_KEY\'] = "<openai-key>"\nos.environ[\'OPENAI_ORG\'] = "<openai-org>"\n```\n\n## TTL Generation\n```python\nfrom owl_builder import build_ttl\n\nresults = build_ttl("He has aims to make Detroit a leader in green energy.")\n```\n\nThe result is\n```ttl\n###  http://graffl.ai/pathology#green_energy\n        :green_energy rdf:type owl:Class ;\n        rdfs:label "Green Energy" ;\n        rdfs:subClassOf :energy .\n###  http://graffl.ai/pathology#energy\n        :energy rdf:type owl:Class ;\n        rdfs:label "Energy" .\n```\n\nYou can also supply your own taxonomy like this:\n```python\nimport pandas as pd\n\nresults = build_ttl(pd.DataFrame([\n    {"Parent": "Alpha", "Child": "Alpha Beta"},\n    {"Parent": "Alpha Beta", "Child": "Alpha Beta Gamma"},\n    {"Parent": "Gamma", "Child": "Gamma Delta"},\n]))\n```\n\nThe result is\n```ttl\n###  http://graffl.ai/pathology#alpha_beta\n        :alpha_beta rdf:type owl:Class ;\n        rdfs:label "Alpha Beta" ;\n        rdfs:subClassOf :alpha .\n###  http://graffl.ai/pathology#alpha\n            :alpha rdf:type owl:Class ;\n            rdfs:label "Alpha" .\n###  http://graffl.ai/pathology#alpha_beta_gamma\n            :alpha_beta_gamma rdf:type owl:Class ;\n            rdfs:label "Alpha Beta Gamma" ;\n            rdfs:subClassOf :alpha_beta .\n###  http://graffl.ai/pathology#alpha_beta\n            :alpha_beta rdf:type owl:Class ;\n            rdfs:label "Alpha Beta" .\n###  http://graffl.ai/pathology#gamma_delta\n            :gamma_delta rdf:type owl:Class ;\n            rdfs:label "Gamma Delta" ;\n            rdfs:subClassOf :gamma .\n###  http://graffl.ai/pathology#gamma\n            :gamma rdf:type owl:Class ;\n            rdfs:label "Gamma" .\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/owl-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
