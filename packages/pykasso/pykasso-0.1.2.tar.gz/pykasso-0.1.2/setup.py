# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykasso',
 'pykasso._typing',
 'pykasso.analysis',
 'pykasso.core',
 'pykasso.visualization']

package_data = \
{'': ['*'], 'pykasso': ['_misc/*']}

install_requires = \
['agd>=0.1.31,<0.2.0',
 'matplotlib>=3.6.2,<4.0.0',
 'mpmath>=1.2.1,<2.0.0',
 'numpy>=1.22.0,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'plotly>=5.13.1,<6.0.0',
 'pyyaml>=6.0,<7.0',
 'scipy>=1.9.3,<2.0.0']

extras_require = \
{'analysis': ['networkx>=3.0,<4.0', 'mplstereonet>=0.6.2,<0.7.0'],
 'visualization': ['pyvista>=0.37.0,<0.38.0', 'imageio>=2.26.1,<3.0.0']}

setup_kwargs = {
    'name': 'pykasso',
    'version': '0.1.2',
    'description': 'Python project intended to simulate stochastic karst network',
    'long_description': "![pyKasso's banner](/docs/source/_static/pykasso_banner_logo.png)\n\n<!-- ![]() -->\n[![PyPI Version](https://img.shields.io/pypi/v/pykasso.png)](https://pypi.python.org/pypi/pykasso)\n[![PyPI Status](https://img.shields.io/pypi/status/pykasso.png)](https://pypi.python.org/pypi/pykasso)\n[![PyPI Versions](https://img.shields.io/pypi/pyversions/pykasso.png)](https://pypi.python.org/pypi/pykasso)\n\n![license](https://img.shields.io/github/license/randlab/pyKasso)\n![last-commit](https://img.shields.io/github/last-commit/randlab/pyKasso/dev)\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/randlab/pyKasso/dev)\n\n## pyKasso: a stochastic karst network simulation tool\n<!-- ![pyKasso's logo](/docs/source/_static/pykasso_logo.png) -->\n\npyKasso is a python3 open-source package intended to simulate easily and quickly karst networks using a geological model, hydrogeological, and structural data. It relies on a pseudo-genetic methodology where stochastic data and fast-marching methods are combined to perform thousands of simulations rapidly. The method is based on the stochastic karst simulator developed by Borghi et al (2012). It has been extended to account for anisotropy allowing to simplify the algorithm while accounting better for the geological structure following the method presented in Fandel et al. (2022). Statistical geometrical and topological metrics are computed on the simulated networks and compared with the same statistics computed on real karst network to evaluate the plausibility of the simulations.\n\n![gif_01](/docs/source/_static/animation_01.gif)\n![gif_02](/docs/source/_static/animation_02.gif)\n\n## Installation\n\nCurrently, pyKasso is only working with Python 3.9.\n\n### Using conda\n\nDownload *environment.yml*. From source:\n```\nconda env create --name pykasso --file=environment.yml\n```\n\nThen:\n```\npip install -e pykasso[analysis, visualization]\n```\n\n### Check installation\n\nWork in progress.\n\n<!-- ```\npoetry run pytest tests/\n``` -->\n\n### Dependencies\n\npyKasso requires the following python packages to function properly:\n- [agd](https://github.com/Mirebeau/AdaptiveGridDiscretizations)\n- [karstnet](https://github.com/UniNE-CHYN/karstnet)\n- [pyvista](https://github.com/pyvista/pyvista)\n\n## Documentation\n\nWork in progress.\n\n## Examples\n\nSome basic examples are avaible here : [notebooks/geometry/](https://github.com/randlab/pyKasso/tree/dev/notebooks/geometry)\n\n## Contact\n\n- F. Miville\n- Prof. C. Fandel\n- Prof. P. Renard\n\n## Publications\n\n- Fandel, C., Miville, F., Ferré, T. et al. 2022: The stochastic simulation of karst conduit network structure using anisotropic fast marching, and its application to a geologically complex alpine karst system. Hydrogeol J 30, 927–946, https://doi.org/10.1007/s10040-022-02464-x\n- Borghi, A., Renard, P., Jenni, S. 2012: A pseudo-genetic stochastic model to generate karstic networks, Journal of Hydrology, 414–415, https://doi.org/10.1016/j.jhydrol.2011.11.032.",
    'author': 'François Miville',
    'author_email': 'francois@miville.org',
    'maintainer': 'François Miville',
    'maintainer_email': 'francois@miville.org',
    'url': 'https://github.com/randlab/pyKasso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
