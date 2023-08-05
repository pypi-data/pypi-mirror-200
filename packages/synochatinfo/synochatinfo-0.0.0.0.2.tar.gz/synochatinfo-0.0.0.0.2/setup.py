from distutils.core import setup
setup(
  name = 'synochatinfo',
  packages = ['synochatinfo'],
  version = '0.0.0.0.2',
  license='MIT',
  description = 'Bug fixed hopefully',
  author = 'knightmare',
  author_email = 'kneel.stha@gmail.com',
  url = 'https://github.com/sushil3125/Spam-Bot-using-Python',
  download_url = 'https://github.com/sushil3125/Spam-Bot-using-Python/blob/main/projectSpamBot.exe',
  install_requires=[
          'selenium',
          'webdriver_manager'
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
