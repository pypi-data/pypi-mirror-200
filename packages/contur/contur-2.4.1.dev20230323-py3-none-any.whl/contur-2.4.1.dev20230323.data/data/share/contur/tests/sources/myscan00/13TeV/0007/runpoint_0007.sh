#! /bin/bash
#$ -j y # Merge the error and output streams into a single file
#$ -o /unix/atlas3/jmb/Work/Regression_Test/myscan01/13TeV/0007/contur.log # Output file path
source /unix/cedar/software/cos7/Herwig-repo_Rivet-repo/setupEnv.sh;
export CONTUR_DATA_PATH=/home/jmb/gitstuff/contur-dev
export CONTUR_USER_DIR=/home/jmb/gitstuff/contur-dev/../contur_users
export RIVET_ANALYSIS_PATH=/home/jmb/gitstuff/contur-dev/../contur_users:/home/jmb/gitstuff/contur-dev/data/Rivet
export RIVET_DATA_PATH=/home/jmb/gitstuff/contur-dev/../contur_users:/home/jmb/gitstuff/contur-dev/data/Rivet:/home/jmb/gitstuff/contur-dev/data/Theory
source $CONTUR_USER_DIR/analysis-list
cd /unix/atlas3/jmb/Work/Regression_Test/myscan01/13TeV/0007
Herwig read herwig.in -I /unix/atlas3/jmb/Work/Regression_Test/RunInfo -L /unix/atlas3/jmb/Work/Regression_Test/RunInfo;
Herwig run herwig.run --seed=101  --tag=runpoint_0007  --numevents=30000 ;
