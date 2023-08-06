import unittest
from pytimbre.waveform import Waveform, weighting_function, trimming_methods, windowing_methods, LeqDurationMode
from pytimbre.audio_files.ansi_standard_formatted_files import StandardBinaryFile
from pytimbre.spectral.time_histories import LogarithmicBandTimeHistory as band_hist
import numpy as np
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt


class TestWaveform(unittest.TestCase):
    @staticmethod
    def get_wfm(f: float = 1000):
        fs = 48000
        w = 2 * np.pi * f
        t = np.arange(0, 10, 1 / fs)

        wfm = Waveform(0.75 * np.sin(w * t), fs, 0.0)

        return wfm

    @staticmethod
    def get_wfm_2(f: float = 1000):
        f = 100
        w = 2 * np.pi * f
        fs = 48000
        t = np.arange(0, 2, 1 / fs)
        signal = np.cos(w * t)

        wfm = Waveform(signal, fs, 0.0)

        return wfm

    @staticmethod
    def std_bin_file_c130_to_wav():
        return str(Path(__file__).parents[1]) + "/Test Data/waveformdata/files/after landing_MIP Rack.bin"

    @staticmethod
    def low_pass_filtered_data():
        return str(Path(__file__).parents[1]) + "/_Test Data/waveformdata/100 hz filtered signal.csv"

    @staticmethod
    def std_bin_file_transient():
        return str(Path(__file__).parents[1]) + "/tests/Test Data/audio_files/calibrated_aversive_spkall_mic1.bin"

    @staticmethod
    def std_bin_file_transient_2():
        return str(Path(__file__).parents[1]) + "/tests/Test Data/audio_files/calibrated_aversive_combo_spkall_mic1.bin"

    def test_constructor(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(0, wfm.samples[0], delta=1e-10)
        self.assertEqual(480000, len(wfm.samples))
        self.assertEqual(10, wfm.duration)
        self.assertEqual(48000, wfm.sample_rate)
        self.assertEqual(0.0, wfm.time0)
        self.assertEqual(len(wfm.samples), len(wfm.times))
        self.assertIsNone(wfm.forward_coefficients)
        self.assertIsNone(wfm.reverse_coefficients)
        self.assertIsNotNone(wfm.signal_envelope)
        self.assertIsNotNone(wfm.normal_signal_envelope)
        self.assertEqual(12, wfm.coefficient_count)
        self.assertEqual(0.0029, wfm.hop_size_seconds)
        self.assertEqual(0.0232, wfm.window_size_seconds)
        self.assertEqual(5, wfm.cutoff_frequency)
        self.assertEqual(0.15, wfm.centroid_threshold)
        self.assertEqual(0.4, wfm.effective_duration_threshold)

    def test_trim(self):
        wfm = TestWaveform.get_wfm()

        s0 = 0
        s1 = 1000

        wfm1 = wfm.trim(s0, s1)
        self.assertEqual(1000, len(wfm1.samples))

        self.assertEqual(0, wfm1.time0)
        for i in range(len(wfm1.samples)):
            self.assertEqual(wfm.samples[i], wfm1.samples[i])

        wfm2 = wfm.trim(1, s1 + 1)
        self.assertEqual(1000, len(wfm2.samples))
        for i in range(len(wfm2.samples)):
            self.assertEqual(wfm.samples[i + 1], wfm2.samples[i])

    def test_apply_window(self):
        import scipy.signal.windows

        wfm = self.get_wfm(1000)

        wfm1 = wfm.apply_window(windowing_methods.tukey, 0.05)
        window = scipy.signal.windows.tukey(len(wfm.samples), 0.05)
        self.assertEqual(len(wfm.samples), len(wfm1.samples))
        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i] * window[i], wfm1.samples[i], delta=1e-6)

        wfm1 = wfm.apply_window(windowing_methods.tukey, 0.5)
        window = scipy.signal.windows.tukey(len(wfm.samples), 0.5)
        self.assertEqual(len(wfm.samples), len(wfm1.samples))
        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i] * window[i], wfm1.samples[i], delta=1e-6)

        wfm1 = wfm.apply_window(windowing_methods.rectangular)
        window = scipy.signal.windows.tukey(len(wfm.samples), 0.0)
        self.assertEqual(len(wfm.samples), len(wfm1.samples))
        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i] * window[i], wfm1.samples[i], delta=1e-6)

        wfm1 = wfm.apply_window(windowing_methods.hanning)
        window = scipy.signal.windows.tukey(len(wfm.samples), 1)
        self.assertEqual(len(wfm.samples), len(wfm1.samples))
        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i] * window[i], wfm1.samples[i], delta=1e-6)

        wfm1 = wfm.apply_window(windowing_methods.hamming)
        window = scipy.signal.windows.hamming(len(wfm.samples))
        self.assertEqual(len(wfm.samples), len(wfm1.samples))
        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i] * window[i], wfm1.samples[i], delta=1e-6)

    def test_apply_iir_filter(self):
        import scipy.signal

        wfm = self.get_wfm(100)

        b, a = scipy.signal.butter(4, 1000 / wfm.sample_rate / 2, btype='low', analog=False, output='ba')

        wfm1 = wfm.apply_lowpass(1000, 4)

        b = np.array([1.55517217808043e-05, 6.22068871232173e-05, 9.33103306848260e-05, 6.22068871232173e-05,
                      1.55517217808043e-05])

        a = np.array([1, -3.65806030240188, 5.03143353336761, -3.08322830175882, 0.710103898341587])

        self.assertEqual(5, len(wfm.forward_coefficients))
        for i in range(5):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i], delta=1e-10)

        self.assertEqual(5, len(wfm.reverse_coefficients))
        for i in range(5):
            self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1e-10)

        wfm2 = wfm.apply_iir_filter(b, a)

        b = np.array([1.55517217808043e-05, 6.22068871232173e-05, 9.33103306848260e-05, 6.22068871232173e-05,
                      1.55517217808043e-05])

        a = np.array([1, -3.65806030240188, 5.03143353336761, -3.08322830175882, 0.710103898341587])

        self.assertEqual(5, len(wfm.forward_coefficients))
        for i in range(5):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i], delta=1e-10)

        self.assertEqual(5, len(wfm.reverse_coefficients))
        for i in range(5):
            self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1e-10)

        self.assertEqual(len(wfm1.samples), len(wfm2.samples))

        for i in range(len(wfm1.samples)):
            self.assertAlmostEqual(wfm1.samples[i], wfm2.samples[i], delta=1e-2)

    def test_AC_Filter_design(self):
        # Check AC_design_filter design against outputs from matlab version
        fs = 2e5

        Ba_matlab = [0.032084206336563, -0.064168412667423, -0.0320842063536748, 0.128336825357664, -0.032084206325157,
                     -0.0641684126902407, 0.0320842063422688]
        Aa_matlab = [1, -5.32939721339437, 11.7682035394565, -13.7759185980543, 9.01251831975431, -3.12310892469402,
                     0.447702876935291]
        Bc_matlab = [0.0260099630889772, 4.62329257443558e-12, -0.0520199261825801, -4.62329257443599e-12,
                     0.0260099630936028]
        Ac_matlab = [1, -3.35568854501294, 4.17126593340454, -2.27533221962382, 0.459754874493225]

        # Call ac_filter_design from python at fs
        coeffA, coeffC = Waveform.AC_Filter_Design(fs)

        # Check all coeffecients across a and c filters
        for i in range(len(Aa_matlab)):
            self.assertAlmostEqual(Ba_matlab[i], coeffA[0][i], delta=1e-8)
            self.assertAlmostEqual(Aa_matlab[i], coeffA[1][i], delta=1e-8)

        for i in range(len(Ac_matlab)):
            self.assertAlmostEqual(Bc_matlab[i], coeffC[0][i], delta=1e-8)
            self.assertAlmostEqual(Ac_matlab[i], coeffC[1][i], delta=1e-8)

    def test_apply_a_weight(self):
        wfm = self.get_wfm_2()

        wfm2 = wfm.apply_a_weight()

        self.assertEqual(wfm.overall_level(weighting=weighting_function.a_weighted),
                         wfm2.overall_level())

    def test_apply_c_weight(self):
        wfm = self.get_wfm_2()

        wfm2 = wfm.apply_c_weight()

        self.assertEqual(wfm.overall_level(weighting=weighting_function.c_weighted),
                         wfm2.overall_level())

    def test_low_pass(self):
        #   Define a signal

        f = 100
        w = 2 * np.pi * f
        fs = 48000
        t = np.arange(0, 2, 1 / fs)
        signal = np.cos(w * t)

        wfm = Waveform(signal, fs, 0.0)

        wfm.apply_lowpass(1000)

        b = np.array([1.55517217808043e-05, 6.22068871232173e-05, 9.33103306848260e-05, 6.22068871232173e-05,
                      1.55517217808043e-05])

        a = np.array([1, -3.65806030240188, 5.03143353336761, -3.08322830175882, 0.710103898341587])

        self.assertEqual(5, len(wfm.forward_coefficients))
        for i in range(5):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i], delta=1e-10)

        self.assertEqual(5, len(wfm.reverse_coefficients))
        for i in range(5):
            self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1e-10)

    def test_is_calibration(self):
        wfm0 = TestWaveform.get_wfm()

        self.assertTrue(wfm0.is_calibration()[0])

        wfm0 = TestWaveform.get_wfm(250)

        self.assertTrue(wfm0.is_calibration()[0])

        wfm0 = TestWaveform.get_wfm(200)

        self.assertFalse(wfm0.is_calibration()[0])

    def test_get_features(self):
        wfm = TestWaveform.get_wfm()

        features = wfm.get_features()
        self.assertAlmostEqual(0.030208333333333, features['attack'], delta=1e-4)
        self.assertAlmostEqual(0.137937500000000, features['decrease'], delta=1e-4)
        self.assertAlmostEqual(10, features['release'], delta=1e-4)
        self.assertAlmostEqual(-1.050813362350563, features['log_attack'], delta=1e-4)
        self.assertAlmostEqual(10.284324504585928, features['attack slope'], delta=2e-1)
        self.assertAlmostEqual(-2.233475973967896e-04, features['decrease slope'], delta=1e-6)
        self.assertAlmostEqual(5.032777294219399, features['temporal centroid'], delta=1e-4)
        self.assertAlmostEqual(9.937354166666667, features['effective duration'], delta=1e-4)
        self.assertAlmostEqual(4.092080415748489e-04, features['amplitude modulation'], delta=1e-6)
        self.assertAlmostEqual(0.065570535881231, features['frequency modulation'], delta=1e-4)
        self.assertEqual(12, features['auto-correlation'].shape[1])
        self.assertEqual(3446, features['auto-correlation'].shape[0])
        self.assertAlmostEqual(0.991427742278755, features['auto-correlation'][0, 0], delta=1e-6)
        self.assertAlmostEqual(-2.94422758033417e-05, features['auto-correlation'][-1, -1], delta=3e-5)
        self.assertEqual(3446, len(features['zero crossing rate']))
        self.assertAlmostEqual(2025.13464991023, features['zero crossing rate'][0], delta=1e-6)
        self.assertAlmostEqual(1982.04667863555, features['zero crossing rate'][-1], delta=1e-6)

    # def test_rms_envelope(self):
    #     #   Open the file containing the signal and the RMS envelope

    def test_attack(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(0.030208333333333, wfm.attack, delta=1e-4)

    def test_decrease(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(0.137937500000000, wfm.decrease, delta=1e-4)

    def test_release(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(10, wfm.release, delta=1e-4)

    def test_log_attack(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(-1.050813362350563, wfm.log_attack, delta=1e-4)

    def test_attack_slope(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(10.284324504585928, wfm.attack_slope, delta=2e-1)

    def test_decrease_slope(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(-2.233475973967896e-04, wfm.decrease_slope, delta=1e-6)

    def test_temporal_centroid(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(5.032777294219399, wfm.temporal_centroid, delta=1e-4)

    def test_effective_duration(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(9.937354166666667, wfm.effective_duration, delta=1e-4)

    def test_amplitude_modulation(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(4.092080415748489e-04, wfm.amplitude_modulation, delta=1e-6)

    def test_frequency_modulation(self):
        wfm = TestWaveform.get_wfm()

        self.assertAlmostEqual(0.065570535881231, wfm.frequency_modulation, delta=1e-4)

    def test_auto_correlation(self):
        wfm = TestWaveform.get_wfm()

        self.assertEqual(12, wfm.auto_correlation.shape[1])
        self.assertEqual(3446, wfm.auto_correlation.shape[0])

        self.assertAlmostEqual(0.991427742278755, wfm.auto_correlation[0, 0], delta=1e-6)
        self.assertAlmostEqual(-2.94422758033417e-05, wfm.auto_correlation[-1, -1], delta=3e-5)

    def test_zero_crossing(self):
        wfm = TestWaveform.get_wfm()

        self.assertEqual(3446, len(wfm.zero_crossing_rate))

        self.assertAlmostEqual(2025.13464991023, wfm.zero_crossing_rate[0], delta=1e-6)
        self.assertAlmostEqual(1982.04667863555, wfm.zero_crossing_rate[-1], delta=1e-6)

    def test_if_Waveform_trim_returns_correct_duration(self):

        sample_rate = 2000
        x = np.linspace(0, 2 * np.pi, 1000)
        pressure = np.sqrt(2) * np.sin(x)
        f1 = Waveform(pressure, sample_rate, start_time=0)

        start_sample_trimmed = 0
        end_sample_trimmed = start_sample_trimmed + int(0.1 * f1.sample_rate)
        f2 = f1.trim(start_sample_trimmed, end_sample_trimmed)
        self.assertEqual(f2.duration, 0.1)

    def TestWaveform_time_setter(self):

        sample_rate = 2000
        x = np.linspace(0, 2 * np.pi, 1000)
        pressure = np.sqrt(2) * np.sin(x)

        f1 = Waveform(pressure, sample_rate, start_time=0)
        self.assertEqual(0.0, f1.times[0])
        self.assertEqual(0.0, f1.time0)
        self.assertEqual(0.0, f1.start_time)

        f1.start_time = 1
        self.assertEqual(1.0, f1.times[0])
        self.assertEqual(1.0, f1.time0)
        self.assertEqual(1.0, f1.start_time)

    def test_filtering_coefficients(self):
        #   Define a signal

        wfm = self.get_wfm(100)

        wfm.apply_lowpass(1000)

        b = np.array([1.55517217808043e-05, 6.22068871232173e-05, 9.33103306848260e-05, 6.22068871232173e-05,
                      1.55517217808043e-05])

        a = np.array([1, -3.65806030240188, 5.03143353336761, -3.08322830175882, 0.710103898341587])

        self.assertEqual(5, len(wfm.forward_coefficients))
        for i in range(5):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i], delta=1e-10)

        self.assertEqual(5, len(wfm.reverse_coefficients))
        for i in range(5):
            self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1e-10)

    def test_apply_bandpass(self):
        wfm = Waveform.generate_tone(250, amplitude_db=94)

        wfm.apply_bandpass(800, 1000, 4)

        # b = np.array([0.99999714952586,-3.99998859810344,5.99998289715516,-3.9998859810344,0.9999971495286])
        # a = np.array([1, -3.91448750483634, 5.74709974634780, -3.75064701042629, 0.918035868172305])

        # coefficient_scale = wfm.forward_coefficients[0] / b[0]

        self.assertEqual(9, len(wfm.forward_coefficients))
        # for i in range(5):
        #     self.assertAlmostEqual(b[i], wfm.forward_coefficients[i] / coefficient_scale, delta=1e-10)
        #     if i > 0:
        #         self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1)

    def test_trim2(self):
        """
        There was an issue with the generation of the subset of the waveform for the determination of the time history.
        The tests pass when the waveform is taken as a whole, but not using these subsets. So this tests the trimming
        to ensure that the subset is correctly determined.
        """

        wfm = Waveform.generate_tone(duration=10)

        integration_time = 0.1

        N = int(np.floor(wfm.duration / integration_time))

        s0 = 0

        for i in range(N):
            subset = wfm.trim(s0, s0 + int(np.floor(integration_time * wfm.sample_rate)), trimming_methods.samples)

            for j in range(s0, s0 + len(subset.samples)):
                self.assertAlmostEqual(subset.samples[j - s0], wfm.samples[j], places=5)

            s0 += len(subset.samples)

    def test_high_pass(self):
        #   Define a signal
        wfm = Waveform.generate_tone(250, amplitude_db=94)

        wfm.apply_highpass(1000)

        b = np.array([0.958141883111421, -3.83256753244568, 5.74885129866853, -3.83256753244568, 0.958141883111421])
        a = np.array([1, -3.91448750483634, 5.74709974634780, -3.75064701042629, 0.918035868172305])

        coefficient_scale = wfm.forward_coefficients[0] / b[0]

        self.assertEqual(5, len(wfm.forward_coefficients))
        for i in range(5):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i] / coefficient_scale, delta=1e-10)
            if i > 0:
                self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1)

    def test_resample(self):
        wfm = self.get_wfm(250)

        wfm_down = wfm.resample(44100)

        self.assertEqual(441000, len(wfm_down.samples))

        wfm_up = wfm.resample(96000)

        self.assertEqual(960000, len(wfm_up.samples))

    # def test_add_operator(self):
    #     self.assertTrue(False, "Not Implemented")
    #
    # def test_sound_quality_metrics(self):
    #     self.assertTrue(False, "Not implemented")
    #
    # def test_apply_tob_equalizer(self):
    #     self.assertTrue(False, "Not Implemented")

    def test_bandpass(self):
        wfm = self.get_wfm(1000)
        wfm.apply_bandpass(800, 1100)

        b = [7.28117247216156e-06, 0, -2.18435174164847e-05, 0, 2.18435174164847e-05, 0, -7.28117247216156e-06]
        a = [1, -5.87687197128807, 14.4349893473931, -18.9674687942193, 14.0619417177387, -5.57704759766939,
             0.924460583186420]

        self.assertEqual(len(b), len(wfm.forward_coefficients))
        for i in range(len(b)):
            self.assertAlmostEqual(b[i], wfm.forward_coefficients[i], delta=1e-6)

        self.assertEqual(len(a), len(wfm.forward_coefficients))
        for i in range(len(a)):
            self.assertAlmostEqual(a[i], wfm.reverse_coefficients[i], delta=1e-6)

    def test_apply_calibration(self):
        #   Test that the function returns a value error when the detected frequency is not what was specified
        calibration = Waveform.generate_tone(250, amplitude_db=75)
        test_wfm = Waveform.generate_noise()
        self.assertRaises(ValueError, test_wfm.apply_calibration, calibration, 114, 1000, False)

        calibration = Waveform.generate_tone(1000, amplitude_db=75)

        calibrated_wfm = test_wfm.apply_calibration(calibration, 114, 1000)
        self.assertAlmostEqual(test_wfm.overall_level()[0] + (114 - 75), calibrated_wfm.overall_level()[0], places=1)

    def test_gps_audio_signal_converter(self):
        filename = str(Path(__file__).parents[0]) + "/Test Data/audio_files/d31s2dr0520180625_0.wav"

        start_time = Waveform.gps_audio_signal_converter(filename)

        # 205057
        self.assertEqual(2018, start_time.year)
        self.assertEqual(6, start_time.month)
        self.assertEqual(25, start_time.day)
        self.assertEqual(20, start_time.hour)
        self.assertEqual(50, start_time.minute)
        self.assertEqual(56, start_time.second)

    def test_correlation(self):
        wfm = Waveform.generate_tone(1000)

        self.assertEqual(wfm.cross_correlation(wfm)[1], 0)

    def test_is_clipped(self):
        from scipy.stats import norm
        import matplotlib.pyplot as plt

        #   Build the signal that is not clipped...a white noise signal
        non_clipped = Waveform.generate_noise()

        #   Clip the samples
        clipped = Waveform(np.clip(non_clipped.samples, -0.5, 0.5), sample_rate=non_clipped.sample_rate, start_time=0)

        self.assertFalse(non_clipped.is_clipped)
        self.assertTrue(clipped.is_clipped)

    def test_noise_generation(self):
        import matplotlib.pyplot as plt

        wfm = Waveform.generate_noise()

        self.assertAlmostEqual(94, wfm.overall_level()[0], delta=1.5)
        # fig, ax = plt.subplots()
        # ax.plot(wfm.times, wfm.samples)
        #
        # plt.show()

    def test_concatenate(self):
        wfm1 = Waveform.generate_tone()
        wfm2 = Waveform.generate_tone()

        wfm3 = wfm1.concatenate(wfm2)

        self.assertEqual(2, wfm3.duration)

    def test_if_equivalent_level_returns_correct_magnitudes(self):

        waveform_duration = 2.0
        waveform_amplitude_db = 85.0
        wfm = Waveform.generate_noise(duration=waveform_duration, amplitude_db=waveform_amplitude_db)

        leq_trans_a = wfm.equivalent_level(
            weighting_function.unweighted,
            leq_mode=LeqDurationMode.transient,
            equivalent_duration=waveform_duration
        )
        self.assertAlmostEqual(waveform_amplitude_db, leq_trans_a, delta=0.2)

        leq_trans_b = wfm.equivalent_level(
            weighting_function.unweighted,
            leq_mode=LeqDurationMode.transient,
            equivalent_duration=waveform_duration * 2
        )
        self.assertAlmostEqual(waveform_amplitude_db - 3, leq_trans_b, delta=0.2)

        leq_cont_8hr = wfm.equivalent_level(
            weighting_function.unweighted,
            leq_mode=LeqDurationMode.continuous,
            equivalent_duration=8 * 3600,
            exposure_duration=8 * 3600
        )
        self.assertAlmostEqual(waveform_amplitude_db, leq_cont_8hr, delta=0.2)

        leq_cont_4hr = wfm.equivalent_level(
            weighting_function.unweighted,
            leq_mode=LeqDurationMode.continuous,
            equivalent_duration=8 * 3600,
            exposure_duration=4 * 3600
        )
        self.assertAlmostEqual(waveform_amplitude_db - 3, leq_cont_4hr, delta=0.2)

        waveform_duration = 1.0
        waveform_amplitude_db = 85.0
        wfm = Waveform.generate_noise(duration=waveform_duration, amplitude_db=waveform_amplitude_db)

        leq_trans_avg = wfm.equivalent_level(
            weighting_function.unweighted,
            leq_mode=LeqDurationMode.continuous
        )
        self.assertAlmostEqual(waveform_amplitude_db + 10 * np.log10(waveform_duration / 8 / 3600), leq_trans_avg,
                               delta=0.2)

    def test_transient_attack(self):
        wfm = StandardBinaryFile(TestWaveform.std_bin_file_transient())
        feat_df = pd.DataFrame()
        t_hist = band_hist(a=wfm, fob_band_width=3, integration_time=0.25, f0=10, f1=10000)
        try:
            for spectrum in t_hist.spectra:
                print(spectrum.waveform.start_time)
                feat_df = feat_df.append(spectrum.get_average_features(include_sq_metrics=True), ignore_index=True)
            self.assertTrue(True, msg='Calculated all metrics for the given waveform. Test passed!')
        except:
            self.assertFalse(True, msg='Failed to calculate features for given spectral time history.')

    def test_transient_attack_2(self):
        wfm = StandardBinaryFile(TestWaveform.std_bin_file_transient_2())
        wfm = wfm.trim(20.5, 21, trimming_methods.times)
        feat_df = pd.DataFrame()
        t_hist = band_hist(a=wfm, fob_band_width=3, integration_time=0.25, f0=10, f1=10000)
        try:
            for spectrum in t_hist.spectra:
                print(spectrum.waveform.start_time)
                feat_df = feat_df.append(spectrum.get_average_features(include_sq_metrics=True), ignore_index=True)
            self.assertTrue(True, msg='Calculated all metrics for the given waveform. Test passed!')
        except:
            self.assertFalse(True, msg='Failed to calculate features for given spectral time history.')
