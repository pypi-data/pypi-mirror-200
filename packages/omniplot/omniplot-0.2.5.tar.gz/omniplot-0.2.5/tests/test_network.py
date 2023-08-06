import sys, os 
import sys
#sys.path.append("../omniplot")
from omniplot  import networkplot as onp
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx
import matplotlib.pyplot as plt
import igraph
from omniplot import igraph_classes
import numpy as np
from natsort import natsorted as nts
from matplotlib.lines import Line2D
import sys
import seaborn as sns
from typing import Union, List, Dict, Optional
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import pandas as pd
from omniplot.chipseq_utils import _calc_pearson
from omniplot.utils import _baumkuchen_xy, _save, _separate_data
from scipy.stats import zscore
from joblib import Parallel, delayed
from scipy.spatial.distance import pdist, squareform
import itertools as it
from datashader.bundling import hammer_bundle
test="pienode"
test="correlation"
test="correlation"
if test=="correlation":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    df=df.reset_index()
    onp.correlation(df, category=["species", "island","sex"], 
                method="pearson", 
                ztransform=True,
                clustering ="asyn_fluidc",show_edges=True, bundle=False)
    plt.show()
    
elif test=="sankey_category":
    df=pd.read_csv("./data/kmeans_result.csv")
    onp.sankey_category(df, ["kmeans2","kmeans3","sex"],
                    colormode="alternative",
                    altcat="species",
                    show_percentage=False,
                    show_percentage_target=False,
                    hatch=True)
    plt.show()
elif test=="pienode":
    edges=[[0,0],[0,1],[0,2],[2,1],[2,3],[3,4],[0,5]]
    edge_width=[1 for i in range(len(edges))]
    nodes=["A","B","C","D","E","F"]
    onp.pie_features={"A":{"frac":np.array([50,50]),"label":np.array(["a","b"])},
                    "B":{"frac":np.array([90,5,5]),"label":np.array(["a","b","c"])},
                    "C":{"frac":np.array([100]),"label":np.array(["c"])},
                    "D":{"frac":np.array([100]),"label":np.array(["b"])},
                    "E":{"frac":np.array([100]),"label":np.array(["a"])},
                    "F":{"frac":np.array([10,20,30]),"label":np.array(["a","b","c"])}}
    
    g=igraph.Graph(edges=edges)
    layout = g.layout("fr")
    fraclist=[100,50,20,0]
    labels=["a","b","c","d"]
    pie_features={"node":[],"label":[],"frac":[]}
    for n in nodes:
        tmp=np.random.choice(fraclist,4)
        for l, f in zip(labels, tmp):
            pie_features["node"].append(n)
            pie_features["label"].append(l)
            pie_features["frac"].append(f)
            
    pie_features=pd.DataFrame(pie_features)
    onp.pienodes(g, 
                vertex_label=nodes,
                node_features=pie_features,
                piesize=0.1,
                layout=layout,
    vertex_color="lightblue",
    edge_color="gray",
    edge_arrow_size=0.03,
    edge_width=edge_width,
    keep_aspect_ratio=True)
    plt.show()