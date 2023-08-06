# -*- python -*-

"""
Miscellaneous helper functions that may be used by more than one contur submodule

"""

import os, glob, subprocess
from builtins import input

import contur
import contur.config.config as cfg
import contur.config.version
import contur.data.static_db as cdb
import contur.factories.likelihood as lh
import contur.data as cdb
import contur.util.utils as cutil



## Import the tqdm progress-bar if possible, otherwise fall back to a safe do-nothing option
try:
    from tqdm import tqdm as progress_bar
except ImportError:
    def progress_bar(iterable, **kwargs):
        return iterable

def splitPath(path):
    """
    Take a yoda histogram path and return the analysis name and the histogram name
    :arg path: the full path of a yoda analysis object
    :type: String

    """
    from rivet.aopaths import AOPath

    aop = AOPath(path)
    parts = AOPath.dirnameparts(aop)
    analysis = parts[len(parts)-1]
    h_name = AOPath.basename(aop)
    return analysis, h_name


def mkoutdir(outdir):
    """
    Function to make an output directory if it does not already exist.
    Also tests if an existing directory is write-accessible.
    """
    if not os.path.exists(outdir):
        try:
            os.makedirs(outdir)
        except:
            msg = "Can't make output directory '%s'" % outdir
            raise Exception(msg)
    if not os.access(outdir, os.W_OK):
        msg = "Can't write to output directory '%s'" % outdir
        raise Exception(msg)


def write_banner():
    """
    Write a text banner giving the version and pointing to the documenation
    """
    msgs = ["Contur version {}".format(contur.config.version.version),
            "See https://hepcedar.gitlab.io/contur-webpage/"]
    for m in msgs:
        try:
            cfg.contur_log.info(m)
        except:
            print(m)


def write_yoda_dat(observable, nostack=False, smtest=False):
    """
    Write a YODA  .dat file (plot formatting) for the histograms in the output directory, for later display.

    :param nostack: flag saying whether to plot data along or stack it on the background (default) 
    :type boolean:

    :param observable: dressed YODA ao
    :type observable: :class:`contur.factories.Observable`

    the output directory is determined by cfg.plot_dir

    """

    import yoda, rivet
    
    ## Check if we have reference data for this observable. If not, then abort.
    if not observable.ref:
        cfg.contur_log.warning("Not writing dat file for {}. No REF data.".format(observable.signal.path()))
        return
    
    # List for the analysis objects which will be in the dat file
    anaobjects = []
    # List for the names of  analysis objects which will be drawn
    drawonly = []

    if (cfg.primary_stat == cfg.databg or observable.thyplot is None) and not smtest:
        show_databg = True
    else:
        show_databg = False
        
    # get the data and signal+data plots
    refdata = observable.refplot
    if nostack:
        # in this case we are just plotting signal, without stacking it on any background
        sigback_databg  = observable.sigplot
    else:
        sigback_databg = observable.stack_databg

    # set annotations for the reference data
    refdata.setAnnotation('ErrorBars', '1')
    refdata.setAnnotation('PolyMarkers', '*')
    refdata.setAnnotation('ConnectBins', '0')
    experiment = refdata.path().split("_")[0][5:]
    refdata.setAnnotation('Title', '{} Data'.format(experiment))
    drawonly.append(refdata.path())
    anaobjects.append(refdata)

        
    # set annotations for the data-as-background signal plot
    if show_databg:

        # Calculate the databg CLs for this individual plot 
        contur.factories.likelihood.likelihood_blocks_find_dominant_ts([observable.likelihood],cfg.databg)
        clh = lh.CombinedLikelihood(cfg.databg)
        clh.add_likelihood(observable.likelihood)
        clh.calc_cls()
        CLs = clh.getCLs()

        # add it to the legend.
        if CLs is not None and CLs > 0:
            if observable.likelihood._index is not None and cfg.databg in observable.likelihood._index.keys():
                indextag=r"Bin {},{:3.0f}\%".format(observable.likelihood._index[cfg.databg],100.*CLs)
            else:
                indextag=r"Correlated {:3.0f}\%".format(100.*CLs)
        else:
            indextag="No exclusion"

        sigback_databg.setAnnotation('Title','Data as BG: {}'.format(indextag))
        drawonly.append(sigback_databg.path())
        sigback_databg.setAnnotation('ErrorBars', '1')
        sigback_databg.setAnnotation('LineColor', 'red')
        anaobjects.append(sigback_databg)

    if observable.thyplot:
        # things we only do if there's a SM prediction.
        theory = observable.thyplot
        # identifier for the theory prediction that was used in this case.
        if nostack:
            # in this case we are just plotting signal, without stacking it on any background
            if smtest:
                sigback_smbg   = None
            else:
                sigback_smbg   = observable.sigplot
        else:
            sigback_smbg   = observable.stack_smbg
        
        # set annotations for the data-as-background signal plo
        theory.setAnnotation('RemoveOptions', '0')
        theory.setAnnotation('ErrorBars', '1')
        theory.setAnnotation('LineColor', 'green')
        theory.setAnnotation('ErrorBands','1')
        theory.setAnnotation('ErrorBandColor','green')
        theory.setAnnotation('ErrorBandOpacity','0.3')
        drawonly.append(theory.path())
        anaobjects.append(theory)

        # get the dominant test likelihood for this plot.
        contur.factories.likelihood.likelihood_blocks_find_dominant_ts([observable.likelihood],cfg.smbg)
        clh = lh.CombinedLikelihood(cfg.smbg)
        clh.add_likelihood(observable.likelihood)

        if smtest:

            # Calculate the compatibility between SM and data, using chi2 survival for the number of points
            pval = observable.get_sm_pval()

            # add the SM vs data compatibility to the legend.
            if observable.likelihood._index is not None and cfg.smbg in observable.likelihood._index.keys():
                indextag="p (Bin {})={:4.2f}".format(observable.likelihood._index[cfg.smbg],pval)
            else:
                indextag="p = {:4.2f}".format(pval)

            theory.setAnnotation('Title','{}, {}'.format(theory.title(),indextag))
            
        else:
          
            # dont do all this stuff if we are running without signal.
            # Calculate the smbg CLs for this individual plot 
            clh.calc_cls()
            CLs = clh.getCLs()

            contur.factories.likelihood.likelihood_blocks_find_dominant_ts([observable.likelihood],cfg.expected)
            clh = lh.CombinedLikelihood(cfg.expected)
            clh.add_likelihood(observable.likelihood)
            clh.calc_cls()
            CLs_exp = clh.getCLs()

            # add them to the legend.
            if CLs is not None and CLs_exp is not None and CLs > 0:
                if observable.likelihood._index is not None and cfg.smbg in observable.likelihood._index.keys():
                    indextag=r"Bin {},{:3.0f}\% ({:3.0f}\% expected)".format(observable.likelihood._index[cfg.smbg],100.*CLs,100.*CLs_exp)
                else:
                    indextag=r"Correlated {:3.0f}\% ({:3.0f}\% expected)".format(100.*CLs,100.*CLs_exp)
            elif CLs_exp is not None:
                indextag=r"No exclusion; expected exclusion was {:3.0f}\%".format(100.*CLs_exp)
            else:
                indextag="No exclusion"

            # set annotations for the sm-as-background signal plot
            sigback_smbg.setAnnotation('Title','SM as BG: {}'.format(indextag))
            sigback_smbg.setAnnotation('ErrorBars', '1')
            sigback_smbg.setAnnotation('LineColor', 'blue')
            sigback_smbg.setPath(sigback_smbg.path()+"-SM")
            drawonly.append(sigback_smbg.path())
            anaobjects.append(sigback_smbg)


            
    # Now the overall attributes for the plot.
    plot = Plot()
    
    # Get any updated attributes from plotinfo files
    plotdirs = ['/']
    plotparser = rivet.mkStdPlotParser(plotdirs, )
    for key, val in plotparser.getHeaders(refdata.path()).items():
        plot[key] = val

    plot['DrawOnly'] = ' '.join(drawonly).strip()
    plot['Legend'] = '1'
    plot['MainPlot'] = '1'
    #plot['LogY'] = '1'
    plot['RatioPlot'] = '1'
    plot['RatioPlotSameStyle'] = 0
    plot['RemoveOptions'] = '1'
    #plot['RatioPlotYMin'] = '0.0'
    # plot['RatioPlotMode'] = 'default'
    plot['RatioPlotMode'] = 'deviation'
    plot['RatioPlotYMin'] = '-3.0'
    plot['RatioPlotYMax'] = '3.0'
    if smtest:
        plot['RatioPlotYLabel'] = 'SM/Data'
    else:
        plot['RatioPlotYLabel'] = 'Ratio to Data'

    plot['RatioPlotErrorBandColor'] = 'Yellow'
    plot['RatioPlotReference'] = refdata.path()

    # now the output directory and file
    output = str(plot)
    from io import StringIO
    sio = StringIO()
    yoda.writeFLAT(anaobjects, sio)
    output += sio.getvalue()
    #ana, tag = splitPath(refdata.path())
    ana, tag = splitPath(observable.signal.path())
    outdir = os.path.join(cfg.plot_dir,observable.pool,ana)
    mkoutdir(outdir)
    if smtest:
        outfile = '{}_{}.dat'.format(tag,observable.sm_prediction.id)
    else:
        outfile = '{}.dat'.format(tag)
    outfilepath = os.path.join(outdir, outfile)

    f = open(outfilepath, 'w')
    f.write(output)
    f.close()


def write_sm_file(ana,out_dir,text_string):
    """
    Write an rst file describing the theory predictions available for this analysis.

    :param ana:  the analysis object
    :param out_dir: name of the directory the write to
    :param text_string: an rst-style link, with text, will be appended to this and returned.

    returns text_string with an rst-style link to the new file appended.

    """    
    import contur.factories.yoda_factories as yf

    th_desc = ana.sm()
    ana_file_stem = ana.name
    ana_file_out = os.path.join(out_dir,"SM",ana_file_stem+".rst")
    dat_file_dir = cfg.paths.user_path(cfg.smdir,ana.poolid,ana.name)
    ana_file_dir = os.path.join(out_dir,"SM",ana_file_stem)

    if th_desc:
        text_string += " SM theory predictions are available :doc:`here <SM/{}>`.\n".format(ana_file_stem)

        # this string is the contents on the RST file for this analysis.
        th_str = ":orphan:\n\nStandard Model Predictions for {}\n{}\n\n".format(ana_file_stem,"="*(31+len(ana_file_stem)))

        for prediction in th_desc:

            yf.load_sm_aos(prediction)
            cfg.contur_log.debug("Getting info for theory prediction {} for {}".format(prediction.short_description,ana.shortname))
            insp_ids = prediction.inspids.split(',')
            bibkeys = ""
            for insp_id in insp_ids:
                try:
                    paper_data = cutil.get_inspire(insp_id) 
                    bibkeys+= paper_data['bibkey']
                    bibkeys+=','
                except cfg.ConturError as e:
                    cfg.contur_log.warning("Could not find bibtex key for inspire ID {} in {}: {}".format(insp_id,ana.name,e))
                except url_error:
                    cfg.contur_log.error("Failed to read from server: {}".format(server_error))

            if len(bibkeys)>0 and (not "Failed" in bibkeys[:-1]):
                th_str += "\n {} :cite:`{}`: {}\n".format(prediction.short_description,bibkeys[:-1],prediction.long_description)
            else:
                th_str += "\n {} (Could not find bibtex key) {}\n".format(prediction.short_description,prediction.long_description)


            plots_file_name = "{}/{}_{}.rst".format(ana_file_dir,ana_file_stem,prediction.id)

            th_str += "\n\n   :doc:`{} prediction {} <{}/{}_{}>`.\n".format(ana.name,prediction.id,ana.name,ana.name,prediction.id)

            plots_str = ":orphan:\n\nStandard Model Predictions for {}\n{}\n\n".format(ana_file_stem,"="*(31+len(ana_file_stem)))

            plots_str += "{} (Prediction ID {})\n\n".format(prediction.long_description,prediction.id)
            plots_str += "\n\nStored in file: {} \n\n".format(prediction.file_name)
            
            for ao in prediction.ao.values():
                
                plots_str += "{}: {}\n".format(ao.title(),ao.name())
                
                plots_str += "\n.. figure:: {}_{}.png\n           :scale: 80%\n\n".format(ao.name(),prediction.id)
                
                plots_file = open(plots_file_name, 'w')
                plots_file.write(plots_str)

        # now make the figures
        cutil.mkoutdir(ana_file_dir)
        mp_command = ["make-plots"]
        mp_command.append("-f")
        mp_command.append("png")
        mp_command.append("-o")
        mp_command.append(ana_file_dir)
        cfg.contur_log.info("Looking for SM dat files in {}".format(dat_file_dir))
        #print("Looking for SM dat files in {}".format(dat_file_dir))
        got_dats=False
        for dat_file in glob.glob(os.path.join(dat_file_dir,"*.dat")):
            got_dats=True
            mp_command.append(dat_file)

        if got_dats: 
            subprocess.Popen(mp_command).wait()
            ana_file = open(ana_file_out, 'w')
            ana_file.write(th_str)
        else:   
            print("No dat files found for {}".format(dat_file_dir))
            
    else:
        text_string += ":red:`No SM theory predictions available for this analysis.` \n"

    return text_string


def mkScatter2D(s1):
    """
    Make a Scatter2D from a Scatter1D by treating the points as y values and adding dummy x bins.
    """

    import yoda
    rtn = yoda.Scatter2D()

    xval = 0.5
    for a in s1.annotations():
        rtn.setAnnotation(a, s1.annotation(a))

    rtn.setAnnotation("Type", "Scatter2D");

    for point in s1.points():

        ex_m = xval-0.5
        ex_p = xval+0.5

        y = point.x()
        ey_p = point.xMax() - point.x()
        ey_m = point.x()    - point.xMin()

        pt = yoda.Point2D(xval, y, (0.5,0.5), (ey_p,ey_m))
        rtn.addPoint(pt)
        xval = xval + 1.0

    return rtn

def walklevel(some_dir, level=1):
    """
    Like os.walk but can specify a level to walk to
    useful for managing directories a bit better

    https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    """
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def newlogspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None):
    """
    Numpy logspace returns base^start to base^stop, we modify this here so it returns logspaced between start and stop
    """
    import numpy
    return numpy.logspace(numpy.log(start)/numpy.log(base), numpy.log(stop)/numpy.log(base), num, endpoint, base, dtype)


def get_inspire(inspire_id):
    """
    Function to query InspireHEP database and return a dictionary containing the metadata

    extracted/adapted from rivet-findid

    if contur.config.config.offline is True, no web query is made and returned variables are set to "Offline"
    if contur.config.config.offline is False, but web query fails, returned variables are set to "Failed"


    :arg inspire_id: the ID of the publication on Inspire
    :type inspire_id: ``string``

    :return: pub_data ``dictionary`` -- selected metadata as a dictionary of strings
    """
    
    if not cfg.offline:
        # Get the necessary packages.
        try:
            from urllib.request import urlopen
            import json
        except ImportError:
            from urllib2 import urlopen
            import json
        except  Exception as e:
            cfg.ConturError("Error importing URL modules: {}".format(e))
            cfg.ConturError("Switching to offline mode")
            cfg.offline=True

    pub_data = {}
        
    if cfg.offline:
        pub_data['bibkey']="Offline"
        pub_data['bibtex']="Offline"
    else:
            
        url = "https://inspirehep.net/api/literature/{}".format(inspire_id)

        ## Get and test JSON
        try:
            cfg.contur_log.debug("Querying inspire: {}".format(inspire_id))
            response = urlopen(url)
            cfg.contur_log.debug("Success")
        except Exception as e:
            pub_data['bibkey']="Failed"
            pub_data['bibtex']="Failed"
            cfg.contur_log.error("Error opening URL {}: {}".format(url,e))
            return pub_data

        metadata = json.loads(response.read().decode("utf-8"))
        if metadata.get("status", "") == 404:
            raise cfg.ConturError('ERROR: id {} not found in the InspireHEP database\n'.format(inspire_id))

        try:
            md=metadata["metadata"]
        except KeyError as ke:
            cfg.contur_log.error("Could not find metadata for inspire ID {}".format(inspire_id))
            pub_data['bibkey']="Failed"
            pub_data['bibtex']="Failed"
            return pub_data

        pub_data['bibkey']=str(md["texkeys"][0])
        biburl = metadata["links"]["bibtex"]

        cfg.contur_log.debug("Querying inspire: {}".format(biburl))
        try:
            pub_data['bibtex']=urlopen(biburl).read().decode()
        except Exception as e:
            cfg.contur_log.error("Failed to read bibtex from {} for inspire ID {}".format(biburl,inspire_id))
            pub_data['bibtex']="Failed"
            return pub_data
            
        cfg.contur_log.debug("Success")

    return pub_data

def generate_rivet_anas(webpages):
    """
    Generate various rivet analysis listings from the Contur database.

    - the .ana files for Herwig running

    - the script to set the analysis list environment variables

    - (optionally) the contur webpage listings.

    :param webpages: if true, also write out the contur webpage listings.
    
    """
    # statics
    rivettxt = "insert Rivet:Analyses 0 "
    
    # make the directory if it doesn't already exist
    output_directory = cfg.output_dir
    mkoutdir(output_directory)
    mkoutdir(output_directory+"/SM")

    # open file for the environment setters
    fl = open(output_directory + "/analysis-list", 'w')

    known_beams = cdb.static_db.get_beams()
    known_pools = cdb.static_db.get_pools()
    envStrings = {}

    # build the .ana and env variable setters
    for beam in known_beams:
        analysis_list = cdb.static_db.get_analyses(beam=beam,filter=False) 
        f = open(os.path.join(output_directory, beam.id + ".ana"), 'w')
        envStrings[beam.id] = "export CONTUR_RA{}=\"".format(beam.id)
        for analysis in analysis_list:
            f.write(rivettxt + analysis.name + " # " + analysis.summary() + "\n")
            envStrings[beam.id] = envStrings.get(beam.id) + analysis.name + ","

        f.close()

    for pool in known_pools:
        analysis_list =cdb.static_db.get_analyses(poolid=pool,filter=False)

        if not analysis_list:
            continue

        f = open(os.path.join(output_directory, pool + ".ana"), 'w')
        envStrings[pool] = "export CONTUR_RA_{}=\"".format(pool)
        for analysis in analysis_list:
            f.write(rivettxt + analysis.name + " # " + analysis.summary() + "\n")
            envStrings[pool] = envStrings.get(pool) + analysis.name + ","
    
        f.close()	

    for estr in envStrings.values():
        estr = estr[:len(estr) - 1] + "\""
        fl.write(estr + "\n \n")

    fl.close()
        
    cfg.contur_log.info("Analysis and environment files written to {}".format(output_directory))

    if not webpages:
        return

    web_dir = os.getenv('CONTUR_WEBDIR')
    if web_dir == None:
        web_dir = output_directory
    else:
        web_dir = os.path.join(web_dir,"datasets")

    cfg.contur_log.info("Writing graphics output to {}".format(web_dir))

        
    # style stuff
    style_stuff = ".. raw:: html \n \n <style> .red {color:red} </style> \n \n.. role:: red\n\n"

    # open file for the web page list
    data_list_file = open(os.path.join(web_dir,"data-list.rst"), 'w')
    data_list = "Current Data \n------------ \n"

    bvetoissue = "\nb-jet veto issue\n---------------- \n\n *The following measurements apply a detector-level b-jet veto which is not part of the particle-level fiducial definition and therefore not applied in Rivet. Also applies to CMS Higgs-to-WW analysis. Off by default, can be turned on via command-line, but use with care.* \n"

    higgsww = "\nHiggs to WW\n----------- \n\n *Typically involve large data-driven top background subtraction. If your model contributes to the background as well the results maybe unreliable. Off by default, can be turned on via command-line.* \n"

    higgsgg = "\nHiggs to diphotons\n------------------ \n\n *Higgs to two photons use a data-driven background subtraction. If your model predicts non-resonant photon production this may lead to unreliable results. On by default, can be turned off via command-line.* \n"

    ratios = "\nRatio measurements\n------------------ \n\n *These typically use SM theory for the denominator, and may give unreliable results if your model contributes to both numerator and denominator. On by default, can be turned off via command-line.* \n"

    searches = "\nSearches\n-------- \n\n *Detector-level, using Rivet smearing functions. Off by default, can be turned on via command-line.*\n"

    nutrue = "\nNeutrino Truth\n-------------- \n\n *Uses neutrino flavour truth info, may be misleading for BSM. Off by default, can be turned on via command-line.*\n"

    for ana in sorted(cdb.static_db.get_analyses(filter=False), key=lambda ana: ana.poolid):

        pool = ana.get_pool()
        pool_str = "\n Pool: **{}**  *{}* \n\n".format(pool.id,pool.description)
        
        tmp_str = "   * `{} <https://rivet.hepforge.org/analyses/{}.html>`_, ".format(ana.name,ana.shortname)
        tmp_str += "{} :cite:`{}`. ".format(ana.summary(),ana.bibkey())

        tmp_str = write_sm_file(ana,web_dir,tmp_str)

        if cdb.static_db.hasRatio(ana.name):
            if pool.id in ratios:
                ratios += tmp_str
            else:
                ratios += pool_str + tmp_str

        elif cdb.static_db.hasSearches(ana.name):
            if pool.id in searches:
                searches += tmp_str
            else:
                searches += pool_str + tmp_str

        elif cdb.static_db.hasHiggsgg(ana.name):
            if pool.id in higgsgg:
                higgsgg += tmp_str
            else:
                higgsgg += pool_str + tmp_str

        elif cdb.static_db.hasHiggsWW(ana.name):
            if pool.id in higgsww:
                higgsww += tmp_str
            else:
                higgsww += pool_str + tmp_str

        elif cdb.static_db.hasNuTrue(ana.name):
            if pool.id in nutrue:
                nutrue += tmp_str
            else:
                nutrue += pool_str + tmp_str

        else:
            if pool.id in data_list:
                data_list += tmp_str
            else:
                data_list += pool_str + tmp_str

        if cdb.static_db.hasBVeto(ana.name):
            if pool.id in bvetoissue:
                bvetoissue += tmp_str
            else:
                bvetoissue += pool_str + tmp_str


    data_list_file.write(style_stuff)
    data_list_file.write(data_list)
    data_list_file.write(ratios)
    data_list_file.write(higgsgg)
    data_list_file.write(searches)
    data_list_file.write(nutrue)
    data_list_file.write(higgsww)
    data_list_file.write(bvetoissue)

    cfg.contur_log.info("Data list written to {}".format(web_dir))

def permission_to_continue(message):
    """Get permission to continue program"""
    permission = ""
    while permission.lower() not in ['no', 'yes', 'n', 'y']:
        permission = str(input("{}\n [y/N]: ".format(message)))
        if len(permission)==0:
            permission = 'N'

    if permission.lower() in ['y', 'yes']:
        return True
    else:
        return False


class Plot(dict):
    ''' A tiny Plot object to help writing out the head in the .dat file '''

    def __repr__(self):
        return "# BEGIN PLOT\n" + "\n".join("%s=%s" % (k, v) for k, v in self.items()) + "\n# END PLOT\n\n"


def cleanupCommas(text):
    '''
    Replace commas and multiple spaces in text by single spaces
    '''
    text=text.replace(","," ")
    
    while "  " in text:
        text=text.replace("  ", " ")
    
    return text.strip()

def remove_brackets(text):
    '''
    remove any brackets from text, and try to turn it into a float.
    return None if not possible.
    '''
    res = text.split("(")[0]+text.split(")")[-1]
    try:
        res = float(res)
    except:
        res = None
        
    return res

def compress_particle_info(name,info):
    ''' 
    Turns a dictionary of properties of the particle <name> into simple string-formatted
    dictionary suitable for storing as parameters: 
    (removes commas, backslashes and spaces and puts <particlename>_<property>)

    '''

    info_dict = {}

    info_dict["{}_mass".format(name)]=info["mass"]
    info_dict["{}_width".format(name)]=info["width"]

    for decay, bf in info.items():
        if not (decay=="mass" or decay=="width"):
            decay = decay.replace(",","")
            decay = decay.replace(" ","")
            decay = decay.replace("\\","")
            info_dict["{}_{}".format(name,decay)]=bf

    return info_dict
    

def compress_xsec_info(info,matrix_elements):
    '''
    compresses a dict of subprocess cross sections into a format they can be stored as AUX params
    (removes commas, backslashes and spaces and puts AUX:<name>_<property>)
    Also, if matrix_elements is not None, then remove any which are not in it.

    '''

    info_dict = {}
    for name, value in info.items():
        name = name.replace(",","")
        name = name.replace(" ","")
        name = name.replace("\\rightarrow","_")
        name = name.replace("\\","")
        if matrix_elements is None or name in matrix_elements:
            name = "AUX:{}".format(name)
            info_dict[name]=value
        
    return info_dict

def hack_journal(bibtex):
    ''' 
    Add a dummy journal field if absent, to stop sphinx barfing.
    '''
    if "journal" in bibtex:
        return bibtex
    else:
        newbibtex = bibtex[:-3]+',journal = "no journal"\n}\n'
        return newbibtex

def find_ref_file(analysis):
    '''
    return the REF data file name and path for analysis with name a_name
    if not found, return an empty string.
    '''
    import rivet
    yoda_name = analysis.shortname+".yoda.gz"
    f = rivet.findAnalysisRefFile(yoda_name)
    return f

def find_thy_predictions(analysis,prediction_id=None):
    '''
    return the THY data file name and path for analysis with name a_name
    and chosen ID.
    if not found, return an empty string.
    '''
    import rivet
    
    predictions = cdb.static_db.get_sm_theory(analysis.name)

    if prediction_id is None:
        return predictions
    
    if predictions is not None:
        for sm in predictions:
            if sm.id == prediction_id:
                return sm
            
    return None, None


def get_beam_dirs(beams):
    """
    return a dict of the paths (under cfg.grid) containing the name of each beam, keyed on beam 
    beams = a list of beams to look for.
    """
    scan_dirs = {}

    for root, dirnames, files in sorted(walklevel(cfg.grid,1)):

        for beam in beams:
            for dir in dirnames:
                if beam.id in dir:                    
                    dir_path = os.path.join(cfg.grid,dir)
                    try:
                        if not dir_path in scan_dirs:
                            scan_dirs[beam.id].append(dir_path)
                        else:
                            cfg.contur_log.warning("Directory name {} is ambiguous as to what beam is belongs to.".format(dir_path))
                    except KeyError:
                        scan_dirs[beam.id] = [os.path.join(cfg.grid,dir)]
                        

    return scan_dirs
    
def analysis_select(name, veto_only=False):
    """ 
    return a list true if the analysis passes the select/veto conditions
    """
    import re
    
    for pattern in cfg.vetoAnalyses:
        if re.compile(pattern).search(name):
            return False

    if veto_only:
        return True
        
    if len(cfg.onlyAnalyses)>0:
        for pattern in cfg.onlyAnalyses:
            if re.compile(pattern).search(name):
                return True
        return False
        
    return True

        
