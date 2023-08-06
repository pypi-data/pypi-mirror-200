# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tessa',
 'tessa.price',
 'tessa.search',
 'tessa.sources',
 'tessa.symbol',
 'tessa.symbol.geo']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'frozendict>=2.3',
 'matplotlib>=3.5',
 'pendulum>=2.1',
 'pycoingecko>=2.2',
 'seaborn>=0.11',
 'yfinance>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'tessa',
    'version': '0.6.0',
    'description': 'Find financial assets and get their price history without worrying about different APIs or rate limiting.',
    'long_description': '\n# tessa – simple, hassle-free access to price information of financial assets 📉🤓📈\n\ntessa is a Python library to help you **easily search asset identifiers** (e.g.,\ntickers) and **retrieve price information** for assets from different sources such as\nYahoo or Coingecko. It takes care of the different APIs, caching, rate limiting, and\nother hassles.\n\ntessa provides a **Symbol class that encapsulates nicely the methods relevant for a\nsymbol**. tessa also provides functionality to **manage collections of symbols**, store\nand load them, and extend their functionality.\n\nFinally, tessa makes sure to be nice to the sites being accessed and tries to **prevent\nusers from being blocked by 429 rate limiting errors** by 1) caching results upon\nretrieval and 2) keeping track of request timestamps and waiting appropriate amounts of\ntime if necessary.\n\n[→ Check out the full documentation. 📖](https://ymyke.github.io/tessa/tessa.html)\n\n\n## How to use\n\nHere\'s a longer example that quickly shows all aspects of the library. Refer to\nsubmodules [symbol](tessa/symbol.html), [search](tessa/search.html), and\n[price](tessa/price.html) for more information.\n\n- Imports:\n\n```python\nfrom tessa import Symbol, SymbolCollection, search\n```\n\n- Create a symbol for MSFT and access some functions:\n\n```python\ns1 = Symbol("MSFT")         # will use "yahoo" as the default source\ns1.price_latest()           # get latest price\n```\n\n- Create another symbol from a bloomberg ticker as it is used by Yahoo Finance:\n\n```python\ns2 = Symbol("SREN.SW")\ns2.price_point("2022-06-30")    # get price at specific point in time\n```\n\n- Create a symbol from the coingecko source with an id as it is used by coingecko:\n\n```python\ns3 = Symbol("bitcoin", source="coingecko")\ns3.price_graph()            # show price graph\n```\n\n- Search for a more crypto ticker on coingecko:\n\n```python\nres = search("GAME")        # search and print search result summary\nfiltered = res.filter(source="coingecko")  # filter results\nfiltered.p()                # print summary of filtered results\nfiltered.buckets[0].symbols # review the best bucket in the filtered results\ns4 = filtered.buckets[0].symbols[2]   # our symbol is the 3rd in that list\ns4.price_history()          # get entire history\n```\n\n- Build a collection of several symbols and use the collection to retrieve symbols:\n\n```python\nsc = SymbolCollection([s1, s2, s3, s4])\nsc.add(Symbol("AAPL"))      # add another one\nsc.find_one("SREN").price_graph()\n```\n\n- Store and load a symbol collection:\n\n```python\nsc.save_yaml("my_symbols.yaml")\nsc_new = SymbolCollection()\nsc_new.load_yaml("my_symbols.yaml")\n```\n\n- Use a different currency preference:\n\n```python\nsc.find_one("game").price_latest()  # will return price in USD\nSymbol.currency_preference = "CHF"\nsc.find_one("game").price_latest()  # will return price in CHF\n```\n\nNote that `currency_preference` will only have an effect with sources that support it.\nIt is supported for Coingecko but not for Yahoo. So you should always verify the\neffective currency you receive in the result.\n\n\n## Data sources\n\ntessa builds on [yfinance](https://pypi.org/project/yfinance/) and\n[pycoingecko](https://github.com/man-c/pycoingecko) and offers **a simplified and\nunified interface**. \n\nWhy these two sources? Yahoo Finance (via yfinance) is fast and offers an extensive\ndatabase that also contains many non-US markets. Coingecko (via pycoingecko) offers\ngreat access to crypto prices. While Yahoo Finance also offers crypto information,\npycoingecko has the advantage that you can have the prices quoted in many more currency\npreferences (a function that is also exposed via tessa).\n\nMore sources can be added in the future. Let me know in the\n[issues](https://github.com/ymyke/tessa/issues) of you have a particular request.\n\n\n## Main submodules\n\n- [symbol](tessa/symbol.html): working with symbols and symbol collections.\n- [search](tessa/search.html): searching the different sources.\n- [price](tessa/price.html): accessing price functions directly instead of via the\n  `Symbol` class.\n- [sources](tessa/sources.html): if you\'d like to add additional sources to the library.\n\n\n## How to install\n\n`pip install tessa`\n\n\n## Prerequisites\n\nSee `pyproject.toml`. Major prerequisites are the `yfinance` and `pycoingecko` packages\nto access finance information as well as the `beautifulsoup4` package to do some\nscraping for searching on Yahoo Finance.\n\n\n## Repository\n\nhttps://github.com/ymyke/tessa\n\n\n## Future Work\n\nThis is an initial version. There are a number of ideas on how to extend. Please leave\nyour suggestions and comments in the [Issues\nsection](https://github.com/ymyke/tessa/issues).\n\n\n## On terminology\n\nI\'m using symbol instead of ticker because a ticker is mainly used for stock on stock\nmarkets, whereas tessa is inteded to be used for any kind of financial assets, e.g. also\ncrypto.\n\n\n## Other noteworthy libraries\n\n- [strela](https://github.com/ymyke/strela): A python package for financial alerts.\n- [pypme](https://github.com/ymyke/pypme): A Python package for PME (Public Market\n  Equivalent) calculation.\n\n\n## On investpy as a data source\n\nTessa used to use the [investpy package](https://github.com/alvarobartt/investpy) as the\nmain source of information until mid 2022 until investing.com introduced Cloudflare,\nwhich broke access by investpy. 😖 It is currently unclear if investpy will be available\nagain in the future. [You can follow the developments in issue\n600.](https://github.com/alvarobartt/investpy/issues/600) The old tessa/investpy code is\nstill available in the [add-symbols-based-on-investpy\nbranch](https://github.com/ymyke/tessa/tree/add-symbols-based-on-investpy).\n',
    'author': 'ymyke',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ymyke/tessa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.13,<3.10',
}


setup(**setup_kwargs)
