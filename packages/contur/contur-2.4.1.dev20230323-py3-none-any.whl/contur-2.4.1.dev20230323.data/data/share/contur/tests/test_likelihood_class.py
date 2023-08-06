import pytest
from pytest import raises
import pickle
import os
import numpy as np
from importlib import reload
import contur
import contur.factories.likelihood as lh
import contur.config.config as cfg

test_dir = os.path.dirname(os.path.abspath(__file__))
args_path = os.path.join(test_dir, 'sources/likelihood_data.p')
with open(args_path, 'rb') as f:
    master_data_dic = pickle.load(f)

contur.config = reload(contur.config)
def check_logger():
  try:
    cfg.contur_log.debug("test")
  except:
    # set up logger if there is none, eg for tests
    cfg.setup_logger("{0}.log".format('likelihoods'))
    cfg.contur_log.debug("Setting up logger")
    
def build_lh():

    cfg.setup_logger(filename="contur.log")    
    return  lh(bw=master_data_dic['bw'][0],
                                        nobs=master_data_dic['nob'][0],
                                        cov=master_data_dic['cov'][0],
                                        uncov=master_data_dic['uncov'][0],
                                        bg=master_data_dic['bg'][0],
                                        s=master_data_dic['s'][0],
                                        serr=master_data_dic['serr'][0],
                                        theorycov=master_data_dic['theCov'][0], theoryuncov=master_data_dic['thunCov'][0],
                                        nuisErrs=master_data_dic['nuiserr'][0], thErrs=master_data_dic['thErrs'][0],
                                        ratio=master_data_dic['ratio'][0],
                                        profile=master_data_dic['profile'][0],
                                        useTheory=master_data_dic['usetheory'][0],
                                        lumi=master_data_dic['lumi'][0],
                                        sxsec=master_data_dic['sxsec'][0], #< and uncertainty?
                                        bxsec=master_data_dic['bxsec'][0], #< TODO: a hack for profiles etc. Improve?
                                        tags=master_data_dic['tags'][0])

# tests for ts_to_pval method
def test_ts_to_pval_monotonic():
    check_logger()
    assert lh.ts_to_pval(0) > lh.ts_to_pval(1)    

def test_ts_to_pval_pass_numpy_array():
    check_logger()
    numpy_array = np.array([[1,2], [3,4]])
    assert lh.ts_to_pval(numpy_array).shape == (2,2)

# tests for ts_to_cls method
def test_ts_to_cls_passing_a_single_tuple_in_list_return_single_cls():
    check_logger()
    test_stats = [(1,1)]
    print(test_stats)
    assert len(lh.ts_to_cls(test_stats,"test")) == 1

def test_ts_to_cls_signal_equals_background_cls_zero():
    check_logger()
    test_stats = [(1,1)]
    assert lh.ts_to_cls(test_stats,"test")[0] == 0

def test_ts_to_cls_signal_greater_than_background_cls_between_0_1():
    check_logger()
    test_stats = [(1,0)]
    assert (lh.ts_to_cls(test_stats,"test")[0] < 1) and (lh.ts_to_cls(test_stats,"test")[0] > 0)

def test_ts_to_cls_signal_less_background_set_to_zero():
    check_logger()
    test_stats = [(0,1)]
    assert lh.ts_to_cls(test_stats,"test")[0] == 0

def test_ts_to_cls_passed_tuple_same_as_list():
    check_logger()
    test_stats = (1,1)
    test_stats_list = [test_stats]
    assert lh.ts_to_cls(test_stats,"test") == lh.ts_to_cls(test_stats_list,"test")

def test_sort_blocks_throws_exception_if_passed_empty_list():
    check_logger()
    with raises(ValueError) as exception:
        lh.sort_blocks([],cfg.databg)

def test_build_full_likelihood_throws_exception_if_passed_empty_list():
    check_logger()
    with raises(ValueError) as exception:
        lh.build_full_likelihood([],cfg.databg)
        
def test_like_block_ts_to_cls_throws_exception_if_passed_empty_list():
    check_logger()
    with raises(ValueError) as exception:
        lh.likelihood_blocks_ts_to_cls([],cfg.databg)

def test_find_dominant_ts_throws_exception_if_passed_empty_list():
    check_logger()
    with raises(ValueError) as exception:
        lh.likelihood_blocks_find_dominant_ts([],cfg.databg)

                                                
