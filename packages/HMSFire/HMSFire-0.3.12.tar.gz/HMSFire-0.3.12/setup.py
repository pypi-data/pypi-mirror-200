from setuptools import setup, find_packages


setup(
    name='HMSFire',
    version='0.3.12',
    license='MIT',
    author="Joel",
    author_email='joel.chacon@cimat.mx',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='This is a proof of concept package for Hazard Mapping System Fire Analysis',
    long_description='**HMSFire** makes searching, downloading and retrieving fire remote-sensing information easy. <BR> The information managed by this package is taken from https://www.ospo.noaa.gov/Products/land/hms.html#maps/ <BR> This package is developed as an effort to offer data more accessible outside the atmospheric scientific community.',
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
