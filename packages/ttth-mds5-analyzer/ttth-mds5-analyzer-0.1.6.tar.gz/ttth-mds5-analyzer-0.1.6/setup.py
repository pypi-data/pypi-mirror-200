from setuptools import setup, find_packages


setup(
    name='ttth-mds5-analyzer',
    version='0.1.6',
    license='MIT',
    author="Data Farmer",
    author_email='datafarmer2019@gmail.com',
    packages=find_packages('analyzer'),
    package_dir={'': 'analyzer'},
    package_data={'': ['*.txt']},
    url='https://github.com/liemvt2008/mds5-analyzer',
    keywords='mds5-analyzer',
    install_requires=[
            'matplotlib',
            'pandas',
            'seaborn',
            'scipy',
            'statsmodels',
            'scipy',
            'regex',
            'underthesea',
            'setuptools'
      ],

)