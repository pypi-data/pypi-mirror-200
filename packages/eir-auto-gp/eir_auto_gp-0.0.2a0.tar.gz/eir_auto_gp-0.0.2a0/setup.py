# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eir_auto_gp',
 'eir_auto_gp.analysis',
 'eir_auto_gp.modelling',
 'eir_auto_gp.preprocess',
 'eir_auto_gp.utils']

package_data = \
{'': ['*']}

install_requires = \
['eir-dl>=0.1.31a0,<0.2.0',
 'plink-pipelines>=0.1.5a0,<0.2.0',
 'qmplot>=0.3.2,<0.4.0',
 'scikit-optimize>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['eirautogp = eir_auto_gp.run:main',
                     'eirautogwas = '
                     'eir_auto_gp.preprocess.gwas_pre_selection:main']}

setup_kwargs = {
    'name': 'eir-auto-gp',
    'version': '0.0.2a0',
    'description': '',
    'long_description': '# EIR-auto-GP\n\n<p align="center">\n  <img src="docs/source/_static/img/eir-auto-gp-logo.svg" alt="Eir Auto GP Logo">\n</p>\n\n<p align="center">\n  <a href="LICENSE" alt="License">\n        <img src="https://img.shields.io/badge/License-APGL-5B2D5B.svg" />\n  </a>\n  \n  <a href="https://www.python.org/downloads/" alt="Python">\n        <img src="https://img.shields.io/badge/python-3.10-blue.svg" />\n  </a>\n  \n  <a href="https://pypi.org/project/eir-auto-gp/" alt="Python">\n        <img src="https://img.shields.io/pypi/v/eir-auto-gp.svg" />\n  </a>\n  \n  \n  <a href="https://codecov.io/gh/arnor-sigurdsson/EIR-auto-GP" > \n        <img src="https://codecov.io/gh/arnor-sigurdsson/EIR-auto-GP/branch/master/graph/badge.svg?token=PODL2J83Y0"/> \n  </a>\n  \n  <a href=\'https://eir-auto-gp.readthedocs.io\'>\n    <img src=\'https://readthedocs.org/projects/eir-auto-gp/badge/?version=latest\' alt=\'Documentation Status\' />\n  </a>\n      \n  \n</p>\n\n`EIR-auto-GP`: Automated genomic prediction (GP) using deep learning models with EIR.\n\n**WARNING**: This project is in alpha phase. Expect backwards incompatible changes and API changes.\n\n## Overview\n\nEIR-auto-GP is a comprehensive framework for genomic prediction (GP) tasks, built on top of the [EIR](https://github.com/arnor-sigurdsson/EIR) deep learning framework. EIR-auto-GP streamlines the process of preparing data, training, and evaluating models on genomic data, automating much of the process from raw input files to results analysis. Key features include:\n\n- Support for `.bed/.bim/.fam` PLINK files as input data.\n- Automated data processing and train/test splitting.\n- Takes care of launching a configurable number of deep learning training runs.\n- SNP-based feature selection based on GWAS, deep learning-based attributions, and a combination of both.\n- Ensemble prediction from multiple training runs.\n- Analysis and visualization of results.\n\n## Installation\n\nFirst, ensure that [plink2](https://www.cog-genomics.org/plink/2.0/) is installed and available in your `PATH`. \n\nThen, install `EIR-auto-GP` using `pip`:\n\n`pip install eir-auto-gp`\n\n## Usage\n\nPlease refer to the [Documentation](https://eir-auto-gp.readthedocs.io/en/latest/) for examples and information.\n\n## Workflow\n\n1. Data processing: EIR-auto-GP processes the input `.bed/.bim/.fam` PLINK files and `.csv` label file, preparing the data for model training and evaluation.\n2. Train/test split: The processed data is automatically split into training and testing sets, with the option of manually specifying splits.\n3. Training: Configurable number of training runs are set up and executed using EIR\'s deep learning models.\n4. SNP feature selection: GWAS based feature selection, deep learning-based feature selection with Bayesian optimization, and mixed strategies are supported.\n5. Test set prediction: Predictions are made on the test set using all training run folds.\n6. Ensemble prediction: An ensemble prediction is created from the individual predictions.\n7. Results analysis: Performance metrics, visualizations, and analysis are generated to assess the model\'s performance.\n\n## Citation\n\nIf you use `EIR-auto-GP` in a scientific publication, we would appreciate if you could use the following citation:\n\n```\n@article{sigurdsson2021deep,\n  title={Deep integrative models for large-scale human genomics},\n  author={Sigurdsson, Arnor Ingi and Westergaard, David and Winther, Ole and Lund, Ole and Brunak, S{\\o}ren and Vilhjalmsson, Bjarni J and Rasmussen, Simon},\n  journal={bioRxiv},\n  year={2021},\n  publisher={Cold Spring Harbor Laboratory}\n}\n```\n',
    'author': 'Arnor Sigurdsson',
    'author_email': 'arnor-sigurdsson@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
