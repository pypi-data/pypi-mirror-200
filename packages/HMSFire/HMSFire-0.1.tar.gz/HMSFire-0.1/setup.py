from setuptools import setup, find_packages


setup(
    name='HMSFire',
    version='0.1',
    license='MIT',
    author="Joel",
    author_email='joel.chacon@cimat.mx',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://ospo-hms-fire.readthedocs.io/en/latest/',
    keywords='HMSFirepy project',
    install_requires=[
          'basemap',
          'pandas',
          'matplotlib',
          'requests',
          'datetime',
      ],

)
