# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ethoscopy', 'ethoscopy.misc']

package_data = \
{'': ['*'], 'ethoscopy.misc': ['tutorial_data/*']}

install_requires = \
['PyWavelets>=1.4.1,<2.0.0',
 'astropy>=5.1.1,<6.0.0',
 'colour>=0.1.5,<0.2.0',
 'hmmlearn>=0.2.8,<0.3.0',
 'kaleido==0.2.1',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'scipy>=1.8.0,<2.0.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'ethoscopy',
    'version': '1.2.7',
    'description': 'A python based toolkit to download and anlyse data from the Ethoscope hardware system.',
    'long_description': "**ethoscopy**\n\nHead to: https://bookstack.lab.gilest.ro/books/ethoscopy for an in-depth tutorial on how to use ethoscopy\n\nA data-analysis toolbox utilising the python language for use with data collected from 'Ethoscopes', a Drosophila video monitoring system.\n\nFor more information on the ethoscope system: https://www.notion.so/The-ethoscope-60952be38787404095aa99be37c42a27\n\nEthoscopy is made to work alongside this system, working as a post experiment analysis toolkit. \n\nEthoscopy provides the tools to download experimental data from a remote ftp servers as setup in ethoscope tutorial above. Downloaded data can be curated during the pipeline in a range of ways, all formatted using the pandas data structure.\n\nFurther the ethoscopy package provides behavpy a subclassed version of pandas that combines metadata with the data for easy manipulation. Behavpy can be used independently of the Ethoscope system data if following the same structure. Within behavpy there are a range of methods to curate your data and then to generate plots using the plotly plotting package. Additionally, there are methods to analyse bout length, contiguous sleep, and many circadian analysis methods including periodograms.\n\nWithin Behavpy is a wrapped version of the python package hmmlearn, a tool for creating hidden markov models. With the update the user can easy train new HMMs from their data and use bult in methods to create graphs analysing the decoded dataset.",
    'author': 'Blackhurst Laurence',
    'author_email': 'l.blackhurst19@imperial.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
