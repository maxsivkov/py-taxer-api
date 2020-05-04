from setuptools import setup, find_packages

setup(name='py_taxer_api',
      version='0.1',
      description='Taxer Api',
      url='https://github.com/maxsivkov/py_taxer_api',
      author='Max Sivkov',
      author_email='maxsivkov@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'selenium',
            'pyyaml',
            'requests',
            'flask-restx',
            'marshmallow-dataclass',
            'marshmallow-union',
            'ujson'
      ],
      zip_safe=False)