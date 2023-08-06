# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlsphinxtheme']

package_data = \
{'': ['*'],
 'qctrlsphinxtheme': ['static/*',
                      'static/css/*',
                      'static/img/*',
                      'static/img/social/*',
                      'static/js/*']}

install_requires = \
['sphinx>=5.0.0,<6.0.0', 'sphinx_rtd_theme>=1.1.1,<1.2.0']

entry_points = \
{'sphinx.html_themes': ['qctrl_sphinx_theme = qctrlsphinxtheme']}

setup_kwargs = {
    'name': 'qctrl-sphinx-theme',
    'version': '0.1.3',
    'description': 'Q-CTRL Sphinx Theme',
    'long_description': '# Q-CTRL Sphinx Theme\n\nThe Q-CTRL Sphinx Theme is a very opinionated [Sphinx](https://www.sphinx-doc.org/) theme intended for use with public [Q-CTRL Documentation](https://docs.q-ctrl.com/) websites such as the [Q-CTRL Python package](https://docs.q-ctrl.com/boulder-opal/references/qctrl/).\n\n## Installation\n\n```shell\npip install qctrl-sphinx-theme\n```\n\n## Usage\n\n1. Add `qctrl-sphinx-theme` as a dev dependency in `pyproject.toml`.\n2. Set the `html_theme` config value in `docs/conf.py`.\n  ```python\n  html_theme = "qctrl_sphinx_theme"\n  ```\n3. Set the `html_theme_options` config value in `docs/conf.py`.\n  ```python\n  html_theme_options = {\n      "segment_write_key": "<YOUR_SEGMENT_WRITE_KEY>"\n  }\n  ```\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
