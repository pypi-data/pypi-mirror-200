from distutils.core import setup
setup(
  name = 'scrapeLinkedinJob',        
  packages = ['scrapeLinkedinJob'],
  version = '0.0.1',
  license='MIT',
  description = 'A simple spam bot for WhatsApp. It can spam a message a given number of times or spam forever. It can be stopped by pressing ctrl.',
  author = 'Sushil Dhakal',
  author_email = 'sushilldhakal25@gmail.com',
  url = 'https://github.com/sushilld/LinkedIn-Job-Scraper',
  download_url = 'https://github.com/sushilld/LinkedIn-Job-Scraper',
  install_requires=[
          "pandas==1.5.0",
          "selenium==4.8.3",
          "webdriver_manager==3.5.4"
      ],
  classifiers=[ 
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)