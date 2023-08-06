from setuptools import setup, find_packages

setup(
  name = 'foxglovetree',
  version = '0.1',
  description = 'The foxglovetree module',
  long_description = 'The foxglovetree module designed by the NCCHD data science team',
  author = 'Kohji',
  author_email = 'okamura-k@ncchd.go.jp',
  url = 'https://aihospital.ncchd.go.jp/foxglovetree',
  keywords = ('NCCHD',),
  license = 'MIT License',
  packages = find_packages(),
  include_package_data = False,
  install_requires = (),
)
