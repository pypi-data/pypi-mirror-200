import datetime
import unittest
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from pytimbre.spectral.spectra import Spectrum, SpectrumByFFT, SpectrumByDigitalFilters
import numpy as np
from pytimbre.audio_files.wavefile import WaveFile, Waveform
from pytimbre.waveform import weighting_function
from pytimbre.spectral.acoustic_weights import AcousticWeights
from pathlib import Path


class TestSpectrum(unittest.TestCase):
    def make_waveform(self):
        sample_rate = 1000
        max_frequency = 100
        self.amplitude_dB = 94
        amplitude_rms = 10 ** (self.amplitude_dB / 20) * 2e-5
        x = np.arange(0, 1, 1 / sample_rate)
        y = amplitude_rms * np.sqrt(2) * np.sin(2 * np.pi * max_frequency * x)

        return Waveform(y, sample_rate, 0)

    def test_spectrum_maker(self):
        f = np.arange(0, 1000)
        p = np.zeros(len(f))
        p[f == 125] = 10

        spec = Spectrum()
        spec.frequencies = f
        spec.pressures_pascals = p
        self.assertIsInstance(spec, Spectrum)
        self.assertIsNotNone(spec.frequencies)
        self.assertIsNotNone(spec.pressures_pascals)

        self.assertAlmostEqual(np.max(spec.pressures_decibels), 114, delta=1e-1)
        self.assertAlmostEqual(np.max(spec.pressures_pascals), 10, delta=1e-1)
        self.assertAlmostEqual(spec.overall_level, 114, delta=1e-1)
        self.assertAlmostEqual(spec.overall_a_weighted_level, 114 - 16.1, delta=2e-1)

    def test_calculate_engineering_unit_scale_factor(self):

        daq_system_gain_V_per_Pa = 1 / 5.0
        calibration_frequency = 250
        calibration_pressure_Pa_rms = 10.0
        calibration_level = 20 * np.log10(calibration_pressure_Pa_rms / 20e-6)

        signal_values_V_rms = calibration_pressure_Pa_rms * daq_system_gain_V_per_Pa
        f = np.array([125, 250, 500])
        p = np.zeros(len(f))
        p[f == calibration_frequency] = signal_values_V_rms

        spec = Spectrum()
        spec.frequencies = f
        spec.pressures_pascals = p
        spec.fractional_octave_bandwidth = 1

        sens_V_per_Pa = spec.calculate_engineering_unit_scale_factor(calibration_level=calibration_level,
                                                                     calibration_frequency=calibration_frequency)
        self.assertAlmostEqual(daq_system_gain_V_per_Pa, sens_V_per_Pa, delta=1e-8)

    def test_time(self):
        t0 = datetime.datetime.now()
        wfm = self.make_waveform()
        wfm.start_time = t0
        spec = Spectrum(wfm)

        self.assertEqual(t0, spec.time)

    def test_time_past_midnight(self):
        t0 = datetime.datetime.now()
        wfm = self.make_waveform()
        wfm.start_time = t0
        spec = Spectrum(wfm)

        tpm = 60 * (60 * t0.hour + t0.minute) + t0.second + t0.microsecond / 1e6
        self.assertEqual(tpm, spec.time_past_midnight)


class Test_SpectrumByFFT(unittest.TestCase):
    @staticmethod
    def pink():
        return str(
            Path(__file__).parents[1]) + '/test Data/audio_files/Files/canonical wave file/pink_44100Hz_32bit.wav'

    @staticmethod
    def pink_noise_waveform():
        wav = WaveFile(Test_SpectrumByFFT.pink())

        return Waveform(pressures=wav.samples,
                        sample_rate=wav.sample_rate,
                        start_time=wav.start_time)

    def test_calculate_spectrum(self):
        freq = 125
        amp_db = 114
        amplitude_rms = 10 ** (amp_db / 20) * 20e-6
        waveform = Waveform.generate_tone(frequency=freq, amplitude_db=amp_db)

        spectrum = SpectrumByFFT(waveform, fft_size=len(waveform.samples))
        spectrum._calculate_spectrum()

        # test _acoustic_pressures_pascals via amplitude of tone
        self.assertAlmostEqual(np.max(spectrum.pressures_pascals), amplitude_rms, delta=2)

        # test _frequencies via identification of tone frequency
        max_f = spectrum._frequencies_nb[abs(spectrum._frequencies_nb - freq) ==
                                         np.min(np.abs(spectrum._frequencies_nb - freq))]
        self.assertAlmostEqual(max_f, freq, delta=1e-5)
        max_f = spectrum._frequencies[abs(spectrum._frequencies - freq) == np.min(np.abs(spectrum._frequencies - freq))]
        self.assertAlmostEqual(max_f, freq, delta=1e-5)

    def test_frequencies(self):
        waveform = Waveform.generate_tone()

        spectrum = SpectrumByFFT(waveform, fft_size=100)
        df = spectrum.frequencies[1] - spectrum.frequencies[0]

        self.assertEqual(len(spectrum.frequencies), 50)
        self.assertEqual(spectrum.frequencies[-1], (spectrum.sample_rate / 2) - df)

    def test_frequencies_double_sided(self):
        waveform = Waveform.generate_tone()

        spectrum = SpectrumByFFT(waveform, fft_size=100)
        df = spectrum.frequencies[1] - spectrum.frequencies[0]

        self.assertEqual(len(spectrum.frequencies_double_sided), 100)
        self.assertEqual(spectrum.frequencies_double_sided[-1], spectrum.sample_rate - df)

        self.assertEqual(len(spectrum._frequencies_double_sided), 100)
        self.assertEqual(spectrum._frequencies_double_sided[-1], spectrum.sample_rate - df)

    def test_fft_size(self):
        waveform = Waveform.generate_tone()

        spectrum = SpectrumByFFT(waveform, fft_size=100)
        self.assertEqual(spectrum.fft_size, 100)

        spectrum = SpectrumByFFT(waveform)
        self.assertEqual(spectrum.fft_size, 2 ** 15)

        self.assertRaises(ValueError, SpectrumByFFT, waveform, fft_size=len(waveform.samples) + 1)

    def test_if_pressures_array_has_correct_number_of_blocks(self):
        waveform = Waveform.generate_tone()

        spectrum = SpectrumByFFT(waveform, fft_size=100)
        self.assertListEqual(list(np.shape(spectrum.pressures_complex_double_sided)), [959, 100])

        self.assertEqual(1, len(spectrum.pressures_pascals.shape))
        self.assertEqual(50, len(spectrum.pressures_pascals))

    def test_frequency_increment(self):
        waveform = Waveform.generate_tone()

        spectrum = SpectrumByFFT(waveform, fft_size=100)

        self.assertEqual(waveform.sample_rate / spectrum.fft_size, spectrum.frequency_increment)

    def test_power_spectrum_max_level_tone(self):
        max_frequency = 1250
        max_level = 114
        waveform = Waveform.generate_tone(frequency=max_frequency, amplitude_db=max_level)
        spectrum = SpectrumByFFT(waveform)

        test_max_level = np.max(spectrum.pressures_decibels)
        self.assertAlmostEqual(max_level, test_max_level, delta=3)

        test_max_frequency = spectrum.frequencies[spectrum.pressures_decibels == test_max_level]
        self.assertAlmostEqual(max_frequency, test_max_frequency, delta=1)

    def test_overall_level(self):
        waveform = Waveform.generate_tone(amplitude_db=114)

        spectrum = SpectrumByFFT(waveform)
        self.assertAlmostEqual(spectrum.overall_level, waveform.overall_level(), delta=0.2)
        self.assertAlmostEqual(waveform.overall_level(weighting=weighting_function.a_weighted),
                               spectrum.overall_a_weighted_level,
                               delta=0.5)

        waveform = Test_SpectrumByFFT.pink_noise_waveform()

        spectrum = SpectrumByFFT(waveform)
        self.assertAlmostEqual(spectrum.overall_level, waveform.overall_level(), delta=0.2)
        self.assertAlmostEqual(waveform.overall_level(weighting=weighting_function.a_weighted),
                               spectrum.overall_a_weighted_level,
                               delta=0.5)

    def test_power_spectral_density_overall_level(self):
        waveform = Test_SpectrumByFFT.pink_noise_waveform()

        spec = SpectrumByFFT(waveform)
        df = spec.frequencies[1] - spec.frequencies[0]

        psd_pa = spec.power_spectral_density
        lf = 10 * np.log10(df * np.sum(psd_pa ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(waveform.overall_level(), lf, delta=3e-1)

        waveform = Waveform.generate_tone(amplitude_db=114)

        spec = SpectrumByFFT(waveform)
        df = spec.frequencies[1] - spec.frequencies[0]

        psd_pa = spec.power_spectral_density
        lf = 10 * np.log10(df * np.sum(psd_pa ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(waveform.overall_level(), lf, delta=3e-1)

    def test_spectrum_maker(self):
        amp_pa = 10
        f_step = 2
        f = np.arange(0, 1000, step=f_step)
        p = np.zeros(len(f))
        p[f == 126] = amp_pa

        spec = SpectrumByFFT()
        spec.frequencies = f
        spec.pressures_pascals = p
        self.assertIsInstance(spec, Spectrum)
        self.assertIsNotNone(spec.frequencies)
        self.assertIsNotNone(spec.pressures_pascals)

        self.assertAlmostEqual(np.max(spec.pressures_decibels), 114, delta=1e-1)
        self.assertAlmostEqual(spec.overall_level, 114, delta=1e-1)
        self.assertEqual(spec.frequency_increment, f_step)
        self.assertAlmostEqual(np.max(spec.power_spectral_density), amp_pa / np.sqrt(2), delta=0.01)

    def test_pink_noise_for_flatness(self):

        # generate pink noise spectrum
        step_f = 0.05
        f_nb = np.arange(0, 1000, step=step_f)
        p = 1 / np.sqrt(f_nb)
        p[0] = 1000

        # verify that power spectral density rolls off with 10 dB per decade of frequency
        psd = 10 * np.log10((1 / step_f) * p ** 2)
        for f_check in [1, 2, 10, 20, 100, 200]:
            self.assertAlmostEqual(psd[f_nb == f_check], psd[f_nb == f_check / 10] - 10, delta=1e-6)

        s = Spectrum()
        s.frequencies = f_nb
        s.pressures_pascals = p

        f_fob, p_fob = SpectrumByFFT.convert_nb_to_fob(s.frequencies, s.pressures_pascals, fob_band_width=1, f0=16,
                                                       f1=500)
        for i in range(1, len(f_fob)):
            self.assertAlmostEqual(p_fob[i], p_fob[i - 1], delta=0.01)

        s_fob = SpectrumByFFT.convert_nb_to_fob(s.frequencies, s.pressures_pascals, fob_band_width=3, f0=16, f1=500)
        for i in range(1, len(f_fob)):
            self.assertAlmostEqual(p_fob[i], p_fob[i - 1], delta=0.01)

        s_fob = SpectrumByFFT.convert_nb_to_fob(s.frequencies, s.pressures_pascals, fob_band_width=6, f0=16, f1=500)
        for i in range(1, len(f_fob)):
            self.assertAlmostEqual(p_fob[i], p_fob[i - 1], delta=0.01)

        s_fob = SpectrumByFFT.convert_nb_to_fob(s.frequencies, s.pressures_pascals, fob_band_width=12, f0=16, f1=500)
        for i in range(1, len(f_fob)):
            self.assertAlmostEqual(p_fob[i], p_fob[i - 1], delta=0.01)

        s_fob = SpectrumByFFT.convert_nb_to_fob(s.frequencies, s.pressures_pascals, fob_band_width=24, f0=16, f1=500)
        for i in range(1, len(f_fob)):
            self.assertAlmostEqual(p_fob[i], p_fob[i - 1], delta=0.01)

    def test_overall_level_with_tone(self):

        # generate tonal spectrum
        amp_db = 114
        f_nb = np.arange(0, 1000, step=0.1)
        p = np.zeros(len(f_nb))
        p[f_nb == 125] = 10 ** (amp_db / 20) * 2e-5

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=1, f0=16, f1=500)
        lf = 10 * np.log10(sum(fob ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(lf, amp_db, delta=0.1)

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=3, f0=16, f1=500)
        lf = 10 * np.log10(sum(fob ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(lf, amp_db, delta=0.1)

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=6, f0=16, f1=500)
        lf = 10 * np.log10(sum(fob ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(lf, amp_db, delta=0.2)

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=12, f0=16, f1=500)
        lf = 10 * np.log10(sum(fob ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(lf, amp_db, delta=0.2)

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=24, f0=16, f1=500)
        lf = 10 * np.log10(sum(fob ** 2) / 20e-6 / 20e-6)
        self.assertAlmostEqual(lf, amp_db, delta=0.2)

    def test_frequency_bin_with_tone(self):

        # generate tonal spectrum
        f_nb = np.arange(0, 1000, step=0.1)
        p = np.zeros(len(f_nb))
        p[f_nb == 125] = 1

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=1, f0=16, f1=500)
        self.assertEqual(fob[np.abs(f - 125) == np.min(np.abs(f - 125))], np.max(fob))

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=3, f0=16, f1=500)
        self.assertEqual(fob[np.abs(f - 125) == np.min(np.abs(f - 125))], np.max(fob))

        # generate tonal spectrum
        f_nb = np.arange(0, 1000, step=0.1)
        p = np.zeros(len(f_nb))
        p[f_nb == 153] = 1

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=6, f0=16, f1=500)
        self.assertEqual(fob[np.abs(f - 153) == np.min(np.abs(f - 153))], np.max(fob))

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=12, f0=16, f1=500)
        self.assertEqual(fob[np.abs(f - 153) == np.min(np.abs(f - 153))], np.max(fob))

        f, fob = SpectrumByFFT.convert_nb_to_fob(f_nb, p, fob_band_width=24, f0=16, f1=500)
        self.assertEqual(fob[np.abs(f - 153) == np.min(np.abs(f - 153))], np.max(fob))

    def test_calculate_engineering_unit_scale_factor(self):
        daq_system_gain_V_per_Pa = 1 / 5.0
        calibration_frequency = 250
        calibration_pressure_Pa_rms = 10.0
        calibration_level = 20 * np.log10(calibration_pressure_Pa_rms / 20e-6)
        signal_values_V_rms = calibration_pressure_Pa_rms * daq_system_gain_V_per_Pa
        signal_level = 20 * np.log10(signal_values_V_rms / 20e-6)
        signal = Waveform.generate_tone(frequency=calibration_frequency, amplitude_db=signal_level)
        spec = SpectrumByFFT(signal)

        with pytest.raises(ValueError):
            spec.calculate_engineering_unit_scale_factor(calibration_level=calibration_level,
                                                         calibration_frequency=calibration_frequency)

        spec_ob = spec.to_fractional_octave_band(bandwidth=1)
        sens_V_per_Pa = spec_ob.calculate_engineering_unit_scale_factor(calibration_level=calibration_level,
                                                         calibration_frequency=calibration_frequency)
        self.assertAlmostEqual(daq_system_gain_V_per_Pa, sens_V_per_Pa, delta=1e-8)


class Test_SpectrumByDigitalFilters(unittest.TestCase):
    @staticmethod
    def pink_noise_file():
        from pathlib import Path

        return str(
            Path(__file__).parents[1]) + '/test Data/audio_files/Files/canonical wave file/pink_44100Hz_32bit.wav'

    def test_constructor(self):
        bank = SpectrumByDigitalFilters(WaveFile(Test_SpectrumByDigitalFilters.pink_noise_file()))

    def test_settle_time(self):
        bank = SpectrumByDigitalFilters(WaveFile(Test_SpectrumByDigitalFilters.pink_noise_file()))

        self.assertTrue(bank.settle_samples < 25000)
        self.assertTrue(bank.settle_time > 0.25)

    def test_calculate_spectrum(self):
        wfm = WaveFile(Test_SpectrumByDigitalFilters.pink_noise_file(), s0=0, s1=44100)

        bank = SpectrumByDigitalFilters(wfm)

        self.assertEqual(31, len(bank.frequencies))
        self.assertAlmostEqual(np.round(bank.waveform.overall_level()), np.round(bank.overall_level), delta=1.0)

        wfm = WaveFile(Test_SpectrumByDigitalFilters.pink_noise_file(), s0=0, s1=(int(np.floor(44100 / 4))))
        bank = SpectrumByDigitalFilters(wfm)

        self.assertEqual(30, len(bank.frequencies))
        self.assertAlmostEqual(12.5, bank.frequencies[0], delta=1)
        self.assertAlmostEqual(np.round(bank.waveform.overall_level()), np.round(bank.overall_level), delta=3.0)

        bank = SpectrumByDigitalFilters(Waveform.generate_tone(duration=1))

        self.assertEqual(31, len(bank.frequencies))
        self.assertAlmostEqual(np.round(bank.waveform.overall_level()), np.round(bank.overall_level), delta=1.0)

    def test_calculate_tob_spectrum_compare_LabVIEW(self):
        """
        There appears to be limitations of the digital filter method for calculating the sound pressure level from
        waveforms. So a 25-second pink noise file was inserted into the test data and passed through the LabVIEW
        20.0.1.1f1 version using the Sound and Vibration Toolkit's 1/3 octave calculation. This will compare the
        analysis here in Python to the output of LabVIEW.
        """
        
        return
        #   Read the waveform
        wfm = WaveFile(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink.wav')

        #   Read the results
        spectral_data = pd.read_csv(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink_tob.csv',
                                    index_col=False, header=None, names=['frequency', 'level'])

        #   Pass this waveform through the Digital Filter Spectral Generation.
        spectrum = SpectrumByDigitalFilters(wfm)

        #   Process the spectra comparison
        self.assertEqual(spectral_data.shape[0], len(spectrum.frequencies))

        #   Since the LabVIEW frequencies are the accepted frequencies, we cannot do more than compare the number. We
        #   can, however, compare the sound pressure levels
        difference = np.max(abs(np.asarray(spectral_data.iloc[:, 1]) - spectrum.pressures_decibels))
        self.assertTrue(difference <= 1.0e0)

        # #   Now process the chirp waveform
        # wfm = WaveFile(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_chirp.wav')
        #
        # #   Read the results
        # spectral_data = pd.read_csv(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_chirp_tob.csv',
        #                             index_col=False, header=None, names=['frequency', 'level'])
        #
        # #   Pass this waveform through the Digital Filter Spectral Generation.
        # spectrum = SpectrumByDigitalFilters(wfm)
        #
        # #   Process the spectra comparison
        # self.assertEqual(spectral_data.shape[0], len(spectrum.frequencies))
        #
        # #   Since the LabVIEW frequencies are the accepted frequencies, we cannot do more than compare the number. We
        # #   can, however, compare the sound pressure levels
        # for i in range(len(spectrum.frequencies)):
        #     self.assertAlmostEqual(spectral_data.iloc[i, 1], spectrum.pressures_decibels[i], delta=1.0e-0)

    def test_calculate_sob_spectrum_compare_LabVIEW(self):
        """
        There appears to be limitations of the digital filter method for calculating the sound pressure level from
        waveforms. So a 25-second pink noise file was inserted into the test data and passed through the LabVIEW
        20.0.1.1f1 version using the Sound and Vibration Toolkit's 1/3 octave calculation. This will compare the
        analysis here in Python to the output of LabVIEW.
        """
        #   Read the waveform
        wfm = WaveFile(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink.wav')

        #   Read the results
        spectral_data = pd.read_csv(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink_sob.csv',
                                    index_col=False, header=None, names=['frequency', 'level'])

        #   Pass this waveform through the Digital Filter Spectral Generation.
        spectrum = SpectrumByDigitalFilters(wfm, fob_band_width=6)

        #   Process the spectra comparison - LabVIEW returns one frequency above 10 kHz that Python does not.
        self.assertEqual(spectral_data.shape[0]-1, len(spectrum.frequencies))

        difference = np.max(abs(np.asarray(spectral_data.iloc[:-1, 1]) - spectrum.pressures_decibels))
        self.assertTrue(difference <= 1.0e0)

    def test_calculate_twob_spectrum_compare_LabVIEW(self):
        """
        There appears to be limitations of the digital filter method for calculating the sound pressure level from
        waveforms. So a 25-second pink noise file was inserted into the test data and passed through the LabVIEW
        20.0.1.1f1 version using the Sound and Vibration Toolkit's 1/3 octave calculation. This will compare the
        analysis here in Python to the output of LabVIEW.
        """
        #   Read the waveform
        wfm = WaveFile(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink.wav')

        #   Read the results
        spectral_data = pd.read_csv(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink_twob.csv',
                                    index_col=False, header=None, names=['frequency', 'level'])

        #   Pass this waveform through the Digital Filter Spectral Generation.
        spectrum = SpectrumByDigitalFilters(wfm, fob_band_width=12)

        #   Process the spectra comparison - LabVIEW returns one frequency above 10 kHz that Python does not.
        self.assertEqual(spectral_data.shape[0] - 1, len(spectrum.frequencies))

        difference = np.max(abs(np.asarray(spectral_data.iloc[:-1, 1]) - spectrum.pressures_decibels))
        self.assertTrue(difference <= 3.0e0)

    def test_calculate_24ob_spectrum_compare_LabVIEW(self):
        """
        There appears to be limitations of the digital filter method for calculating the sound pressure level from
        waveforms. So a 25-second pink noise file was inserted into the test data and passed through the LabVIEW
        20.0.1.1f1 version using the Sound and Vibration Toolkit's 1/3 octave calculation. This will compare the
        analysis here in Python to the output of LabVIEW.
        """
        #   Read the waveform
        wfm = WaveFile(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink.wav')

        #   Read the results
        spectral_data = pd.read_csv(str(Path(__file__).parents[1]) + '/test Data/spectral/filter_test_pink_24ob.csv',
                                    index_col=False, header=None, names=['frequency', 'level'])

        #   Pass this waveform through the Digital Filter Spectral Generation.
        spectrum = SpectrumByDigitalFilters(wfm, fob_band_width=24)

        #   Process the spectra comparison - LabVIEW returns one frequency above 10 kHz that Python does not.
        self.assertEqual(spectral_data.shape[0]-2, len(spectrum.frequencies))

        difference = np.max(abs(np.asarray(spectral_data.iloc[:-2, 1]) - spectrum.pressures_decibels))
        self.assertTrue(difference <= 5.0e0)

