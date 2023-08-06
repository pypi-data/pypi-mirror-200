# QUAK/ESR analysis utility

This is work in progress.

This repository contains a collection of classes and utilities to handle
and work with QUAK/ESR data files.

## Installation

```
pip install quakesranalysis-tspspi
```

### Upgrading

```
pip install --upgrade quakesranalysis-tspspi
```

## Utilities

### ```quakesrplot```

The ```quakesrplot``` is capable of generating standard plots for single peak
scans and 1D scans. Those include:

* ```iqmean``` is just a standard plot of the mean values and standard deviations
  of all captured I/Q samples in scan, zero scan and difference
* ```apmean``` calculated amplitude and phase out of I/Q samples and plots
  them for scan, zero scan and difference
* ```wndnoise``` provides a sliding window noise calculation by calculating the
  standard deviation inside this configurable sliding window to show how noise
  changes over time.
* ```offsettime``` plots the offset of all three captured signal types over time
* ```allan``` calculates the Allan deviation of the system for all samples points
  along the main axis (frequency, B0, ...) as well as a worst case Allan deviation
* ```decompose``` decomposes the found signal, zero signal and difference signal
  into a mixture of Gaussians (this can be inspected by setting ```decomposedebug```)
* ```mixfit``` does the same as decompose but for more different function types (Gaussian,
  Cauchy, Difference of Gaussian, Difference of Cauchy, Constant, ...). Inspection
  of the fitting behaviour is also possible using ```mixfitdebug```
* ```metrics``` outputs collected metrics into a JSON data file. This should be
  run at the end.

All plots are stored along the source datafile and named with the same prefix.

Example usage:

```
quakesrplot -iqmean -apmean -wndnoise 10 -wndnoise 3 -offsettime -mixfit -allan *_peak.npz 
```

To see a list of all supported features execute without arguments:

```
quakesrplot
```

When outputting debug plots for ```decompose``` or ```mixfit``` the ```QtAgg``` backend
of ```matplotlib``` tends to crash sometimes. One can then launch the application using
a different backend such as ```TkAgg``` on via the ```MPLBACKEND``` environment variable:

```
env MPLBACKEND=tkagg quakesrplot -iqmean -apmean -wndnoise 10 -wndnoise 3 -offsettime -mixfitdebug -allan *_peak.npz
```

### ```quakesrslice```

The ```quakesrslice``` utility is capable of slicing nD scans (1D/2D scans)
into separate ```.npz``` files.

```
Usage: quakesrslice [OPTIONS] FILENAMES

Slices nD scans into single NPZs

Options:
\t--outdir DIRECTORY
\t\tWrite all sliced NPZs into the specified output directory (setable
\t\tonly once for all input files)
```

### ```quakesrfetch```

```
Usage: quakesrfetch [OPTIONS] FROMDATE [TODATE]

Fetches all NPZ and run files from QUAK/ESR runs from the configured
measurement directory that are taken since the specified dates and times.
If no end date is specified all runs starting from the given timestamp will
be fetched.

The date and timestamps can be supplied either as

	YYYYMMDD
		When addressing a whole day
	YYYYMMDDHHMMSS
		When adressing a given date and time

Options:
	--outdir DIRECTORY
		Write all fetched NPZs into the specified output directory
	--list
		Also write a list of fetched NPZs onto standard output to be passed
		to an analysis tool
	--sshkey KEYFILE
		Specified the SSH keyfile to use. It's assumed to be a passwordless (!)
		keyfile ...
```
