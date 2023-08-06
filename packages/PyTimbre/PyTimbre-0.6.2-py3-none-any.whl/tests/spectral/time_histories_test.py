import unittest
import numpy as np
import os
from pathlib import Path
from pytimbre.waveform import Waveform, weighting_function
from pytimbre.audio_files.wavefile import WaveFile
from pytimbre.audio_files.ansi_standard_formatted_files import StandardBinaryFile
from pytimbre.spectral.time_histories import NarrowbandTimeHistory, LogarithmicBandTimeHistory, TimeHistory


class test_Timehistory(unittest.TestCase):
    @staticmethod
    def time_history_example():
        from pathlib import Path

        return str(Path(__file__).parents[1]) + "/Test Data/spectral/SITE01_RUN104.tob.csv"

    @staticmethod
    def std_bin_example():
        from pathlib import Path

        return str(Path(__file__).parents[1]) + "/Test " \
                                                "Data/audio_files/files/standard_bin_file_write/" \
                                                "test_standard_bin_file.bin"

    def test_load(self):
        th = TimeHistory.load(test_Timehistory.time_history_example())

        self.assertEqual(29, len(th._header))
        self.assertEqual(47, len(th.spectra))

        for i in range(47):
            self.assertIsNotNone(th.spectra[i])

    def test_if_save_replaces_unwanted_strings_in_header(self):
        th = TimeHistory.load(test_Timehistory.time_history_example())
        th._header = {'X,M' if k == 'X' else k: v for k, v in th._header.items()}
        th.save('temp_timehist_fortest.spl.csv')

        th_test = TimeHistory.load('temp_timehist_fortest.spl.csv')
        self.assertIsNotNone(th_test._header['X_M'])
        os.remove('temp_timehist_fortest.spl.csv')

    def test_spectrogram_array_decibels(self):
        th = TimeHistory.load(test_Timehistory.time_history_example())

        self.assertEqual(np.shape(th.spectrogram_array_decibels), (len(th.times), len(th.frequencies)))


class test_Narrowband_TimeHistory(unittest.TestCase):
    @staticmethod
    def test_bin_write():
        return str(Path(__file__).parents[1]) + "/Test Data/audio_files/files/standard_bin_file_write" \
                                                "/test_standard_bin_file.bin "

    @staticmethod
    def out_TOB_example():
        from pathlib import Path

        return str(Path(__file__).parents[1]) + "/Test Data/spectral/nb_to_fob.csv"

    def make_waveform(self, f: float = 1000, fs: float = 48000):
        sample_rate = fs
        max_frequency = f
        self.amplitude_dB = 94
        amplitude_rms = 10 ** (self.amplitude_dB / 20) * 2e-5
        x = np.arange(0, 2, 1 / sample_rate)
        y = amplitude_rms * np.sqrt(2) * np.sin(2 * np.pi * max_frequency * x)

        return Waveform(y, sample_rate=sample_rate, start_time=0.0)

    def test_constructor(self):
        wfm = self.make_waveform()
        th = NarrowbandTimeHistory(wfm)

        self.assertIsNotNone(th.waveform)
        self.assertEqual(8192, th.fft_size)
        self.assertEqual(0.25 * 48000, th.sample_size)
        self.assertIsNotNone(th.integration_time)
        self.assertEqual(0.25, th.integration_time)
        self.assertIsNone(th._spectra)
        self.assertIsNone(th._times)
        self.assertEqual(wfm.sample_rate, th.sample_rate)
        self.assertEqual(2, th.duration)

        t = np.arange(0, 2, 0.25)
        for i in range(len(t)):
            self.assertEqual(t[i], th.times[i])

    def test_overall_levels(self):
        wfm = self.make_waveform()
        th = NarrowbandTimeHistory(wfm)
        self.assertEqual(2 / 0.25, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(0.25)[i], th.spectra[i].overall_level, delta=1e0)
            self.assertAlmostEqual(wfm.overall_level(0.25, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

    def test_to_fob_spectra(self):
        wfm = self.make_waveform()
        nb_th = NarrowbandTimeHistory(wfm)
        self.assertEqual(2 / 0.25, len(nb_th.spectra))

        fob_th = nb_th.to_logarithmic_band_time_history()

        for i in range(len(fob_th.spectra)):
            self.assertEqual(31, len(fob_th.spectra[i].frequencies))
            self.assertAlmostEqual(wfm.overall_level(0.25)[i], fob_th.spectra[i].overall_level, delta=1e0)
            self.assertAlmostEqual(wfm.overall_level(0.25, weighting=weighting_function.a_weighted)[i],
                                   fob_th.spectra[i].overall_a_weighted_level, delta=1e0)

    def test_nb_from_standard_bin_file(self):
        wfm = StandardBinaryFile(self.test_bin_write())
        nb_th = NarrowbandTimeHistory(wfm, integration_time=1.0)
        self.assertEqual(nb_th.sample_rate, wfm.sample_rate)
        # self.assertEqual(nb_th.header, wfm.header)
        self.assertEqual(nb_th.times[0], wfm.start_time)
        self.assertAlmostEqual(nb_th.duration, wfm.duration, delta=1.0)

    def test_to_logarithmic_band_time_history_save_load(self):
        wfm = StandardBinaryFile(test_Timehistory.std_bin_example())
        self.assertIsNotNone(wfm._header)
        nb_th = NarrowbandTimeHistory(wfm, integration_time=1.0)
        self.assertIsNotNone(nb_th.header)
        tob_th = nb_th.to_logarithmic_band_time_history()
        self.assertIsNotNone(tob_th._header)
        tob_th.save(self.out_TOB_example())

        tob_th_test = TimeHistory.load(self.out_TOB_example())
        self.assertNotEqual(0, len(tob_th_test._header))
        self.assertEqual(int(tob_th_test._header['HEADER SIZE']), len(wfm._header) + 1)
        self.assertAlmostEqual(tob_th_test.duration, wfm.duration, delta=1.0)
        os.remove(self.out_TOB_example())


class test_FilterFOB_TimeHistory(unittest.TestCase):
    @staticmethod
    def pink_noise_file():
        from pathlib import Path

        return str(Path(__file__).parents[1]) + '/test Data/audio_files/Files/canonical wave file/pink_44100Hz_32bit.wav'

    def make_waveform(self, f: float = 1000, fs: float = 48000):
        sample_rate = fs
        max_frequency = f
        self.amplitude_dB = 94
        amplitude_rms = 10 ** (self.amplitude_dB / 20) * 2e-5
        x = np.arange(0, 2, 1 / sample_rate)
        y = amplitude_rms * np.sqrt(2) * np.sin(2 * np.pi * max_frequency * x)

        return Waveform(y, sample_rate=sample_rate, start_time=0.0)

    def test_constructor(self):
        wfm = self.make_waveform()
        th = LogarithmicBandTimeHistory(wfm)

        self.assertIsNotNone(th.waveform)
        self.assertEqual(0.25 * 48000, th.sample_size)
        self.assertIsNotNone(th.integration_time)
        self.assertEqual(0.25, th.integration_time)
        self.assertEqual(3, th.bandwidth)
        self.assertEqual(10, th.start_frequency)
        self.assertEqual(10000, th.stop_frequency)
        self.assertIsNone(th._spectra)
        self.assertIsNone(th._times)
        self.assertEqual(wfm.sample_rate, th.sample_rate)
        self.assertEqual(2, th.duration)

        t = np.arange(0, 2, 0.25)
        for i in range(len(t)):
            self.assertEqual(t[i], th.times[i])

    def test_overall_levels(self):

        #   process the waveform as a tone

        wfm = self.make_waveform()
        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=1)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=1e-1)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=3)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=1e-1)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=6)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=3e-1)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=12)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=3e-1)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=24)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=3e-1)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1.5e0)

        #   Now process the noise waveform
        wfm = WaveFile(test_FilterFOB_TimeHistory.pink_noise_file())
        wfm = wfm.trim(0, 2 * wfm.sample_rate)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=1)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=1.5e0)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=1e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=3)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=2.0e0)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=2.0e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=6)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=2.5)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=2.5e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=12)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=2.5)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=2.5e0)

        th = LogarithmicBandTimeHistory(wfm, integration_time=1, fob_band_width=24)
        self.assertEqual(2, len(th.spectra))

        for i in range(len(th.spectra)):
            self.assertAlmostEqual(wfm.overall_level(1)[i], th.spectra[i].overall_level, delta=2.5)
            self.assertAlmostEqual(wfm.overall_level(1, weighting=weighting_function.a_weighted)[i],
                                   th.spectra[i].overall_a_weighted_level, delta=2.5e0)

    def test_get_features(self):
        wfm = self.make_waveform()

        th = LogarithmicBandTimeHistory(wfm)

        dataset = th.get_features

        self.assertEqual(th.duration / th.integration_time, dataset.shape[0])
