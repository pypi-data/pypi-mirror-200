# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ugctools']

package_data = \
{'': ['*'], 'ugctools': ['assets/hello/*']}

install_requires = \
['PyMuPDF>=1.21.1,<2.0.0',
 'arrow>=1.2.3,<2.0.0',
 'fire>=0.5.0,<0.6.0',
 'markdown>=3.4.3,<4.0.0']

entry_points = \
{'console_scripts': ['ugc = ugctools.app:main']}

setup_kwargs = {
    'name': 'ugctools',
    'version': '0.1.0',
    'description': '',
    'long_description': '# resume.md\n\n![Resume](resume.png)\n\nWrite your resume in\n[Markdown](https://raw.githubusercontent.com/mikepqr/resume.md/main/resume.md),\nstyle it with [CSS](resume.css), output to [HTML](resume.html) and\n[PDF](resume.pdf).\n\n## Prerequisites\n\n - Python ≥ 3.6\n - [python-markdown](https://python-markdown.github.io/) (`pip install\n   markdown`)\n - Optional, required for PDF output: Google Chrome or Chromium\n\n## Usage\n\n 1. Download [resume.py](resume.py), [resume.md](resume.md) and\n    [resume.css](resume.css) (or make a copy of this repository by [using the\n    template](https://github.com/mikepqr/resume.md/generate), forking, or\n    cloning).\n\n 2. Edit [resume.md](resume.md) (the placeholder text is taken with thanks from\n    the [JSON Resume Project](https://jsonresume.org/themes/))\n\n 3. Run `python3 resume.py` to build resume.html and resume.pdf.\n\n     - Use `--no-html` or `--no-pdf` to disable HTML or PDF output.\n\n     - Use `--chrome-path=/path/to/chrome` if resume.py cannot find your Chrome\n       or Chromium executable.\n\n## Customization\n\nEdit [resume.css](resume.css) to change the appearance of your resume. The\ndefault style is extremely generic, which is perhaps what you want in a resume,\nbut CSS gives you a lot of flexibility. See, e.g. [The Tech Resume\nInside-Out](https://www.thetechinterview.com/) for good advice about what a\nresume should look like (and what it should say).\n\nChange the appearance of the PDF version (without affecting the HTML version) by\nadding rules under the `@media print` CSS selector.\n\nChange the margins and paper size of the PDF version by editing the [`@page` CSS\nrule](https://developer.mozilla.org/en-US/docs/Web/CSS/%40page/size).\n\n[python-markdown](https://python-markdown.github.io/) is by default a very basic\nmarkdown compiler, but it has a number of optional extensions that you may want\nto enable (by adding to [the list of extensions\nhere](https://github.com/mikepqr/resume.md/blob/f1b0699a9b66833cb67bb59111f45a09ed3c0f7e/resume.py#L112)).\n<code><a\nhref="https://python-markdown.github.io/extensions/attr_list/">attr_list</a></code>\nin particular may by useful if you are editing the CSS.\n[abbreviations](https://python-markdown.github.io/extensions/abbreviations/)\nextension is already enabled.\n\n# 安装\n## mac用户需要安装poppler:\n```\nbrew install poppler\n```\n## Linux用户\n```\npip install pdf2image\n```\n\n',
    'author': 'aaron yang',
    'author_email': 'aaron_yang@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
