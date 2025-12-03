# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:29:52 2025

@author: laurenan
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec

from netCDF4 import Dataset

# from sklearn.metrics import r2_score
import seaborn as sns

sns.set()

# OWN simulations

# REFERENCE data to Ojanen & Minkkinen 2019
fig = plt.figure(num="co2", figsize=(12, 5))


# folderName=r'C:/Users/laurenan/OneDrive - University of Helsinki/codes/susi_11/outputs/' #'sensitivity/'
folderName = (
    r"C:/Users/laurenan/OneDrive - University of Helsinki/SUSI/mikko_niemi//outputs/"
)

facecolor = "#f2f5eb"
fs = 15
# fig = plt.figure(num='shallowing', figsize=(15,18))   #width, height
gs = gridspec.GridSpec(ncols=12, nrows=6, figure=fig, wspace=6.0, hspace=4.25)


ax = fig.add_subplot(gs[0:6, 0:6])

fdata = r"C:/Users/laurenan/OneDrive - University of Helsinki/SUSI/mikko_niemi/CO2_vs_WT.xlsx"
ojanen_data = pd.read_excel(
    fdata,
    "CO2_vs_WT",
    usecols=[
        "Site",
        "N",
        "E",
        "Region",
        "Site type",
        "Trophic level",
        "WT",
        "CO2",
        "Source",
    ],
    nrows=76,
)

ojanen_data = ojanen_data[ojanen_data["Site type"] != "Jätkg"]

ojanen_data["CO2"] = -1 * ojanen_data["CO2"]


sns.scatterplot(
    data=ojanen_data, x="WT", y="CO2", hue="Region", style="Site type", s=150
)
ax.set_facecolor(facecolor)
plt.hlines(0, 0, 140, color="grey", linestyles="dashed")
plt.ylabel("CO$_2$ g m$^{-2}$ yr$^{-1}$", fontsize=fs)
plt.xlabel("WT, cm", fontsize=fs)
ax.text(5, 500, "a", fontsize=fs)

# OWN simulations
scen = 0

outnames = [
    "SF_22.nc",
    "SF_31.nc",
    "SF_32.nc",
    "SF_41.nc",
    "SF_51.nc",
    "CF_22.nc",
    "CF_31.nc",
    "CF_32.nc",
    "CF_41.nc",
    "CF_51.nc",
    "NOBK_22.nc",
    "NOBK_31.nc",
    "NOBK_32.nc",
    "NOBK_41.nc",
    "NOBK_51.nc",
    "Lap_22.nc",
    "Lap_31.nc",
    "Lap_32.nc",
    "Lap_41.nc",
    "Lap_51.nc",
]

colors = [
    "blue",
    "blue",
    "blue",
    "blue",
    "blue",
    "orange",
    "orange",
    "orange",
    "orange",
    "orange",
    "green",
    "green",
    "green",
    "green",
    "green",
    "red",
    "red",
    "red",
    "red",
    "red",
]

mks = [
    "o",
    "X",
    "X",
    "s",
    "+",
    "o",
    "X",
    "X",
    "s",
    "+",
    "o",
    "X",
    "X",
    "s",
    "+",
    "o",
    "X",
    "X",
    "s",
    "+",
]

# folderName=r'C:/Users/laurenan/OneDrive - University of Helsinki/codes/susi_11/outputs/' #'sensitivity/'
folderName = (
    r"C:/Users/laurenan/OneDrive - University of Helsinki/SUSI/mikko_niemi//outputs/"
)


for outn, colos, mk in zip(outnames, colors, mks):
    ff = folderName + outn
    ncf = Dataset(ff, mode="r")

    bal = (
        -1
        * (
            ncf["balance"]["C"]["soil_c_balance_co2eq"][scen, 1:, 1:-1]
            + ncf["balance"]["C"]["LMWdoc_to_water"][scen, 1:, 1:-1] * 44 / 12
            + ncf["balance"]["C"]["HMW_to_water"][scen, 1:, 1:-1] * 44 / 12
        )
        / 10
        * -1
    )

    dfbal = pd.DataFrame(bal)
    wt = ncf["strip"]["dwtyr_growingseason"][scen, 1:, 1:-1]
    dfwt = pd.DataFrame(wt)
    ncf.close()
    # for c in range(17):
    #    wts = dfwt[c].values*-100
    #    bals = dfbal[c].values
    #    plt.plot(wts, bals, 'o', color = 'grey', alpha = 0.20)
    wts = dfwt.mean(axis=1).values * -100
    bals = dfbal.mean(axis=1).values
    ax.plot(wts, bals, mk, color=colos, alpha=0.5, markerfacecolor="none", markersize=4)
    plt.xlim([0, 150])
    plt.ylim([-1500, 600])

    # print (dfwt)
    # dfwt.to_clipboard()


# CAI figure
ax = fig.add_subplot(gs[0:6, 6:12])

# fig = plt.figure(num='growth')

for outn, colos, mk in zip(outnames, colors, mks):
    ff = folderName + outn
    ncf = Dataset(ff, mode="r")

    growth0 = np.mean(ncf["stand"]["volumegrowth"][0, 1:, 1:-1])
    growth1 = np.mean(ncf["stand"]["volumegrowth"][1, 1:, 1:-1])
    growth2 = np.mean(ncf["stand"]["volumegrowth"][2, 1:, 1:-1])

    wt0 = np.mean(ncf["strip"]["dwtyr_growingseason"][0, 1:, 1:-1]) * -100
    wt1 = np.mean(ncf["strip"]["dwtyr_growingseason"][1, 1:, 1:-1]) * -100
    wt2 = np.mean(ncf["strip"]["dwtyr_growingseason"][2, 1:, 1:-1]) * -100

    wts = np.array([wt0, wt1, wt2])
    gr = np.array([growth0, growth1, growth2])
    ax.plot(
        wts,
        gr,
        mk,
        color=colos,
        alpha=0.5,
        markerfacecolor="none",
        markersize=5,
        linestyle="-",
        label=outn[:-3],
    )
    # plt.xlim([0,150])
    # plt.ylim([-600, 2000])
    plt.xlabel("WT, cm")
    plt.ylabel("Volume growth m$^3$ ha$^{-1}$ yr$^{-1}$")
    ax.set_facecolor(facecolor)

    ncf.close()
ax.text(15, 10, "b", fontsize=fs)

plt.savefig(
    r"C:\Users\laurenan\OneDrive - University of Helsinki\Persons\PhD students\Annastiina Saari/realitychek.png"
)
# plt.legend(loc='best', ncols=5)

# plt.legend(['o', 'X', 's', '+'],['RhTkg', 'MTkg', 'PTkg', 'VaTkg'], loc='lower right')
