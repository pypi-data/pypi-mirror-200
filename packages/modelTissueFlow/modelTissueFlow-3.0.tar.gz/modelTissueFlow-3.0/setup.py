import sys
import glob
import numpy
from os import path

#######################
# setup-tool-packages #
#######################
try:
    from setuptools import setup
    from setuptools import Extension
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    from distutils.find_packages import find_packages

from setuptools.dist import Distribution
Distribution(dict(setup_requires='Cython'))

###################
# cython-packages #
###################
try:
    from Cython.Distutils import build_ext
except ImportError:
    print("Could not import Cython.Distutils. Install `cython` and rerun.")
    sys.exit(1)

module1 = Extension(    name         = "modelTissueFlow.modules.PIV",
                        sources      = ["modelTissueFlow/modules/processPIV/PIV.pyx"],
                        include_dirs = [numpy.get_include()],
                   )
                    
ext_modules = [module1]

################################
# project-description-in: PyPi #
################################
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#################
# setup-details #
################# 
setup(
    name='modelTissueFlow',
    version='3.0',    
    description='tissue-flow-analysis',
    author='Bandan Chakrabortty',
    author_email='bandan13@gmail.com',
    packages=['modelTissueFlow','modelTissueFlow/modules'], # find_packages(),
    url='https://github.com/HiBandan/modelTissueFlow', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe = False,        
    ext_modules = ext_modules, 
    cmdclass = {'build_ext': build_ext},
    install_requires=['shapely','sklearn','scikit-image'], 
    )



