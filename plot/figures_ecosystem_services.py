# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:39:56 2024

@author: laurenan
"""

import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec

from netCDF4 import Dataset

import seaborn as sns
from matplotlib.lines import Line2D

from susi.config import CONFIG

sns.set()

optdiff = False  # difference between scenarios
optns = False  # control no shallowing
opts = True  # treatment shallowing

if optdiff:
    figname = "difference"
if optns:
    figname = "no_shallowing"
if opts:
    figname = "shallowing"

# --------Setup------------------------------
facecolor = "#f2f5eb"
fs = 15
fig = plt.figure(num="shallowing", figsize=(15, 18))  # width, height
gs = gridspec.GridSpec(ncols=12, nrows=24, figure=fig, wspace=3.0, hspace=0.25)

labs = ["SF", "CF", "NOBK", "Lapland"]

folderName = r"../outputs/no_shallow/"

folderTreat = str(CONFIG.paths.output_folder) + "/shallow/"


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
    "D",
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

custom_lines = [
    Line2D([0], [0], color="blue", lw=2),
    Line2D([0], [0], color="orange", lw=2),
    Line2D([0], [0], color="green", lw=2),
    Line2D([0], [0], color="red", lw=2),
    Line2D([0], [0], marker="o", color="0.9", markeredgecolor="black", lw=2),
    Line2D([0], [0], marker="D", color="0.9", markeredgecolor="black", lw=2),
    Line2D([0], [0], marker="X", color="0.9", markeredgecolor="black", lw=2),
    Line2D([0], [0], marker="s", color="0.9", markeredgecolor="black", lw=2),
    Line2D([0], [0], marker="+", color="0.9", markeredgecolor="black", lw=2),
]

Rhtkgs = ["SF_22.nc", "CF_22.nc", "NOBK_22.nc", "Lap_22.nc"]
MtkgsPine = ["SF_31.nc", "CF_31.nc", "NOBK_31.nc", "Lap_31.nc"]
MtkgsSpruce = ["SF_32.nc", "CF_32.nc", "NOBK_32.nc", "Lap_32.nc"]
Ptkgs = ["SF_41.nc", "CF_41.nc", "NOBK_41.nc", "Lap_41.nc"]
Vatkgs = ["SF_51.nc", "CF_51.nc", "NOBK_51.nc", "Lap_51.nc"]

sitesets = [Rhtkgs, MtkgsPine, MtkgsSpruce, Ptkgs, Vatkgs]
sites = Rhtkgs


def difference_plot(
    ax,
    x,
    y,
    ylabel,
    fs,
    colo,
    markers=["o", "s", "+"],
    scens=[0, 1, 2],
    lab="SF",
    sums=True,
    legen=False,
    hidex=False,
    hidey=False,
    elevation=None,
):
    # linestyles = ["dotted", "dashed", "solid"]
    # colors =['blue', 'green', 'red']
    # markers=['o', 's', '+']
    # scens = [0, 1, 2]
    # labs = ['0.3 m', '0.6 m', '0.9 m']
    # labs = []
    # if sums:
    #     mval = np.max(np.cumsum(y, axis=1))
    #     minval = np.min(np.cumsum(y, axis=1))
    # else:
    #     mval = np.max(y)
    #     minval = np.min(y)

    for scen, mk in zip(scens, markers):
        if sums:
            dg = np.cumsum(np.mean(y[scen, :, :], axis=1))
        else:
            dg = np.mean(y[scen, :, :], axis=1)
        plt.plot(
            x,
            dg,
            mk,
            color=colo,
            alpha=0.5,
            markerfacecolor="none",
            markersize=5,
            linestyle="solid",
            label=lab,
        )

    if hidey:
        ax.get_yaxis().set_visible(False)
    else:
        plt.ylabel(ylabel)
    if hidex:
        ax.get_xaxis().set_visible(False)
    else:
        plt.xlabel("Time, years")

    # if legen: plt.legend(loc='lower left')
    if legen:
        ax.legend(
            custom_lines,
            [
                "SF",
                "CF",
                "NOBK",
                "Lapland",
                "Rhtkg",
                "Mtkg Pine",
                "Mtkg Spruce",
                "Ptkg",
                "Vatkg",
            ],
            ncol=2,
            fontsize=8,
        )
    return ax


def color_axis(ax, x, ylims, goodup):
    minval = ylims[0]
    mval = ylims[1]
    if goodup:
        plt.fill_between(
            [0.0, x[-1]], [0, 0], [mval, mval], color="green", alpha=0.2
        )  # above zero
        plt.fill_between(
            [0.0, x[-1]], [0.0], [minval, minval], color="red", alpha=0.2
        )  # below zero
    else:
        plt.fill_between(
            [0.0, x[-1]], [0, 0], [mval, mval], color="red", alpha=0.2
        )  # above zero
        plt.fill_between(
            [0.0, x[-1]], [0.0], [minval, minval], color="green", alpha=0.2
        )  # below zero

    return ax


# *************** GROWTH **************************************************************
ax = fig.add_subplot(gs[0:4, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        growths = ncfs["stand"]["volumegrowth"][:, 1:, 1:-1]
        growth = ncf["stand"]["volumegrowth"][:, 1:, 1:-1]
        deltagr = growths - growth
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)
        legen = True if i < 1 else False
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltagr,
                "$\Delta$ volume growth, m$^{3}$ ha$^{-1}$ ",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                lab=lab,
                legen=legen,
                hidex=True,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                growth,
                "Volume growth, m$^{3}$ ha$^{-1} yr{^{-1}}$ ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[0],
                lab=lab,
                legen=legen,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                growths,
                "Volume growth, m$^{3}$ ha$^{-1} yr{^{-1}}$ ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[0],
                lab=lab,
                legen=legen,
                hidex=True,
            )

        ax.set_facecolor(facecolor)

ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ax.set_title("0.3 m")
ylims = ax.get_ylim()
ax.text(1, ylims[1], "a", fontsize=fs)


ax = fig.add_subplot(gs[0:4, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo in zip(sites, colors[0:20:5]):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        growths = ncfs["stand"]["volumegrowth"][:, 1:, 1:-1]
        growth = ncf["stand"]["volumegrowth"][:, 1:, 1:-1]
        deltagr = growths - growth
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltagr,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                hidex=True,
                hidey=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                growth,
                " ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[1],
                legen=False,
                hidex=True,
                hidey=False,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                growths,
                " ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[1],
                legen=False,
                hidex=True,
                hidey=False,
            )

        ax.set_facecolor(facecolor)

ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ax.set_title("0.6 m")
ylims = ax.get_ylim()
ax.text(1, ylims[1], "b", fontsize=fs)


ax = fig.add_subplot(gs[0:4, 8:12])
for i, sites in enumerate(sitesets):
    for outn, colo in zip(sites, colors[0:20:5]):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        growths = ncfs["stand"]["volumegrowth"][:, 1:, 1:-1]
        growth = ncf["stand"]["volumegrowth"][:, 1:, 1:-1]
        deltagr = growths - growth
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltagr,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                hidex=True,
                hidey=False,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                growth,
                " ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[2],
                legen=False,
                hidex=True,
                hidey=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                growths,
                " ",
                fs,
                colo,
                sums=False,
                markers=mks[i],
                scens=[2],
                legen=False,
                hidex=True,
                hidey=False,
            )

        ax.set_facecolor(facecolor)

ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ax.set_title("0.9 m")
ylims = ax.get_ylim()
ax.text(1, ylims[1], "c", fontsize=fs)

# *************** WT ***************************************************************************

ax = fig.add_subplot(gs[4:8, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        wtss = ncfs["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        wts = ncf["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        deltawts = wtss - wts
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltawts,
                "$\Delta$ WT, cm ",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                wts,
                "WT, cm ",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                wtss,
                "WT, cm ",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "d", fontsize=fs)


ax = fig.add_subplot(gs[4:8, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        wtss = ncfs["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        wts = ncf["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        deltawts = wtss - wts
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltawts,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                wts,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                wtss,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "e", fontsize=fs)


ax = fig.add_subplot(gs[4:8, 8:12])

for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        wtss = ncfs["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        wts = ncf["strip"]["dwtyr_growingseason"][:, 1:, 1:-1] * 100
        deltawts = wtss - wts
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltawts,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                wts,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                wtss,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "f", fontsize=fs)

# *************** ecosystem C balance ***************************************************************************
ax = fig.add_subplot(gs[8:12, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        standcs = ncfs["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                "$\Delta$ ecosystem C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                "Ecosystem C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                "Ecosystem C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "c", fontsize=fs)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "g", fontsize=fs)


ax = fig.add_subplot(gs[8:12, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        standcs = ncfs["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "h", fontsize=fs)

ax = fig.add_subplot(gs[8:12, 8:12])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        standcs = ncfs["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["stand_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)

ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "i", fontsize=fs)

# **************** soil c balance*************************
ax = fig.add_subplot(gs[12:16, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        standcs = ncfs["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                "$\Delta$ soil C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                "Soil C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                "Soil C balance, kg C ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "j", fontsize=fs)

ax = fig.add_subplot(gs[12:16, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        standcs = ncfs["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )

        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "k", fontsize=fs)


ax = fig.add_subplot(gs[12:16, 8:12])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        standcs = ncfs["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        standc = ncf["balance"]["C"]["soil_c_balance_c"][:, 1:, 1:-1]
        deltastandc = standcs - standc
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltastandc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=True,
                hidex=True,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                standc,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                standcs,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=True,
            )

        ax.set_facecolor(facecolor)

ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=True)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "l", fontsize=fs)

# **************** N export *************************
ax = fig.add_subplot(gs[16:20, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["N"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["N"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                "$\Delta$ N export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                "N export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                "N export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "m", fontsize=fs)


ax = fig.add_subplot(gs[16:20, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["N"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["N"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "n", fontsize=fs)


ax = fig.add_subplot(gs[16:20, 8:12])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["N"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["N"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "o", fontsize=fs)


# **************** P export *************************
ax = fig.add_subplot(gs[20:24, 0:4])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["P"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["P"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                "$\Delta$ P export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                "P export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                "P export, kg ha$^{-1}$",
                fs,
                colo,
                markers=mks[i],
                scens=[0],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "p", fontsize=fs)


ax = fig.add_subplot(gs[20:24, 4:8])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["P"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["P"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[1],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "q", fontsize=fs)


ax = fig.add_subplot(gs[20:24, 8:12])
for i, sites in enumerate(sitesets):
    for outn, colo, lab in zip(sites, colors[0:20:5], labs):
        ff = folderName + outn
        ffs = folderTreat + outn

        ncfs = Dataset(ffs, mode="r")  # shallowing
        ncf = Dataset(ff, mode="r")  # no shallowing

        yrs = np.shape(growth)[1]
        t = np.arange(1, yrs + 1, 1)

        n = ncf["balance"]["P"]["to_water"][:, 1:, 1:-1]
        ns = ncfs["balance"]["P"]["to_water"][:, 1:, 1:-1]
        deltans = ns - n
        if optdiff:
            ax = difference_plot(
                ax,
                t,
                deltans,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=True,
                hidex=False,
            )
        if optns:
            ax = difference_plot(
                ax,
                t,
                n,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )
        if opts:
            ax = difference_plot(
                ax,
                t,
                ns,
                " ",
                fs,
                colo,
                markers=mks[i],
                scens=[2],
                legen=False,
                lab=lab,
                sums=False,
                hidex=False,
            )

        ax.set_facecolor(facecolor)


ylims = ax.get_ylim()
if optdiff:
    ax = color_axis(ax, t, ylims, goodup=False)
ylims = ax.get_ylim()
ax.text(1, ylims[1], "r", fontsize=fs)

plt.savefig(r"../outputs/figures/" + figname + ".svg", format="svg")

ncf.close()
ncfs.close()
