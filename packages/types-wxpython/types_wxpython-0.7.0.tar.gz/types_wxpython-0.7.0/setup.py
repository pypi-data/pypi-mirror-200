# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wx-stubs',
 'wx-stubs.DateTime',
 'wx-stubs.FileType',
 'wx-stubs.Image',
 'wx-stubs.TopLevelWindow',
 'wx-stubs.Window',
 'wx-stubs.adv',
 'wx-stubs.aui',
 'wx-stubs.dataview',
 'wx-stubs.glcanvas',
 'wx-stubs.grid',
 'wx-stubs.grid.GridBlocks',
 'wx-stubs.html',
 'wx-stubs.html2',
 'wx-stubs.lib',
 'wx-stubs.lib.agw',
 'wx-stubs.lib.agw.ribbon',
 'wx-stubs.lib.agw.ribbon.buttonbar',
 'wx-stubs.lib.agw.ribbon.gallery',
 'wx-stubs.lib.agw.ribbon.toolbar',
 'wx-stubs.lib.analogclock',
 'wx-stubs.lib.analogclock.lib_setup',
 'wx-stubs.lib.analogclock.lib_setup.fontselect',
 'wx-stubs.lib.buttons',
 'wx-stubs.lib.calendar',
 'wx-stubs.lib.colourselect',
 'wx-stubs.lib.newevent',
 'wx-stubs.lib.scrolledpanel',
 'wx-stubs.lib.wxpTag',
 'wx-stubs.media',
 'wx-stubs.propgrid',
 'wx-stubs.ribbon',
 'wx-stubs.richtext',
 'wx-stubs.stc',
 'wx-stubs.xml',
 'wx-stubs.xrc']

package_data = \
{'': ['*'],
 'wx-stubs': ['ActivateEvent/*',
              'ConfigBase/*',
              'DataObject/*',
              'HelpEvent/*',
              'StandardPaths/*',
              'StaticBitmap/*',
              'StockPreferencesPage/*'],
 'wx-stubs.grid': ['Grid/*', 'GridActivationSource/*'],
 'wx-stubs.lib': ['dialogs/*']}

setup_kwargs = {
    'name': 'types-wxpython',
    'version': '0.7.0',
    'description': 'Typing stubs for wxPython',
    'long_description': '[![PyPI version](https://badge.fury.io/py/types-wxpython.svg)](https://badge.fury.io/py/types-wxpython)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/types-wxpython)\n![GitHub branch checks state](https://img.shields.io/github/checks-status/AlexionSoftware/types-wxpython/main)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/types-wxpython)\n![GitHub](https://img.shields.io/github/license/AlexionSoftware/types-wxpython)\n\n# Typing stubs for wxPython\nVersion: wxPython 4.2.0\n\nThis package contains typings stubs for [wxPython](https://pypi.org/project/wxPython/)\n\nThis package is not maintained by the maintainers of wxPython. This is made by users of wxPython.\n\nAny help is always welcome.\n',
    'author': 'Alexion Software',
    'author_email': 'info@alexion.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlexionSoftware/types-wxpython',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
