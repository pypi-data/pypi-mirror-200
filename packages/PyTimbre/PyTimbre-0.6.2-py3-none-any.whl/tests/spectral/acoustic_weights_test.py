import datetime
import math
from unittest import TestCase
import numpy
from pytimbre.spectral.acoustic_weights import AcousticWeights


class TestAcousticWeights(TestCase):
    def test_sound_exposure_level(self):
        y = []
        x = []
        max = int(20 / 0.1)
        for index in range(0, max, 1):
            input = index * 0.1
            x.append(datetime.datetime.min + datetime.timedelta(seconds=input))
            y.append(100 * math.exp(-math.pow(input - 10.0, 2.0) / math.sqrt(100)))
        self.assertAlmostEqual(114.09, AcousticWeights.sound_exposure_level(x, y, 10), places=2)

    def test_find_dB_down_limits(self):
        y = []
        max = int(20 / 0.1)
        for index in range(0, max, 1):
            input = index * 0.1
            y.append(100 * math.exp(-math.pow(input - 10.0, 2.0) / math.sqrt(2)))
        start, stop = AcousticWeights.find_dB_down_limits(y, 10)
        self.assertEqual(96, start)
        self.assertEqual(104, stop)
        y = []
        for index in range(0, max, 1):
            input = index * 0.1
            y.append(100 * math.exp(-math.pow(input - 10.0, 2.0) / math.sqrt(500)))
        start, stop = AcousticWeights.find_dB_down_limits(y, 10)
        self.assertEqual(84, start)
        self.assertEqual(116, stop)

    def test_leq(self):
        spl = [50, 55, 55, 50]
        self.assertAlmostEqual(53.18, AcousticWeights.leq(spl, 0.25, 1, 0, 3), places=2)
        spl = [50, 50, 50, 50]
        self.assertAlmostEqual(50, AcousticWeights.leq(spl, 0.25, 1, 0, 3), places=2)

    def test_lf(self):
        spls = [70.9, 78.4, 83.3, 87.6, 87.3, 93.5, 93.8, 97, 99.9, 98.2]
        lf = AcousticWeights.lf(spls)
        self.assertAlmostEqual(104.38, lf, places=1)

    def test_la(self):
        spls = [70.9, 78.4, 83.3, 87.6, 87.3, 93.5, 93.8, 97, 99.9, 98.2]
        freqs = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        la = AcousticWeights.la(spls, freqs)
        self.assertAlmostEqual(103.2, la[0], places=1)

    def test_aw(self):
        a_weights = [-39.53, -26.22, -16.19, -8.68, -3.25, 0, 1.20, 0.96, -1.14, -6.7]
        freqs = numpy.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
        for i in range(0, len(freqs), 1):
            aw = AcousticWeights.aw(freqs[i])
            self.assertAlmostEqual(a_weights[i], aw, places=1)

    def test_cw(self):
        c_weights = [-3.03, -0.82, -0.18, 0, 0.03, 0, -0.17, -0.83, -3.05, -8.63]
        freqs = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        for i in range(0, len(freqs), 1):
            cw = AcousticWeights.cw(freqs[i])
            self.assertAlmostEqual(c_weights[i], cw, places=1)

    def test_pnl(self):
        spl = numpy.array([0, 0, 0, 0, 0, 0, 0, 79.5, 78.5, 82.9, 89.6, 92.3, 83, 90.7, 85.1, 90.6, 89.8, 90.2, 89.8,
                           88.8, 88.5, 87.8, 87.6, 88, 88.8, 86.6, 88.7, 78.3, 70.3, 61.8, 58.3])
        self.assertEqual(31, len(spl))
        actual = AcousticWeights.pnl(spl)
        print('actual: {}'.format(actual))
        self.assertAlmostEqual(112.3, actual, delta=1e-1)

    def test_tone_corrections(self):
        spl = [0, 0, 0, 0, 0, 0, 0, 79.5, 78.5, 82.9, 89.6, 92.3, 83, 90.7, 85.1, 90.6, 89.8, 90.2, 89.8, 88.8, 88.5,
               87.8, 87.6, 88, 88.8, 86.6, 88.7, 78.3, 70.3, 61.8, 58.3]
        self.assertAlmostEqual(2.11, AcousticWeights.tone_correction(spl), places=1)

