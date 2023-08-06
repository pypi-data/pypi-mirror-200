"""
Perform various manipulations on an existing contur scan grid or grids, but NOT the actual contur statistical analysis.

"""

import logging
import os
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import contur
import contur.data.data_access_db as cdba
import contur.config.config as cfg
from contur.config.config import ConturError
import contur.scan.grid_tools as cgt

def main(args):
    """
    arguments should be passed as a dictionary.

    """

    contur.run.arg_utils.setup_common(args)
    print("Writing log to {}".format(cfg.logfile_name))

    cfg.grid = args['GRID']
        
    if args['INIT_DB']:
        cfg.results_dbfile = cfg.path('data', 'DB', 'responsive_storage.db')
        cfg.contur_log.info("generate db with model and parameter data initialised")
        contur.data.generate_model_and_parameter()
        
    Clean = True
    if args['DO_NOT_CLEAN']:
        cfg.contur_log.info("Not removing unnecessary files from grid")
        Clean = False

    elif len(args['ANAPATTERNS'])>0 or len(args['ANAUNPATTERNS'])>0:
        cfg.onlyAnalyses = args['ANAPATTERNS']
        cfg.vetoAnalyses = args['ANAUNPATTERNS']
        cfg.contur_log.info("Extracting histograms from particular analyses into a new grid:")
        if len(args['ANAPATTERNS'])>0:
            cfg.contur_log.info("Analyses matching any of {} will be extracted".format(cfg.onlyAnalyses))
        if len(args['ANAUNPATTERNS'])>0:
            cfg.contur_log.info("Analyses matching any of {} will not be extracted (veto takes precedence).".format(cfg.vetoAnalyses))
        cgt.grid_loop(extract=True, clean=Clean)
        
    elif args['RM_MERGED']:
        cfg.contur_log.info("If unmerged yodas exist, unzipping them and removing merge yodas.")
        cgt.grid_loop(unmerge=True, clean=Clean)

    elif args['COMPRESS_GRID']:
        cfg.contur_log.info("Archiving this directory tree")
        cgt.grid_loop(archive=True)

    elif args['CHECK_GRID'] or args['CHECK_ALL']:
        cfg.contur_log.info("Checking directory tree")
        if args['CHECK_ALL']:
            cfg.contur_log.info("Also counting jobs without batch logs as failed")
        cgt.grid_loop(check=True, resub=args['RESUB'], check_all=args['CHECK_ALL'], queue=args['queue'])

    elif args['FINDPARAMS']:
        # find the specified parameter point.
        yoda_files = []
        paramList =  args['FINDPARAMS']

        if len(args['FINDPARAMS'])>0:        
            try:
                if not cfg.results_dbfile:
                    cfg.results_dbfile = cfg.path('data', 'DB', 'responsive_storage.db')

                if args['PARAM_DETAIL']:
                    yoda_files = cdba.show_param_detail_db(paramList)
                else:
                    yoda_files = cdba.find_param_point_db(paramList)
                    
            except ConturError as dboe:
                cfg.contur_log.info(dboe)
                cfg.contur_log.info("Could not get info from DB. Will use file system instead.")

            if len(yoda_files)==0:
                # nothing found in the DB. try the file system.
                yoda_files = cgt.find_param_point(args['scan_dirs'], cfg.tag, paramList, verbose=True)

        if args['PLOT']:
            cfg.contur_log.info("*************************************************")
            cfg.contur_log.info("Starting making histogram for matched yoda files")
            for yoda_file in yoda_files:
                os.system("gzip -d " + yoda_file)
                yoda_file_unziped = ".".join(yoda_file.split(".")[:-1])
                os.system("contur " + yoda_file_unziped)
                os.chdir(os.path.dirname(yoda_file_unziped))
                os.system("contur-mkhtml " + yoda_file_unziped)

    elif Clean:
        cgt.grid_loop(scan_path=args['scan_dirs'][0], clean=Clean)


    sys.exit(0)


def doc_argparser():
    """ wrap the arg parser for the documentation pages """
    from contur.run.arg_utils import get_argparser
    return get_argparser('grid_tool')
