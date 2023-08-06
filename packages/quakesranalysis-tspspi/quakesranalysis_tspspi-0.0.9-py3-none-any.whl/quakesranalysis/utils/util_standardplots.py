import sys
sys.path.append("../")
sys.path.append("../../")


import numpy as np
import matplotlib.pyplot as plt

import sys
import os
import textwrap
import json

from quakesranalysis import scanhandler
from quakesranalysis import gaussianmixture
from quakesranalysis import mixturefit
from quakesranalysis import allan

def printUsage():
    print(textwrap.dedent("""
        Standard plots generation tool for QUAK/ESR

        \t{} [options] FILENAME [FILENAME ...]

        This tool accepts either runfiles or NPZ files and generates a
        selectable set of standard plots for reporting purposes. The
        set of plots is selected by different options:

        \t-iqmean\t\tGenerated I/Q mean and noise plots
        \t-iqslices N\t\tPlot I/Q mean and noise plots for slices N samples long
        \t-apmean\t\tGenerate amplitude and phase from I/Q samples
        \t-powermean\tMean and standard deviation of power measurement
        \t-wndnoise N\tPlots noise in a sliding window of N samples
        \t-offsettime\tPlot offset change (mean of all samples) over time
        \t-allan\tPlot allan deviations for all sampled points along main axis
        \t-timejitter\tPlot time between samples
        \t-mixfit\tDecompose into Gaussian and Cauchy distributions for all channels
        \t-mixfitdebug\tDump all fitting steps (might require MPLBACKEND=tkagg instead of qt?agg)
        \t-decompose\tDecompose gaussian mixture for all channels (old fitter)
        \t-metrics\tCollect core metrics in metrics.json for this run
        \t-agreport\tWrite an aggregate report HTML file (agreport.html)
    """).format(sys.argv[0]))

def metrics_collect_core(fileprefix, scan, metrics = {}, aggregateHTMLReport = None):
    #   Allan deviation -> converges or diverges? How well is it a 1/r?

    metrics['core'] = {}

    # Spans

    meanI, stdI, meanQ, stdQ = scan.get_signal_mean_iq()
    meanIZ, stdIZ, meanQZ, stdQZ = scan.get_zero_mean_iq()
    if meanIZ is not None:
        meanIDiff, stdIDiff, meanQDiff, stdQDiff = scan.get_diff_mean_iq()

    metrics['core']['vpp_signalI'] = np.max(meanI) - np.min(meanI)
    metrics['core']['vpp_signalQ'] = np.max(meanQ) - np.min(meanQ)
    metrics['core']['mean_signalI'] = np.mean(meanI)
    metrics['core']['mean_signalQ'] = np.mean(meanQ)
    metrics['core']['maxnoise_signalI'] = np.max(stdI)
    metrics['core']['maxnoise_signalQ'] = np.max(stdQ)
    metrics['core']['meannoise_signalI'] = np.mean(stdI)
    metrics['core']['meannoise_signalQ'] = np.mean(stdQ)
    if meanIZ is not None:
        metrics['core']['vpp_signalIZero'] = np.max(meanIZ) - np.min(meanIZ)
        metrics['core']['vpp_signalQZero'] = np.max(meanQZ) - np.min(meanQZ)
        metrics['core']['vpp_signalIDiff'] = np.max(meanIDiff) - np.min(meanIDiff)
        metrics['core']['vpp_signalQDiff'] = np.max(meanQDiff) - np.min(meanQDiff)
        metrics['core']['mean_signalIZero'] = np.mean(meanIZ)
        metrics['core']['mean_signalQZero'] = np.mean(meanQZ)
        metrics['core']['mean_signalIDiff'] = np.mean(meanIDiff)
        metrics['core']['mean_signalQDiff'] = np.mean(meanQDiff)
        metrics['core']['maxnoise_signalIZero'] = np.max(stdIZ)
        metrics['core']['maxnoise_signalQZero'] = np.max(stdQZ)
        metrics['core']['maxnoise_signalIDiff'] = np.max(stdIDiff)
        metrics['core']['maxnoise_signalQDiff'] = np.max(stdQDiff)
        metrics['core']['meannoise_signalIZero'] = np.mean(stdIZ)
        metrics['core']['meannoise_signalQZero'] = np.mean(stdQZ)
        metrics['core']['meannoise_signalIDiff'] = np.mean(stdIDiff)
        metrics['core']['meannoise_signalQDiff'] = np.mean(stdQDiff)

    return metrics

def metrics_write(fileprefix, scan, metrics, aggregateHTMLReport = None):
    # Write metrics file with all collected metrics ...
    with open(f"{fileprefix}_metrics.json", "w") as outfile:
        outfile.write(json.dumps(metrics))

    if aggregateHTMLReport is not None:
        if "Metrics file" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append("Metrics file")
        if f"Metrics file" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Metrics file"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Metrics file"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Metrics file"] + f"<a href=\"{fileprefix}_metrics.json\">{fileprefix}_metrics.json</a><br>"

    print(f"[METRICS] Written {fileprefix}_metrics.json")

def plot_allan(fileprefix, scan, aggregateHTMLReport = None):
    print(f"[ALLAN] Starting for {fileprefix}")

    res, worstres = allan.get_allan_deviations(scan)

    maindata = scan.get_main_axis_data()

    fig, ax = plt.subplots(len(maindata), 1, squeeze = False, figsize=(6.4, 4.8 * len(maindata)))

    for i in range(len(maindata)):
        ax[i][0].set_title("Allan deviation for {} = {}".format(scan.get_main_axis_symbol(), res['I'][i][f"{scan.get_main_axis_symbol()}"]))
        ax[i][0].set_ylabel("Allan deviation")
        ax[i][0].set_xlabel("Time (samples)")
        for channel in res:
            # Check if channel is present or empty ...
            if len(res[channel]) == len(maindata):
                ax[i][0].plot(res[channel][i]['taus'], res[channel][i]['ad'], label = f"{channel}")
        ax[i][0].legend()
        ax[i][0].grid()

    plt.tight_layout()
    ##plt.savefig(f"{fileprefix}_allanall.svg")
    plt.savefig(f"{fileprefix}_allanall.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allanall")

    fig, ax = plt.subplots()
    ax.set_title(f"Worst Allan deviation (from all {scan.get_main_axis_symbol()})")
    ax.set_ylabel("Allan deviation")
    ax.set_xlabel("Time (samples)")
    for channel in worstres:
        ax.plot(worstres[channel]['taus'], worstres[channel]['ad'], label = f"{channel}")
    ax.legend()
    ax.grid()

    if aggregateHTMLReport is not None:
        if "Worst Allan deviation" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append("Worst Allan deviation")
        if f"Worst Allan deviation" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation"] + f"<img src=\"{fileprefix}_allan.png\" alt=\"\"><br>"


    plt.tight_layout()
    ##plt.savefig(f"{fileprefix}_allan.svg")
    plt.savefig(f"{fileprefix}_allan.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allan")

    fig, ax = plt.subplots()
    ax.set_title(f"Worst Allan deviation (from all {scan.get_main_axis_symbol()})")
    ax.set_ylabel("Allan deviation")
    ax.set_xlabel("Time (samples)")
    ax.set_yscale('log')
    ax.set_xscale('log')
    for channel in worstres:
        ax.plot(worstres[channel]['taus'], worstres[channel]['ad'], label = f"{channel}")
    ax.legend()
    ax.grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_allan_log.svg")
    plt.savefig(f"{fileprefix}_allan_log.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allan_log")

    if aggregateHTMLReport is not None:
        if "Worst Allan deviation (Log)" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append("Worst Allan deviation (Log)")
        if f"Worst Allan deviation (Log)" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation (Log)"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation (Log)"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Worst Allan deviation (Log)"] + f"<img src=\"{fileprefix}_allan_log.png\" alt=\"\"><br>"



def plot_decompose_mixturefit(fileprefix, scan, metrics = {}, debugplots = False, aggregateHTMLReport = None):
    print(f"[MIXFIT] Starting for {fileprefix}")

    mf = mixturefit.MixtureFitter()

    # Decompose for each channel in the scan ...
    scanx = scan.get_main_axis_data()
    scanxsymbol = scan.get_main_axis_symbol()

    meanI, _, meanQ, _ = scan.get_signal_mean_iq()
    amp, _ = scan.get_signal_ampphase()
    pwr, _ = scan.get_signal_mean_power()

    meanIZero, _, meanQZero, _ = scan.get_zero_mean_iq()
    ampZero, _ = scan.get_zero_ampphase()
    pwrZero, _ = scan.get_zero_mean_power()
    meanIDiff, _, meanQDiff, _ = scan.get_diff_mean_iq()
    ampDiff, _ = scan.get_diff_ampphase()
    pwrDiff, _ = scan.get_diff_mean_power()

    metrics['decompose'] = {}

    resmixture = {
        'I' : mf.fitMixture(scanx, meanI, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_I", printprogress = True),
        'Q' : mf.fitMixture(scanx, meanQ, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_Q", printprogress = True),
        'A' : mf.fitMixture(scanx, amp, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_A", printprogress = True),
        'P' : mf.fitMixture(scanx, pwr, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_P", printprogress = True)
    }

    if meanIZero is not None:
        resmixture = resmixture | {
            'IZero' : mf.fitMixture(scanx, meanIZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_IZero", printprogress = True),
            'QZero' : mf.fitMixture(scanx, meanQZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_QZero", printprogress = True),
            'AZero' : mf.fitMixture(scanx, ampZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_AZero", printprogress = True),
            'PZero' : mf.fitMixture(scanx, pwrZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_PZero", printprogress = True),

            'IDiff' : mf.fitMixture(scanx, meanIDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_IDiff", printprogress = True),
            'QDiff' : mf.fitMixture(scanx, meanQDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_QDiff", printprogress = True),
            'ADiff' : mf.fitMixture(scanx, ampDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_ADiff", printprogress = True),
            'PDiff' : mf.fitMixture(scanx, pwrDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_PDiff", printprogress = True)
        }

    chanlist = [ 'I', 'Q', 'A' ]
    if meanIZero is not None:
        chanlist = chanlist + [ 'IZero' , 'QZero' , 'AZero', 'PZero', 'IDiff', 'QDiff', 'ADiff', 'PDiff' ]

    for chan in chanlist:
        #fig, ax = mf.mixtures2barplot(resmixture[chan], yunitlabel = scanxsymbol, chanlabel = chan)
        #plt.savefig(f"{fileprefix}_mixfit_{chan}.png")
        #plt.close()
        #print(f"[MIXFIT] Written {fileprefix}_mixfit_{chan}")

        #if aggregateHTMLReport is not None:
        #    if f"Mixture fit report ({chan})" not in aggregateHTMLReport['columntitles']:
        #        aggregateHTMLReport['columntitles'].append(f"Mixture fit report ({chan})")
        #    if f"Mixture fit report ({chan})" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
        #        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mixture fit report ({chan})"] = ""
        #    aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mixture fit report ({chan})"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mixture fit report ({chan})"] + f"<img src=\"{fileprefix}_mixfit_{chan}.png\" alt=\"\"><br>"

        metrics['decompose'][chan] = mf.mixtures2dictlist(resmixture[chan])

        fig, ax = mf.mixtures2componentplots(scanx, resmixture[chan], yunitlabel = scanxsymbol, chanlabel = chan)
        if fig != None:
            plt.savefig(f"{fileprefix}_mixcomponents_{chan}.png")
            plt.close()
        print(f"[MIXFIT] Written {fileprefix}_mixcomponents_{chan}")

    print("[MIXFIT] Done")
    return metrics


def plot_decompose(fileprefix, scan, metrics = {}, debugplots = False, aggregateHTMLReport = None):
    print(f"[DECOMPOSE] Starting for {fileprefix}")

    res = gaussianmixture.decompose_gaussian_mixtures(scan, progressPrint = True, debugplots = debugplots, debugplotPrefix=f"{fileprefix}_fitdebug_")
    fig, ax = gaussianmixture.decompose_gaussian_mixtures_plotfit(scan, res)

    #plt.savefig(f"{fileprefix}_gaussianmixture_fit.svg")
    plt.savefig(f"{fileprefix}_gaussianmixture_fit.png")
    print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_fit")
    plt.close(fig)

    # Show fit results
    print("[DECOMPOSE]")
    print("[DECOMPOSE] \tCenter\tFWHM\tOffset\tAmplitude")

    metrics['decompose'] = {}

    for channel in res:
        metrics['decompose'][channel] = []

        res[channel] = sorted(res[channel], key=lambda x : x['mu'])
        print(f"[DECOMPOSE] Channel {channel}")
        for params in res[channel]:
            fwhm = 2.0 * np.sqrt(2.0 * np.log(2)) * params['sigma']
            print(f"[DECOMPOSE] \t{params['mu']}\t{fwhm}\t{params['off']}\t{params['amp']}")
            metrics['decompose'][channel].append({
                'type' : params['type'],
                'mu' : params['mu'],
                'fwhm' : fwhm,
                'off' : params['off'],
                'amp' : params['amp']
            })
    print("[DECOMPOSE]")

    # Generate component plots if debugplots is enabled
    if debugplots:
        for channel in res:
            fig, ax = gaussianmixture.decompose_gaussian_mixtures_plotcomponents(scan, res[channel])
            # plt.savefig(f"{fileprefix}_gaussianmixture_fitcomponents_{channel}.svg")
            plt.savefig(f"{fileprefix}_gaussianmixture_fitcomponents_{channel}.png")
            print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_fitcomponents_{channel}.png")
            plt.close(fig)

            if aggregateHTMLReport is not None:
                if "Gaussian decomposition" not in aggregateHTMLReport['columntitles']:
                    aggregateHTMLReport['columntitles'].append("Gaussian decomposition")
                if f"Gaussian decomposition" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                    aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Gaussian decomposition"] = ""
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Gaussian decomposition"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Gaussian decomposition"] + f"<img src=\"{fileprefix}_gaussianmixture_fitcomponents_{channel}.png\" alt=\"\"><br>"


    for channel in res:
        with open(f"{fileprefix}_gaussianmixture_peaks_{channel}.dat", 'w') as outfile:
            outfile.write("#Center\tFWHM\tOffset\tAmplitude\n")
            for params in res[channel]:
                fwhm = 2.0 * np.sqrt(2.0 * np.log(2)) * params['sigma']
                typestring = "Unknown"
                if params['type'] == gaussianmixture.FUNTYPE_DIFFGAUSSIAN:
                    typestring = "Diff. Gaussian"
                elif params['type'] == gaussianmixture.FUNTYPE_GAUSSIAN:
                    typestring = "Gaussian"

                outfile.write(f"{typestring}\t{params['mu']}\t{fwhm}\t{params['off']}\t{params['amp']}\n")
        print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_peaks_{channel}.dat")

    print("[DECOMPOSE] Finished")

    return metrics


def plot_offsettime(fileprefix, scan, aggregateHTMLReport = None):
    # Calculate offset drift over time

    print(f"[OFFSETTIME] Starting for {fileprefix}")

    sigI, sigQ = scan.get_raw_signal_iq()
    sigIZero, sigQZero = scan.get_raw_zero_iq()

    # Calculate means for each time ...
    times = len(sigI[0])

    offtimes = {
        'I' : np.zeros((times,)),
        'Q' : np.zeros((times,)),
        'Amp' : np.zeros((times,)),
        'Phase' : np.zeros((times,)),
        'IZero' : np.zeros((times,)),
        'QZero' : np.zeros((times,)),
        'ZeroAmp' : np.zeros((times,)),
        'ZeroPhase' : np.zeros((times,)),
        'IDiff' : np.zeros((times,)),
        'QDiff' : np.zeros((times,)),
        'DiffAmp' : np.zeros((times,)),
        'DiffPhase' : np.zeros((times,))
    }

    for tm in range(times):
        offtimes['I'][tm] = np.mean(sigI[:,tm])
        offtimes['Q'][tm] = np.mean(sigQ[:,tm])
        offtimes['Amp'][tm] = np.mean(np.sqrt(sigI[:,tm]*sigI[:,tm] + sigQ[:,tm]*sigQ[:,tm]))
        offtimes['Phase'][tm] = np.mean(np.arctan(sigQ[:,tm] / sigI[:,tm]))

        if sigIZero is not None:
            offtimes['IZero'][tm] = np.mean(sigIZero[:,tm])
            offtimes['QZero'][tm] = np.mean(sigQZero[:,tm])
            offtimes['ZeroAmp'][tm] = np.mean(np.sqrt(sigIZero[:,tm]*sigIZero[:,tm] + sigQZero[:,tm]*sigQZero[:,tm]))
            offtimes['ZeroPhase'][tm] = np.mean(np.arctan(sigQZero[:,tm] / sigIZero[:,tm]))

            sigIDiff = sigI[:,tm] - sigIZero[:,tm]
            sigQDiff = sigQ[:,tm] - sigQZero[:,tm]

            offtimes['IDiff'][tm] = np.mean(sigIDiff)
            offtimes['QDiff'][tm] = np.mean(sigQDiff)
            offtimes['DiffAmp'][tm] = np.mean(np.sqrt(sigIDiff * sigIDiff + sigQDiff * sigQDiff))
            offtimes['DiffPhase'][tm] = np.mean(np.arctan(sigQDiff / sigIDiff))

    # Plot ...
    if sigIZero is None:
        fig, ax = plt.subplots(1, 3, squeeze=False, figsize=(6.4 * 3, 4.8 * 1))
    else:
        fig, ax = plt.subplots(3, 3, squeeze=False, figsize=(6.4 * 3, 4.8 * 3))


    fig.suptitle("Offset drift over time")

    ax[0][0].set_title("Signal offset (I/Q)")
    ax[0][0].set_xlabel("Sample number")
    ax[0][0].set_ylabel("Offset signal $\mu V$")
    ax[0][0].plot(offtimes['I'], label = 'I Offset signal')
    ax[0][0].plot(offtimes['Q'], label = 'Q Offset signal')
    ax[0][0].legend()
    ax[0][0].grid()

    ax[0][1].set_title("Signal offset (Amplitude)")
    ax[0][1].set_xlabel("Sample number")
    ax[0][1].set_ylabel("Offset signal amplitude $\mu V$")
    ax[0][1].plot(offtimes['Amp'], label = 'Amplitude signal')
    ax[0][1].legend()
    ax[0][1].grid()

    ax[0][2].set_title("Signal offset (Phase)")
    ax[0][2].set_xlabel("Sample number")
    ax[0][2].set_ylabel("Offset signal phase $rad$")
    ax[0][2].plot(offtimes['Phase'], label = "Phase signal")
    ax[0][2].legend()
    ax[0][2].grid()

    if sigIZero is not None:
        ax[1][0].set_title("Zero offset (I/Q)")
        ax[1][0].set_xlabel("Sample number")
        ax[1][0].set_ylabel("Offset zero $\mu V$")
        ax[1][0].plot(offtimes['IZero'], label = 'I Offset zero signal')
        ax[1][0].plot(offtimes['QZero'], label = 'Q Offset zero signal')
        ax[1][0].legend()
        ax[1][0].grid()

        ax[1][1].set_title("Zero offset (Amplitude)")
        ax[1][1].set_xlabel("Sample number")
        ax[1][1].set_ylabel("Offset zero amplitude $\mu V$")
        ax[1][1].plot(offtimes['ZeroAmp'], label = 'Amplitude zero')
        ax[1][1].legend()
        ax[1][1].grid()

        ax[1][2].set_title("Zero offset (Phase)")
        ax[1][2].set_xlabel("Sample number")
        ax[1][2].set_ylabel("Offset zero phase $rad$")
        ax[1][2].plot(offtimes['ZeroPhase'], label = "Phase zero")
        ax[1][2].legend()
        ax[1][2].grid()

        ax[2][0].set_title("Difference offset (I/Q)")
        ax[2][0].set_xlabel("Sample number")
        ax[2][0].set_ylabel("Offset difference $\mu V$")
        ax[2][0].plot(offtimes['IDiff'], label = 'I Offset difference signal')
        ax[2][0].plot(offtimes['QDiff'], label = 'Q Offset difference signal')
        ax[2][0].legend()
        ax[2][0].grid()

        ax[2][1].set_title("Difference offset (Amplitude)")
        ax[2][1].set_xlabel("Sample number")
        ax[2][1].set_ylabel("Offset difference amplitude $\mu V$")
        ax[2][1].plot(offtimes['DiffAmp'], label = 'Amplitude difference')
        ax[2][1].legend()
        ax[2][1].grid()

        ax[2][2].set_title("Difference offset (Phase)")
        ax[2][2].set_xlabel("Sample number")
        ax[2][2].set_ylabel("Offset difference phase $rad$")
        ax[2][2].plot(offtimes['DiffPhase'], label = "Phase difference")
        ax[2][2].legend()
        ax[2][2].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_offsettime.svg")
    plt.savefig(f"{fileprefix}_offsettime.png")
    plt.close(fig)
    print(f"[OFFSETTIME] Written {fileprefix}_offsettime")
    print("[OFFSETTIME] Finished")

    if aggregateHTMLReport is not None:
        if "Offset over time" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append("Offset over time")
        if f"Offset over time" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Offset over time"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Offset over time"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]["Offset over time"] + f"<img src=\"{fileprefix}_offsettime.png\" alt=\"\"><br>"



def plot_wndnoise(fileprefix, scan, job, aggregateHTMLReport = None):
    wndSize = job['n']

    print(f"[WNDNOISE] Starting for {fileprefix}, window size {wndSize}")

    sigI, sigQ = scan.get_raw_signal_iq()
    sigIZero, sigQZero = scan.get_raw_zero_iq()

    windowCount = len(sigI[0]) - wndSize + 1
    mainlen = len(sigI)

    noiseData = {
        'I' : np.zeros((windowCount,)),
        'Q' : np.zeros((windowCount,)),
        'IMax' : np.zeros((windowCount,)),
        'QMax' : np.zeros((windowCount,)),

        'IZero' : np.zeros((windowCount,)),
        'QZero' : np.zeros((windowCount,)),
        'IMaxZero' : np.zeros((windowCount,)),
        'QMaxZero' : np.zeros((windowCount,)),

        'IDiff' : np.zeros((windowCount,)),
        'QDiff' : np.zeros((windowCount,)),
        'IMaxDiff' : np.zeros((windowCount,)),
        'QMaxDiff' : np.zeros((windowCount,))
    }

    pctfinishedLast = None
    for xstart in range(windowCount):
        # We have to recalculate std and mean ourself ...
        pctfinished = int((xstart / windowCount) * 100)
        if pctfinishedLast != pctfinished:
            pctfinishedLast = pctfinished
            if pctfinished % 10 == 0:
                print(f"[WNDNOISE] Start index {xstart}, {pctfinished}% done")

        stdI = np.zeros((mainlen,))
        stdQ = np.zeros((mainlen,))

        if sigIZero is not None:
            stdIZero = np.zeros((mainlen,))
            stdQZero = np.zeros((mainlen,))
            stdIDiff = np.zeros((mainlen,))
            stdQDiff = np.zeros((mainlen,))

        for imain in range(mainlen):
            stdI[imain] = np.std(sigI[imain][xstart:xstart+wndSize-1])
            stdQ[imain] = np.std(sigQ[imain][xstart:xstart+wndSize-1])
            if sigIZero is not None:
                stdIZero[imain] = np.std(sigIZero[imain][xstart:xstart+wndSize-1])
                stdQZero[imain] = np.std(sigQZero[imain][xstart:xstart+wndSize-1])
                stdIDiff[imain] = np.std(sigI[imain][xstart:xstart+wndSize-1] - sigIZero[imain][xstart:xstart+wndSize-1])
                stdQDiff[imain] = np.std(sigQ[imain][xstart:xstart+wndSize-1] - sigQZero[imain][xstart:xstart+wndSize-1])

        noiseData['I'][xstart] = np.max(stdI)
        noiseData['Q'][xstart] = np.max(stdQ)
        noiseData['IMax'][xstart] = np.argmax(stdI)
        noiseData['QMax'][xstart] = np.argmax(stdQ)

        if sigIZero is not None:
            noiseData['IZero'][xstart] = np.max(stdIZero)
            noiseData['QZero'][xstart] = np.max(stdQZero)
            noiseData['IMaxZero'][xstart] = np.argmax(stdIZero)
            noiseData['QMaxZero'][xstart] = np.argmax(stdQZero)

            noiseData['IDiff'][xstart] = np.max(stdIDiff)
            noiseData['QDiff'][xstart] = np.max(stdQDiff)
            noiseData['IMaxDiff'][xstart] = np.argmax(stdIDiff)
            noiseData['QMaxDiff'][xstart] = np.argmax(stdQDiff)

    if sigIZero is None:
        fig, ax = plt.subplots(1, 2, squeeze=False, figsize=(6.4 * 1, 4.8 * 2))
    else:
        fig, ax = plt.subplots(3, 2, figsize=(6.4 * 3, 4.8 * 2))

    fig.suptitle(f"Noise in window (width: {wndSize} samples")
    ax[0][0].set_title("Signal noise")
    ax[0][0].set_xlabel("Window start sample")
    ax[0][0].set_ylabel("Noise maximum $\mu V$")
    ax[0][0].plot(noiseData['I'], label = 'I')
    ax[0][0].plot(noiseData['Q'], label = 'Q')
    ax[0][0].grid()
    ax[0][0].legend()

    ax[0][1].set_title("Signal noise maximum position")
    ax[0][1].set_xlabel("Window start sample")
    ax[0][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
    ax[0][1].plot(noiseData['IMax'], label = 'I')
    ax[0][1].plot(noiseData['QMax'], label = 'Q')
    ax[0][1].grid()
    ax[0][1].legend()

    if sigIZero is not None:
        ax[1][0].set_title("Zero noise")
        ax[1][0].set_xlabel("Window start sample")
        ax[1][0].set_ylabel("Noise maximum $\mu V$")
        ax[1][0].plot(noiseData['IZero'], label = 'IZero')
        ax[1][0].plot(noiseData['QZero'], label = 'QZero')
        ax[1][0].grid()
        ax[1][0].legend()

        ax[1][1].set_title("Zero noise maximum position")
        ax[1][1].set_xlabel("Window start sample")
        ax[1][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
        ax[1][1].plot(noiseData['IMaxZero'], label = 'IZero')
        ax[1][1].plot(noiseData['QMaxZero'], label = 'QZero')
        ax[1][1].grid()
        ax[1][1].legend()

        ax[2][0].set_title("Difference noise")
        ax[2][0].set_xlabel("Window start sample")
        ax[2][0].set_ylabel("Noise maximum $\mu V$")
        ax[2][0].plot(noiseData['IDiff'], label = 'IDiff')
        ax[2][0].plot(noiseData['QDiff'], label = 'QDiff')
        ax[2][0].grid()
        ax[2][0].legend()

        ax[2][1].set_title("Difference noise maximum position")
        ax[2][1].set_xlabel("Window start sample")
        ax[2][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
        ax[2][1].plot(noiseData['IMaxDiff'], label = 'IDiff')
        ax[2][1].plot(noiseData['QMaxDiff'], label = 'QDiff')
        ax[2][1].grid()
        ax[2][1].legend()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_wndnoise_{wndSize}.svg")
    plt.savefig(f"{fileprefix}_wndnoise_{wndSize}.png")
    plt.close(fig)
    print(f"[WNDNOISE] Written {fileprefix}_wndnoise_{wndSize}")
    print("[WNDNOISE] Finished")

    if aggregateHTMLReport is not None:
        if f"Noise in sliding window (wndsize={wndSize})" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append(f"Noise in sliding window (wndsize={wndSize})")
        if f"Noise in sliding window (wndsize={wndSize})" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Noise in sliding window (wndsize={wndSize})"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Noise in sliding window (wndsize={wndSize})"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Noise in sliding window (wndsize={wndSize})"] + f"<img src=\"{fileprefix}_wndnoise_{wndSize}.png\" alt=\"\"><br>"

def plot_ampphase(fileprefix, scan, aggregateHTMLReport = None):
    print(f"[AMPHASE] Starting for {fileprefix}")

    x = scan.get_main_axis_data()
    xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

    fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
    amp, phase = scan.get_signal_ampphase()

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("Amplitude $\mu V$")
    ax[0].plot(x, amp, label = "Amplitude")
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("Phase $rad$")
    ax[1].plot(x, phase, label = "Istd")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_signal_ap.svg")
    plt.savefig(f"{fileprefix}_signal_ap.png")
    print(f"[AMPHASE] Written {fileprefix}_signal")
    plt.close(fig)

    if aggregateHTMLReport is not None:
        if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append(f"Amplitude and phase (from I/Q)")
        if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] + f"<img src=\"{fileprefix}_signal_ap.png\" alt=\"\"><br>"

    amp, phase = scan.get_zero_ampphase()
    if amp is not None:
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Zero amplitude $\mu V$")
        ax[0].plot(x, amp, label = "Zero amplitude")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Zero phase $rad$")
        ax[1].plot(x, phase, label = "Zero phase")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_zero_ap.svg")
        plt.savefig(f"{fileprefix}_zero_ap.png")
        print(f"[AMPHASE] Written {fileprefix}_zero_ap")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"Amplitude and phase (from I/Q)")
            if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] + f"<img src=\"{fileprefix}_zero_ap.png\" alt=\"\"><br>"


        amp, phase = scan.get_diff_ampphase()
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Difference amplitude $\mu V$")
        ax[0].plot(x, amp, label = "Difference amplitude")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Difference phase $rad$")
        ax[1].plot(x, phase, label = "Difference phase")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_diff_ap.svg")
        plt.savefig(f"{fileprefix}_diff_ap.png")
        print(f"[AMPHASE] Written {fileprefix}_diff_ap")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"Amplitude and phase (from I/Q)")
            if f"Amplitude and phase (from I/Q)" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Amplitude and phase (from I/Q)"] + f"<img src=\"{fileprefix}_diff_ap.png\" alt=\"\"><br>"

    print("[AMPHASE] Finished")


def plot_iqmean(fileprefix, scan, aggregateHTMLReport = None):
    print(f"[IQMEAN] Starting for {fileprefix}")
    x = scan.get_main_axis_data()
    xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

    fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
    meanI, stdI, meanQ, stdQ = scan.get_signal_mean_iq()

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("Signal $\mu V$")
    ax[0].plot(x, meanI, label = "I")
    ax[0].plot(x, meanQ, label = "Q")
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("Noise $\mu V$")
    ax[1].plot(x, stdI, label = "Istd")
    ax[1].plot(x, stdQ, label = "Qstd")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_signal.svg")
    plt.savefig(f"{fileprefix}_signal.png")
    print(f"[IQMEAN] Written {fileprefix}_signal")
    plt.close(fig)

    if aggregateHTMLReport is not None:
        if f"I/Q samples" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append(f"I/Q samples")
        if f"I/Q samples" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] + f"<img src=\"{fileprefix}_signal.png\" alt=\"\"><br>"

    meanI, stdI, meanQ, stdQ = scan.get_zero_mean_iq()
    if meanI is not None:
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Zero signal $\mu V$")
        ax[0].plot(x, meanI, label = "IZero")
        ax[0].plot(x, meanQ, label = "QZero")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Zero noise $\mu V$")
        ax[1].plot(x, stdI, label = "IZero std")
        ax[1].plot(x, stdQ, label = "QZero std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_zero.svg")
        plt.savefig(f"{fileprefix}_zero.png")
        print(f"[IQMEAN] Written {fileprefix}_zero")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"I/Q samples" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"I/Q samples")
            if f"I/Q samples" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] + f"<img src=\"{fileprefix}_zero.png\" alt=\"\"><br>"

        meanI, stdI, meanQ, stdQ = scan.get_diff_mean_iq()
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Difference signal $\mu V$")
        ax[0].plot(x, meanI, label = "IDiff")
        ax[0].plot(x, meanQ, label = "QDiff")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Difference noise $\mu V$")
        ax[1].plot(x, stdI, label = "IDiff std")
        ax[1].plot(x, stdQ, label = "QDiff std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_diff.svg")
        plt.savefig(f"{fileprefix}_diff.png")
        print(f"[IQMEAN] Written {fileprefix}_diff")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"I/Q samples" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"I/Q samples")
            if f"I/Q samples" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"I/Q samples"] + f"<img src=\"{fileprefix}_diff.png\" alt=\"\"><br>"

    print("[IQMEAN] Finished")

def plot_timejitter(fileprefix, scan, aggregateHTMLReport = None):
    print(f"[TIMEJITTER] Starting for {fileprefix}")

    meanT = scan.get_raw_signal_timestamps()
    if meanT is None:
        print(f"[TIMEJITTER] No timing data present")
        return

    meanTZero = scan.get_raw_zero_timestamps()

    if meanTZero is None:
        fig, ax = plt.subplots(1, 3, squeeze = False, figsize=(6.4*3, 4.8))
    else:
        fig, ax = plt.subplots(2, 3, squeeze = False, figsize=(6.4*3, 4.8*2))

    dtSig = (meanT.flatten('F'))[1:] - (meanT.flatten('F'))[0:-1]
    ax[0][0].set_title("Time difference signal")
    ax[0][0].set_xlabel("Sample")
    ax[0][0].set_ylabel("Time difference")
    ax[0][0].plot(dtSig)
    ax[0][0].grid()

    ax[0][1].set_title("Time difference signal (detail, 99% quantile max)")
    ax[0][1].set_xlabel("Sample")
    ax[0][1].set_ylabel("Time difference")
    ax[0][1].plot(dtSig)
    ax[0][1].set_ylim([np.min(dtSig), np.quantile(dtSig, 0.99)])
    ax[0][1].grid()

    if meanTZero is not None:
        dtZero = (meanTZero[1:].flatten('F') - meanTZero[0:-1].flatten('F'))
        ax[1][0].set_title("Time difference reference / zero")
        ax[1][0].set_xlabel("Sample")
        ax[1][0].set_ylabel("Time difference")
        ax[1][0].plot(dtZero)
        ax[1][0].grid()

        ax[1][1].set_title("Time difference reference / zero (detail, 99% quantile max)")
        ax[1][1].set_xlabel("Sample")
        ax[1][1].set_ylabel("Time difference")
        ax[1][1].plot(dtZero)
        ax[1][1].set_ylim([np.min(dtZero), np.quantile(dtZero, 0.99)])
        ax[1][1].grid()

    ax[0][2].set_title("Raw timestamps (signal)")
    ax[0][2].set_xlabel("Sample")
    ax[0][2].set_ylabel("Timestamp")
    ax[0][2].plot(meanT.flatten('F'))
    ax[0][2].grid()

    if meanTZero is not None:
        ax[1][2].set_title("Raw timestamps (reference / zero)")
        ax[1][2].set_xlabel("Sample")
        ax[1][2].set_ylabel("Timestamp")
        ax[1][2].plot(meanTZero.flatten('F'))
        ax[1][2].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_diff.svg")
    plt.savefig(f"{fileprefix}_jitterplot.png")
    print(f"[TIMEJITTER] Written {fileprefix}_jitterplot")
    plt.close(fig)

    if meanTZero is not None:
        allts = np.sort(np.concatenate((meanT.flatten('F'), meanTZero.flatten('F'))))
        fig, ax = plt.subplots(2, 1, squeeze = False, figsize=(6.4, 4.8 * 2))
    else:
        allts = np.sort(meanT.flatten('F'))
        fig, ax = plt.subplots(1, 1, squeeze = False, figsize=(6.4, 4.8))

    alldts = allts[1:] - allts[:-1]

    ax[0][0].set_title("All timestamps and differences")
    ax[0][0].set_xlabel("Sampling point")
    ax[0][0].set_ylabel("Timestamp")
    ax[0][0].plot(allts)
    ax[0][0].grid()

    if meanTZero is not None:
        ax[1][0].set_title("All time differences")
        ax[1][0].set_xlabel("Sampling point")
        ax[1][0].set_ylabel("Time difference")
        ax[1][0].plot(alldts)
        ax[1][0].grid()

    plt.tight_layout()
    plt.savefig(f"{fileprefix}_timestamps.png")
    print(f"[TIMEJITTER] Written {fileprefix}_timestamps")
    plt.close(fig)

    if aggregateHTMLReport is not None:
        if f"Time Jitter" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append(f"Time Jitter")
        if f"Time Jitter" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Time Jitter"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Time Jitter"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Time Jitter"] + f"<img src=\"{fileprefix}_jitter.png\" alt=\"\"><br>"

    print("[TIMEJITTER] Done")


def plot_powermean(fileprefix, scan, aggregateHTMLReport = None):
    print(f"[POWERMEAN] Starting for {fileprefix}")
    x = scan.get_main_axis_data()
    xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

    fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
    meanP, stdP = scan.get_signal_mean_power()

    if meanP is None:
        meanP = np.full((len(x)), np.nan)
        stdP = np.full((len(x)), np.nan)

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("RF Power $mV_{rms}$")
    ax[0].plot(x, meanP * 1e3, label = "P")
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("RF power noise $mV_{rms}$")
    ax[1].plot(x, stdP * 1e3, label = "Pstd")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_signal.svg")
    plt.savefig(f"{fileprefix}_signal_power.png")
    print(f"[POWERMEAN] Written {fileprefix}_signal_power")
    plt.close(fig)

    if aggregateHTMLReport is not None:
        if f"Mean power" not in aggregateHTMLReport['columntitles']:
            aggregateHTMLReport['columntitles'].append(f"Mean power")
        if f"Mean power" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mean power"] = ""
        aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mean power"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Mean power"] + f"<img src=\"{fileprefix}_signal_power.png\" alt=\"\"><br>"

    meanPzero, stdPzero = scan.get_zero_mean_power()

    if meanPzero is not None:
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Zero RF power $mV_{rms}$")
        ax[0].plot(x, meanPzero * 1e3, label = "PZero")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Zero RF power noise $mV_{rms}$")
        ax[1].plot(x, stdPzero * 1e3, label = "PZero std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_zero.svg")
        plt.savefig(f"{fileprefix}_zero_power.png")
        print(f"[POWERMEAN] Written {fileprefix}_zero_power")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"Zero mean power" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"Zero mean power")
            if f"Zero mean power" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Zero mean power"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Zero mean power"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Zero mean power"] + f"<img src=\"{fileprefix}_zero_power.png\" alt=\"\"><br>"

        #meanP, stdP = scan.get_diff_mean_power()
        stdP = np.sqrt(stdP * stdP + stdPzero * stdPzero) * 1e6
        meanP = (meanP - meanPzero) * 1e6

        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("RF power $\mu V_{rms}$")
        ax[0].plot(x, meanP, label = "PDiff")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Difference RF power noise $\mu V_{rms}$")
        ax[1].plot(x, stdP, label = "PDiff std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_diff.svg")
        plt.savefig(f"{fileprefix}_diff_power.png")
        print(f"[IQMEAN] Written {fileprefix}_diff_power")
        plt.close(fig)

        if aggregateHTMLReport is not None:
            if f"Difference mean power" not in aggregateHTMLReport['columntitles']:
                aggregateHTMLReport['columntitles'].append(f"Difference mean power")
            if f"Difference mean power" not in aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]:
                aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Difference mean power"] = ""
            aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Difference mean power"] = aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1][f"Difference mean power"] + f"<img src=\"{fileprefix}_diff_power.png\" alt=\"\"><br>"

    print("[POWERMEAN] Finished")


def plot_iqmean_sliced(fileprefix, scan, aggregateHTMLReport = None, nslices = 10):
    print(f"[IQMEANSLICES] Starting for {fileprefix}")

    sliceStart = 0
    while sliceStart < len(scan.get_raw_signal_iq()[0][0]):
        print(len(scan.get_raw_signal_iq()[0][0]))
        dataslice = [sliceStart, nslices]

        print(f"[IQMEANSLICES]\tStarting from {sliceStart}, {nslices} samples")

        x = scan.get_main_axis_data()
        xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
        meanI, stdI, meanQ, stdQ = scan.get_signal_mean_iq(slice = dataslice)

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Signal $\mu V$")
        ax[0].plot(x, meanI, label = "I")
        ax[0].plot(x, meanQ, label = "Q")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Noise $\mu V$")
        ax[1].plot(x, stdI, label = "Istd")
        ax[1].plot(x, stdQ, label = "Qstd")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_signal.svg")
        plt.savefig(f"{fileprefix}_signal_slices_{sliceStart}.png")
        print(f"[IQMEANSLICES] Written {fileprefix}_signal_slices_{sliceStart}")
        plt.close(fig)

        meanI, stdI, meanQ, stdQ = scan.get_zero_mean_iq(slice = dataslice)
        if meanI is not None:
            fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel("Zero signal $\mu V$")
            ax[0].plot(x, meanI, label = "IZero")
            ax[0].plot(x, meanQ, label = "QZero")
            ax[0].legend()
            ax[0].grid()

            ax[1].set_xlabel(xlabel)
            ax[1].set_ylabel("Zero noise $\mu V$")
            ax[1].plot(x, stdI, label = "IZero std")
            ax[1].plot(x, stdQ, label = "QZero std")
            ax[1].legend()
            ax[1].grid()

            plt.tight_layout()
            #plt.savefig(f"{fileprefix}_zero.svg")
            plt.savefig(f"{fileprefix}_zero_slices_{sliceStart}.png")
            print(f"[IQMEANSLICES] Written {fileprefix}_zero_slices_{sliceStart}")
            plt.close(fig)

            meanI, stdI, meanQ, stdQ = scan.get_diff_mean_iq(slice = dataslice)
            fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel("Difference signal $\mu V$")
            ax[0].plot(x, meanI, label = "IDiff")
            ax[0].plot(x, meanQ, label = "QDiff")
            ax[0].legend()
            ax[0].grid()

            ax[1].set_xlabel(xlabel)
            ax[1].set_ylabel("Difference noise $\mu V$")
            ax[1].plot(x, stdI, label = "IDiff std")
            ax[1].plot(x, stdQ, label = "QDiff std")
            ax[1].legend()
            ax[1].grid()

            plt.tight_layout()
            #plt.savefig(f"{fileprefix}_diff.svg")
            plt.savefig(f"{fileprefix}_diff_slices_{sliceStart}.png")
            print(f"[IQMEANSLICES] Written {fileprefix}_diff_slices_{sliceStart}")
            plt.close(fig)

        sliceStart = sliceStart + nslices

    print("[IQMEANSLICES] Finished")



def main():
    jobs = []
    jobfiles = []

    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    aggregateHTMLReport = None

    # We get called with one or more runfiles or NPZs as argument ...
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].strip() == "-iqmean":
            jobs.append({ 'task' : 'iqmean' })
        elif sys.argv[i].strip() == "-apmean":
            jobs.append({ 'task' : 'apmean' })
        elif sys.argv[i].strip() == "-powermean":
            jobs.append({ 'task' : 'powermean' })
        elif sys.argv[i].strip() == "-offsettime":
            jobs.append({ 'task' : 'offsettime' })
        elif sys.argv[i].strip() == "-decompose":
            jobs.append({ 'task' : 'decompose', 'debug' : False })
        elif sys.argv[i].strip() == "-decomposedebug":
            jobs.append({ 'task' : 'decompose', 'debug' : True })
        elif sys.argv[i].strip() == "-mixfit":
            jobs.append({ 'task' : 'mixfit', 'debug' : False })
        elif sys.argv[i].strip() == "-mixfitdebug":
            jobs.append({ 'task' : 'mixfit', 'debug' : True })
        elif sys.argv[i].strip() == "-allan":
            jobs.append({ 'task' : 'allan' })
        elif sys.argv[i].strip() == "-metrics":
            jobs.append({ 'task' : 'metrics' })
        elif sys.argv[i].strip() == "-agreport":
            aggregateHTMLReport = {
                'reportdata' : [],
                'columntitles' : []
            }
        elif sys.argv[i].strip() == "-timejitter":
            jobs.append({ 'task' : 'timejitter' })
        elif sys.argv[i].strip() == "-wndnoise":
            n = 0
            if i == (len(sys.argv)-1):
                print("Missing length argument for wndnoise, require window size")
                sys.exit(1)
            try:
                n = int(sys.argv[i+1])
            except:
                print(f"Failed to interpret {sys.argv[i+1]} as window size (integer sample count)")
                sys.exit(1)
            if n < 1:
                print(f"Failed to interpret {sys.argv[i+1]} as window size (has to be a positive integer sample count)")
                sys.exit(1)
            jobs.append({'task' : 'wndnoise', 'n' : n })
            # Skip N
            i = i + 1
        elif sys.argv[i].strip() == "-iqslices":
            n = 0
            if i == (len(sys.argv)-1):
                print("Missing slice length for iqslices")
                sys.exit(1)
            try:
                n = int(sys.argv[i+1])
            except:
                print(f"Failed to interpret {sys.argv[i+1]} as window size (integer sample count)")
                sys.exit(1)
            jobs.append({'task' : 'iqmean_sliced', 'n' : n })
            # Skip N
            i = i+ 1
        else:
            if sys.argv[i].strip().startswith("-"):
                print(f"Unrecognized option {sys.argv[i]}")
                sys.exit(1)

            # Check if file exists
            if os.path.isfile(sys.argv[i].strip()):
                if (not sys.argv[i].strip().endswith(".npz")) and (not sys.argv[i].strip().endswith("_run.txt")):
                    print(f"Unrecognized file type for file {sys.argv[i]} (by name)")
                    sys.exit(1)
                jobfiles.append(sys.argv[i].strip())
            else:
                print(f"File {sys.argv[i]} not found")
        i = i + 1

    for jobfile in jobfiles:
        try:
            sc = None
            if jobfile.endswith(".npz"):
                # Try to load as single scan or as 1D scan
                try:
                    sc = scanhandler.load_npz(jobfile)
                except Exception as e:
                    print(f"Failed to load {jobfile} due to NPZ error:")
                    print(e)

            # Execute jobs ...
            scanQuantity, scanQuantityTitle, scanQuantityData, scans = sc.get_scans()
            print(scans)
            for iscan, scan in enumerate(scans):
                if aggregateHTMLReport is not None:
                    aggregateHTMLReport['reportdata'].append({})
                    aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]['Run'] = jobfile
                    aggregateHTMLReport['reportdata'][len(aggregateHTMLReport['reportdata'])-1]['Scan'] = str(scan)
                    if "Run" not in aggregateHTMLReport['columntitles']:
                        aggregateHTMLReport['columntitles'].append("Run")
                        aggregateHTMLReport['columntitles'].append("Scan")

                metrics = {}
                if len(scans) < 2:
                    fnprefix = f"{jobfile}"
                else:
                    fnprefix = f"{jobfile}_scan{iscan}"
                for job in jobs:
                    if job['task'] == "iqmean":
                        plot_iqmean(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "apmean":
                        plot_ampphase(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "wndnoise":
                        plot_wndnoise(fnprefix, scan, job, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "offsettime":
                        plot_offsettime(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "decompose":
                        metrics = plot_decompose(fnprefix, scan, metrics = metrics, debugplots = job['debug'], aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "allan":
                        plot_allan(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "metrics":
                        metrics = metrics_collect_core(fnprefix, scan, metrics, aggregateHTMLReport = aggregateHTMLReport)
                        metrics_write(fnprefix, scan, metrics, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "mixfit":
                        metrics = plot_decompose_mixturefit(fnprefix, scan, metrics = metrics, debugplots = job['debug'], aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "iqmean_sliced":
                        plot_iqmean_sliced(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport, nslices = job['n'])
                    if job['task'] == "timejitter":
                        plot_timejitter(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
                    if job['task'] == "powermean":
                        plot_powermean(fnprefix, scan, aggregateHTMLReport = aggregateHTMLReport)
        except:
            print("Ignoring job due to previous errors ...")

    if aggregateHTMLReport is not None:
        # Generate webpage containing a table with all generated graphics
        print("[AGREPORT] Writing "+str(os.path.join(os.path.dirname(os.path.realpath(f"{fnprefix}")), "agreport.html")))
        with open(os.path.join(os.path.dirname(os.path.realpath(f"{fnprefix}")), "agreport.html"), "w") as htmlout:
            htmlout.write(textwrap.dedent("""
                <!DOCTYPE HTML>
                <html>
                    <head>
                        <title> QUAK/ESR report output </title>
                        <style type="text/css">
                        <!--
                            td {
                                vertical-align: top;
                            }
                        -->
                        </style>
                    </head>
                    <body>
                        <table border="1">
                            <thead>
                                <tr>
            """))
            for colmn in aggregateHTMLReport['columntitles']:
                htmlout.write(f"<td>{colmn}</td>")
            htmlout.write(textwrap.dedent("""
                                </tr>
                            </thead>
                            <tbody>
            """))

            for run in aggregateHTMLReport['reportdata']:
                htmlout.write("<tr>")
                for colmn in aggregateHTMLReport['columntitles']:
                    htmlout.write(f"<td>{run[colmn]}</td>")

            htmlout.write(textwrap.dedent("""
                            </tbody>
                        </table>
                    </body>
                </html>
            """))
if __name__ == "__main__":
    main()
