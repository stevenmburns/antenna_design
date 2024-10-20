#
#  Simple vertical monopole antenna simulation using python-necpp
#  pip install necpp
#
from necpp import *
import math
import numpy as np

from scipy.optimize import minimize_scalar, minimize


def handle_nec(result):
  if (result != 0):
    print(nec_error_message())

def geometry(freq, slope, base, length):
  
  conductivity = 5.8e7 # Copper
  ground_conductivity = 0.002
  ground_dielectric = 10

  wavelength = 3e8/(1e6*freq)
  n_seg = 50
  eps = 0.01

  # length = sqr(y ^2 + (y*slope)^2) = y * sqrt(1+slope^2)
  # length = sqr((z/slope) ^2 + z2) = z * sqrt(1+1/slope^2)

  x = 0.5*length/math.sqrt(1+slope**2)
  z = math.sqrt((0.5*length)**2 - x**2)

  nec = nec_create()
  handle_nec(nec_wire(nec, 1, n_seg, 0, -x,   base-z, 0, -eps, base,   0.002, 1.0, 1.0))
  handle_nec(nec_wire(nec, 2, 3,     0, -eps, base,   0, eps,  base,   0.002, 1.0, 1.0))
  handle_nec(nec_wire(nec, 3, n_seg, 0, eps,  base,   0, x,    base-z, 0.002, 1.0, 1.0))
  handle_nec(nec_geometry_complete(nec, 1))
  handle_nec(nec_ld_card(nec, 5, 0, 0, 0, conductivity, 0.0, 0.0))
  handle_nec(nec_gn_card(nec, 0, 0, ground_dielectric, ground_conductivity, 0, 0, 0, 0))
  handle_nec(nec_fr_card(nec, 0, 1, freq, 0))
  handle_nec(nec_ex_card(nec, 0, 2, 2, 0, 1.0, 0, 0, 0, 0, 0)) 

  return nec

def impedance(freq, slope, base, length):
  nec = geometry(freq, slope, base, length)
  handle_nec(nec_xq_card(nec, 0)) # Execute simulation
  index = 0
  z = complex(nec_impedance_real(nec,index), nec_impedance_imag(nec,index))
  nec_delete(nec)
  return z

def objective(independent_variables, freq, base):
    (length, slope) = independent_variables
    z = impedance(freq, slope, base, length)
    print("Impedance at freq = %0.2f, slope=%0.2f, base=%0.2f, length=%0.2f : (%6.1f,%+6.1fI) Ohms" % (freq, slope, base, length, z.real, z.imag))
    return (z - 50).real**2 + (z-50).imag**2

if __name__ == '__main__':
  freq, slope, base, length = 14.3, .5, 10, 10.5

  result = minimize(objective, x0=(length, slope), method='Powell', bounds=((9,11),(0,1)), args=(freq, base))
  print(result)
  length, slope = result.x

  z = impedance(freq = freq, slope=slope, base = base, length = length)
  print("Impedance at freq = %0.2f, slope=%0.2f, base=%0.2f, length=%0.2f : (%6.1f,%+6.1fI) Ohms" % (freq, slope, base, length, z.real, z.imag))





