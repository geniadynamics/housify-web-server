# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

os.environ["SPHINX_AUTODOC_RELOAD_MODULES"] = "1"


project = "Housify"
copyright = "2023, GeniaDynamics"
author = "GeniaDynamics"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.coverage",
    # "sphinx_immaterial",
]

# html_theme = "sphinx_material"
# html_theme = "sphinx_immaterial"
html_theme = "piccolo_theme"
# html_theme = 'sphinx_rtd_theme'
# templates_path = ['_templates']

#pygments_style = "stata-dark"

html_theme_options = {
    "show_theme_credit": False,
    "source_url": "https://self-hosted.foo.com/",
    "source_icon": "gitlab",

}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_static_path = ["_static"]
