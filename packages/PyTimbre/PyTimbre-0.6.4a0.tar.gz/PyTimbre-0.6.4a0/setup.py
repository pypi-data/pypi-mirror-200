from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

    with open('HISTORY.md') as history_file:
        HISTORY = history_file.read()

        with open('LICENSE.txt') as license_file:
            LICENSE = license_file.read()

setup_args = dict(
    name='PyTimbre',
    version='0.6.4a0',
    description='Python conversion of Timbre Toolbox',
    long_description_content_type="text/markdown",
    long_description=README+'\n\n' + HISTORY+'\n\n' + LICENSE,
    license='MIT',
    packages=find_packages(),
    author='Dr. Frank Mobley',
    author_email='frank.mobley.1@afrl.af.mil',
    keywords=['machine learning', 'feature extraction', 'MATLAB', 'audio'],
    url='https://gitlab.com/python-audio-feature-extraction/pytimbre',
    download_url=''
)

install_requires = [
    'numpy',
    'pandas',
    'scipy',
    'statsmodels',
    'mosqito',
    'colorednoise',
    'clipdetect',
    'librosa'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)