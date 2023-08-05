#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import PyMieSim


root_path = Path(PyMieSim.__path__[0])

project_path = root_path.parents[0]

test_data_path = root_path.parents[0].joinpath('tests/data')

static_doc_path = root_path.parents[0].joinpath('docs/images')

lp_mode_path = root_path.joinpath('lp_modes')

examples_path = root_path.joinpath('examples')

version_path = root_path.joinpath('VERSION')

validation_data_path = root_path.joinpath('validation_data')

doc_path = root_path.parents[0].joinpath('docs')

logo_path = doc_path.joinpath('images/logo.png')

doc_css_path = doc_path.joinpath('source/_static/default.css')

rtd_example = 'https://pymiesim.readthedocs.io/en/latest/Examples.html'

rtd_material = 'https://pymiesim.readthedocs.io/en/latest/Material.html'

rtd_lp_mode = 'https://pymiesim.readthedocs.io/en/latest/LPModes.html'
