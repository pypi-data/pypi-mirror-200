Usage
=====

Calculation of IBP Index
------------------------

To calculate the IBP index use :py:func:`ibpmodel.ibpforward.calculateIBPindex()` function. It returns a pandas.DataFrame:

.. code-block:: python

   >>> from ibpmodel import calculateIBPindex
   >>> calculateIBPindex(day_month=15, longitude=0, local_time=20.9, f107=150)                           
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

   >>> calculateIBPindex(day_month=[1,15,31], longitude=[-170,175,170], 
      local_time=0, f107=120)
      Doy  Month  Lon  LT  F10.7     IBP
   0    1      1 -170   0    120  0.0274
   1    1      1  175   0    120  0.0304
   2    1      1  170   0    120  0.0324
   3   15      1 -170   0    120  0.0293
   4   15      1  175   0    120  0.0325
   5   15      1  170   0    120  0.0347
   6   31      1 -170   0    120  0.0341
   7   31      1  175   0    120  0.0378
   8   31      1  170   0    120  0.0403

Read coefficient file
---------------------

You can load the coefficient file. :py:func:`ibpmodel.ibpcalc.read_model_file()`:

.. code-block:: python

   >>> from ibpmodel import read_model_file
   >>> c = read_model_file()
   >>> c.keys()
   dict_keys(['Parameters', 'Intensity', 'Monthly_LT_Shift', 'Density_Estimators', 
      'Density_Estimator_Lons'])
   >>> c['Intensity']
   array([  -6.99518975,   -0.93264132,   96.49049553,    8.81167779,
         -135.50937181])





Plotting of the probability
---------------------------

There are two functions to plot IBP index. function :py:func:`ibpmodel.ibpforward.plotIBPindex()` and :py:func:`ibpmodel.ibpforward.plotButterflyData()`.
By default, the plot is displayed immediately. If you want to make changes or additions, the parameter getFig must be set equal to ``True``. 
Then you get matplat.axis as return value:

.. code-block:: python
   
   >>> import ibpmodel as ibp
   >>> ibp.plotIBPindex(doy=349)

.. image:: _static/example_plotIBP.png
   :alt: Contour plot of the IBP index for the given day
   :align: center
.. code-block:: python

   >>> ibp.plotButterflyData(f107=150)

.. image:: _static/example_plotButterfly.png
   :alt: Contour plot of result from function ButterflyData() 
   :align: center

.. code-block:: python
   
   >>> import matplotlib.pyplot as plt
   >>> ax=ibp.plotIBPindex(310,getFig=True)
   >>> plt.show()


