from unittest import TestCase
import numpy as np
from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools
import pandas as pd
from pathlib import Path


class TestFractionalOctaveBand(TestCase):
    @staticmethod
    def one_sixth_fc():
        return str(
            Path(__file__).parents[1]) + '/Test Data/Spectral/one-sixth-ob-fc.csv'

    @staticmethod
    def one_twelvth_fc():
        return str(
            Path(__file__).parents[1]) + '/Test Data/Spectral/one-twelvth-ob-fc.csv'

    @staticmethod
    def fractional_octave_center_frequency_analysis():
        return str(
            Path(__file__).parents[1]) + '/Test Data/Spectral/Fractional Octave Bandwidth Center Frequency ' \
                                         'analysis.xlsx'

    @staticmethod
    def fractional_octave_shapes():
        return str(
            Path(__file__).parents[1]) + '/Test Data/Spectral/hsq band definition.xlsx'

    @staticmethod
    def minimum_audible_field():
        return str(Path(__file__).parents[1]) + '/Test Data/Spectral/minimumaudiblefield.csv'

    def test_nearest_band(self):
        self.assertEqual(0, FractionalOctaveBandTools.nearest_band(1, 1000))
        self.assertEqual(30, FractionalOctaveBandTools.nearest_band(3, 1000))

    def test_center_frequency(self):
        self.assertEqual(1000, FractionalOctaveBandTools.center_frequency(1, 0))
        self.assertEqual(1000, FractionalOctaveBandTools.center_frequency(3, 30))

        labView_values = np.loadtxt(TestFractionalOctaveBand.one_twelvth_fc())

        for band in range(-80, 41):
            expected = float(labView_values[80+band])
            actual = FractionalOctaveBandTools.center_frequency(12, band)

            percent_error = abs(expected - actual) / expected
            self.assertTrue(percent_error < 3e-2)

        test_values = pd.read_excel(TestFractionalOctaveBand.fractional_octave_center_frequency_analysis(),
                                    sheet_name='one-24-ob-fc', skiprows=79, header=None)

        for i in range(test_values.shape[0] - 1):
            expected = test_values.iloc[i, 0]
            actual = FractionalOctaveBandTools.center_frequency(24, test_values.iloc[i, 3])

            percent_error = abs(expected - actual) / expected
            self.assertTrue(percent_error < 5e-2, msg='Error at {} with expected {} and actual {}'.format(
                i, expected, actual
            ))

        test_values = pd.read_excel(TestFractionalOctaveBand.fractional_octave_center_frequency_analysis(),
                                    sheet_name='one-6-ob', header=None)

        for i in range(test_values.shape[0]):
            expected = test_values.iloc[i, 0]
            actual = FractionalOctaveBandTools.center_frequency(6, test_values.iloc[i, 1])

            percent_error = abs(expected - actual) / expected
            self.assertTrue(percent_error < 3e-2, msg='Error at {} with expected {} and actual {}'.format(
                i, expected, actual
            ))

    def test_lower_frequency(self):
        self.assertAlmostEqual(707.107, FractionalOctaveBandTools.lower_frequency(1, 0), delta=1e-2)
        self.assertAlmostEqual(890.899, FractionalOctaveBandTools.lower_frequency(3, 30), delta=1e-2)

    def test_upper_frequency(self):
        self.assertAlmostEqual(1414.214, FractionalOctaveBandTools.upper_frequency(1, 0), delta=1e-2)
        self.assertAlmostEqual(1122.462, FractionalOctaveBandTools.upper_frequency(3, 30), delta=1e-2)

    def test_bandwidth(self):
        self.assertAlmostEqual(707.107, FractionalOctaveBandTools.band_width(1, 0), delta=1e-2)
        self.assertAlmostEqual(231.563, FractionalOctaveBandTools.band_width(3, 30), delta=1e-2)

    def test_frequencies(self):
        freq_list = FractionalOctaveBandTools.frequencies(10, 40, 3)
        self.assertEqual(31, len(freq_list))
        self.assertEqual(1000, freq_list[30 - 10])

    def test_min_audible_field(self):
        contents = pd.read_csv(TestFractionalOctaveBand.minimum_audible_field())
        for line_index in range(contents.shape[0]):
            f = contents.iloc[line_index, 0]
            expected = contents.iloc[line_index, -1]
            self.assertAlmostEqual(expected, FractionalOctaveBandTools.min_audible_field(f), delta=1e-5)

    def test_get_min_audible_field_tob(self):
        db = FractionalOctaveBandTools.get_min_audible_fields()
        self.assertEqual(31, len(db))

    def test_tob_frequencies_ansi(self):
        freq = FractionalOctaveBandTools.tob_frequencies_ansi()
        self.assertEqual(31, len(freq))
        self.assertEqual(1000, freq[20])

    def test_tob_frequencies(self):
        freq = FractionalOctaveBandTools.tob_frequencies()
        self.assertEqual(31, len(freq))
        self.assertEqual(1000, freq[20])

    def test_tob_to_erb(self):
        corrections = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.984947508,
                       -1.886499608, -2.675271289, -3.356668021, -3.938319912, -4.429410575, -4.839970954, -5.180235728,
                       -5.460125156, -5.688877443, -5.874826467, -6.025301356, -6.146617156, -6.244126428, -6.322306421,
                       -6.384862746, -6.434836444, -6.474706281, -6.506481782]

        n = 0

        for f in FractionalOctaveBandTools.tob_frequencies():
            actual = FractionalOctaveBandTools.tob_to_erb(f, 0)
            self.assertAlmostEqual(corrections[n], actual, delta=1e-5)

            n += 1

    def test_center_frequency_to_erb(self):
        corrections = [25.76245795, 26.03861314, 26.38654688, 26.82491591, 27.37722628, 28.07309375, 28.94983182,
                       30.05445257,
                       31.4461875, 33.19966364, 35.40890513, 38.192375, 41.69932728, 46.11781027, 51.68475, 58.69865455,
                       67.53562054, 78.6695, 92.6973091, 110.3712411,
                       132.639, 160.6946182, 196.0424821, 240.578, 296.6892364, 367.3849643, 456.456, 568.6784728,
                       710.0699286, 888.212, 1112.656946]

        for i in range(0, len(corrections), 1):
            self.assertAlmostEqual(corrections[i], FractionalOctaveBandTools.center_frequency_to_erb(
                FractionalOctaveBandTools.tob_frequencies()[i]), delta=1e-5)

    def test_frequencies_ansi_preferred(self):

        self.assertListEqual(list(FractionalOctaveBandTools.frequencies_ansi_preferred(63, 1000, 1)),
                             [63, 125, 250, 500, 1000])

        self.assertListEqual(list(FractionalOctaveBandTools.frequencies_ansi_preferred(100, 1000, 3)),
                             [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000])

    def test_filter_shape(self):
        sheet_name = 'Calculation of shape 1.25khz'
        data = pd.read_excel(TestFractionalOctaveBand.fractional_octave_shapes(), sheet_name)

        shape = FractionalOctaveBandTools.filter_shape(3, 1250, data.iloc[:, 0])

        self.assertEqual(data.shape[0], len(shape))

        for i in range(data.shape[0]):
            self.assertAlmostEqual(data.iloc[i, -2], shape[i], delta=1e-6)

        sheet_name = 'Calculation of shape 1khz'
        data = pd.read_excel(TestFractionalOctaveBand.fractional_octave_shapes(), sheet_name)

        shape = FractionalOctaveBandTools.filter_shape(3, 1000, data.iloc[:, 0])

        self.assertEqual(data.shape[0], len(shape))

        for i in range(data.shape[0]):
            self.assertAlmostEqual(data.iloc[i, -2], shape[i], delta=1e-6)

    def test_plot_filtershape(self):
        manual = False
        if manual:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()

            fc = 1000
            freq, lo, hi = FractionalOctaveBandTools.ansi_band_limits(0, fc, 3)

            sheet_name = 'Calculation of shape 1khz'
            data = pd.read_excel(TestFractionalOctaveBand.fractional_octave_shapes(), sheet_name)

            shape = FractionalOctaveBandTools.filter_shape(3, fc, data.iloc[:, 0])

            ax.semilogx(freq, 10**(lo/20), 'k')
            ax.semilogx(freq, 10**(hi/20), 'b')
            ax.semilogx(data.iloc[:, 0], shape, 'r')

            ax.set_xlim([fc * 2**(-6), fc * 2**6])
            ax.set_ylim([0, 1.2])

            plt.show()

    def test_get_fob_frequencies(self):
        f = FractionalOctaveBandTools.get_frequency_array(band_width=1, f0=16, f1=500)
        freq_list = [16, 31.5, 63, 125, 250, 500]
        for i in range(len(freq_list)):
            self.assertAlmostEqual(f[i], freq_list[i], delta=1)

        f = FractionalOctaveBandTools.get_frequency_array(3, 10, 10000)

        self.assertEqual(len(FractionalOctaveBandTools.tob_frequencies()), len(f))

        for i in range(len(f)):
            self.assertAlmostEqual(FractionalOctaveBandTools.tob_frequencies()[i], f[i], delta=1)

        bw = 2
        self.assertRaises(ValueError, FractionalOctaveBandTools.get_frequency_array, bw, 16, 500)