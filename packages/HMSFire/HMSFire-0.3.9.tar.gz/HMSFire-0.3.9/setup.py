from setuptools import setup, find_packages


setup(
    name='HMSFire',
    version='0.3.9',
    license='MIT',
    author="Joel",
    author_email='joel.chacon@cimat.mx',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://ospo-hms-fire.readthedocs.io/en/latest/',
    keywords='HMSFirepy project',
    summary='test description',
    package_data={'HMSFire': ['src/OSPO/HMSFire/*csv']},
    include_package_data=True,
    install_requires=[
          'basemap',
          'pandas',
          'matplotlib',
          'requests',
          'datetime',
      ],

)
