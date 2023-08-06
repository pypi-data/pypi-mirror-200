from setuptools import setup, find_packages

# following https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/
# and https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='bmdal_reg',
    version='3.0.1',    
    description='Deep Batch Active Learning for Regression',
    url='https://github.com/dholzmueller/bmdal_reg',
    author='David Holzmüller',
    author_email='nextuser@live.de',
    license='Apache 2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['torch',
                      'numpy',
                      'dill',
                      'psutil',
                      'matplotlib',
                      'seaborn',
                      'pandas',
                      'openml',
                      'mat4py',
                      'scipy'                     
                      ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)

