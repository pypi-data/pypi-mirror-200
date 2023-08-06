# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strela', 'strela.alertstates']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23',
 'pandas>=1.3.5',
 'python-slugify>=5.0.0',
 'tessa>=0,<1',
 'yagmail>=0.15.280']

setup_kwargs = {
    'name': 'strela',
    'version': '0.3.4',
    'description': 'A python package for financial alerts',
    'long_description': '# strela - a python package for financial alerts 📈🚨📉\n\nstrela provides a toolbox to generate and send different kinds of alerts based on\nfinancial information.\n\nThe package is intended to be used to write a Python script that can be scheduled via\ncronjob or similar facilities and runs everything necessary according to your needs. See\n`strela.my_runner` as an example.\n\n[→ Check out the full documentation. 📖](https://ymyke.github.io/strela/strela.html)\n\n## Features & overview\n\n- `strela.alert_generator`: The central logic that brings all the building blocks\n  together to retrieve and analyze the financial metrics and to generate and send alerts\n  if applicable.\n- `strela.alertstates.alertstate.AlertState`: The abstract base class for all alert\n  states. Alert states encapsulate the logic to determine whether an alert has triggered\n  or not. There are two concrete types of alerts:\n    - `strela.alertstates.fluctulertstate.FluctulertState`: Alerts for fluctuations (up\n      or down) over certain thresholds.\n    - `strela.alertstates.doubledownalertstate.DoubleDownAlertState`: Alerts for\n      significant downward movement which could trigger an over-proportional buy.\n- `strela.templates`: Classes to turn alerts into text or html strings that can be\n  printed or mailed.\n- `strela.mailer`: To send alerts via email.\n- `strela.config`: Configuration management. Use the override mechanism described there\n  to put your own user config file in place that overrides the settings in the default\n  config file according to your environment.\n- `strela.my_runner`: The script that brings it all together and runs the alert\n  generator according to your requirements. Use this script as a blueprint to build your\n  own runner script.\n- `strela.alertstates.alertstaterepository`: Repositories (in memory or on disk) to\n  store and retrieve alert states.\n\n## How to install and use\n\n1. Install the package. Two options:\n   - `pip install strela`\n   - Clone the repository and install the requirements using poetry.\n2. Set up your config file `my_config.py` based on the documentation in `strela.config`.\n   (Review your config via `strela.config.print_current_configuation`.)\n3. Write your own runner script based on the blueprint in `strela.my_runner`. (Test your\n   script by running it and -- if necessary -- setting `strela.config.ENABLE_ALL_DOWS`\n   and/or `strela.config.NO_MAIL` to `True`.)\n4. Install your runner script as a daily cronjob or similar.\n\n## Example alerts\n\nWhat a single Fluctulert looks like in the alert e-mail:\n\n![Fluctulert example](https://raw.githubusercontent.com/ymyke/strela/master/docs/images/fluctulert_example.png)\n\nWhat a single DoubleDownAlert looks like in the alert e-mail:\n\n![DoubleDownAlert example](https://raw.githubusercontent.com/ymyke/strela/master/docs/images/doubledownalert_example.png)\n\n## Limitations\n\nThe overall software architecture features decent modularization and separation of\nconcerns, but also has a lot of room left for improvement. E.g., better separation of\nconcerns in AlertStates (mixing logic and output currently), better parametrization of\nalert states and templates, better extensibility, etc. \n\n## strela vs tessa\n\nThe strela package works seamlessly with [tessa](https://github.com/ymyke/tessa) and its\nSymbol class and financial information access functionality.\n\nAt the same time, care was taken to make strela open and flexible enough to be used with\nother packages and/or your own code.\n\nStill, many or most people will end up using strela together with tessa so it\'s worth\ndiscussing whether strela should be incorporated into tessa.\n\nI decided to keep strela separate from tessa because strela has a distinctly different\ncharacter: a) it is not purely a library but needs some script to be built on top and\nthen called as a CLI tool / cronjob, b) it tends to rely on external files such as a\nlist of symbols to be loaded, c) it needs a place to store the alert state (and will\nfail if that place doesn\'t exist, which seems to be unacceptable behavior for a pure\nlibrary such as tessa).\n\nBut I would like to have your thoughts on this. Should strela and tessa be separate\npackages or better both in one? [Add your thoughts to the respective\nissue.](https://github.com/ymyke/strela/issues/1)\n\n## A note on tests\n\nSome of the tests hit the net and are marked as such with `pytest.mark.net`. That way,\nyou can easily run exclude those tests if you like: `pytest -m "not net"`.\n\n## Link to Repository\n\nhttps://github.com/ymyke/strela\n\n## Other noteworthy libraries\n\n- [tessa](https://github.com/ymyke/tessa): Find financial assets and get their price history without worrying about different APIs or rate limiting.\n- [pypme](https://github.com/ymyke/pypme): A Python package for PME (Public Market Equivalent) calculation.\n',
    'author': 'ymyke',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ymyke/strela',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.13,<3.10',
}


setup(**setup_kwargs)
