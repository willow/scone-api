import numpy as np
from src.libs.numpy_utils import array_utils

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20])

def test_filter_by_median_absolute_standard_deviation():
  y = array_utils.filter_by_median_absolute_standard_deviation(x)
  assert y.max() == 9

def test_filter_by_median_absolute_deviation():
  y = array_utils.filter_by_median_absolute_deviation(x)
  assert y.max() == 10
