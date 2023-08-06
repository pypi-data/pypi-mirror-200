"""

The Depot module contains the Depot class. This is intended to be the high level analysis control, 
most user access methods should be implemented at this level

"""

import os
import pickle
import numpy as np
import sqlite3 as db 
import scipy.stats as spstat
import contur
import contur.factories.likelihood as lh
import contur.config.config as cfg
import contur.data.static_db as cdb
import contur.util.utils as cutil
from contur.factories.yoda_factories import YodaFactory
from contur.factories.likelihood_point import LikelihoodPoint
from contur.data.data_access_db import write_grid_data


class Depot(object):
    """ Parent analysis class to initialise

    This can be initialised as a blank canvas, then the desired workflow is to add parameter space points to the Depot using
    the :func:`add_point` method. This appends each considered point to the objects internal :attr:`points`. To get the point 
    message from database rather than map file to the Depot using the :func:`add_point_from_db` method. 

    Path for writing out objects is determined by cfg.plot_dir

    """

    def __init__(self):

        self._point_list = []

    def write(self, outDir, args):
        """Function to write depot information to disk
        
        write a results db files to outDir
        if cfg.mapfile is not None, also write out a "map" file containing the full pickle of this depot instance

        :param outDir:
            String of filesystem location to write out the pickle of this instance to
        :type outDir: ``string``

        """
        cutil.mkoutdir(outDir)

        # populate the local database for this grid
        try:
            write_grid_data(args,self)
        except cfg.ConturError as ce:
            cfg.contur_log.error("Failed to write results database. Error was: {}".format(ce))

        if cfg.mapfile is not None:
            path_out = os.path.join(outDir,cfg.mapfile)
            cfg.contur_log.info("Writing output map to : " + path_out)

            with open(path_out, 'wb') as f:
                pickle.dump(self, f, protocol=2)


    def add_point(self, yodafile, param_dict):
        """
        Add yoda file and the corresponding parameter point into the depot
        """

        try:
            yFact = YodaFactory(yodaFilePath=yodafile)
            lh_point = LikelihoodPoint(yodaFactory=yFact, paramPoint=param_dict)

        except cfg.ConturError as ce:
            cfg.contur_log.warning(ce)
            cfg.contur_log.warning("Skipping file.")
            return

        for stat_type in cfg.stat_types:
            
            # get test statistics for each block
            lh.likelihood_blocks_find_dominant_ts(lh_point.likelihood_blocks,stat_type)
                    
            # get cls for each block
            lh.likelihood_blocks_ts_to_cls(lh_point.likelihood_blocks,stat_type)
                

            
        # combine subpools (does it for all test stats, but has to be done after we have found the dominant bin for each test stat (above)
        lh.combine_subpool_likelihoods(lh_point.likelihood_blocks, omitted_pools="")

        for stat_type in cfg.stat_types:
            
            # sort the blocks according to this test statistic
            lh_point.set_sorted_likelihood_blocks(lh.sort_blocks(lh_point.likelihood_blocks,stat_type),stat_type)
            lh_point.set_full_likelihood(stat_type,lh.build_full_likelihood(lh_point.get_sorted_likelihood_blocks(stat_type),stat_type))

            if lh_point.get_full_likelihood(stat_type) is not None:
                cfg.contur_log.info(
                    "Added yodafile with reported {} exclusion of: {} ".format(stat_type,str(lh_point.get_full_likelihood(stat_type).getCLs())))
                lh_point.fill_pool_dict(stat_type)

            else:
                cfg.contur_log.info("No {} likelihood could be evaluated".format(stat_type))
                
        # TODO: move to just using point_list and Likelihood points
        self._point_list.append(lh_point)

        
    def add_points_from_db(self, file_path):
        """
        Get the info of model points from the result database into the depot class
        """
        cfg.results_dbfile = os.path.join(os.getcwd(), file_path)
        try:
            conn = db.connect(cfg.results_dbfile)
        except db.OperationalError:
            cfg.contur_log.error("Failed to open result DB file: {}".format(cfg.results_dbfile))
            raise
                
        c = conn.cursor()
        # start with map_id to select all related data info in a run
        id = c.execute("select id from map").fetchall()
        for map_id in id:
            map_id = map_id[0]
            # select all run_id which map_id is same as current map_id
            run_id_list = c.execute("select id from run where map_id = " + str(map_id) + ";").fetchall()
            run_id_start = run_id_list[0][0]
            run_id_end = run_id_list[-1][0]
            # calculate the number of points in current run
            point_num = (run_id_end-run_id_start+1) / 3
            for num in range(int(point_num)):
                # set a flag to avoid reading param_point repeatedly in the same point
                flag = True
                likelihood_point = LikelihoodPoint()
                param_point = {}

                for run_id in range(3*num+run_id_start,3*num+run_id_start+3):
                    model_point_id = c.execute("select model_point_id from run where id =" + str(run_id) + ";").fetchone()[0]
                    stat_type = c.execute("select stat_type from run where id =" + str(run_id) + ";").fetchone()[0]
                    if flag:        
                        flag = False
                        search_sql1 = "select name from parameter_value where model_point_id =" + str(model_point_id) + ";"
                        name = c.execute(search_sql1).fetchall()
                        search_sql2 = "select value from parameter_value where model_point_id =" + str(model_point_id) + ";"
                        value = c.execute(search_sql2).fetchall()
                        # store parameter name and value in a dicionary
                        for index, point_name in enumerate(name):
                            param_point[point_name[0]] = value[index][0]
                        

                    combined_exclusion = c.execute("select combined_exclusion from run where model_point_id =" + str(model_point_id) + ";").fetchone()[0]
                    
                    pool_name = c.execute("select pool_name from exclusions where run_id =" + str(run_id) + ";").fetchall()
                    exclusion = c.execute("select exclusion from exclusions where run_id =" + str(run_id) + ";").fetchall()
                    # use a dictionary to store pool name and exclusion result in each run
                    pool_exclusion = {}
                    for index, name in enumerate(pool_name):
                        pool_exclusion[name[0]] = exclusion[index][0]

                    pool_name = c.execute("select pool_name from intermediate_result where run_id =" + str(run_id) + ";").fetchall()
                    ts_b = c.execute("select ts_b from intermediate_result where run_id =" + str(run_id) + ";").fetchall()
                    ts_s_b = c.execute("select ts_s_b from intermediate_result where run_id =" + str(run_id) + ";").fetchall()
                    # use the dictionaries to store pool name and ts_b/ts_s_b result in each run
                    pool_ts_b = {}
                    pool_ts_s_b = {}
                    for index, name in enumerate(pool_name):
                        pool_ts_b[name[0]] = ts_b[index][0]
                        pool_ts_s_b[name[0]] = ts_s_b[index][0]


                    # use a list to store each data type in a map
                    likelihood_point.store_point_info(stat_type, combined_exclusion, pool_exclusion, pool_ts_b, pool_ts_s_b)
                likelihood_point.store_param_point(param_point)
                # add the likelihood point into the point list
                self._point_list.append(likelihood_point)
        conn.commit()
        conn.close()

    def resort_points(self):
        """Function to trigger rerunning of the sorting algorithm on all items in the depot, 
        typically if this list has been affected by a merge by a call to :func:`contur.depot.merge`
        """

        for p in self.points:
            for stat_type in cfg.stat_types:
                p.resort_blocks(stat_type)

    def merge(self, depot):
        """
        Function to merge this conturDepot instance with another.
        
        Points with identical parameters will be combined. If point from the input Depot is not present in this Depot,
        it will be added.

        :param depot:
            Additional instance to conturDepot to merge with this one
        :type depot: :class:`contur.conturDepot`


        """
        new_points = []
        for point in depot.points:

            merged = False

            # look through the points to see if this matches any.
            for p in self.points:

                if not merged:
                    same = True
                    valid = True
                    for parameter_name, value in p.param_point.items():
                        try:
                            # we don't demand the auxilliary parameters match, since they can be things like
                            # cross secitons, which will depend on the beam as well as the model point.
                            if point.param_point[parameter_name] != value and not parameter_name.startswith("AUX:"):
                                same = False
                                break
                        except KeyError:
                            cfg.contur_log.warning("Not merging. Parameter name not found:" + parameter_name)
                            valid = False

                    # merge this point with an existing one
                    if same and valid:
                        cfg.contur_log.debug("Merging {} with {}".format(point.param_point,p.param_point))
                        for stat_type in cfg.stat_types:
                            try:
                                cfg.contur_log.debug("Previous CLs: {} , {}".format(point.get_full_likelihood(stat_type).getCLs(),p.get_full_likelihood(stat_type).getCLs()))
                                blocks = p.get_sorted_likelihood_blocks(stat_type)
                                blocks.extend(point.get_sorted_likelihood_blocks(stat_type))
                            except AttributeError:
                                # This happens when not likelihood was evaluated for a particular block, so
                                # we can't query it for a CLs...
                                pass

                        merged = True

            # this is a new point
            if not merged:
                new_points.append(point)
                cfg.contur_log.debug("Adding new point {} with dominant.".format(point.param_point))
                

        if len(new_points)>0:
            cfg.contur_log.debug("Adding {} new points to {}".format(len(new_points),len(self.points)))
            self.points.extend(new_points)


    def _build_frame(self, include_dominant_pools=False, include_per_pool_cls=False):
        """:return pandas.DataFrame of the depot points"""
        try:
            import pandas as pd
        except ImportError:
            cfg.contur_log.error("Pandas module not available. Please, ensure it is installed and available in your PYTHONPATH.")

        try:
            frame = pd.DataFrame(
                [likelihood_point.param_point for likelihood_point in self.points])

            for stat_type in cfg.stat_types:
                frame['CL{}'.format(stat_type)] = [
                    likelihood_point.get_full_likelihood(stat_type).getCLs() for likelihood_point in self.points]

                if include_dominant_pools:
                    frame['dominant-pool{}'.format(stat_type)] = [
                        likelihood_point.get_dominant_pool(stat_type).pools
                        for likelihood_point in self.points
                    ]
                    frame['dominant-pool-tag{}'.format(stat_type)] = [
                        likelihood_point.get_dominant_pool(stat_type).tags
                        for likelihood_point in self.points
                    ]

                if include_per_pool_cls:
                    poolsDict = {}
                    for likelihood_point in self.points:
                       for block in likelihood_point.get_sorted_likelihood_blocks(stat_type):
                          poolName = block.pools
                          poolCLS = block.getCLs(stat_type)
                          if not poolName in poolsDict.keys(): poolsDict[poolName] = []
                          poolsDict[poolName] += [poolCLS]
                       maxLen = max([len(v) for k,v in poolsDict.items()])

                       #deal with cases where an entry for a given pool is missing
                       for k,v in poolsDict.items():
                         while len(v) < maxLen:
                            cfg.contur_log.warning("Point {} has no entry for pool {}: padding with 0.".format(self.points.index(likelihood_point), k))
                            v += [0]

                    for  pool, cls_values in sorted(poolsDict.items()):
                      frame[pool+stat_type] = cls_values
            return frame
        except:
#            cfg.contur_log.error("List of LikelihoodPoints is empty, add parameter points to depot")
            raise
            
    def export(self, path, include_dominant_pools=True, include_per_pool_cls=False):
        self._build_frame(include_dominant_pools, include_per_pool_cls).to_csv(path, index=False)

    def write_summary_file(self, message):
        """
        Write a brief text summary of a conturDepot, describing the run conditions and results.

        If cfg.gridMode is False, will also write info about the
        most sensitive histograms in each pool, for parsing by contur-mkhtml

        :param message: text (string) message containing the run conditions for this depot

        the name of the directory to write the file into will be determined by cfg.output_dir

        """

        cutil.mkoutdir(cfg.output_dir)
        sumfn = open(os.path.join(cfg.output_dir,cfg.summary_file), 'w')

        if cfg.gridMode:
            sumfn.write(message)

        else:

            # summary function will just read the first point in the depot
            result = ""
            for stat_type in cfg.stat_types:
                try:
                    result += "\nCombined {:<{}} exclusion for these plots is {:.2%}".format(stat_type, len(max(cfg.stat_types, key=len)), self.points[0].combined_exclusion_dict[stat_type])
                except:
                    result += "\nCould not evaluate {} exclusion for these data.".format(stat_type)
                    
                    
            sumfn.write(message + "\n" + result + "\n")
            sumfn.write("\npools")

            if len(self.points)>0:
                lh_point = self.points[0]
                for pool in cdb.get_pools():
                    pool_summary = "\nPool:{}\n".format(pool)


                    got_it = []
                    for lhb in lh_point.likelihood_blocks:            
                        if lhb.pools == pool:
                            for stat_type in cfg.stat_types:
                                if lh_point.get_sorted_likelihood_blocks(stat_type) is not None and lhb in lh_point.get_sorted_likelihood_blocks(stat_type):
                                    pool_summary+="Exclusion with {}={:.8f}\n".format(stat_type,lhb.getCLs(stat_type))
                                    pool_summary+="{}\n".format(lhb.tags)
                                    got_it.append(stat_type)

                    if len(got_it)>0:
                        for stat_type in cfg.stat_types:
                            if not stat_type in got_it:
                                pool_summary+="No exclusion evaluated for {}\n".format(stat_type,lhb.getCLs(stat_type))
                        sumfn.write(pool_summary)

            cfg.contur_log.info(result)

            sumfn.close()

    
    def write_summary_dict(self, output_opts):
        """
        Write a brief text summary of a conturDepot to a (returned) dictionary,
        intended for use with yoda stream input.

        :param output_opts: list of requested outputs to put in the summary dict
        """  
        summary_dict = {}
        for stat_type in cfg.stat_types:
            summary_dict[stat_type] = {}

            # As in write_summary_file above, summary function will 
            # just read the first entry in the depot.
            #full_like = self.points[0].combined_exclusion_dict[stat_type]
            full_like = self.points[0].get_full_likelihood(stat_type)
            like_blocks = self.points[0].get_sorted_likelihood_blocks(stat_type)

            if "LLR" in output_opts:
                if (full_like.get_ts_s_b() is not None and full_like.get_ts_b() is not None):
                    summary_dict[stat_type]["LLR"] = full_like.get_ts_s_b() - full_like.get_ts_b()
                else:
                    summary_dict[stat_type]["LLR"] = 0.0

            if "CLs" in output_opts:
                summary_dict[stat_type]["CLs"] = full_like.getCLs()

            if "Pool_LLR" in output_opts:
                summary_dict[stat_type]["Pool_LLR"] = {}
                for block in like_blocks:
                    if ((block.get_ts_s_b(stat_type) is not None)
                    and (block.get_ts_b(stat_type) is not None)):
                        summary_dict[stat_type]["Pool_LLR"][block.pools] = (
                            block.get_ts_s_b(stat_type) - block.get_ts_b(stat_type))
                    else:
                        summary_dict[stat_type]["Pool_LLR"][block.pools] = 0.0

            if "Pool_CLs" in output_opts:
                summary_dict[stat_type]["Pool_CLs"] = {}
                for block in like_blocks:
                    summary_dict[stat_type]["Pool_CLs"][block.pools] = block.getCLs(stat_type)

            if "Pool_tags" in output_opts:
                summary_dict[stat_type]["Pool_tags"] = {}
                for block in like_blocks:
                    summary_dict[stat_type]["Pool_tags"][block.pools] = block.tags

        return summary_dict

       
    @property
    def points(self):
        """
        The master list of :class:`~contur.factories.depot.LikelihoodPoint` instances added to the Depot instance

        **type** ( ``list`` [ :class:`~contur.factories.depot.LikelihoodPoint` ])
        """
        return self._point_list
    
    @property
    def frame(self):
        """
        A ``pandas.DataFrame`` representing the CLs interval for each point in :attr:`points`

        **type** (``pandas.DataFrame``)
        """
        return self._build_frame()

    def __repr__(self):
        return "%s with %s added points" % (self.__class__.__name__, len(self.points))


    
def ts_to_cls(ts_tuple_list):
    """
    calculate the final cls value
    """
    if type(ts_tuple_list) == tuple:
        ts_tuple_list = [ts_tuple_list] #place in list

    log_p_vals = spstat.norm.logsf(np.sqrt(np.array(ts_tuple_list)))
    cls = []

    for ts_index in range(len(log_p_vals)):
        log_pval_b = log_p_vals[ts_index][1]
        log_pval_sb = log_p_vals[ts_index][0]

        try:
            # have stayed with logs for as long as possible for numerical stability
            cls_ts_index = 1 - np.exp(log_pval_sb - log_pval_b)
        except FloatingPointError:
            cls_ts_index = 1

        if (cls_ts_index is not None and cls_ts_index < 0):
            cls_ts_index = 0

        cls.append(cls_ts_index)
    
    return cls  
