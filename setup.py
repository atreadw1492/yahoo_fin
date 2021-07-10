from setuptools import setup

setup(name='yahoo_fin',
      version='0.8.9.1',
      description="""Download historical stock prices (daily / weekly / monthly),
                     realtime-prices, fundamentals data, income statements, 
                     cash flows, analyst info, current cryptocurrency prices,
                     option chains, earnings history, and more with yahoo_fin.
                    """,
      url='http://theautomatic.net/yahoo_fin-documentation/',
      author='Andrew Treadway',
      author_email='opensourcecoder11@gmail.com',
      license='MIT',
      packages=['yahoo_fin'],
      install_requires = ["requests_html", "feedparser", "requests", "pandas"],
      keywords = ["yahoo finance", "stocks", "options", "fundamentals"],
zip_safe=False)
