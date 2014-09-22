import numpy as np


def filter_by_median_absolute_deviation(data, m=2.):
  # credit: http://stackoverflow.com/a/16562028/173957

  d = np.abs(data - np.median(data))
  mdev = np.median(d)
  s = d / mdev if mdev else 0.
  return data[s < m]


def filter_by_median_absolute_standard_deviation(data):
  # credit: http://stackoverflow.com/a/16562028/173957 and guidetodatamining.com chapter 4

  # get median
  median = np.median(data)

  # normalize the median for each val in the list
  abs_data = np.abs(data - median)

  # sample size = data.size - 1
  # refer to guidetodatamining chapter 4 for abs standard devation
  mdev = (1 / (data.size - 1)) * abs_data.sum()

  s = abs_data <= mdev

  return data[s]
