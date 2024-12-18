import os

os.environ["OMP_NUM_THREADS"] = "8"
os.environ["OPENBLAS_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["VECLIB_MAXIMUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"

import time

from antenna_designer import pysim
from antenna_designer.core import save_or_show
from antenna_designer.pysim_accelerators import dist_outer_product

from matplotlib import pyplot as plt
import numpy as np
from icecream import ic

import skrf

fn = None
#fn = '/dev/null'



def test_extension():
    nsegs = 20000
    pts = np.array([[0,0,z] for z in range(nsegs+1)])/(2*nsegs)

    t = time.time()
    for i in range(10):
        _ = dist_outer_product(pts, pts)
    ic('dist_outer_product', time.time()-t)


def test_impedance_nsegs():
    xs = [21, 41, 61, 81, 101, 201, 401, 801]
    xs = np.array(xs)
    z0 = 50



    fig, ax0 = plt.subplots()
    skrf.plotting.smith(draw_labels=True, chart_type='z')


    #plt.plot(xs, np.abs(zs), marker='s')
    #plt.plot(xs, np.imag(zs), marker='s')

    for ntrap in [0,2,8,16]:

        zs = []
        for nsegs in xs:
            z, _ = pysim.PySim(nsegs=nsegs).augmented_compute_impedance(ntrap=ntrap)
            ic(nsegs,z)
            zs.append(z)

        zs = np.array(zs)

        normalized_zs = zs/z0
        color = 'tab:green'
        reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
        skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    zs = []
    for nsegs in xs:
        z, _ = pysim.PySim(nsegs=nsegs).vectorized_compute_impedance()
        ic(nsegs,z)
        zs.append(z)

    zs = np.array(zs)



    normalized_zs = zs/z0
    color = 'tab:red'
    reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
    skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    #plt.plot(xs, np.abs(zs), marker='s')
    #plt.plot(xs, np.imag(zs), marker='s')

    save_or_show(plt, fn)


def test_svd_currents_nsmallest():

    nsegs=101

    _, (i, i_svd_all) = pysim.PySim(nsegs=nsegs, run_svd=True).vectorized_compute_impedance()

    color = 'tab:blue'
    plt.plot(np.abs(i), color=color)

    color = 'tab:red'
    plt.plot(np.abs(i_svd_all), color=color)

#    for rcond in [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]:
    color = 'tab:green'
    for nsmallest in [1, 2, 3]:
        _, (_, i_svd) = pysim.PySim(nsegs=nsegs,nsmallest=nsmallest, run_svd=True).vectorized_compute_impedance()
        ic(nsmallest, np.linalg.norm(i_svd-i_svd_all))
        plt.plot(np.abs(i_svd), color=color)

    save_or_show(plt, fn)


def test_iterative_improvement():
    pysim.PySim(nsegs=401, run_iterative_improvement=True).vectorized_compute_impedance()


def test_sweep_halfdriver():

    nsegs=1001
    z0 = 50

    fig, ax0 = plt.subplots()
    skrf.plotting.smith(draw_labels=True, chart_type='z')

    xs = np.linspace(.9,1,21)

    t = time.time()
    zs = []
    for x in xs:
        z, _ = pysim.PySim(halfdriver_factor=x,nsegs=nsegs).stamp_vectorized_compute_impedance()
        zs.append(z)
    print('stamp', time.time()-t)
    zs = np.array(zs)

    normalized_zs = zs/z0
    color = 'tab:red'
    reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
    skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    t = time.time()
    zs = []
    for x in xs:
        z, _ = pysim.PySim(halfdriver_factor=x,nsegs=nsegs).vectorized_compute_impedance()
        zs.append(z)
    print('vectorized', time.time()-t)
    zs = np.array(zs)

    normalized_zs = zs/z0
    color = 'tab:blue'
    reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
    skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    t = time.time()
    zs = []
    for x in xs:
        z, _ = pysim.PySim(halfdriver_factor=x,nsegs=nsegs).augmented_compute_impedance(ntrap=4)
        zs.append(z)
    print('augmented ntrap=4', time.time()-t)
    zs = np.array(zs)

    normalized_zs = zs/z0
    color = 'tab:green'
    reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
    skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    t = time.time()
    zs = []
    for x in xs:
        z, _ = pysim.PySim(halfdriver_factor=x,nsegs=nsegs).augmented_compute_impedance(ntrap=16)
        zs.append(z)
    print('augmented ntrap=16', time.time()-t)
    zs = np.array(zs)

    normalized_zs = zs/z0
    color = 'tab:purple'
    reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
    skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')


    if False:
        t = time.time()
        zs = []
        for x in xs:
            z, _ = pysim.PySim(halfdriver_factor=x,nsegs=nsegs).compute_impedance()
            zs.append(z)
        print('slow', time.time()-t)
        zs = np.array(zs)

        normalized_zs = zs/z0
        color = 'tab:green'
        reflection_coefficients = (normalized_zs-1)/(normalized_zs+1)
        skrf.plotting.plot_smith(reflection_coefficients, color=color, draw_labels=True, chart_type='z', marker='s', linestyle='None')

    save_or_show(plt, fn)

def test_slow():
    ps = pysim.PySim()
    z, i = ps.compute_impedance()

nsegs = 801
nrepeat = 1
ntrap = 8

def test_stamp():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.stamp_vectorized_compute_impedance(engine='fusion')
    ic('stamp', time.time()-t)

def test_augmented_python_ntrap0():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.augmented_compute_impedance(ntrap=0, engine='python')
    ic('augmented python ntrap=0', time.time()-t)

def test_augmented():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.augmented_compute_impedance(ntrap=ntrap, engine='accelerated')
    ic('augmented accelerated', time.time()-t)

def test_augmented_python():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.augmented_compute_impedance(ntrap=ntrap, engine='python')
    ic('augmented python', time.time()-t)

def test_augmented_test():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.augmented_compute_impedance(ntrap=ntrap, engine='test')
    ic('augmented test', time.time()-t)

def test_stamp_split():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.stamp_vectorized_compute_impedance(engine='split')
    ic('stamp_split', time.time()-t)

def test_stamp_python():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.stamp_vectorized_compute_impedance(engine='python')
    ic('stamp_split', time.time()-t)

def test_vectorized():
    ps = pysim.PySim(nsegs=nsegs)

    t = time.time()
    for i in range(nrepeat):
        z, i = ps.vectorized_compute_impedance()
    ic('vectorized', time.time()-t)
