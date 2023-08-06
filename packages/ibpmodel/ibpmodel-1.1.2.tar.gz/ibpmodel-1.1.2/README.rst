Ionospheric Bubble Probability (IBP)
====================================

The ionospheric bubble probability statistical model is a Swarm L2 product, named IBP_CLI. The output of the Ionospheric Bubble Probability (IBP) product is an index, that depends  on the day of year or the month of the year, geographic longitude, local time and solar flux index. 

The output floating point index ranges 0-1 and characterizes the percentage probability of low latitude bubble occurence at the specified time, location and solar flux.

This empirical IBP model  has been derived from magnetic observations obtained by the CHAMP and Swarm missions. The model is representative for the altitude range 350 - 500 km and low geographic latitudes of +/- 45 degree.

.. inclusion-marker-install

Documentation
-------------

Detailed documentation can be found at: `<https://ibp-model.readthedocs.io>`_

Quick Start
-----------


Installation
^^^^^^^^^^^^

Using pip:

.. code-block:: console

    $ pip install ibpmodel


Dependencies:

- numpy
- pandas
- matplotlib
- scipy
- cdflib


Usage
^^^^^
The return value of the function *ibpmodel.calculateIBPindex()* is of type pandas.DataFrame.


.. code-block:: python

    >>> from ibpmodel import *
    >>> calculateIBPindex(day_month=15,    # Day of Year or Month 
                  longitude=0,                        # Longitude in degree
                  local_time=20.9,                    # Local time in hours 
                  f107=150)                           # F10.7 cm Solar Flux index
       Doy  Month  Lon    LT  F10.7     IBP
    0   15      1    0  20.9    150  0.3547

.. code-block:: python

    >>> calculateIBPindex(day_month=['Jan','Feb','Mar'], local_time=22)
         Doy  Month  Lon  LT  F10.7     IBP
    0     15      1 -180  22    150  0.0739
    1     15      1 -175  22    150  0.0722
    2     15      1 -170  22    150  0.0717
    3     15      1 -165  22    150  0.0728
    4     15      1 -160  22    150  0.0771
    ..   ...    ...  ...  ..    ...     ...
    211   74      3  155  22    150  0.2061
    212   74      3  160  22    150  0.2025
    213   74      3  165  22    150  0.1994
    214   74      3  170  22    150  0.1967
    215   74      3  175  22    150  0.1943

   [216 rows x 6 columns]

.. code-block:: python

    >>> plotIBPindex(doy=349)
    >>>

.. image:: https://igit.iap-kborn.de/ibp/ibp-model/-/raw/main/docs/source/_static/example_plotIBP.png
    :alt: Contour plot of the IBP index for the given day
    :align: center

.. code-block:: python

    >>> plotButterflyData(f107=150)
    >>>

.. image:: https://igit.iap-kborn.de/ibp/ibp-model/-/raw/main/docs/source/_static/example_plotButterfly.png
    :alt: Contour plot of result from function ButterflyData()  
    :align: center



.. inclusion-marker-reference

References
----------


*Stolle et al.*, `An empirical climatological model of the occurrence of F region equatorial plasma irregularities <https://igit.iap-kborn.de/ibp/ibp-model/-/raw/main/docs/source/_static/8thSwarmDataQualityWorkshop_slides.pdf>`_, 8th Swarm data quality workshop at ESA/ESRIN, October 2017. 

*Lucas Schreiter*, Anwendungsorientierte Modellierung der Auftretenswahrscheinlichkeit und relativen Häufigkeit von äquatorialen Plasmabubbles,  Master's thesis, Institute of Mathematics, University of Potsdam, 2016. (in German only.)

.. inclusion-marker-acknow


