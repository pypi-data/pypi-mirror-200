import numpy as np
import contur
import contur.config.config as cfg
import contur.data.static_db as cdb
 
class CovarianceBuilder(object):
    """
    `ao` Yoda AO
    apply_min: apply the minimum number of systematic uncertainties criteria when determining
    whether or not to use the error breakdown for correlations.

    Class to handle retrieval of annotations/errors from YODA objects
    """
    def __init__(self, ao, apply_min=True):
        self.ao=ao
        self.hasBreakdown=self._getBreakdownAttr(apply_min)
        self.readMatrix  =self._getMatrixAttr()
        self.nbins=self.ao.numPoints()
        self.cov=None
        self.uncov=None
        self.errorBreakdown=None
        self.covariance_matrix=None

    def _getBreakdownAttr(self,apply_min):
        """
        return true if this AO has an error breakdown
        """
        if not self.ao.hasValidErrorBreakdown():
            return False
        if apply_min and len(self.ao.variations())<cfg.min_num_sys:
            return False
        return True

    def _getMatrixAttr(self):
        """
        return true if this AO has a covariance matrix stored in another AO. 

        """

        if cfg.diag:
            return False
        
        self._covname =  cdb.get_covariance_name(self.ao.path())
        if self._covname:
            return True
        else:
            self._corrname =  cdb.get_correlation_name(self.ao.path())
            if self._corrname:
                return True

        return False
    
    def read_cov_matrix(self,aos):
        """
        read the covariance matrix from another AO and return it.
        """
        if not self.readMatrix:
            return None

        # if it has alreader been read, don't do it again.
        if self.covariance_matrix is not None:
            return self.covariance_matrix

        if self._covname:
            is_cov = True
            name = self._covname
            cfg.contur_log.debug("reading covariance matrix {}".format(self._covname))
        else:
            is_cov = False
            name = self._corrname
            cfg.contur_log.debug("reading correlation matrix {}".format(self._corrname))
            
        # read the covariance matrix into an array.
        matrix_ao = aos[name]

        try:
            nbins = len(self.ao.xVals()) 
            self.covariance_matrix = np.zeros((nbins,nbins))

            i = 0
            j = 0
            for z in matrix_ao.zVals():
                self.covariance_matrix[i][j] = z
                i=i+1
                if i==nbins:
                    i=0
                    j=j+1
        except:
            cfg.contur_log.error("failed to read {}".format(self._covname))
            raise

        if not is_cov:
            # need to pre and post muliply by uncertainties
            cfg.contur_log.debug("Converting correaltion to covariance. {}".format(self.covariance_matrix))
            yErrs = np.diag(self.ao.yErrAvgs())
            self.covariance_matrix = np.dot(yErrs, np.dot(self.covariance_matrix, yErrs))
            cfg.contur_log.debug("resulting matrix is: {}".format(self.covariance_matrix))
            
        return self.covariance_matrix

    
    def buildCovFromBreakdown(self,ignore_corrs=False):
        """
        Get the covariance, calculated by YODA from the error breakdown, and return it.
        """
        
        return self.ao.covarianceMatrix(ignore_corrs) 

    def buildCovFromErrorBar(self):
        """
        Build the diagonal covariance from error bars and return it.
        """
        
        dummyM = np.outer(range(self.nbins), range(self.nbins))
        covM = np.zeros(dummyM.shape)
        systErrs = np.zeros(self.nbins)
        
        for ibin in range(self.nbins):
            #symmetrize the errors (be conservative - use the largest!)
            systErrs[ibin] = max(abs(self.ao.points()[ibin].yErrs()[0]),abs(self.ao.points()[ibin].yErrs()[1]))
            # Note that yoda will take the average (below) when it computes a covariance matrix from the error breakdown.
            # There can also be round errors depending on the precision of the error breakdown.
            #systErrs[ibin] = (abs(self.ao.points()[ibin].yErrs()[0])+abs(self.ao.points()[ibin].yErrs()[1]))*0.5
            
        covM += np.diag(systErrs * systErrs)

        return covM

    def getErrorBreakdown(self):
        """ return the breakdown of (symmetrised) uncertainties """

        if self.hasBreakdown:
            if self.errorBreakdown is not None:
                return self.errorBreakdown

            else:
                self.errorBreakdown={}
                # Build the error breakdown from the annotation
                errMap_values = {}
                ibin=0
                for point in self.ao.points():
                    try:
                        errMap_values[ibin] = point.errMap()
                    except:
                        # handle occasional messed up entries
                        cfg.contur_log.error("Corrupted point error")
                        raise
                    ibin=ibin+1

                for source in self.ao.variations():
                    if len(source)>0:
                        systErrs = np.zeros(self.nbins)
                        ibin=0
                        for point in self.ao.points():
                            nomVal = point.y()
                            errMap_single_value = errMap_values[ibin]
                            #symmetrize the errors (be conservative - use the largest!)
                            # Note that yoda will take the average when it computes a covariance matrix from the error breakdown.
                            # There can also be round errors depending on the precision of the error breakdown.
                            systErrs[ibin]=max(abs(errMap_single_value[source][0]),abs(errMap_single_value[source][1]))
                            
                            ibin=ibin+1
                        self.errorBreakdown[source] = systErrs

            cfg.contur_log.debug("Error breakdown is: {}".format(self.errorBreakdown))

            return self.errorBreakdown
            
        else:
            return {}

            


