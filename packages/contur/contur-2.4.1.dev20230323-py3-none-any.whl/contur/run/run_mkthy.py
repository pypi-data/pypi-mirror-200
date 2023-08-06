
# functions build theory reference yodas from various raw inputs.

import contur
import re
import sys
import os
import rivet
import yoda
from contur.data.sm_theory_builders import *
import contur.config.config as cfg
import contur.data.static_db as cdb
import contur.util.utils as cutil
from contur.run.arg_utils import setup_common

def make_sm_yoda(analysis):
    '''
    Make the SM yoda file for analysis

    This is a pretty clunky and bespoke set of scripts because it has to handle data from a very varied set of sources.
    From these sources it produces standard SM prediction files to be stored in data/Theory

    If source == "REF", will look for additonal y axes on the REF plots (labelled y02 by default, others from axis parameter) 
                        and replace them to convert into y01 /THY versions. 
                        Filters out analysis objects which are not assigned to an analysis pool.

    if source == "RAW" will look in the TheoryRaw areas for /THY/ yodas and just filter them.

    if source == "HEPDATA" will look in the TheoryRaw area for a (possibly modified) HEPDATA download where the y-axis name
                                  should be replace y-axis of the REF histogram name

    if source == "HEPDATA_APPEND" will look in the TheoryRaw area for a (possibly modified) HEPDATA download where the y-axis name
                                  should be appended to the REF histogram name

    if source == "SPECIAL" invoke a special routine for this analysis (usually reading from
                           text files supplied by theorists).

    the above will only be applied to histograms with a regexp match to the pattern.

    '''

    ao_out = []
    a_name = analysis.shortname    
    if analysis.sm() is None:
        return
    

    output_aos = {}
    
    for prediction in analysis.sm():
    
        # only read each prediction file once
        if prediction.file_name not in output_aos:
            output_aos[prediction.file_name] = []
        
        if prediction.origin == "RAW":

            cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
            f = os.path.join(os.getenv("CONTUR_ROOT"),"data","TheoryRaw",a_name,a_name)
            if prediction.axis is not None:
                f = f+"-Theory"+prediction.axis+".yoda"
            else:
                f = f+"-Theory.yoda"
            if  os.path.isfile(f):
                cfg.contur_log.debug("Reading from {}".format(f))
                aos = yoda.read(f)
                for path, ao in aos.items():

                    if rivet.isTheoryPath(path) and analysis.name in path:
                        pool = cdb.get_pool(path=path)
                        if pool is not None:
                            if ao.type() == "Scatter1D":
                                ao = cutil.mkScatter2D(ao)
                            ao.setTitle(prediction.short_description)
                            output_aos[prediction.file_name].append(ao)
                        else:
                            cfg.contur_log.debug("No pool for {}".format(path))

            else:
                cfg.contur_log.critical("File {} does not exist.".format(f))

        elif prediction.origin == "REF":
            # from the installed ref data (with traditional -yNNN axis labelling)
            cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
            
            f = contur.util.utils.find_ref_file(analysis)
            aos = yoda.read(f)
            for path, ao in aos.items():            
                pool = cdb.get_pool(path=path)
                if pool is not None:
                    if re.search(prediction.pattern, path) and cdb.validHisto(path,filter=False):
                        cfg.contur_log.debug("Found a prediction for {}. Axis is {}.".format(path,prediction.axis))
                        # get the appropriate theory axis for this plot (assumes they are the same length)
                        thypath = path[:-len(prediction.axis)]+prediction.axis
                        try:
                            thy_ao = aos[thypath]
                        except:
                            cfg.contur_log.debug("not found")
                            continue
                                                    
                        if thy_ao.type() == "Scatter1D":
                            thy_ao = cutil.mkScatter2D(thy_ao)
                        thy_ao.setPath("/THY"+path[4:])
                        thy_ao.setTitle(prediction.short_description)
                        output_aos[prediction.file_name].append(thy_ao)

        elif prediction.origin.startswith("HEPDATA"):
            
            # from specially downloaded HEPData
            cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
            f = os.path.join(os.getenv("CONTUR_ROOT"),"data","TheoryRaw",a_name,a_name)
            f = f+".yoda.gz"

            aos = yoda.read(f)            
            cfg.contur_log.debug("Reading from {}".format(f))
            for path, ao in aos.items():            
                pool = cdb.get_pool(path=path)
                cfg.contur_log.debug("Pool is {} for {}".format(pool.id,path))
                if pool is not None:
                    if re.search(prediction.pattern, path) and cdb.validHisto(path,filter=False):
                        cfg.contur_log.debug("Getting a prediction for {}. Axis is {}.".format(path,prediction.axis))
                        if prediction.origin.endswith("APPEND"):
                            thypath = path+prediction.axis
                        else:
                            thypath = path[:-len(prediction.axis)]+prediction.axis
                        try:
                            thy_ao = aos[thypath]
                            cfg.contur_log.debug("Found a prediction for {} at {}.".format(path,thypath))
                        except:
                            cfg.contur_log.debug("not found")
                            continue

                        if thy_ao.type() == "Scatter1D":
                            thy_ao = cutil.mkScatter2D(thy_ao)
                        thy_ao.setPath("/THY"+path[4:])
                        thy_ao.setTitle(prediction.short_description)
                        output_aos[prediction.file_name].append(thy_ao)
                        
        elif prediction.origin == "SPECIAL":

            if analysis.name == "ATLAS_2016_I1457605":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2016_I1457605(prediction)

            if analysis.name == "ATLAS_2017_I1645627":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2017_I1645627(prediction)

            if analysis.name == "ATLAS_2012_I1199269":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2012_I1199269(prediction)
                
            if analysis.name == "ATLAS_2017_I1591327":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2017_I1591327(prediction)

            if analysis.name == "ATLAS_2016_I1467454:LMODE=MU":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                # this actually does both EL and MU
                do_ATLAS_2016_I1467454(prediction)

            if analysis.name == "CMS_2017_I1467451":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_CMS_2017_I1467451(prediction)

            if analysis.name == "ATLAS_2015_I1408516:LMODE=MU":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                # this actually does both EL and MU
                do_ATLAS_2015_I1408516(prediction)

            if analysis.name == "ATLAS_2019_I1725190":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2019_I1725190(prediction)
                
            if analysis.name == "ATLAS_2021_I1852328":
                cfg.contur_log.info("Making SM theory for {}, prediction {}".format(analysis.name,prediction.id))            
                do_ATLAS_2021_I1852328(prediction)
                
            if analysis.name == "ATLAS_2019_I1764342":
                cfg.contur_log.info("Making SM theory for {} prediction {}".format(analysis.name,prediction.id))
                do_ATLAS_2019_I1764342(prediction)
                
        else:
            cfg.contur_log.critical("Unknown source {}".format(source))
            sys.exit(1)

    for fname, ao_out in output_aos.items():
        if len(ao_out)>0:
            yoda.write(ao_out, fname)
        elif prediction.origin != "SPECIAL":
            cfg.contur_log.warning("No objects found to write to {}".format(fname))
    return


def main(args):
    """
    Main programme to run over the known analysis and build SM theory yodas from the TheoryRaw or REF areas.
    """
#    cfg.setup_logger(filename="contur_mkthy.log")
    setup_common(args)
    print("Writing log to {}".format(cfg.logfile_name))

    if args['ANAUNPATTERNS']:
        cfg.vetoAnalyses = args['ANAUNPATTERNS']
    if args['ANAPATTERNS']:
        cfg.onlyAnalyses = args['ANAPATTERNS']

    cfg.input_dir = args["INPUTDIR"]
    cfg.contur_log.info("Looking for raw theory files in {}".format(cfg.input_dir))
        
#    do_all = (args['ANALYSIS'] == "all")

    # -------------------------------------
    for analysis in cdb.get_analyses(filter=False):
        if cutil.analysis_select(analysis.name):
            make_sm_yoda(analysis)            
        
