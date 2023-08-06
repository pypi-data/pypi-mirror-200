from setuptools import setup, find_packages


setup(
    name='HMSFire',
    version='0.3.4',
    license='MIT',
    author="Joel",
    author_email='joel.chacon@cimat.mx',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://ospo-hms-fire.readthedocs.io/en/latest/',
    keywords='HMSFirepy project',
    summary='test description',
    package_data={'': ['license.txt']},
    include_package_data=True,
    install_requires=[
          'basemap',
          'pandas',
          'matplotlib',
          'requests',
          'datetime',
      ],

)
