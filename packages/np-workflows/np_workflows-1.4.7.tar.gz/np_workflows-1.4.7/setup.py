# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_workflows',
 'np_workflows.experiments',
 'np_workflows.experiments.task_trained_network',
 'np_workflows.experiments.task_trained_network.camstim_scripts',
 'np_workflows.shared']

package_data = \
{'': ['*'], 'np_workflows': ['assets/images/*']}

install_requires = \
['ipylab>=0.6.0,<0.7.0',
 'ipywidgets>=7,<8',
 'jupyter-scheduler>=1.2.0,<2.0.0',
 'jupyterlab-git>=0.41.0,<0.42.0',
 'jupyterlab>=3.6,<4.0',
 'np-datajoint',
 'np-probe-targets',
 'np-services>=0.1.45',
 'np-session>=0.4.27',
 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'np-workflows',
    'version': '1.4.7',
    'description': 'Ecephys and behavior workflows for the Mindscope Neuropixels team.',
    'long_description': '# np_workflows\n\nThis package contains all the Python code required to run Mindscope Neuropixels experiments.\n\nExperiment workflows and related tasks are coordinated by Jupyter notebooks maintained here:\nhttps://github.com/AllenInstitute/np_notebooks\n\nRunning the notebooks requires a Python environment with:\n- Python >= 3.11\n- np_workflows\n- Jupyter / JupyterLab\n\n```\ngit clone https://github.com/AllenInstitute/np_notebooks\nconda create -n workflows python=3.11\npip install np_workflows\npip install jupyterlab\n```\n\n\nKeep the `np_workflows` package up-to-date by running `pip install\nnp_workflows -U` before each use\n\nTo develop this package `git clone` then `poetry install`\n',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
