import sys, os 
import sys
#sys.path.append("../omniplot")
from omniplot  import plot as op
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt 
#test="dotplot"
#test="triangle_heatmap"
test="decomp"
test="manifold"
test="triangle_heatmap"
test="radialtree"
test="violinplot"
test="cluster"
test="regression"
test="complex_clustermap"
test="dotplot"
test="regression"
test="nice_piechart_num"
test="pie_scatter"
test="correlation"
test="manifold"
test="stacked"
test="stackedlines"
test="correlation"
test="cluster"
test="nested_piechart"
test="radialtree"
test="scatterplot"


if test=="stackedlines":
    f="/media/koh/grasnas/home/data/omniplot/energy/owid-energy-data.csv"
    df=pd.read_csv(f)
    _df=df.loc[df["country"]=="Japan"]
    cols=['biofuel_consumption',
            'coal_consumption',
            'gas_consumption',
            'hydro_consumption',
            'nuclear_consumption',
            'oil_consumption',
            'other_renewable_consumption',
            'solar_consumption',
            'wind_consumption']
    op.stackedlines(df=_df, x="year",y=cols,title="Japan", remove_all_zero=True, inverse=True,show_values=True, hatch=True, yunit="twh")
    
    _df=pd.DataFrame({"x":np.arange(100),
                        "y0":np.random.normal(loc=0.0, scale=1.0, size=100)-3,
                        "y1":np.random.normal(loc=0.0, scale=1.0, size=100)+3,
                        "y2":np.random.normal(loc=0.0, scale=1.0, size=100)-4})
    op.stackedlines(df=_df, x="x",y=["y0","y1", "y2"],title="Japan",bbox_to_anchor=[1,1], sort=True, remove_all_zero=False, inverse=False,show_values=False, yunit="twh")
    
    plt.show()
elif test=="nice_piechart":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    tmp=[]
    for num, (sp, i ,se) in enumerate(zip(df["species"], df["island"],df["sex"])):
        if num/df.shape[0] > 0.98:
            tmp.append("NA")
        else:
            tmp.append(sp[0]+"_"+i[0]+"_"+se[0])
    df["combine"]=tmp
    print(df)
    op.nice_piechart(df, category=["species", "island","sex","island"],ncols=3, hatch=True)
    plt.show()
elif test=="nested_piechart":
    # df=sns.load_dataset("titanic")
    # df=df[["class","embark_town","sex"]].fillna("NA")
    # op.nested_piechart(df, category=["class","embark_town","sex"], title="Titanic", 
    #                    ignore=0.01, 
    #                    show_legend=True,
    #                    show_values=False,
    #                    hatch=False, skip_na=True)
    df=sns.load_dataset("penguins")
    df[["species","sex","island"]]=df[["species","sex","island"]].fillna("NA")
    op.nested_piechart(df,
                       category=["species","sex","island"],
                       #variable="body_mass_g",
                       title="Penguins", 
                       ignore=0.01, 
                       show_legend=True,
                       show_values=False,
                       show_percentage=False,order="largest",
                       hatch=False, skip_na=True,colormode="independent")
    df=pd.read_csv("/media/koh/grasnas/home/data/omniplot/energy/owid-energy-data_curated_with_continents.csv")
    df=df.loc[df["year"]==2021]
    op.nested_piechart(df,
                       category=["Continent","country"],
                       variable="coal_electricity",
                       title="Coal electricity in 2021 (terawatt-hours)", 
                       ignore=0.03, 
                       show_legend=True,
                       show_values=True,
                       show_percentage=True,order="largest",
                       hatch=False, skip_na=True,colormode="hierarchical")
    plt.show()
elif test=="stacked": 
    # df=sns.load_dataset("penguins")
    # df=df.dropna(axis=0)
    # op.stacked_barplot(df, x=["species","island"],
    #                     hue=["sex","island"], scale="absolute", order=[
    #                                                                 ["Chinstrap","Gentoo","Adelie"],
    #                                                                 ["Dream","Biscoe","Torgersen"]],
    #                     test_pairs=[["Adelie","Gentoo"]], hatch=True)
    # op.stacked_barplot(df, x="species",
    #                     hue="sex", scale="percentage", hatch=True)

    df=sns.load_dataset("titanic")
    op.stacked_barplot(df=df,x=["sex"],hue=["age","alone"], bin_num=10)

    plt.show()


elif test=="nice_piechart_num":
    f="/home/koh/ews/omniplot/data/energy_vs_gdp.csv"
    df=pd.read_csv(f, comment='#')
    df=df.set_index("country")
    op.nice_piechart_num(df, hue=['biofuel_electricity',
                                                    'coal_electricity',
                                                    'gas_electricity',
                                                    'hydro_electricity',
                                                    'nuclear_electricity',
                                                    'oil_electricity',
                                                    'other_renewable_electricity',
                                                    'solar_electricity',
                                                    'wind_electricity'],ncols=10)
    
    
    plt.show()
elif test=="correlation":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    
        
    op.correlation(df, category=["species", "island","sex"], method="pearson", ztransform=True)
    plt.show()

elif test=="regression":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    op.regression_single(df, x="bill_length_mm",y="body_mass_g", method="robust",category="species")
    plt.show()
elif test=="dotplot":
    df=pd.DataFrame({"Experiments":["exp1","exp1","exp1","exp1","exp2","exp2","exp3"],
                        "GO":["nucleus","cytoplasm","chromosome","DNA binding","chromosome","RNA binding","RNA binding"],
                        "FDR":[10,1,5,3,1,2,0.5],
                        "odds":[3.3,1.1,2.5,2.1,0.8,2.3,0.9]})
    op.dotplot(df, row="GO",col="Experiments", size_val="FDR",color_val="odds", highlight="FDR",
    color_title="Odds", size_title="-log10 p",scaling=20)
    # df=pd.read_csv("/home/koh/ews/idr_revision/clustering_analysis/cellloc_longform.csv")
    # print(df.columns)
    # df=df.fillna(0)
    # #dotplot(df, size_val="pval",color_val="odds", highlight="FDR",color_title="Odds ratio", size_title="-log10 p value",scaling=20)
    #
    # dotplot(df, row="Condensate",col="Cluster", size_val="pval",color_val="odds", highlight="FDR",
    #         color_title="Odds", size_title="-log10 p value",scaling=20)
    plt.show()
elif test=="triangle_heatmap":
    s=20
    mat=np.arange(s*s).reshape([s,s])
    import string, random
    letters = string.ascii_letters+string.digits
    labels=[''.join(random.choice(letters) for i in range(10)) for _ in range(s)]
    df=pd.DataFrame(data=mat, index=labels, columns=labels)
    op.triangle_heatmap(df,grid_pos=[2*s//10,5*s//10,7*s//10],grid_labels=["A","B","C","D"])
elif test=="complex_clustermap":
    # _df=pd.DataFrame(np.arange(100).reshape([10,10]))
    # cmap=plt.get_cmap("tab20b")
    # complex_clustermap(_df,
    #                    row_colormap={"test1":[cmap(v) for v in np.linspace(0,1,10)]},
    #                    row_plot={"sine":np.sin(np.linspace(0,np.pi,10))},
    #                    approx_clusternum=3,
    #                    merginalsum=True)
    df=sns.load_dataset("penguins")
    
    df=df.dropna(axis=0)
    dfcol=pd.DataFrame({"features":["bill","bill","flipper"]})
    op.complex_clustermap(df,
                        dfcol=dfcol,
                        variables=["bill_length_mm","bill_depth_mm","flipper_length_mm"],
                        row_colors=["species","sex"],
                        row_scatter=["body_mass_g"],
                        row_plot=["body_mass_g"],
                        row_bar=["body_mass_g"],
                        col_colors=["features"],
                        approx_clusternum=3,
                        merginalsum=True, title="Penguins")
    plt.show()
elif test=="radialtree":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    variables=["bill_length_mm","bill_depth_mm","flipper_length_mm"]
    op.radialtree(df, variables=variables, category=["species","island","sex"])#,figsize=[8,8])
    plt.show()

elif test=="violinplot":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    op.violinplot(df,x="species",y="bill_length_mm", 
                pairs=[["Adelie","Chinstrap" ],["Gentoo","Chinstrap" ],["Adelie","Gentoo" ]],
                test="mannwhitneyu",
                significance="symbol",swarm=True)
    plt.show()



elif test=="decomp":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    variables=["bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"]

    op.decomplot(df, variables=variables,category=["species","sex"],method="pca",markers=True)
    plt.show()
elif test=="manifold":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    variables=["bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"]
    #df=df[features]
    op.manifoldplot(df, 
                    variables=variables,
                    category=["species", "island"],
                    method="tsne",markers=True)
    plt.show()
elif test=="cluster":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    features=["species","sex","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"]
    df=df[features]
    #op.clusterplot(df,category=["species","sex"],method="kmeans",n_clusters="auto", markers=True,topn_cluster_num=3,reduce_dimension="tsne")
    op.clusterplot(df,category=["species","sex"],method="fuzzy",n_clusters=3, piesize_scale=0.03,sp_kw={"marginal_dist":True})#,topn_cluster_num=3)
    #clusterplot(df,category=["species","sex"],method="hdbscan",eps=0.35)
    #clusterplot(df,category=["species","sex"],method="hdbscan",n_clusters="auto")
    plt.show()


elif test=="pie_scatter":
    f="/home/koh/ews/omniplot/data/energy_vs_gdp.csv"
    df=pd.read_csv(f, comment='#')
    df=df.set_index("country")
    op.pie_scatter(df, x="gdppc",y="pop", category=['biofuel_electricity',
                                                    'coal_electricity',
                                                    'gas_electricity',
                                                    'hydro_electricity',
                                                    'nuclear_electricity',
                                                    'oil_electricity',
                                                    'other_renewable_electricity',
                                                    'solar_electricity',
                                                    'wind_electricity'],logscalex=True,logscaley=True,
                                                piesizes="sum_of_each",
                                                min_piesize=0.3, label="topn_of_sum")
    plt.show()

elif test=="scatterplot":
    df=sns.load_dataset("penguins")
    df=df.dropna(axis=0)
    #features=["species","sex","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"]
    #df=df[features]
    print(df.shape)
    op.scatterplot(df, x="bill_length_mm",y="bill_depth_mm",xunit="mm", yunit="mm", 
                   category=['species',"sex","island"],
                   colors=["flipper_length_mm"],
                   sizes="body_mass_g",
                   show_labels={"val": "body_mass_g", "topn":5},
                   marginal_dist=True,
                   kmeans=True,
                                                )
    fig, ax=plt.subplots()
    op.scatterplot(df, ax=ax,
               x="bill_length_mm",
               y="bill_depth_mm", 
                sizes="flipper_length_mm")
    plt.show()