# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ozcore',
 'ozcore.core',
 'ozcore.core.aggrid',
 'ozcore.core.data',
 'ozcore.core.data.csv',
 'ozcore.core.data.sqlite',
 'ozcore.core.df',
 'ozcore.core.path',
 'ozcore.core.utils']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "all"': ['typeguard>=3.0.2,<4.0.0',
                     'typer>=0.7.0,<0.8.0',
                     'sqlalchemy==1.4.46',
                     'alembic>=1.10.2,<2.0.0',
                     'numpy>=1.24.2,<2.0.0',
                     'pandas>=1.5.3,<2.0.0',
                     'matplotlib>=3.7.1,<4.0.0'],
 'all': ['faker>=18.3.1,<19.0.0',
         'tqdm>=4.65.0,<5.0.0',
         'dynaconf>=3.1.12,<4.0.0',
         'seaborn>=0.12.2,<0.13.0',
         'lxml>=4.9.2,<5.0.0',
         'requests>=2.28.2,<3.0.0',
         'ipyaggrid>=0.3.2,<0.4.0',
         'html5lib>=1.1,<2.0',
         'html2text>=2020.1.16,<2021.0.0',
         'markdown2>=2.4.8,<3.0.0',
         'ipykernel>=6.22.0,<7.0.0',
         'ipywidgets>=8.0.6,<9.0.0',
         'nbformat>=5.8.0,<6.0.0',
         'jupyter-contrib-nbextensions>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'ozcore',
    'version': '2.0.2',
    'description': 'My core.',
    'long_description': '======\nOzCore\n======\n\nOzCore is my core.\n\n\n.. image:: https://badge.fury.io/py/ozcore.svg\n    :target: https://pypi.python.org/pypi/ozcore/\n    :alt: PyPI version\n\n\n.. image:: https://readthedocs.org/projects/ozcore/badge/?version=latest\n    :target: https://ozcore.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n\n.. image:: http://hits.dwyl.com/ozgurkalan/OzCore.svg\n    :target: http://hits.dwyl.com/ozgurkalan/OzCore\n    :alt: HitCount\n\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n\n\nOzCore is automating my boring stuff. A time saver gadget for me. \n\n\nInstallation\n============\n\n\n\nI. Pip simple\n~~~~~~~~~~~~~\nPublished latest stable version\n\n.. code:: bash\n\n    pip install ozcore\n\n\n\nII. Latest from GitHub with Pip\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nLatest dev version from GitHub\n\n.. code:: bash\n\n    pip install git+https://github.com/ozgurkalan/OzCore --force-reinstall --no-deps\n\n\nIII. GitHub clone\n~~~~~~~~~~~~~~~~~\n\n.. code:: bash\n\n    git clone https://github.com/ozgurkalan/OzCore.git\n\n\n\nJupyter Kernel\n==============\n\nFor your Jupyter Notebook to run in your dedicated environment, use the following script::\n\n    # add kernell to Jupyter\n    python -m ipykernel install --user --name=<your_env_name>\n\n\nFresh installs may have problems with enabling extentions. You shall run the commands below to activate.\n\n.. code:: bash\n\n    jupyter nbextension enable --py --sys-prefix widgetsnbextension\n\n\nJupyter Extensions\n==================\n\nThis step copies the ``nbextensions`` javascript and css files into the jupyter server’s search directory, and edits some jupyter config files. \n\n.. code:: bash\n\n    jupyter contrib nbextension install --system\n\n\n\n\n\n',
    'author': 'Ozgur Kalan',
    'author_email': 'ozgurkalan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ozcore.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
