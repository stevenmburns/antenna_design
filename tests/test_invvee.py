from antenna import *
from invvee import *


def test_invvee_sweep_freq():
  sweep_freq(InvVeeBuilder(**get_invvee_data()), fn='invvee_sweep_freq.pdf')

def test_invvee_sweep_length():
  sweep(InvVeeBuilder(**get_invvee_data()), 'length', (4,6), fn='invvee_sweep_length.pdf')

def test_invvee_sweep_slope():
  sweep(InvVeeBuilder(**get_invvee_data()), 'slope', (.2,1), fn='invvee_sweep_slope.pdf')


def test_invvee_optimize():

  gold_params = get_invvee_data()

  params = optimize(InvVeeBuilder(**gold_params), ['length','slope'], z0=50)

  for k, v in gold_params.items():
    assert math.fabs(params[k]-v) < 0.01
