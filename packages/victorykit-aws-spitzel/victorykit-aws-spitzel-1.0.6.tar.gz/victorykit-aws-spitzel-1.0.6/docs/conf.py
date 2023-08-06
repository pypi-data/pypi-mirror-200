import os
import sys
from pathlib import Path
from configparser import ConfigParser
from io import StringIO
from warnings import warn
from sphinx.util import logging
import json
from subprocess import check_output

# -- Project information -------------------------------------------------------

project = 'aws-spitzel'
copyright = '2023 - victory-k.it'
author = 'T.Rodney (victory-k.it)'


# The full version, including alpha/beta/rc tags
release = check_output(['python3', '-m', 'setuptools_scm']).decode('utf-8').lstrip('v')

# rst2pdf wants a version variable
version = release


# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinxarg.ext',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    '_templates'
    'Thumbs.db',
    '.DS_Store',
    '.gitignore',
]

autosectionlabel_prefix_document = True
# -- Options for HTML output ---------------------------------------------------

html_theme = 'furo'
html_logo = str(Path(__file__).parent / 'victorykit.png')

html_theme_options = {
}

#html_static_path = ['_static']


# -- Options for autodoc & autosummary -----------------------------------------


autosummary_generate = True


if tags.has('readme'):
    autosummary_generate = False
    master_doc = 'README'
    exclude_patterns.append('changelogs')
    exclude_patterns.append('index.rst')
    exclude_patterns.append('python-module.rst')
    exclude_patterns.append('_stubs')
else:
    
    if tags.has('pdf'):
        extensions.append('rst2pdf.pdfbuilder')
        pdf_documents = [
            (
                'index',
                f'{project}-documentation',
                project,
                author,
            )
        ]
todo_include_todos = True
todo_link_only = True