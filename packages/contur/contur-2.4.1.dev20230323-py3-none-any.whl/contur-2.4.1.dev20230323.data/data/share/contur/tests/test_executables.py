try:
    import yoda, rivet, contur
except:
    print("Exiting test suite, could not find the dependencies of YODA, Rivet or contur in PYTHONPATH")
    raise
    
import os
import shutil

import pytest
import yaml

import pickle as pkl
from pandas._testing import assert_frame_equal

import contur.config.config as cfg

test_dir = os.path.join(os.getenv("PWD"))
# define the test sandbox
result_dir = cfg.paths.user_path("tests")

from contur.run.run_analysis import main as main_ana
from contur.run.run_smtest import main as main_sm
from contur.run.run_extract_xs_bf import main as main_xsbf
from contur.run.run_plot import main as main_mapplot
from contur.run.arg_utils import get_args
from contur.export.contur_export import export
from contur.oracle.cli import start_oracle

from importlib import reload 

args_path = os.path.join(test_dir, 'sources/grid_cl_args.yaml')
with open(args_path, 'r') as f:
    arguments_examples = yaml.load(f, yaml.FullLoader)


def build_executable_cmd(cl_args_dict):
    cl_string=[cl_args_dict["command"]]
    try:
        for v in cl_args_dict["args"]:
            #load the optional args to a string
            cl_string.append("{}".format(v))
    except:
        pass
    try:
        for k,v in cl_args_dict["options"].items():
            #load the optional args to a string
            cl_string.append("--%s=%s" % (k,v))
    except:
        pass
    try:
        for v in cl_args_dict["switches"]:
            #load the optional switches to the string
            cl_string.append("-%s" % v)
    except:
        pass

    return cl_string


main_run_cmds={}

for k,v in arguments_examples.items():
    cmd=build_executable_cmd(v)
    cfg.output_dir=result_dir
    cfg.smdir=result_dir
    cfg.input_dir=result_dir
    if "contur-smtest" in cmd:
        main_run_cmds[k]=get_args(cmd[1:],'smtest')
    elif "contur-extract-xs-bf" in cmd:
        main_run_cmds[k]=get_args(cmd[1:],'extract_xs_bf')
    elif "contur-plot" in cmd:
        main_run_cmds[k]=get_args(cmd[1:],'plot')
    elif "contur-export" in cmd:
        v1=v
        v1['export_test']=None
        main_run_cmds[k]=v1
    elif "contur-oracle" in cmd:
        v1=v
        v1['oracle_test']=None
        main_run_cmds[k]=v1
    else:
        main_run_cmds[k]=get_args(cmd[1:],'analysis')
        

# @pytest.mark.first
@pytest.mark.parametrize("fixture", main_run_cmds.values(), ids=main_run_cmds.keys())
def test_run_main(fixture):
    contur.config.config = reload(contur.config.config)
    cfg.output_dir=result_dir
    cfg.smdir=result_dir
    #print("FIXTURE KEYS",fixture.keys())
    cfg.input_dir=result_dir
    if "yodafiles" in fixture.keys():
        main_ana(fixture)
    elif "foldBRs" in fixture.keys():
        main_xsbf(fixture)
    elif "variables" in fixture.keys():
        main_mapplot(fixture)
    elif "export_test" in fixture.keys():
        export(fixture["options"]["input"], fixture["options"]["output"])
    elif "oracle_test" in fixture.keys():
        oracle_dir = os.path.join(result_dir,"oracle")
        os.system("cp -r sources/oracle {}".format(result_dir))
        os.system("cp {}/oracle.config.0.yaml {}/oracle.config.yaml".format(oracle_dir,oracle_dir))
        start_oracle(oracle_dir)
    else:
        main_sm(fixture)


def test_regression_single_yoda_run():
    """
    Regression test of current contur output on single yoda file against base 
    output given by live version of contur code run on same yoda file.
    
    Test will fail if an update to contur code changes the txt file output from
    a single contur run
    
    """
    args_path = os.path.join(test_dir, 'sources/single_yoda_run.txt')
    with open(args_path) as sf:
        base = sf.read().splitlines(True)
    
    args_path = os.path.join(result_dir, 'Summary.txt')
    with open(args_path) as sf:
        target = sf.read().splitlines(True)
    assert base[3:] == target[3:] #the text file has information about where contur was run,
                                          #we don't want to include this in our comparison.

    
def test_regression_grid_run():
    """
    Regression test of current contur output on grid against base 
    output given by live version of contur code run on same the same grid.
    
    Test will fail if an update to contur code changes the map file (read with pickle
    to get the Depot contur object) output from a grid run
    
    """
    
    args_path = os.path.join(test_dir, 'sources/contur.map')
    with open(args_path, 'rb') as file:
        base = pkl.load(file)._build_frame()
    args_path = os.path.join(result_dir, 'contur.map')
    with open(args_path, 'rb') as file:
        target = pkl.load(file)._build_frame()
    assert_frame_equal(base, target)

def test_export():
    """
    Regression test of exporting a map to csv 
    
    Test will fail if an update to contur-export code changes the format of the resulting csv.
    
    """
    
    args_path = os.path.join(test_dir, 'sources/contur.csv')
    with open(args_path) as sf:
        base = sf.read().splitlines(True)
    args_path = os.path.join(result_dir, 'contur.csv')
    with open(args_path) as sf:
        target = sf.read().splitlines(True)
    assert base == target
    

'''
#For now lets comment this out so at a basic level the tests run the executables once but nothing fancy

def test_calculations():
    target_path = os.path.join(test_dir, "sources/contur.map")
    performed_path = os.path.join(test_dir, "tmp/single/contur.map")

    with open(target_path, 'rb') as f:
        file_target = pickle.load(f)
        target = {}
        for bucket in file_target.conturDepotInbox[0].yoda_factory.sortedBuckets:
            target[bucket.pools] = (bucket.CLs,bucket.tags)
    with open(performed_path, 'rb') as f:
        file_perf = pickle.load(f)
        perf = {}
        for bucket in file_perf.conturDepotInbox[0].yoda_factory.sortedBuckets:
            perf[bucket.pools] = (bucket.CLs,bucket.tags)

    for k,v in perf.items():
        print "Reference value %s, Reference histoIDs %s, Reference bucket %s" % (str(target[k][0]), target[k][1], k )
        print "Generated value %s, Generated histoIDs %s, Generated bucket %s \n" % (str(v[0]), v[1], k )
        assert numpy.isclose(target[k][0],v[0])
    return
'''

@pytest.mark.last
def test_teardown_module():
    """Clean up test area"""
    #direct = os.path.join(test_dir, 'tmp')
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    direct = os.path.join(test_dir, 'cache')
    #if os.path.exists(direct):
    #    shutil.rmtree(direct)

    #os.remove(os.path.join(test_dir,"entropy-sorted-predictions.csv"))
    #os.remove(os.path.join(test_dir,"probs.pdf"))
    #os.remove(os.path.join(test_dir,"sources/oracle/classifiers/classifier-2.pkl"))
    #os.remove(os.path.join(test_dir,"sources/oracle/input_points/input-points-2.csv"))
    #os.remove(os.path.join(test_dir,"sources/oracle/input_points/input-points-2.pkl"))
    #os.remove(os.path.join(test_dir,"sources/oracle/oracle.config.yaml"))
    #os.remove(os.path.join(test_dir,"sources/oracle/param_files/param_file_2.dat"))
    

