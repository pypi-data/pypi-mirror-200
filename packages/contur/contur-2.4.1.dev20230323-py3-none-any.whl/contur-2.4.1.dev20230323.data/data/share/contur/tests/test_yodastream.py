import pytest
import os
import pickle
from importlib import reload
import contur
from contur.run.arg_utils import get_argparser
from contur.run.arg_utils import get_args
from contur.run.run_analysis import main
import contur.config.config as cfg
import contur.util.utils as cutil
import gzip
from io import StringIO
import numpy as np

test_dir = os.path.join(os.getenv("PWD"))
# define the test sandbox
result_dir = cfg.paths.user_path("tests")


def test_yodastream():
    sourcepath = os.path.join(test_dir, "sources/myscan00/13TeV/0014/runpoint_0014.yoda.gz")

    with gzip.open(sourcepath, 'rt') as f:
        yodastream = StringIO(f.read())

    yodastream.seek(0)
    args = get_args("", "analysis")

    args["YODASTREAM"] = yodastream
    #Ask for all output types to test fully.
    args['YODASTREAM_API_OUTPUT_OPTIONS'] = ["LLR", "Pool_LLR", "Pool_tags", "CLs", "Pool_CLs"]

    #TODO @TP: copied this from the other tests. Is it needed?
    contur.config = reload(contur.config)

    summaryDict = main(args)
    stat_types = summaryDict.keys()

    comparisonpath = os.path.join(test_dir, "sources/yodastream_results_dict.pkl")
    with open(comparisonpath, 'rb') as f:
        compareDict = pickle.load(f)
    
    #Check consistency

    pkl_out = os.path.join(result_dir,"yodastream_results.pkl")

    try:

        if not (
            #LLR Values must be consistent -> this should mean CLs is also fine.
            (np.allclose(np.array([compareDict[i]["LLR"] for i in stat_types], dtype=float),
                np.array([summaryDict[i]["LLR"] for i in stat_types], dtype=float))) or
            #Pool-by-pool LLR values must also be consistent
            (np.allclose(np.concatenate([np.array(list(compareDict[i]["Pool_LLR"].values())) for i in stat_types]),
                np.concatenate([np.array(list(summaryDict[i]["Pool_LLR"].values())) for i in stat_types])))  
        ):
            #Dump a copy of the results dict for debugging if something is wrong
            #Or as a replacement version if e.g. new analyses/theory available.
            
            cutil.mkoutdir(result_dir)
            with open(pkl_out, "wb") as f:
                pickle.dump(summaryDict, f)
                print("Results do not match expected values - has an analysis been added?")
                assert(False)

    except:
        #Dump a copy of the results dict for debugging if something is wrong
        #Or as a replacement version if e.g. new analyses/theory available.
        cutil.mkoutdir(result_dir)
        with open(pkl_out, "wb") as f:
            pickle.dump(summaryDict, f)
        print("Results do not match expected values - has an analysis been added?")
        raise
    
