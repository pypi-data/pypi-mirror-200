#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:52:31 2022

@author: iwehner
"""

import pytest
import numpy as np
import os

import ibp

@pytest.mark.parametrize("a,b,expected",[([1, 2, 3],['A', 'B'], [[1, 1, 2, 2, 3, 3],['A', 'B', 'A', 'B', 'A', 'B']])] )
def test_tiler(a,b,expected):
    result = ibp.tiler(a,b)
    np.testing.assert_array_equal(result, expected)

def test_align_time_of_year():
    result = ibp.align_time_of_year(162,3)
    assert result == (162, 6)
   
file = os.path.abspath(os.path.join(ibp.__file__,'SW_TEST_IBP_CLI_2__00000000T000000_99999999T999999_0001.cdf'))
@pytest.mark.parametrize("a,df", [(file, 118.517957224598)])
def test_read_model_file(a,df):
    data = ibp.read_model_file(a)
    result = data['Intensity'][2]
    assert result == df