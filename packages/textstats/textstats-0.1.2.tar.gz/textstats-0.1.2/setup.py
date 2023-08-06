# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['textstats']
install_requires = \
['argparse>=1.4.0,<2.0.0',
 'emoji>=2.2.0,<3.0.0',
 'prettytable>=3.6.0,<4.0.0',
 'spacy>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'textstats',
    'version': '0.1.2',
    'description': 'This is a Pakcage for Extracting Info from the text.',
    'long_description': 'TextStats is the package used for analysis of the text.\n\nTextSats gives out various Information for the text provided to it.\nSome of them includes :\n1. Line Count\n2. Word Count\n3. Emoji Count\n4. Email Count\n5. URL Count\n6. Proper Punctuation Count\n7. ImProper Punctuation Count\n\nApart from this it also contains NER model i.e spacy to classify the words into named entities.\n\n\n\n',
    'author': 'varun',
    'author_email': 'varunkatiyar819@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
