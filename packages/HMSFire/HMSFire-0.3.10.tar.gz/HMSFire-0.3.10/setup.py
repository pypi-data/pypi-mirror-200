from setuptools import setup, find_packages


setup(
    name='HMSFire',
    version='0.3.10',
    license='MIT',
    author="Joel",
    author_email='joel.chacon@cimat.mx',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='This is a proof of concept package for Hazard Mapping System Fire Analysis',
    long_description='**HMSFire** make searching, downloading and retrieving data of the Hazard Mapping System easy https://www.ospo.noaa.gov/Products/land/hms.html#maps/ This package is developed as an effor to offer data more accessible outside the atmospheric scientific community.',
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
