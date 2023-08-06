from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys, os, logging
from shutil import copyfile

import contur.config.version
import contur.config.config as cfg
from contur.data.static_db import get_beams, get_beam_names

def get_args(argv, arg_group="unknown argument group"):
    """Parse command line arguments"""

    parser = get_argparser(arg_group)
    args = parser.parse_args(argv)
    args = vars(args)
    return args


def get_argparser(arg_group):
    """
    Build and return an argument parser

    :param arg_groups: which argument groups will be used.

    The arg_group corresponds one-to-one to the run_XXX.py modules.
    It picks out the relevant subset of arguments to add.

    * group **analysis** for running analysis on a grid or a single yoda file
    * group **batch_submit** for running evgen batch jobs
    * group **extract_xs_bf** for extracting cross sections and branching fractions from a single yoda
    * group **extract_xs_bf_scan** for extracting and plottingcross sections and branching fractions from a grid
    * group **grid_tool** for running grid utilities
    * group **init** initialisation
    * group **mkbib** for making html pages
    * group **mkhtml** for making html pages
    * group **mkthy** for making html pages
    * group **plot** for plotting map file
    * group **smtest** for running statistical tests on SM theory

    """

    if arg_group == 'analysis':
        parser_description = ("This is the main analysis executable for Contur: Constraints on new theories using Rivet\n ")
        active_groups = ['io', 'grid', 'dress', 'select', 'stats', 'params', 'ana_select', 'beams']
        
    elif arg_group == 'batch_submit':
        parser_description = ("Run a parameter space scan and submit batch jobs.\n"
            "Produces a directory for each beam containing generator config file detailing the "
            "parameters used at that run point and a shell script to run the generator "
            "that is then submitted to batch. (if --single, just make one example directory)\n")
        active_groups = ['batch','mceg_select','grid','beams']
        
    elif arg_group == 'extract_xs_bf':
        parser_description = ("Extract and plot cross section and branching ratio information from single run.\n")
        active_groups = ['xsbf','mceg_select']
        
    elif arg_group == 'grid_tool':
        parser_description = ("Various manipulations on a grid.\n")
        active_groups = ['tools', 'batch', 'mceg_select','params', 'grid', 'ana_select']

    elif arg_group == 'init':
        parser_description = ("Building contur user area.\n")
        active_groups = ['init']

    elif arg_group == 'mkbib':
        parser_description = ("Building contur LaTeX bibliography files.\n")
        active_groups = ['outdir','select']

    elif arg_group == 'mkhtml':
        parser_description = ("Make web page for single contur run.\n")
        active_groups = ['html','ana_select']
        
    elif arg_group == 'mkthy':
        parser_description = ("Rebuild SM theory library.\n")
        active_groups = ['smtheory','ana_select']
        
    elif arg_group == 'plot':
        parser_description = ("Plot contur data from a .map file.\n")
        active_groups = ['map_plotting']
        
    elif arg_group == 'scan_xs_bf':
        parser_description = ("Extract and plot cross section and branching ratio information from scan.\n")
        active_groups = ['xsbf','xsscan','mceg_select']
        
    elif arg_group == 'smtest':
        parser_description = ("Running Standard Model comparisons.\n")
        active_groups = ['stats', 'select', 'outdir', 'ana_select', 'beams']

    else:
        print("Do not recognize the requested argument group: {}".format(arg_group))
        raise Exception("Argh")     

    parser = ArgumentParser(usage=__doc__, description=parser_description,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # add the arguments that are always there.
    add_generic(parser)

    # arguments used when initialising the user area
    if "init" in active_groups:
        parser.add_argument("-w", "--webpages", dest="WEBPAGES", action="store_true",
                          default=False,
                          help="Also build the webpage rsts for sphinx")
        add_outputdir(parser,cfg.share)
                
    # minimal io arguments
    if "outdir" in active_groups:        
        add_outputdir(parser)

    # arguments specifying a results grid
    if "grid" in active_groups:
        add_grid_info(parser)
        
    if "beams" in active_groups:
        parser.add_argument("-b", "--beams", dest="BEAMS", default="all",
                            help=f"""Select beams to run on. Default is to run on all possible.
                            Known beams are {get_beam_names(allow_all=True)}. NOTE: em_ep_91_2 is currently beta, see https://gitlab.com/hepcedar/rivet/-/issues/293.""")

    # io arguments for major contur run
    if "io" in active_groups:
        io = parser.add_argument_group("I/O")
        add_outputdir(io,default=cfg.output_dir)        
        io.add_argument('yodafiles', nargs='*', help='List of indiviudal yoda files to process.')
        
    # arguments for adding extra info to contur run or tweaking display
    if "dress" in active_groups:
        add_dressing(parser)

    if "ana_select" in active_groups:
        add_analysis_selection(parser)
        
    # arguments for selecting other subsets of data
    if "select" in active_groups:
        add_data_selection(parser)

    # arguments for selecting model parameters
    if "params" in active_groups:
        parser.add_argument("-f", "--find-point", action="append", dest="FINDPARAMS", default=[],
                            help="identify points consistent with these parameters and make histograms for them")
        
    # arguments for tweaking the statistical treatment
    if "stats" in active_groups:
        add_stats(parser)
       
    # arguments used when plotting from map file
    if "map_plotting" in active_groups:
        add_outputdir(parser,default="conturPlot")
        add_plotting(parser)
        
    # arguments for manipulating a grid of results
    if "tools" in active_groups:
        add_tools(parser)
        
    # arguments for handling batch job submission
    if "batch" in active_groups:
        add_outputdir(parser,default=cfg.batch_output_dir)
        add_batch(parser)

    # arguments specific to making SM theory files.
    if "smtheory" in active_groups:  
        parser.add_argument("-i", "--input", dest="INPUTDIR",
                          default=contur.config.paths.data_path("data/TheoryRaw"),
                          help="Root directory for the theory raw data")

    if "mceg_select" in active_groups:
        parser.add_argument("-m", "--mceg", dest="mceg", default=cfg.mceg,
                            type=str, help="MC event generator.")
        
    if "xsbf" in active_groups:

        # should this use add_grid?
        parser.add_argument('inputDir', nargs='*', help="Path to scan directory")
        parser.add_argument("--tolerance", type=float,
                            help="Minimum cross-section in fb for a process to be drawn", dest="tolerance", default=0.0)
        parser.add_argument("--txs", "--xs-frac-tolerance", type=float,
                            help="Fractional tolerance for which processes to include. Processes which contribute less than this xs at a given point are ignored", dest="fractolerance", default=0.0)
        parser.add_argument("--br", "--fold-BRs", help="Whether or not to fold in the branching ratios",
                            dest="foldBRs", default=False, action="store_true")
        parser.add_argument("--bsm-br", "--fold-BSM-BRs", help="Whether or not to fold in the BSM branching ratios ",
                            dest="foldBSMBRs", default=False, action="store_true")
        parser.add_argument("--sl", "--split-leptons", help="Leptons e, mu tau are set to l by default. Apply this flag to split them again",
                            dest="splitLeptons", default=False, action="store_true")
        parser.add_argument("--mb", "--merge-bosons", help="Set W, Z, H to V",
                            dest="mergeEWBosons", default=False, action="store_true")
        parser.add_argument("--sp", "--split-incoming-partons", help="We normally don't care about the incoming partons, just set them to pp. Apply this flag to split them again",
                            dest="splitIncomingPartons", default=False, action="store_true")
        parser.add_argument("--sa", "--split-antiparticles", help="Particles and antiparticles are merged by default. Add this options to split them out",
                            dest="splitAntiParticles", default=False, action="store_true")
        parser.add_argument("--sb", "--splitB", help="u, d, s, c, b are grouped into q by default. Add this options to split out the b",
                            dest="splitBQuarks", default=False, action="store_true")
        parser.add_argument("--sq", "--split-light-quarks", help="u, d, s, c, b are grouped into q by default. Add this options to split them out",
                            dest="splitLightQuarks", default=False, action="store_true")
        parser.add_argument("--p", "--pools", help="Split into pools based on final state ? Only works with --br option",
                            dest="splitIntoPools", default=False, action="store_true")
        parser.add_argument("--xy", help="Variables to scan", dest="xy", default=None )
        parser.add_argument("--bro", "--onlyBRs", help="Print ONLY the BSM branching ratios and exit.",
                            dest="printBRsOnly", default=False, action="store_true")
        parser.add_argument("--ws","--website", help="Alternative format output for web-visializer",
                            dest="ws", default=False, action="store_true")

    # arguments for handling the cross section scan
    if "xsscan" in active_groups:
        add_outputdir(parser,default="CONTUR_xs_scans/")
        parser.add_argument("--xc", "--ignore-cache",
                            help="Extraction of the cross-sections for each point are cached by default to speed up processing."
                            "If you don't want to use caching, use this flag", dest="ignoreCache", default=False, action="store_true")
        parser.add_argument("--cc", "--clear-cache",
                            help="Extraction of the cross-sections for each point are cached by default to speed up processing."
                            "If you want to reset the cache, use this flag",
                            dest="clearCache", default=False, action="store_true")
        parser.add_argument("--do", "--draw-to", help="Output directory for plots of BRs, if using.",
                            dest="drawToDir", default="")

    if "html" in active_groups:
        
        add_outputdir(parser,default="contur-plots")
        add_html(parser)
        
    return parser

def valid_mceg_arg(args):
    '''
    Checks the arguments for what mceg is selected, and set cfg.mceg
    Returns False if the selection is isvalid.
    '''

    if not args['mceg'] in cfg.known_mcegs:
        cfg.contur_log.error("Unrecognised event generator: {}".format(args['mceg']))
        return False
    else:
        cfg.mceg = args['mceg']
        try:
            cfg.mceg_template = os.path.basename(args['template_file'])
        except:
            # this is ok, the template file arg is not defined when extracting xsecs, for example
            pass
        return True
    
def valid_beam_arg(args):
    '''
    Checks the arguments for what beams are selected and return them in a list. 
    Returns None if the selection is isvalid.
    '''

    known_beams = get_beams()
    try:
        if args['BEAMS'] == "all":
            return known_beams

        else:
            beams = []
            try_beams = args['BEAMS'].split(",")
            for try_beam in try_beams:
                found_beam = False
                for beam in known_beams:
                    if try_beam == beam.id:
                        beams.append(beam)
                        found_beam = True
                if not found_beam:
                    contur.config.contur_log.error("Beam {} is not known. Possible beams are: {}".format(try_beam, get_beam_names(allow_all=True)))
                    return None
            return beams

    except KeyError:
        return known_beams
            

def valid_batch_arguments(args):
    """
    Check that command line arguments are valid; return True or False.
    This function is also responsible for formatting some arguments e.g.
    converting the RunInfo path to an absolute path and checking it contains .ana files.
    valid_args = True

    """
    valid_args = True

    beams = valid_beam_arg(args)
    if beams is None:
        return False, None
    

    if args['walltime'] is not None:
        timespans = args['walltime'].split(":")
        if len(timespans) != 2:
            cfg.contur_log.error("Have to give max wall time in the format <hh:mm>!")
            valid_args = False
        else:
            try:
                for span in timespans:
                    span = int(span)
                    if span >= 60:
                        cfg.contur_log.error(
                            "Have to give time spans of less than 60 [units]!")
                        valid_args = False
            except ValueError:
                cfg.contur_log.error("Have to give time spans that can be converted to integers!")
                valid_args = False

    if args['memory'] is not None:
        number, unit = args['memory'][0:-1], args['memory'][-1]
        valid_units = ["M", "G"]
        if unit not in valid_units:
            cfg.contur_log.error("'%s' is not a valid unit for the memory. (%s are valid units.)" % (
                unit, valid_units))
            valid_args = False
        if not number.isdigit():
            cfg.contur_log.error("'%s' is not a valid number for the memory." % number)
            valid_args = False

    if args['GRID']:
        cfg.contur_log.info("Analysing existing grid: {}".format(args['GRID']))
        if args['num_points']:
            try:
                n_points = int(args['num_points'])
                cfg.contur_log.info(
                    "Splitting into {} parameter points per map file.".format(args['num_points']))
            except ValueError:
                cfg.contur_log.error(
                    "Number of points {} cannot be converted to integer!".format(args['num_points']))
                valid_args = False

        return valid_args, beams

    if not os.path.exists(args['param_file']):
        cfg.contur_log.error("Param file '%s' does not exist!" % args['param_file'])
        valid_args = False

    if not os.path.exists(args['template_file']):
        cfg.contur_log.error("Template file '%s' does not exist!" % args['template_file'])
        valid_args = False

    if args['run_info'].lower() == 'none':
        args['run_info'] = None
    else:
        args['run_info'] = os.path.abspath(args['run_info'])
        if not os.path.isdir(args['run_info']):
            cfg.contur_log.info("Creating run information directory '{}'!".format(args['run_info']))
            from contur.util.utils import mkoutdir
            mkoutdir(args['run_info'])

        for beam in beams:
            afile = beam.id + ".ana"
            if not os.path.exists(os.path.join(args['run_info'], afile)):
                gpfrom = os.path.join(cfg.share, afile)
                gpto = os.path.join(args['run_info'], afile)
                cfg.contur_log.info("Copying {} to {}".format(gpfrom, gpto))
                copyfile(gpfrom, gpto)

    try:
        int(args['num_events'])
    except ValueError:
        cfg.contur_log.error("Number of events '%s' cannot be converted to integer!"
                                       % args['num_events'])
        valid_args = False

    try:
        args['seed'] = int(args['seed'])
    except ValueError:
        cfg.contur_log.error("Seed '%s' cannot be converted to integer!" % args['seed'])
        valid_args = False

    valid_args = valid_mceg_arg(args)
        
    return valid_args, beams


def setup_common(args):
    """
    Set up the configuration parameters for the common arguments/flags.
    If printVersion is set, do this and exit
    """

    if args['printVersion']:
        print("Contur " + contur.config.version.version)
        sys.exit(0)

    cfg.logfile_name = args['LOG']
    cfg.setup_logger(filename=cfg.logfile_name,logstream=args.get("LOGSTREAM"))
    
    cfg.contur_log.setLevel(logging.INFO)
    if args['QUIET']:
        cfg.contur_log.setLevel(logging.WARNING)
    else:
        from contur.util.utils import write_banner
        write_banner()
    if args['DEBUG']:
        cfg.contur_log.setLevel(logging.DEBUG)

    if args['OFFLINE']:
        cfg.contur_log.info("Running in offline mode")
        cfg.offline=True
        
    # This is a very common flag but there are some cases where it isn't defined.
    try:
        cfg.output_dir = args['OUTPUTDIR']
        if not os.path.isabs(cfg.output_dir):
            cfg.output_dir = os.path.join(os.getcwd(),cfg.output_dir)
    except KeyError:
        pass
    except TypeError:
        pass

def setup_batch(args):
    """
    setup up the configuration parameters for the batch arguments/flags
    """

    cfg.param_steering_file = args['param_file']

    cfg.using_condor = (args['batch_system'] == 'condor')
    cfg.using_slurm = (args['batch_system'] == 'slurm')
    cfg.using_qsub = not (
            cfg.using_condor or cfg.using_slurm)


def setup_stats(args, message):
    """
    setup the parameters for the stats argument group
    """

    if args['LLE']:
        cfg.look_elsewhere = True
        
    if args['SIGPBG']:
        cfg.sig_plus_bg = True
        
    if not (args['MNS'] == cfg.min_num_sys):
        print("args[MNS]",args['MNS'],cfg.min_num_sys)        
        cfg.min_num_sys = args['MNS']
        message += "Minimum number of systematic uncertainties contributions for correlations changed to {} \n".format(
            cfg.min_num_sys)
        
    cfg.useTheoryCorr = args['THCORR']
    if cfg.useTheoryCorr:
        message += "Theory uncertainties assumed correlated. \n"
    else:
        message += "Theory uncertainties assumed uncorrelated. \n"        


    if args['UNCORR']:
        cfg.diag = True
        message += "No data systematic correlations being used. \n"

    else:                

        if not cfg.min_syst == args['MIN_SYST']:
            cfg.min_syst = float(args['MIN_SYST'])
            message += "Systematic materiality cutoff changed to {} \n".format(
                cfg.min_syst)

        # are we minimising nuisance parameters?
        if args['MIN_NP']:
            message += "Attempting marginalisation over nuisance parameters \n"
            cfg.min_np = True

            if not cfg.ll_prec == float(args['LL_PREC']):
                cfg.ll_prec = float(args['LL_PREC'])
                message += "LL precision criterion changed to  {} \n".format(
                    cfg.ll_prec)

            if not cfg.n_iter == int(args['N_ITER']):
                cfg.n_iter = int(args['N_ITER'])
                message += "max number of iterations changed to  {} \n".format(
                    cfg.n_iter)

            if not cfg.err_prec == float(args['ERR_PREC']):
                cfg.err_prec = float(args['ERR_PREC'])
                message += "Precision cut off in nuisance parameters when minimizing LL changed to {} \n".format(
                    cfg.err_prec)

    return message

def setup_selection(args,modeMessage):

    if args['EXCLUDEHGG']:
        cfg.excludeHgg = True
        modeMessage += "Excluding Higgs to photons measurements \n"

    if args['USESEARCHES']:
        cfg.exclude_searches = False
        modeMessage += "Using search analyses \n"

    if args['TRACKSONLY']:
        cfg.tracks_only=True
        modeMessage += "Including only plots which are based on tracking information \n"

    if args['USESOFTPHYSICS']:
        cfg.exclude_soft_physics=False
        modeMessage += "Including soft QCD stuff. Hope you know what you are doing! \n"

    if args['USEHWW']:
        cfg.exclude_hww = False
        modeMessage += "Including Higgs to WW measurements if available \n"

    if args['USEBV']:
        cfg.exclude_b_veto = False
        modeMessage += "Including secret b-veto measurements if available \n"

    if args['USEAWZ']:
        cfg.exclude_awz = False
        modeMessage += "Including ATLAS WZ SM measurement \n"

    if args['EXCLUDEMETRAT']:
        cfg.exclude_met_ratio = True
        modeMessage += "Excluding MET ratio measurements \n"

    return modeMessage

    
def add_generic(parser):

    # generic arguments, always allowed.
    parser.add_argument("-v", "--version", action="store_true", dest="printVersion",
                        default=False, help="print version number and exit.")
    parser.add_argument("-d", "--debug", action="store_true", dest="DEBUG", default=False,
                        help="Switch on Debug to all, written to log file")
    parser.add_argument("-q", "--quiet", action="store_true", dest="QUIET", default=False,
                        help="Suppress info messages")
    parser.add_argument("-l", "--log", dest="LOG",
                        default=cfg.logfile_name, help="Specify logfile name.")
    parser.add_argument("--offline", action="store_true", dest="OFFLINE",
                        default=False, help="Run in offline mode (no querying of inspire).")

def add_outputdir(parser,default=None):
    
    parser.add_argument('-o', '--outputdir', type=str, default=default, dest="OUTPUTDIR",
                        help="Output path.")

def add_grid_info(parser,default=None):

    gridinfo = parser.add_argument_group("Options relating to grid of results")
    
    gridinfo.add_argument("-g", "--grid", dest="GRID", default=None,
                          help="Run in grid mode on a folder containing a structured grid of points.")
    gridinfo.add_argument("--runname", dest="RUNNAME", default="my_run",
                          help="Identifier for grid run")
    gridinfo.add_argument('--tag', dest='TAG', default=cfg.tag,
                          help='Identifier for merged yoda files.')
    gridinfo.add_argument("--map", dest="MAPFILE", default=None,
                          help="Name of map file output (in grid mode).")
    gridinfo.add_argument("--remerge", action="store_true", dest="REMERGE",
                          help="Do use any existing merges of yoda files: merge yoda files anew (in grid mode).")
    gridinfo.add_argument("--addtoDB", action="store_true", dest="ADD_DB", default=False,
                          help="add results of an existing DB file (in grid mode).")
    gridinfo.add_argument("--keep-hepmc", action="store_true", dest="KEEPHEPMC", default=False,
                          help="preserve the HepMC files if they are being generated (in grid mode).")
        
def add_dressing(parser):
    dress = parser.add_argument_group("Dressing options to embellish outputs")
    dress.add_argument("-p", "--paramfile", dest="PARAM_FILE", default=cfg.paramfile,
                       help="Optionally specify a parameter file.")
    dress.add_argument("--model", dest="MODEL",
                       help="Optionally give name for model used. Only used for documentation.")
    dress.add_argument("-P", "--particleinfo", nargs="?", dest="PI", default=None, const="ALL",
                       help="Comma-separated list of particles for which mass, width, branchings will be stored. "
                       "If flag is present with no list, info will be saved for all particles found.")
    dress.add_argument("-M", "--matrix_element", nargs="?", dest="ME", default=None, const="ALL",
                       help="Comma-separated list of matrix elements for which cross sections will be stored."
                       "If flag is present with no list, info will be saved for all non-zero processes found.")
    dress.add_argument("--slha", dest="SLHA", default="MASS",
                       help="read parameters from a comma-seperated list of blocks in an SLHA file")
    dress.add_argument("--BW", "--binwidth", dest="BINWIDTH",
                       help="optional binning of SLHA paramters")
    dress.add_argument("--BO", "--binoffset", dest="BINOFFSET",
                       help="optional bin offset for SLHA parameters")
    # TODO. When we move to YODA2, this should be something for mkhtml
    dress.add_argument("--ns", "--nostack",
                       action="store_true", dest="NOSTACK", default=False,
                       help="in single run mode, do not stack the histograms in dat file output")

def add_analysis_selection(parser):

    parser.add_argument("--ana-match", action="append", dest="ANAPATTERNS", default=[],
                            help="only run on analyses whose name matches this regex")
    parser.add_argument("--ana-unmatch", action="append", dest="ANAUNPATTERNS", default=[],
                            help="exclude analyses whose name matches this regex")

def add_data_selection(parser):

    select = parser.add_argument_group("Options to exclude/include subsets of data")
    select.add_argument("--all",
                        action="store_true", dest="USEALL", default=False,
                        help="Convenience option to use all data. Overrides any other selections.")
    select.add_argument("--xr", "--nometratio",
                        action="store_true", dest="EXCLUDEMETRAT", default=cfg.exclude_met_ratio,
                        help="Exclude plots where exclusion would be based on a ratio to the SM dileptons"
                             "Use this when you have ehnanced Z production in your model.")
    select.add_argument("--tracks-only",
                        action="store_true", dest="TRACKSONLY", default=cfg.tracks_only,
                        help="Only use plots which are based on tracking information"
                        "Useful for models where calorimeter jet calibration may be suspect (e.g. dark showers).")
    select.add_argument("--soft-physics",
                        action="store_true", dest="USESOFTPHYSICS", default=(not cfg.exclude_soft_physics),
                        help="Include plots which are very sensitive to soft QCD."
                        "Not reliable unless you really know what you are doing.")

    select.add_argument("--xhg", "--nohiggsgamma",
                        action="store_true", dest="EXCLUDEHGG", default=cfg.exclude_hgg,
                        help="Exclude plots where Higgs to photons signal is background-subtracted by fitting continuum."
                             "Do this when you have large non-Higgs diphoton production from your model.")
    select.add_argument("--whw", "--withhiggsww",
                        action="store_true", dest="USEHWW", default=(not cfg.exclude_hww),
                        help="Include plots where Higgs to WW signal is background-subtracted using data."
                             "Only try this when you have large Higgs WW from your model and not much top or other source of WW.")
    select.add_argument("--wbv", "--withbvetos",
                        action="store_true", dest="USEBV", default=(not cfg.exclude_b_veto),
                        help="Include plots where a b-jet veto was applied in the measurement but not in the fiducial definition."
                             "Only try this when you have large W+jets enhancements and no extra top or other source of W+b.")
    select.add_argument("--awz", "--atlas-wz",
                        action="store_true", dest="USEAWZ", default=(not cfg.exclude_awz),
                        help="Include the ATLAS WZ analysis with dodgy SM assumptions."
                             "Might be useful for enhanced WZ cross sections but be careful.")
    select.add_argument("-s", "--use-searches",
                        action="store_true", dest="USESEARCHES", default=(not cfg.exclude_searches),
                        help="Use reco-level search analyses in the sensitivity evaluation (beta).")
    select.add_argument("--wn", "--weight-name", dest="WEIGHTNAME", default="",
                        help="for weighted events/histos, select the name of the weight to use.")


def add_stats(parser):
    stats = parser.add_argument_group(
        'Options to Manipulate the constructed test statistic. They dont apply if correlations are switched off')
    stats.add_argument("-u", "--diagonalise-cov", action="store_true", dest="UNCORR", default=False,
                       help="Use diagonal version of covariance matrix (ie no systematic correlations).")
    stats.add_argument("--xtc", "--notheorycorr", dest="THCORR", default=True, action="store_false",
                       help="Assume SM theory uncertainties are uncorrelated")
    stats.add_argument("--mnp", "--minimize-np", action="store_true", dest="MIN_NP", default=False,
                       help="If using correlations, perform nuisance parameter minimization (slow)")
    stats.add_argument("--min-syst", dest="MIN_SYST", default=cfg.min_syst, type=float,
                       help="Correlated systematic errors with a maximum fractional contribution below this will be ignored")
    stats.add_argument("--error-precision", dest="ERR_PREC", default=cfg.err_prec,
                       help="precision cut off in nuisance parameters when minimizing LL")
    stats.add_argument("--ll-precision", dest="LL_PREC", default=cfg.ll_prec,
                       help="precision cut off in LL when minimizing it")
    stats.add_argument("--n-iter", dest="N_ITER", default=cfg.n_iter, type=int,
                       help="minimize cuts off after n_iter*n_variables iterations")
    stats.add_argument("--min-num-sys", dest="MNS", default=cfg.min_num_sys, type=int,
                       help="minimum number of systematic nuisance parameters for them to be treated as correlated")
    stats.add_argument('--databg', dest="DATABG", default=False,
                       action="store_true",
                       help="Make data-as-background the primary exclusion.")
    stats.add_argument("--split-pools", action="append", dest="POOLPATTERNS", default=[],
                       help="write out histograms from analyses in given pools separately")
    stats.add_argument("--ana-split", action="append", dest="ANASPLIT", default=[],
                       help="write out histograms from given analyses separately")
    stats.add_argument('--spb', '--signal-plus-background',dest="SIGPBG", default=False,
                       action="store_true",
                       help="Tell contur that the input histos are signal-plus-background, not just signal")
    stats.add_argument('--lle','--look-elsewhere', dest="LLE", default=False,
                       action="store_true",
                       help="Treat plots with no signal as agreeing well. Otherwise (default) they are ignored.")

def add_plotting(parser):

    mapplot = parser.add_argument_group("Map file plotting arguments")
    mapplot.add_argument('file', nargs=1, type=str, help=('Path to result database file or map file that '
                                                    'containing the info of model points .'))
    mapplot.add_argument('variables', nargs='*', type=str,
                        help=('x, y [and z] variables to plot.'))

    # Optional arguments
    mapplot.add_argument("-i", "--indir", dest="INPUTDIR",
                         default=cfg.input_dir, help="the directory to look in for results.")

    mapplot.add_argument('-ef', "--externalFunction", type=str, default=None,
                        help="Python file with external functions to load and plot")
    mapplot.add_argument('-eg', "--externalGrid", type=str, default=None,
                        help="Python file loading alternative external grids")

    mapplot.add_argument('-xl', "--xlog", action="store_true",
                        help="Set the xaxis to be displayed on a log scale")
    mapplot.add_argument('-yl', "--ylog", action="store_true",
                        help="Set the yaxis to be displayed on a log scale")
    mapplot.add_argument('--pools', dest="plot_pools", action='store_true',
                        help="Turn on plotting of individual analysis pools (much slower!)")
    mapplot.add_argument('-O', '--omit', type=str,
                        help='Name of pool to omit (will slow things down!)', default="")

    mapplot.add_argument('-x', '--xlabel', type=str, default=None,
                        help='x-axis label. Accepts latex formatting but special characters must be input with a slash, e.g. \\$M\_\{z\'\}\$~\[GeV\]')
    mapplot.add_argument('-y', '--ylabel', type=str, default=None,
                        help='y-axis label. Accepts latex formatting but special characters must be input with a slash, e.g. \\$M\_\{z\'\}\$~\[GeV\]')
    mapplot.add_argument('-sp', '--save-plots', action='store_true',
                        help="Save the raw matplotlib axes to a file for graphical manipulation")
    mapplot.add_argument('-t', '--title', type=str,
                        help='Title for plot.', default="")
    mapplot.add_argument('--ilevel', '--iLevel', type=int,
                        help='interpolation zoom level', default=3)
    mapplot.add_argument('--style', dest="style", default="DRAFT", choices=["DRAFT", "FINAL"], type=str.upper,
                        help="Global flag for plot-styling variations: 'final' will have no title or cmap key and will produce a .tex file containing a colour legend for the dominant pools plot")
    mapplot.add_argument('--isigma', '--iSigma', type=float,
                        help='interpolation smoothing radius, in mesh cells', default=0.75)
    mapplot.add_argument('--num-dpools', dest="ndpools", type=int,
                        help='Number of levels of (sub)dominant pool plots to make.', default=1)
    mapplot.add_argument('--clstxt', dest="showcls", default=False, action="store_true",
                        help="Write CLs values on top of the mesh in the detailed dominant-pool plots.")
    mapplot.add_argument('--no-clsdpool', dest="simplecls", default=False, action="store_true",
                        help="Skip the detailed dominant-pool plot with lead/sub/diff CLs meshes.")
#        mapplot.add_argument('-c', '--contour_colour', dest="contour_colour", default=cfg.contour_colour,
#                            type=dict, help="Dict of colours for the 68/95 contours")
    mapplot.add_argument('-f', '--format', dest="plot_format", default=cfg.plot_format,
                        type=str, help="format for plots (pdf, png...)")
    mapplot.add_argument('--databg', dest="DATABG", default=False,
                        action="store_true",
                         help="Make data-as-background the primary exclusion.")
    mapplot.add_argument('--secondary-contours', dest="secondary_contours", default=False,
                        action="store_true",
                         help="Add contour(s) for stats other than the default.")

def add_tools(parser):

    options = parser.add_argument_group("Control options")

    options.add_argument("--merge", action="store_true", dest="MERGE_GRIDS",
                         default=False, help="merge two or more grids using symbolic links. Excludes other options")

    options.add_argument("--rm", "--remove-merged", action="store_true", dest="RM_MERGED",
                         default=False, help="if unmerged yodas exist, unzip them, and remove merged ones")

    options.add_argument("--nc", "--no-clean", action="store_true", dest="DO_NOT_CLEAN",
                         default=False, help="do not remove unnecessary files.")

    options.add_argument("--archive", action="store_true", dest="COMPRESS_GRID",
                         default=False, help="remove intermediate and unncessary files, and compress others.")

    options.add_argument("-c", "--check", action="store_true", dest="CHECK_GRID",
                         default=False, help="check whether all grid points have valid yodas")

    options.add_argument("--ca", "--check-all", action="store_true", dest="CHECK_ALL",
                         default=False, help="include grid points without logfiles when checking for yodas")

    options.add_argument("-S", "--submit", action="store_true", dest="RESUB",
                         default=False, help="(re)submit any jobs which are found to have failed.")

    options.add_argument("--detail", action="store_true", dest="PARAM_DETAIL", default=False,
                         help="output detailed information for certain parameter point")

    options.add_argument("--plot", action="store_true", dest="PLOT", default=False,
                         help="make histograms for specified parameters (much slower!)")


def add_batch(parser):
   
    parser.add_argument('-p', '--param_file', dest='param_file', type=str,
                        default=cfg.param_steering_file, help='File specifying parameter space.')
    parser.add_argument('--template', dest='template_file',
                        default=cfg.mceg_template, help='Template Herwig .in file.')
    parser.add_argument("-r", "--runinfo", dest="run_info", type=str, default=cfg.run_info, 
                        help=("Directory with required run information. Set to 'none' to not use one."))
    parser.add_argument("-n", "--numevents", dest="num_events",
                        default=cfg.default_nev, type=int, help="Number of events to generate.")
    parser.add_argument('--seed', dest='seed', default=cfg.seed,
                        type=int, help="Seed for random number generator.")
    parser.add_argument("-Q", "--queue", dest="queue", default="", type=str, help="batch queue.")
    parser.add_argument('-s', '--scan-only', '--scan-only', dest='scan_only', default=False,
                        action='store_true', help='Only perform scan and do not submit batch job.')
    parser.add_argument('-P', '--pipe-hepmc', '--pipe-hepmc', dest="pipe_hepmc", default=False,
                        action='store_true', help="Rivet reading from pipe.")
    parser.add_argument('-w', '--walltime', type=str, default=None,
                        help="Set maximum wall time for jobs (HH:MM).")
    parser.add_argument('--memory', type=str, default=None,
                        help="Set maximum memory consumption for jobs (e.g. 2G).")
    parser.add_argument('-B', '--batch', dest="batch_system", default='qsub',
                        type=str, help="Specify which batch system is using, support: qsub, condor or slurm")
    parser.add_argument('-V', '--variable-precision', dest="variable_precision", action='store_true',
                        help='Use this flag to make number of events for each point variable')
    parser.add_argument("--single", action="store_true", dest="SINGLE", default=False,
                        help="just generate one example directory, no job submission")
    parser.add_argument("-N", "--numpoints", dest="num_points", default=50,
                        help="break an analysis run down into jobs/maps with N parameter points in each")
    parser.add_argument("-a", "--analysis-flags", dest="analysis_flags", default="",
                        help="flags to pass to the contur analysis step (separate with commas)")
    parser.add_argument("--setup", dest="setup_script", default=None,
                        help="specify a setup script to be sourced at start of analysis batch job.")
    parser.add_argument("-db", "--initDB", action="store_true", dest="INIT_DB", default=False,
                         help="init responsive db for grid mode")
    parser.add_argument("--main-program", dest="main_program", default="main93",
                        type=str, help="Specify whether to use the main93 or main89 program for pythia8. Number of events for main89 presently have to be specified within your command file.")


def add_html(parser):

    # not a grid
    parser.add_argument("-i", "--indir", dest="INPUTDIR",
                        default=cfg.input_dir, help="the directory storing contur output")

    parser.add_argument("-n", "--num-threads", metavar="NUMTHREADS", dest="NUMTHREADS", type=int,
                        default=None, help="request make-plots to use a specific number of threads")
    parser.add_argument("--no-cleanup", dest="NO_CLEANUP", action="store_true", default=False,
                        help="keep plotting temporary directory")
    parser.add_argument("--no-subproc", dest="NO_SUBPROC", action="store_true", default=False,
                        help="don't use subprocesses to render the plots in parallel -- useful for debugging")
    parser.add_argument("--pwd", dest="PATH_PWD", action="store_true", default=False,
                        help="append the current directory (pwd) to the analysis/data search paths (cf. $RIVET_ANALYSIS_PATH)")        
    parser.add_argument("--all", dest="ALLPLOTS", default=False, action="store_true",
                        help="Make all plots. (By default only those contributing to the exclusion are made.)")
    parser.add_argument("--vis","--forVisualiser", dest="FORVISUALISER", action="store_true", default=False,
                        help="Tweak the way the output is written, for use in contur-visualiser")

    stygroup = parser.add_argument_group("Style options")
    stygroup.add_argument("-t", "--title", dest="TITLE",
                          default="Constraints On New Theories Using Rivet",
                          help="title to be displayed on the main web page")
    stygroup.add_argument("--all-errbars", dest="ALL_ERRBARS", action="store_true",
                          default=False, help="Draw error bars on all histos.")
    stygroup.add_argument("--font", dest="OUTPUT_FONT", choices="palatino,cm,times,helvetica,minion".split(","),
                          default="palatino", help="choose the font to be used in the plots")
    stygroup.add_argument("--config", dest="CONFIG",
                          default="", help="supply a plot config file. See examples in $CONTUR_ROOT/data/Plotting")

