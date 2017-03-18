# -*- coding: utf-8 -*-
#
# butterfly documentation build configuration file, created by
# sphinx-quickstart on Fri Mar 17 13:11:45 2017.
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'content'

# General information about the project.
project = u'butterfly'
copyright = u'2017, Harvard Visual Computing Group'
author = u'Harvard Visual Computing Group'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'2.0'
# The full version, including alpha/beta/rc tags.
release = u'2.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

primary_domain = 'py'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

from collections import OrderedDict

html_theme = 'alabaster'

extra_links = OrderedDict()

api_link = '{site}{repo}{path}#{anchor}'.format(
    site = 'https://github.com/',
    repo = 'microns-ariadne/ariadne-nda/',
    path = 'blob/master/specs/finished.md',
    anchor = 'readme'
)

wiki_link = '{site}{repo}{path}'.format(
    site = 'https://github.com/',
    repo = 'Rhoana/butterfly/',
    path = 'wiki'
)

extra_links['Full API documentation'] = api_link
extra_links['Guides on Github Wiki'] = wiki_link

html_theme_options = dict(
    logo = 'bfly.png',
    logo_name = False,
    font_size = '1.0em',
    page_width = '875px',
    github_button = False,
    show_powered_by = False,
    github_user = 'Rhoana',
    github_repo = 'butterfly',
    code_font_size = 'inherit',
    extra_nav_links = extra_links,
    description = 'The butterfly image server',
    code_font_family = '"Anonymous Pro", monospace',
    sidebar_link_underscore = '#ACE',
    link = '#ACE',
    gray_1 = '#CCC',
    gray_2 = '#CCC',
    gray_3 = '#CCC',
    body_text = '#CCC',
    footer_text = '#CCC',
    sidebar_link = '#CCC',
    link_hover = '#FFF',
    sidebar_header = '#FFF',
    anchor_hover_fg = '#FFF',
    anchor_hover_bg = '#000',
    font_family = "'Lato', Arial, sans-serif",
    head_font_family = "'Raleway', Arial, sans-serif"
)

html_sidebars = {
    '**': [
        'about.html',
        'relations.html',
        'navigation.html',
        'searchbox.html',
    ]
}
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'butterflydoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'butterfly.tex', u'butterfly Documentation',
     u'Harvard Visual Computing Group', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'butterfly', u'butterfly Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'butterfly', u'butterfly Documentation',
     author, 'butterfly', 'One line description of project.',
     'Miscellaneous'),
]



