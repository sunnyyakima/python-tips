
# process scRNAseq files: concat, and filter

import pandas as pd
import re

df_AB2945 = pd.read_csv("GSM_AB2945.txt", sep='\t')
df_AB2948 = pd.read_csv("GSM_AB2948.txt", sep="\t")
df_AB2955 = pd.read_csv("GSM_AB2955.txt", sep='\t')
df_AB2956 = pd.read_csv("GSM_AB2956.txt", sep="\t")
df_AB2963 = pd.read_csv("GSM_AB2963.txt", sep="\t")
df_AB2969 = pd.read_csv("GSM_AB2969.txt", sep="\t")
df_AB3061 = pd.read_csv("GSM_AB3061.txt", sep="\t")
df_AB3060 = pd.read_csv("GSM_AB3060.txt", sep="\t")
df_AB3326 = pd.read_csv("GSM_AB3326.txt", sep="\t")
df_AB3337 = pd.read_csv("GSM_AB3337.txt", sep="\t")
df_AB4468 = pd.read_csv("GSM_AB4468.txt", sep="\t")
df_AB4470 = pd.read_csv("GSM_AB4470.txt", sep="\t")
df_AB4469 = pd.read_csv("GSM_AB4469.txt", sep="\t")
df_AB4471 = pd.read_csv("GSM_AB4471.txt", sep="\t")
df_AB4472 = pd.read_csv("GSM_AB4472.txt", sep="\t")

df = pd.concat([df_AB2945,df_AB2948,df_AB2955,df_AB2956,df_AB2963,df_AB2969,df_AB3061,df_AB3060,df_AB3326,df_AB3337,df_AB4468,df_AB4470,df_AB4469,df_AB4471,df_AB4472], axis = 1) 

df_droped = df.drop([x for x in df.index if re.match("IG", x)] )

df_droped.to_csv("MGUS_concat_filterIG.csv")

# running scenic
# use virenv
# . activate pyscenic2

import os
import glob
import pickle
import pandas as pd
import numpy as np
 
from dask.diagnostics import ProgressBar

from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2
 
from pyscenic.rnkdb import FeatherRankingDatabase as RankingDatabase
from pyscenic.utils import modules_from_adjacencies, load_motifs
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell
 
import seaborn as sns
 
DATA_FOLDER="./tmp"
RESOURCES_FOLDER="./resources"
DATABASE_FOLDER = "./databases/"

ADJACENCIES_FNAME = os.path.join(DATA_FOLDER, "adjacencies.tsv")
DATABASES_GLOB = os.path.join(DATABASE_FOLDER, "hg19-*.feather")
MOTIF_ANNOTATIONS_FNAME = os.path.join(RESOURCES_FOLDER, "motifs-v9-nr.hgnc-m0.001-o0.0.tbl")
MM_TFS_FNAME = os.path.join(RESOURCES_FOLDER, 'TF_names_v_1.01.txt')

# expression 
SC_EXP_FNAME = os.path.join(RESOURCES_FOLDER, "MGUS_concat_filterIG.csv")
REGULONS_FNAME = os.path.join(DATA_FOLDER, "regulons.p")
MOTIFS_FNAME = os.path.join(DATA_FOLDER, "motifs.csv")
MODULES_FNAME = os.path.join(DATA_FOLDER, "modules.p")
 
ex_matrix = pd.read_csv(SC_EXP_FNAME, sep='\t', header=0, index_col=0).T
ex_matrix.shape
#(0, 57418)
ex_matrix = pd.read_csv(SC_EXP_FNAME, sep=',', header=0, index_col=0).T
ex_matrix.shape
#(5760, 57418)
 
tf_names = load_tf_names(MM_TFS_FNAME)
db_fnames = glob.glob(DATABASES_GLOB) 
 
def name(fname):
    return os.path.basename(fname).split(".")[0]
 
dbs = [RankingDatabase(fname=fname, name=name(fname)) for fname in db_fnames]
dbs
[FeatherRankingDatabase(name="hg19-tss-centered-10kb-10species"), FeatherRankingDatabase(name="hg19-tss-centered-5kb-10speci
es"), FeatherRankingDatabase(name="hg19-500bp-upstream-7species"), FeatherRankingDatabase(name="hg19-tss-centered-5kb-7speci
es"), FeatherRankingDatabase(name="hg19-500bp-upstream-10species"), FeatherRankingDatabase(name="hg19-tss-centered-10kb-7spe
cies")]
 
adjacencies = grnboost2(ex_matrix, tf_names=tf_names, verbose=True) 

adjacencies.head()
adjacencies.to_csv(ADJACENCIES_FNAME, index=False, sep='\t')
#adjacencies = pd.read_csv(ADJACENCIES_FNAME, sep='\t')

modules = list(modules_from_adjacencies(adjacencies, ex_matrix))

with open(MODULES_FNAME, 'wb') as f:
    pickle.dump(modules, f)

#with open(MODULES_FNAME, 'rb') as f:
#    modules = pickle.load(f) 

# Phase II: Prune modules for targets with cis regulatory footprints
df = prune2df(dbs, modules, MOTIF_ANNOTATIONS_FNAME) # computational extensive  
df.head()
df.to_csv(MOTIFS_FNAME)
regulons = df2regulons(df)

with open(REGULONS_FNAME, 'wb') as f:
    pickle.dump(regulons, f)
#with open(REGULONS_FNAME, 'rb') as f:
#    regulons = pickle.load(f)

auc_mtx = aucell(ex_matrix, regulons, num_workers=1)

sns.clustermap(auc_mtx, figsize=(12,12))
import matplotlib.pyplot as plt
plt.show()



