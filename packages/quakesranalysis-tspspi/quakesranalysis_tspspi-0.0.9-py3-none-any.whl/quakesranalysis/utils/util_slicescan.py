import sys
sys.path.append("../")
sys.path.append("../../")

import numpy as np

import sys
import os

import textwrap

def printUsage():
    print(textwrap.dedent("""
        Usage: {} [OPTIONS] FILENAMES

        Slices nD scans into single NPZs

        Options:
        \t--outdir DIRECTORY
        \t\tWrite all sliced NPZs into the specified output directory (setable
        \t\tonly once for all input files)
    """.format(sys.argv[0])))



def main():
    jobfiles = []

    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    i = 1
    outputDir = None

    while i < len(sys.argv):
        if sys.argv[i].strip().startswith("--outdir"):
            if i == (len(sys.argv) - 1):
                print("Error: Missing output directory after --outdir")
                print("\n")
                printUsage()
                sys.exit(1)
            outputDir = sys.argv[i+1]

            # Check output directory exists
            if not os.path.isdir(outputDir):
                print(f"Output directory {outputDir} not found")
                print("\n")
                printUsage()
                sys.exit(1)

            i = i + 2
            continue

        if sys.argv[i].strip().startswith("-"):
            print(f"Unrecognized option {sys.argv[i]}")
            sys.exit(1)

        # Check if file exists
        if os.path.isfile(sys.argv[i].strip()):
            if (not sys.argv[i].strip().endswith(".npz")):
                print(f"Unrecognized file type for file {sys.argv[i]} (by name)")
                sys.exit(1)
            jobfiles.append(sys.argv[i].strip())
        else:
            print(f"File {sys.argv[i]} not found")

        i = i + 1

    singlefiles = []

    for npzfile in jobfiles:
        pathNPZ = os.path.dirname(os.path.abspath(npzfile))
        if outputDir is None:
            npzOutputDir = pathNPZ
        else:
            npzOutputDir = outputDir

        basename = os.path.basename(os.path.abspath(npzfile))

        # Strip extension
        basename = basename[:-4]



        # Load the given NPZ ...
        data = np.load(npzfile)
        print(f"[SLICE] Loaded {npzfile}")

        # Check if this is a scan. If not warning message and abort ...

        scansizes = []

        if "scan" in data:
            # This is a 1D scan
            ndims = 1
            scansizes.append(len(data["scan"]))
        elif "scan0" in data:
            # 2D or higher scan ...
            ndims = 0
            while f"scan{ndims}" in data:
                scansizes.append(len(data[f"scan{ndims}"]))
                ndims = ndims + 1
        else:
            ndims = 0

        print(f"[SLICE] Scan is a {ndims}D scan (0D is a peakscan)")

        # If ndims > 1 first unroll ...
        if ndims >= 1:
            # Calculate total number of scans ...
            totalscans = 1
            for scs in scansizes:
                totalscans = totalscans * scs

            print(f"[SLICE] Slicing {ndims}D scan into {totalscans} peakscans")

            # Initialize indices ...
            idx = []
            for i in range(len(scansizes)):
                idx.append(0)

            processedscans = 0
            while processedscans < totalscans:
                # Fetch current scan into separate (peak scan) npz
                fname = f"{basename}"
                for i in idx:
                    fname = fname + f"_{i}"
                fname = fname + ".npz"

                fname = os.path.join(npzOutputDir, fname)

                # Extract data ...
                newdata = { }
                for k in data.keys():
                    print(f"[SLICE] Processing {k} with shape {data[k].shape}")
                    if k.startswith("sigI") or k.startswith("sigQ"):
                        payl = data[k]
                        for i in idx:
                            payl = payl[i]
                        newdata[k] = payl
                    else:
                        newdata[k] = data[k]

                np.savez(fname, **newdata)
                singlefiles.append(fname)
                print(f"[SLICE] Created {fname}")

                processedscans = processedscans + 1

                # Incremend key ...
                if processedscans == totalscans:
                    break
                i = 0
                while True:
                    idx[i] = idx[i] + 1
                    if idx[i] >= scansizes[i]:
                        idx[i] = 0
                        i = i + 1
                        continue
                    break
        else:
            singlefiles.append(npzfile)

    # Now process NPZ files ...




if __name__ == "__main__":
    main()