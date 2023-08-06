

HMSFire Project
===============
HMSFire make searching, downloading and retrieving data of the Hazard Mapping System easy.

To take a look at some examples make sure to read `<https://ospo-hms-fire.readthedocs.io/en/latest/>`
Installing
============

.. code-block:: bash

    pip install HMSFire

Usage
=====

.. code-block:: bash

    >>>from OSPO.HMSFire import HMSF
    >>>Fires = HMSF.HMSFire(startDate='2023-01-01', endDate='2023-02-01')
    >>>data = Fires.getDataFrame()
    >>>Fires.plot()
