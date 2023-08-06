# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web3cat',
 'web3cat.data',
 'web3cat.data.chainlink',
 'web3cat.data.erc20s',
 'web3cat.data.ethers',
 'web3cat.data.gearbox',
 'web3cat.data.portfolios',
 'web3cat.fetcher',
 'web3cat.fetcher.balances',
 'web3cat.fetcher.blocks',
 'web3cat.fetcher.calls',
 'web3cat.fetcher.erc20_metas',
 'web3cat.fetcher.events',
 'web3cat.fetcher.events_indices',
 'web3cat.view',
 'web3cat.view.wireframes']

package_data = \
{'': ['*'], 'web3cat.data.gearbox': ['abi/*']}

install_requires = \
['bokeh>=2.4.3,<3.0.0',
 'jupyter-bokeh>=3.0.5,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'polars>=0.14.18,<0.15.0',
 'web3>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'web3cat',
    'version': '0.1.7',
    'description': 'Data visualization for EVM-based blockchains',
    'long_description': '.. image:: https://readthedocs.org/projects/web3cat/badge/?version=latest\n    :target: https://web3cat.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nWelcome to Web3cat!\n===================\n\n.. image:: /docs/images/web3cat.png\n    :width: 180\n\n**Meow, fellow researcher!**\n\nWeb3cat is a framework for fetching and analyzing blockchain data.\n\nCurrently, it supports only EVM chains: `Ethereum <https://ethereum.org>`_,\n`Polygon <https://polygon.technology>`_, `BNB <https://www.bnbchain.org>`_, etc.\n\nDesign philosophy\n-----------------\n\n#. Visualize the data with minimum code\n#. Free for downloading, saving, and analyzing the data however you want\n#. Cache the data to avoid re-fetching anything at all\n#. Fully decentralized, that is, depending only on the blockchain RPC\n\n\nQuick demo\n----------\n.. image:: /docs/images/web3cat_demo.gif\n\n\nGetting started\n---------------\n\n1. Install python package \n\n.. code::\n\n    pip install web3cat\n\n2. Set up your archive node rpc. The easiest (and also free) way is to use\n   `Alchemy <https://alchemy.com>`_.\n\n3. Set initial configuration\n\n.. code::\n\n    import os\n    os.environ[\'WEB3_PROVIDER_URI\'] = \'https://eth-mainnet.g.alchemy.com/v2/<YOUR_ALCHEMY_API_KEY>\'\n    os.environ[\'WEB3_CACHE_PATH\']="cache.sqlite3"\n\n4. (optional for Jupyter) Initialize bokeh for python notebooks\n\n.. code::\n\n    from bokeh.io import output_notebook\n\n    output_notebook()\n\n5. Run sample visualization\n\n.. code::\n\n    from web3cat.view import View\n    from datetime import datetime\n\n    v = View(token="DAI", start=datetime(2022, 6, 1), end = datetime(2022, 10, 30)) \\\n        .total_supply() \\\n        .balance(["0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643", "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"])\n    v.show()\n\n.. image:: docs/images/view1.png\n\n6. Get underlying data\n\n    .. code::\n\n        v.get_data(0).transfers[["date", "block_number", "from", "to", "value"]]\n\n    .. image:: docs/images/view_getting_started1.png\n\nRoadmap\n-------\n\nUse framework base layers to add analytics for protocols like\nUniswap, Liquity, Aave, Compound, Frax, etc.\n\nContributing\n------------\n\nSo far no bureaucracy here, open issues, make pull requests, and have fun!',
    'author': 'Mono6',
    'author_email': 'monowhile6@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
