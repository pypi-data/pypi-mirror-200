import unittest
from pytimbre.audio_files.ansi_standard_formatted_files import StandardBinaryFile, WaveFile, Waveform
from pathlib import Path
import os.path
import numpy as np
import datetime


class TestStandardBinaryFile(unittest.TestCase):
    @staticmethod
    def test_bin_write():
        return str(Path(__file__).parents[1]) + "/Test Data/audio_files/files/standard_bin_file_write" \
                                                "/test_standard_bin_file.bin "

    @staticmethod
    def make_waveform():
        """
        Generate the acoustic waveform that was created in Matlab to make the various spectral features

        Parameters
        ----------
        None

        Returns
        -------
        Waveform of a 1000 Hz signal 10s in duration.
        """
        fs = 48000
        f = 1000
        w = 2 * np.pi * f
        t = np.arange(0, 10, 1 / fs)
        signal = 0.75 * np.sin(w * t)

        return Waveform(signal, fs, datetime.datetime.now())

    def test_StandardBinaryFile_init(self):
        '''
        This tests the constructor for the file

        @author: Frank Mobley

        '''

        sbf = StandardBinaryFile(self.test_bin_write())

        self.assertEqual(204800, sbf.sample_rate)
        self.assertEqual(4194304, sbf.sample_count)
        self.assertEqual(8, len(sbf._header))
        self.assertEqual(sbf.sample_count, len(sbf.samples))

        sbf = StandardBinaryFile()
        self.assertIsNone(sbf._header)
        self.assertIsNone(sbf.samples)
        self.assertIsNone(sbf.sample_rate)
        self.assertIsNone(sbf.start_time)

        sbf = StandardBinaryFile(wfm=self.make_waveform())
        self.assertIsNone(sbf._header)
        self.assertIsNotNone(sbf.samples)
        self.assertIsNotNone(sbf.sample_rate)
        self.assertIsNotNone(sbf.start_time)
        self.assertEqual(48000, sbf.sample_rate)

    def test_write_std_binary_file(self):
        wfm = self.make_waveform()

        output_filename = str(Path(__file__).parents[1]) + "/Test "\
                                                           "Data/audio_files/files/standard_bin_file_write/test.bin"

        if os.path.exists(output_filename):
            os.remove(output_filename)

        header = dict()
        header['name'] = "Dr. Frank Mobley"
        header['description'] = "Std Bin File Writing Test"

        StandardBinaryFile.write_std_binary_file(wfm, header, output_filename)

        std_bin = StandardBinaryFile(output_filename)

        self.assertIsNotNone(std_bin)
        self.assertIsNotNone(std_bin._header)
        for key in header.keys():
            self.assertEqual(header[key], std_bin._header[key.upper()])

        self.assertEqual(wfm.sample_rate, std_bin.sample_rate)
        self.assertEqual(wfm.duration, std_bin.duration)
        self.assertEqual(wfm.start_time, std_bin.start_time)

        for i in range(len(wfm.samples)):
            self.assertAlmostEqual(wfm.samples[i], std_bin.samples[i], places=5)

        os.remove(output_filename)

    def test_make_wav_file(self):
        #   Make the standard binary file from a simple waveform object
        wfm = self.make_waveform()
        output_filename = str(Path(__file__).parents[1]) + "/Test " \
                                                           "Data/audio_files/files/standard_bin_file_write/test.bin"

        if os.path.exists(output_filename):
            os.remove(output_filename)

        header = dict()
        header['name'] = "Dr. Frank Mobley"
        header['description'] = "Std Bin File Writing Test"

        StandardBinaryFile.write_std_binary_file(wfm, header, output_filename)

        #   Read this temporary file into the object
        input = StandardBinaryFile(output_filename)

        #   Check that we have the correct number of header lines within the interface
        self.assertEqual(8, input.header_line_count)

        #   Write a new wave file with additional information specified in the function arguments.
        input.make_wav_file(output_filename,
                            "WPAFB",
                            "S. Conner Campbell",
                            "711 HPW/RHWS",
                            "Cleared",
                            "None",
                            None,
                            "Frank Mobley",
                            "Waveform Test",
                            "Waveform Test of writing wave file",
                            "Test of wave file header information",
                            "no specific test point",
                            "no aircraft",
                            "generic waveform representation",
                            "AFRL",
                            "Digital",
                            None,
                            102
                            )

        self.assertTrue(os.path.exists(output_filename))

        cwf = WaveFile(output_filename)

        self.assertEqual(input.sample_rate, cwf.sample_rate)
        self.assertEqual(input.sample_count, len(cwf.samples))

        for key in input._header.keys():
            self.assertTrue(key in cwf.header.keys())

            self.assertEqual(input._header[key], cwf.header[key])

        for i in range(input.sample_count):
            self.assertAlmostEqual(input.samples[i], cwf.samples[i], delta=1e-3)

    def test_read_ill_formed_file(self):
        filename = str(Path(__file__).parents[1]) + "/Test Data/audio_files/test_header_format.bin"

        self.assertRaises(ValueError, StandardBinaryFile, filename)
        self.assertRaises(ValueError, StandardBinaryFile, filename, None, None, "SAMPLE RATE (HZ)", "START TIME")
        sbf = StandardBinaryFile(filename, 24, None, "SAMPLE RATE (HZ)", "START TIME", "MACHINE FORMAT")

        self.assertEqual(1484800, len(sbf.samples))
        self.assertTrue(isinstance(sbf.start_time, datetime.datetime))
        self.assertEqual(2020, sbf.start_time.year)
        self.assertEqual(1, sbf.start_time.month)
        self.assertEqual(15, sbf.start_time.day)
        self.assertEqual(21, sbf.start_time.hour)
        self.assertEqual(49, sbf.start_time.minute)
        self.assertEqual(45, sbf.start_time.second)
        self.assertEqual(0.088e6, sbf.start_time.microsecond)

    def test_getting_header_only(self):
        sbf = StandardBinaryFile(self.test_bin_write(), header_only=True)

        self.assertIsNone(sbf.samples)
        self.assertIsNotNone(sbf.header)

    def test_get_waveform_subset(self):
        #   Read the file
        sbf = StandardBinaryFile(self.test_bin_write())
        self.assertFalse(np.any(np.isnan(sbf.samples)))

        #   Create a new waveform that is trimmed from this data
        subset1 = sbf.trim(0, 1000)
        self.assertFalse(np.any(np.isnan(subset1.samples)))

        #   Since the samples are automatically adjusted for DC offset, we must complete that again here.
        subset1._samples -= np.mean(subset1.samples)

        #   Create a new waveform by not reading all the data and then trimming
        subset2 = StandardBinaryFile(self.test_bin_write(), s0=0, s1=1000)
        self.assertFalse(np.any(np.isnan(subset2.samples)))
        self.assertEqual(subset2.duration, subset1.duration)
        self.assertEqual(subset2.start_time, subset1.start_time)
        for i in range(len(subset2.samples)):
            self.assertEqual(subset2.samples[i], subset1.samples[i])

        #   Do the same thing, but this time make it a non-zero starting sample
        s0 = int(1)
        s1 = int(1001)
        subset1 = sbf.trim(s0, s1)
        self.assertFalse(np.any(np.isnan(subset1.samples)))
        subset1._samples -= np.mean(subset1.samples)
        subset2 = StandardBinaryFile(self.test_bin_write(), s0=s0, s1=s1)
        self.assertFalse(np.any(np.isnan(subset2.samples)))
        self.assertEqual(subset2.duration, subset1.duration)
        self.assertEqual(subset2.start_time, subset1.start_time)
        for i in range(len(subset2.samples)):
            self.assertEqual(subset2.samples[i], subset1.samples[i])

        # self.assertIsNone(sbf.samples)
        self.assertIsNotNone(sbf.header)

    def test_get_subset(self):
        sbf = StandardBinaryFile(self.test_bin_write())
        self.assertFalse(np.any(np.isnan(sbf.samples)))

        s0 = 0
        s1 = 1000
        subset1 = sbf.trim(s0, s1)
        subset1._samples -= np.mean(subset1.samples)
        subset2 = StandardBinaryFile(self.test_bin_write(), s0=s0, s1=s1)
        self.assertEqual(subset2.duration, subset1.duration)
        self.assertEqual(subset2.start_time, subset1.start_time)
        for i in range(len(subset1.samples)):
            self.assertEqual(subset2.samples[i], subset1.samples[i])

        s0 = 1
        s1 = 1000
        subset1 = sbf.trim(s0, s1)
        subset1._samples -= np.mean(subset1.samples)
        subset2 = StandardBinaryFile(self.test_bin_write(), s0=s0, s1=s1)
        self.assertEqual(subset2.duration, subset1.duration)
        self.assertEqual(subset2.start_time, subset1.start_time)
        for i in range(len(subset1.samples)):
            self.assertEqual(subset2.samples[i], subset1.samples[i])
