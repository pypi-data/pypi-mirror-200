import contur.config.config as cfg
import contur.factories.likelihood as lh


class LikelihoodPoint(object):
    """
    Save the statistical information about likelihood points in a run,  which can then be manipulated to sort them,
    calculate a full likelihood result, exclusions result, test b result, test s+b result with related stat_type 
    and a parameter point dictionary

    If instantiated with a valid parameter dictionary this will be added as a property
    If instantiated with a valid YodaFactory, its likielihood blocks will be associated with this likelihood point

    If these are not provided, a blank point will be created which can be populated later (e.g. from a results database)

    """

    def __init__(self, paramPoint={}, yodaFactory=None):
        """
        :param paramPoint:
            Dictionary of model parameter: value pairs.
        :type paramPoint: ``dict``

        :param yodaFactory:
            String of filesystem location to write out the pickle of this instance to
        :type yodaFactory: ``contur.factiories.yoda_factories.YodaFactory``
        """

        self.param_point = paramPoint
        self.pool_exclusion_dict = {}
        self.pool_ts_b = {}
        self.pool_ts_s_b = {}
        self.combined_exclusion_dict = {}
        self.likelihood_blocks = None

        self._sorted_likelihood_blocks = {}
        self._full_likelihood = {}

        # set up three versions of the full likelihood, one for each type of stat calculation.
        for stat_type in cfg.stat_types:
            self._full_likelihood[stat_type] = lh.CombinedLikelihood(stat_type)
        
        if yodaFactory is not None:
            self.likelihood_blocks = yodaFactory._likelihood_blocks            
            for stat_type in cfg.stat_types:

                if self.get_sorted_likelihood_blocks(stat_type) is not None:
                    self.fill_pool_dict(stat_type)
                    
    def fill_pool_dict(self,stat_type):
        pool_dict = {}
        try:
            self.combined_exclusion_dict[stat_type] = self.get_full_likelihood(stat_type).getCLs()
            for p in self.get_sorted_likelihood_blocks(stat_type):
                pool_dict[p.pools] = p.getCLs(stat_type)

        except AttributeError:
            self.combined_exclusion_dict[stat_type] = None

        self.pool_exclusion_dict[stat_type] = pool_dict

                    
    def resort_blocks(self,stat_type,omitted_pools=""):
        """
        Function to sort the :attr:`sorted_likelihood_blocks` list. Used for resorting after a merging exclusively.
        :Keyword Arguments:
        * *stat_type* (``string``) -- which statisic type (default, SM background or expected) is being sorted by.
        """

        try:
            self._sorted_likelihood_blocks[stat_type] = lh.sort_blocks(self._sorted_likelihood_blocks[stat_type],stat_type,omitted_pools="")
            self._full_likelihood[stat_type] = lh.build_full_likelihood(self.get_sorted_likelihood_blocks(stat_type),stat_type)
        except ValueError as ve:
            cfg.contur_log.warning("Unable to sort likelihoods for {}. Exception: {}".format(stat_type,ve))

        self._full_likelihood[stat_type] = lh.build_full_likelihood(self.get_sorted_likelihood_blocks(stat_type),stat_type)
    
        # cleanup some bulk we don't need  @TODO make this a separate cleanup function.
        if hasattr(self, '_likelihood_blocks'):
            del self._likelihood_blocks
        if hasattr(self, 'yodaFilePath'):
            del self.yodaFilePath
    
    def get_sorted_likelihood_blocks(self,stat_type=None):
        """
        The list of reduced component likelihood blocks extracted from the result file, sorted according
        the test statisitic of type `stat_type`. If stat_type is None, return the whole dictionary.

        **type** ( ``list`` [ :class:`~contur.factories.likelihood.Likelihood` ])

        """
        if stat_type is None:
            return self._sorted_likelihood_blocks

        if stat_type in self._sorted_likelihood_blocks.keys():
            return self._sorted_likelihood_blocks[stat_type]
        else:
            return None
        
    def set_sorted_likelihood_blocks(self, value, stat_type):
        self._sorted_likelihood_blocks[stat_type] = value


    def get_dominant_pool(self,stat_type):
        """returns the likelihood block with the highest confidence level"""
        try:
            tmp = max(self._sorted_likelihood_blocks[stat_type], key=lambda block: block.getCLs(stat_type))
        except ValueError:
            tmp = None
        return tmp

                
    def __repr__(self):
        return repr(self.param_point)

    def store_point_info(self, statType, combinedExclusion, poolExclusion, poolTestb, poolTestsb):
        """
        :param statType:
            string, represent the point type
        :type combinedExclusion: ``string``
        :param combinedExclusion:
            full likelihood for a parameter point
        :type combinedExclusion: ``float``
        :param poolExclusion:
            **key** ``string`` pool name : **value** ``double``
        :type poolExclusion: ``dict``
        :param poolTestb:
            **key** ``string`` pool name : **value** ``double``
        :type poolTestb: ``dict``
        :param poolTestsb:
            **key** ``string`` pool name : **value** ``double``
        :type poolTestsb: ``dict``
        """
        self.combined_exclusion_dict[statType] = combinedExclusion
        self.pool_exclusion_dict[statType] = poolExclusion
        self.pool_ts_b[statType] = poolTestb
        self.pool_ts_s_b[statType] = poolTestsb
        
    def store_param_point(self, paramPoint):
        """
        :param paramPoint:
            **key** ``string`` param name : **value** ``float``
        :type paramPoint: ``dict``
        """
        self.param_point = paramPoint

    def recalculate_CLs(self, stat_type, omitted_pools=""):
        """
        recalculate the combined exclusion after excluding the omitted pool in the class
        :param omitted_pools:
            string, the name of the pool to ignore 
        :type omiited_pools: ``string``
        """
        if omitted_pools in self.pool_ts_b[stat_type].keys():
            self.pool_ts_b[stat_type].pop(omitted_pools)
            self.pool_ts_s_b[stat_type].pop(omitted_pools)

            sum_ts_b = 0
            sum_ts_s_b = 0
            for pool in self.pool_ts_b[stat_type]:
                sum_ts_b += self.pool_ts_b[stat_type][pool]
            for pool in self.pool_ts_s_b[stat_type]:
                sum_ts_s_b += self.pool_ts_s_b[stat_type][pool]
            cls = ts_to_cls([(sum_ts_b, sum_ts_s_b)])[0]
            self.combined_exclusion_dict[stat_type] = cls
        return self.combined_exclusion_dict[stat_type]

    @property
    def likelihood_blocks(self):
        """The list of all component likelihood blocks extracted from the result file

        This attribute is the total information in the result` file, but does not account for potential correlation/
        overlap between the members of the list

        **type** ( ``list`` [ :class:`~contur.factories.likelihood.Likelihood` ])
        """
        return self._likelihood_blocks
    
    @likelihood_blocks.setter
    def likelihood_blocks(self, value):
        self._likelihood_blocks = value


    def get_full_likelihood(self,stat_type=None):
        """
        The full likelihood representing the result file in it's entirety.

        If stat_type is specified, return to entry for it. Else return the dict of all of them.

        **type** (:class:`~contur.factories.likelihood.CombinedLikelihood`)
        """
        try:
            if stat_type is None:
                return self._full_likelihood
            else:
                return self._full_likelihood[stat_type]
        except:
            if stat_type is None:
                return self.yoda_factory._full_likelihood
            else:
                return self.yoda_factory._full_likelihood[stat_type]


            
    def set_full_likelihood(self, stat_type, value):
        self._full_likelihood[stat_type] = value
        
    def set_full_likelihood(self, stat_type, value):
        self._full_likelihood[stat_type] = value

    def __repr__(self):
        return "%s with %s blocks, holding %s" % (self.__class__.__name__, len(self.likelihood_blocks), self.likelihood)

