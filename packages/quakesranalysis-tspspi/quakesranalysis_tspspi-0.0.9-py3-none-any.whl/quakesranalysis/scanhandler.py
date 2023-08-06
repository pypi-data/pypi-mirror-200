import numpy as np

def load_npz(filename):
    data = np.load(filename)
    if "scan" not in data:
        return QUAKESRScan.load(filename)
    else:
        return QUAKESRScan1D.load(filename)

class QUAKESRScan:
    @staticmethod
    def load(filename):
        # Loads a single scan from an NPZ
        mainAxis = None
        mainAxisTitle = None
        sigI = None
        sigQ = None
        sigIZero = None
        sigQZero = None

        sigP = None
        sigPZero = None
        sigT = None
        sigTZero = None

        data = np.load(filename)
        if "f_RF" in data:
            mainAxis = "f_RF"
            mainAxisTitle = "RF frequency"
        else:
            raise ValueError("Unsupported scan type (not a frequency scan)")

        sigI = data["sigI"]
        sigQ = data["sigQ"]

        if "sigT" in data:
            sigT = data["sigT"]
        if "sigTzero" in data:
            sigTZero = data["sigTzero"]
        if "sigP" in data:
            sigP = data["sigP"]
        if "sigPzero" in data:
            sigPZero = data["sigPzero"]
        
        if "sigIzero" in data:
            sigIZero = data["sigIzero"]
            sigQZero = data["sigQzero"]

        return QUAKESRScan(data[mainAxis], mainAxis, mainAxisTitle, sigI, sigQ, sigIZero, sigQZero, sigT, sigTZero, sigP, sigPZero, filename)

    def __init__(self, mainAxisData, mainAxis, mainAxisTitle, sigI, sigQ, sigIZero = None, sigQZero = None, sigT = None, sigTZero = None, sigP = None, sigPZero = None, filename = None):
        self._main_axis_data = mainAxisData
        self._main_axis = mainAxis
        self._main_axis_title = mainAxisTitle

        self._sigI = sigI
        self._sigQ = sigQ

        self._sigI_Mean = None
        self._sigI_Std = None
        self._sigQ_Mean = None
        self._sigQ_Std = None
        self._sig_Amp = None
        self._sig_Phase = None

        self._sigIZero = sigIZero
        self._sigQZero = sigQZero

        self._sigIZero_Mean = None
        self._sigIZero_Std = None
        self._sigQZero_Mean = None
        self._sigQZero_Std = None
        self._sigZero_Amp = None
        self._sigZero_Phase = None

        self._sigIDiff_Mean = None
        self._sigIDiff_Std = None
        self._sigQDiff_Mean = None
        self._sigQDiff_Std = None
        self._sigDiff_Amp = None
        self._sigDiff_Phase = None

        self._sigT = sigT
        self._sigTZero = sigTZero

        self._sigP = sigP
        self._sigPZero = sigPZero
        self._sigPDiff = None

        self._sigP_Mean = None
        self._sigP_Std = None
        self._sigPZero_Mean = None
        self._sigPZero_Std = None
        self._sigPDiff_Mean = None
        self._sigPDiff_Std = None

        # Convert power into V
        if self._sigP is not None:
            self._sigP = np.sqrt(np.power(10, self._sigP / 10) * 1e-3 * 50)
        if self._sigPZero is not None:
            self._sigPZero = np.sqrt(np.power(10, self._sigPZero / 10) * 1e-3 * 50)

        self._filename = filename

    def get_scans(self):
        return ( None, None, None, [ self ] )

    def get_main_axis_title(self):
        return self._main_axis_title

    def get_main_axis_symbol(self):
        return self._main_axis

    def get_main_axis_data(self):
        return self._main_axis_data
        
    def get_raw_signal_iq(self, slice = None):
        if slice is None:
            return self._sigI, self._sigQ
        else:
            if (slice[0] > len(self._sigI[0])) or (slice[0] < 0):
                raise IndexError("Slice start has to be positive and within length of captured data")
            if (slice[1] < 0):
                raise IndexError("Slice length has to be a positive integer")
            if (slice[0] + slice[1] >= len(self._sigI[0])):
                # Clamp to last segment ...
                slice[1] = len(self._sigI[0]) - slice[0]

            return self._sigI[:, slice[0] : slice[0] + slice[1]], self._sigQ[:, slice[0] : slice[0] + slice[1]]
    def get_raw_zero_iq(self, slice = None):
        if slice is None:
            return self._sigIZero, self._sigQZero
        else:
            if (slice[0] > len(self._sigIZero[0])) or (slice[0] < 0):
                raise IndexError("Slice start has to be positive and within length of captured data")
            if (slice[1] < 0):
                raise IndexError("Slice length has to be a positive integer")
            if (slice[0] + slice[1] >= len(self._sigI)):
                # Clamp to last segment ...
                slice[1] = len(self._sigIZero[0]) - slice[0]
            return self._sigIZero[:, slice[0] : slice[0] + slice[1]], self._sigQZero[:, slice[0] : slice[0] + slice[1]]

    def get_raw_signal_timestamps(self, slice = None):
        if self._sigT is None:
            return None

        if slice is None:
            return self._sigT
        else:
            if (slice[0] > len(self._sigI[0])) or (slice[0] < 0):
                raise IndexError("Slice start has to be positive and within length of captured data")
            if (slice[1] < 0):
                raise IndexError("Slice length has to be a positive integer")
            if (slice[0] + slice[1] >= len(self._sigI[0])):
                # Clamp to last segment ...
                slice[1] = len(self._sigI[0]) - slice[0]

            return self._sigT[:, slice[0] : slice[0] + slice[1]]

    def get_raw_zero_timestamps(self, slice = None):
        if self._sigTZero is None:
            return None
        if slice is None:
            return self._sigTZero
        else:
            if (slice[0] > len(self._sigI[0])) or (slice[0] < 0):
                raise IndexError("Slice start has to be positive and within length of captured data")
            if (slice[1] < 0):
                raise IndexError("Slice length has to be a positive integer")
            if (slice[0] + slice[1] >= len(self._sigI[0])):
                # Clamp to last segment ...
                slice[1] = len(self._sigI[0]) - slice[0]

            return self._sigTZero[:, slice[0] : slice[0] + slice[1]]

    def get_signal_mean_iq(self, slice = None):
        if slice is None:
            if self._sigI_Mean is not None:
                return self._sigI_Mean, self._sigI_Std, self._sigQ_Mean, self._sigQ_Std

            self._sigI_Mean = np.zeros(self._main_axis_data.shape)
            self._sigQ_Mean = np.zeros(self._main_axis_data.shape)
            self._sigI_Std = np.zeros(self._main_axis_data.shape)
            self._sigQ_Std = np.zeros(self._main_axis_data.shape)
            
            for i in range(len(self._main_axis_data)):
                self._sigI_Mean[i] = np.mean(self._sigI[i])
                self._sigQ_Mean[i] = np.mean(self._sigQ[i])
                self._sigI_Std[i] = np.std(self._sigI[i])
                self._sigQ_Std[i] = np.std(self._sigQ[i])

            return self._sigI_Mean, self._sigI_Std, self._sigQ_Mean, self._sigQ_Std
        else:
            sigi, sigq = self.get_raw_signal_iq(slice = slice)

            sigI_Mean = np.zeros(self._main_axis_data.shape)
            sigQ_Mean = np.zeros(self._main_axis_data.shape)
            sigI_Std = np.zeros(self._main_axis_data.shape)
            sigQ_Std = np.zeros(self._main_axis_data.shape)

            for i in range(len(self._main_axis_data)):
                sigI_Mean[i] = np.mean(sigi[i])
                sigQ_Mean[i] = np.mean(sigq[i])
                sigI_Std[i] = np.std(sigi[i])
                sigQ_Std[i] = np.std(sigq[i])

            return sigI_Mean, sigI_Std, sigQ_Mean, sigQ_Std

    def get_signal_mean_power(self, slice = None):
        if self._sigP is None:
            return np.full(self._main_axis_data.shape, np.nan), np.full(self._main_axis_data.shape, np.nan)

        if slice is None:
            if self._sigP_Mean is not None:
                return self._sigP_Mean, self._sigP_Std

            self._sigP_Mean = np.zeros(self._main_axis_data.shape)
            self._sigP_Std = np.zeros(self._main_axis_data.shape)
            
            for i in range(len(self._main_axis_data)):
                self._sigP_Mean[i] = np.mean(self._sigP[i])
                self._sigP_Std[i] = np.std(self._sigP[i])

            return self._sigP_Mean, self._sigP_Std
        else:
            raise NotImplementedError()

    def get_zero_mean_power(self, slice = None):
        if self._sigPZero is None:
            return np.full(self._main_axis_data.shape, np.nan), np.full(self._main_axis_data.shape, np.nan)

        if slice is None:
            if self._sigPZero_Mean is not None:
                return self._sigPZero_Mean, self._sigPZero_Std

            self._sigPZero_Mean = np.zeros(self._main_axis_data.shape)
            self._sigPZero_Std = np.zeros(self._main_axis_data.shape)

            for i in range(len(self._main_axis_data)):
                self._sigPZero_Mean[i] = np.mean(self._sigPZero[i])
                self._sigPZero_Std[i] = np.std(self._sigPZero[i])

            return self._sigPZero_Mean, self._sigPZero_Std
        else:
            raise NotImplementedError()

    def get_diff_mean_power(self, slice = None):
        if self._sigPZero is None:
            return None, None

        if slice is None:
            if self._sigPDiff_Mean is not None:
                return self._sigPDiff_Mean, self._sigPDiff_Std

            pmean, pstd = self.get_signal_mean_power()
            pzmean, pzstd = self.get_zero_mean_power()

            dmean = pmean - pzmean
            dstd = np.sqrt(pstd * pstd + pzstd * pzstd)

            self._sigPDiff_Mean = dmean
            self._sigPDiff_Std = dstd

            return self._sigPDiff_Mean, self._sigPDiff_Std
        else:
            raise NotImplementedError()

    def get_signal_ampphase(self, slice = None):
        if slice is None:
            if self._sig_Amp is not None:
                return self._sig_Amp, self._sig_Phase

            #if self._sigI_Mean is None:
            #    # Generate mean and standard deviations
            #    _, _, _, _ = self.get_signal_mean_iq()

            #self._sig_Amp = np.sqrt(self._sigI_Mean * self._sigI_Mean + self._sigQ_Mean * self._sigQ_Mean)
            #self._sig_Phase = np.arctan(self._sigQ_Mean / self._sigI_Mean)

            self._sig_Amp = np.zeros(self._main_axis_data.shape)
            self._sig_Phase = np.zeros(self._main_axis_data.shape)
            for i in range(len(self._main_axis_data)):
                self._sig_Amp[i] = np.mean(np.sqrt(self._sigI[i] * self._sigI[i] + self._sigQ[i] * self._sigQ[i]))
                self._sig_Phase[i] = np.mean(np.arctan(self._sigQ[i] / self._sigI[i]))

            return self._sig_Amp, self._sig_Phase
        else:
            sigIMean, sigIStd, sigQMean, sigQStd = self.get_signal_mean_iq(slice = slice)

            return (
                np.sqrt(sigIMean * sigIMean + sigQMean * sigQMean),
                np.arctan(sigQMean / sigIMean)
            )

    def get_zero_mean_iq(self, slice = None):
        if slice is None:
            if self._sigIZero is None:
                # This has not been a diffscan ...
                return None, None, None, None

            if self._sigIZero_Mean is not None:
                return self._sigIZero_Mean, self._sigIZero_Std, self._sigQZero_Mean, self._sigQZero_Std

            self._sigIZero_Mean = np.zeros(self._main_axis_data.shape)
            self._sigQZero_Mean = np.zeros(self._main_axis_data.shape)
            self._sigIZero_Std = np.zeros(self._main_axis_data.shape)
            self._sigQZero_Std = np.zeros(self._main_axis_data.shape)
            
            for i in range(len(self._main_axis_data)):
                self._sigIZero_Mean[i] = np.mean(self._sigIZero[i])
                self._sigQZero_Mean[i] = np.mean(self._sigQZero[i])
                self._sigIZero_Std[i] = np.std(self._sigIZero[i])
                self._sigQZero_Std[i] = np.std(self._sigQZero[i])

            return self._sigIZero_Mean, self._sigIZero_Std, self._sigQZero_Mean, self._sigQZero_Std
        else:
            if self._sigIZero is None:
                return None, None, None, None

            if (slice[0] > len(self._sigIZero[0])) or (slice[0] < 0):
                raise IndexError("Slice start has to be positive and within length of captured data")
            if (slice[1] < 0):
                raise IndexError("Slice length has to be a positive integer")
            if (slice[0] + slice[1] >= len(self._sigI[0])):
                # Clamp to last segment ...
                slice[1] = len(self._sigIZero) - slice[0]

            sigIZero_Mean = np.zeros(self._main_axis_data.shape)
            sigQZero_Mean = np.zeros(self._main_axis_data.shape)
            sigIZero_Std = np.zeros(self._main_axis_data.shape)
            sigQZero_Std = np.zeros(self._main_axis_data.shape)

            for i in range(len(self._main_axis_data)):
                sigIZero_Mean[i] = np.mean(self._sigIZero[i, slice[0] : slice[0] + slice[1]])
                sigQZero_Mean[i] = np.mean(self._sigQZero[i, slice[0] : slice[0] + slice[1]])
                sigIZero_Std[i] = np.std(self._sigIZero[i, slice[0] : slice[0] + slice[1]])
                sigQZero_Std[i] = np.std(self._sigQZero[i, slice[0] : slice[0] + slice[1]])

            return sigIZero_Mean, sigIZero_Std, sigQZero_Mean, sigQZero_Std

    def get_zero_ampphase(self, slice = None):
        if slice is None:
            if self._sigIZero is None:
                # This has not been a diffscan ...
                return None, None

            if self._sigZero_Amp is not None:
                return self._sigZero_Amp, self._sigZero_Phase

            if self._sigIZero_Mean is None:
                # Generate mean and standard deviations
                _, _, _, _ = self.get_zero_mean_iq()

            self._sigZero_Amp = np.sqrt(self._sigIZero_Mean * self._sigIZero_Mean + self._sigQZero_Mean * self._sigQZero_Mean)
            self._sigZero_Phase = np.arctan(self._sigQZero_Mean / self._sigIZero_Mean)

            return self._sigZero_Amp, self._sigZero_Phase
        else:
            sigIZero_Mean, _, sigQZero_Mean, _ = self.get_zero_mean_iq(slice = slice)
            amp = np.sqrt(sigIZero_Mean * sigIZero_Mean + sigQZero_Mean * sigQZero_Mean)
            phase = np.arctan(sigQZero_Mean, sigIZero_Mean)
            return amp, phase

    def get_diff_mean_iq(self, slice = None):
        if slice is None:
            if self._sigIZero is None:
                # This has not been a diffscan ...
                return None, None, None, None

            if self._sigIDiff_Mean is not None:
                return self._sigIDiff_Mean, self._sigIDiff_Std, self._sigQDiff_Mean, self._sigQDiff_Std

            # Ensure means are available ...
            _, _, _, _ = self.get_signal_mean_iq()
            _, _, _, _ = self.get_zero_mean_iq()

            self._sigIDiff_Mean = self._sigIZero_Mean - self._sigI_Mean
            self._sigQDiff_Mean = self._sigQZero_Mean - self._sigQ_Mean
            self._sigIDiff_Std = np.sqrt(self._sigIZero_Std * self._sigIZero_Std + self._sigI_Std * self._sigI_Std)
            self._sigQDiff_Std = np.sqrt(self._sigQZero_Std * self._sigQZero_Std + self._sigQ_Std * self._sigQ_Std)

            return self._sigIDiff_Mean, self._sigIDiff_Std, self._sigQDiff_Mean, self._sigQDiff_Std
        else:
            if self._sigIZero is None:
                return None, None, None, None

            # Ensure means are available ...
            sigI, sigIStd, sigQ, sigQStd = self.get_signal_mean_iq(slice = slice)
            sigIZero, sigIZeroStd, sigQZero, sigQZeroStd = self.get_zero_mean_iq(slice = slice)

            sigIDiff_Mean = sigI - sigIZero
            sigQDiff_Mean = sigQ - sigQZero
            sigIDiff_Std = np.sqrt(sigIZeroStd * sigIZeroStd + sigIStd * sigIStd)
            sigQDiff_Std = np.sqrt(sigQZeroStd * sigQZeroStd + sigQStd * sigQStd)

            return sigIDiff_Mean, sigIDiff_Std, sigQDiff_Mean, sigQDiff_Std

    def get_diff_ampphase(self, slice = None):
        if slice is None:
            if self._sigIZero is None:
                # This has not been a diffscan ...
                return None, None

            if self._sigDiff_Amp is not None:
                return self._sigDiff_Amp, self._sigDiff_Phase

            # Make sure our means are present
            _, _, _, _ = self.get_diff_mean_iq()

            self._sigDiff_Amp = np.sqrt(self._sigIDiff_Mean * self._sigIDiff_Mean + self._sigQDiff_Mean * self._sigQDiff_Mean)
            self._sigDiff_Phase = np.arctan(self._sigQDiff_Mean / self._sigIDiff_Mean)

            return self._sigDiff_Amp, self._sigDiff_Phase
        else:
            if self._sigIZero is None:
                # This has not been a diffscan ...
                return None, None

            sigIDiff_Mean, sigIDiff_Std, sigQDiff_Mean, sigQDiff_Std = self.get_diff_mean_iq()
            

            amp = np.sqrt(sigIDiff_Mean*sigIDiff_Mean + sigQDiff_Mean*sigQDiff_Mean)
            phase = np.arctan(sigQDiff_Mean / sigIDiff_Mean)

            return amp, phase

class QUAKESRScan1D:
    @staticmethod
    def load(filename, scannedQuantity = "X", scannedQuantityTitle = "Unknown scanned parameter"):
        data = np.load(filename)
        if "scan" not in data:
            raise ValueError("Not a 2D scan")
        if len(data["scan"].shape) != 1:
            raise ValueError("Not a 2D scan")

        mainAxisData = None
        mainAxisTitle = None
        mainAxis = None

        if "f_RF" in data:
            mainAxis = "f_RF"
            mainAxisTitle = "RF frequency"
            mainAxisData = data["f_RF"]
        else:
            raise ValueError("Unsupported main axis")

        scanned_quantity = scannedQuantity
        scanned_quantity_data = data["scan"]
        scanned_quantity_title = scannedQuantityTitle

        scans = []

        for iScanParam, scanParam in enumerate(data["scan"]):
            sigIZero = None
            sigQZero = None
            if "sigIzero" in data:
                sigIZero = data["sigIzero"][iScanParam]
                sigQZero = data["sigQzero"][iScanParam]

            sigT = None
            sigTZero = None
            sigP = None
            sigPZero = None

            if "sigT" in data:
                sigT = data["sigT"][iScanParam]
            if "sigTzero" in data:
                sigTZero = data["sigTzero"][iScanParam]
            if "sigP" in data:
                sigP = data["sigP"][iScanParam]
            if "sigPzero" in data:
                sigPZero = data["sigPzero"][iScanParam]


            newscan = QUAKESRScan(mainAxisData, mainAxis, mainAxisTitle, data["sigI"][iScanParam], data["sigQ"][iScanParam], sigIZero, sigQZero, sigT, sigTZero, sigP, sigPZero, f"{filename}_scan_{scanParam}")
            scans.append(newscan)

        return QUAKESRScan1D(scanned_quantity, scanned_quantity_data, scanned_quantity_title, scans)
             

    def __init__(self, scannedQuantity, scannedQuantityData, scannedQuantityTitle, scans):
        self._scanned_quantity = scannedQuantity
        self._scanned_quantity_data = scannedQuantityData
        self._scans = scans
        self._scanned_quantity_title = scannedQuantityTitle

    def get_scans(self):
        return self._scanned_quantity, self._scanned_quantity_title, self._scanned_quantity_data, self._scans