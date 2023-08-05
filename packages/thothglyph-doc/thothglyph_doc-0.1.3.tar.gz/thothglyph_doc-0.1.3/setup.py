# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thothglyph',
 'thothglyph.app',
 'thothglyph.ext',
 'thothglyph.node',
 'thothglyph.reader',
 'thothglyph.writer']

package_data = \
{'': ['*'],
 'thothglyph': ['data/*',
                'template/common/*',
                'template/docx/default/*',
                'template/html/default/*',
                'template/html/preview/*',
                'template/latex/default/*']}

install_requires = \
['cairosvg>=2.5.2,<3.0.0', 'pillow>=9.2.0,<10.0.0']

entry_points = \
{'console_scripts': ['thothglyph = thothglyph.app.converter:main']}

setup_kwargs = {
    'name': 'thothglyph-doc',
    'version': '0.1.3',
    'description': 'A Documentation converter and language for Engineers',
    'long_description': '# Thothglyph\n\nA Documentation converter and language for Engineers\n\n(Θωθ)\n\n## Requirements\n\n* python >= 3.7\n* pillow\n* cairosvg\n\n## Installation\n\nMinimum\n\n```sh\npip install thothglyph-doc\n```\n\n\\+ writers\n\n```\n# pdf\nsudo apt install texlive-luatex texlive-fonts-recommended texlive-fonts-extra texlive-lang-cjk\n# docx\npip install python-docx\n```\n\n\\+ extensions\n\n```\n# graphviz\nsudo apt install graphviz\npip install graphviz\n# blockdiag\npip install blockdiag actdiag seqdiag nwdiag\n# wavedrom\npip install wavedrom\n```\n\n## Usage\n\n```sh\nthothglyph -t html document.tglyph\n```\n\n## Thothglyph Language\n\nSee [quick-reference.ja.md](doc/language/quick-reference.ja.md)\n\n## Tools\n\n* [vim-thothglyph](https://github.com/nakandev/vim-thothglyph)\n* [vscode-thothglyph](https://github.com/nakandev/vscode-thothglyph)\n',
    'author': 'nakandev',
    'author_email': 'nakandev.s@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
