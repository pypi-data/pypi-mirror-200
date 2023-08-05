"""setup.py script for warp-rna TensorFlow wrapper
mostly copied from https://github.com/HawkAaron/warp-transducer/blob/master/tensorflow_binding/setup.py
Original License: Apache License 2.0
Changes are basically just adapted to the RNA code (and some formatting changes).
"""

from __future__ import print_function

import os
import platform
import re
import warnings
import setuptools
import sys
import unittest
from setuptools.command.build_ext import build_ext as orig_build_ext
from distutils.version import LooseVersion

# We need to import tensorflow to find where its include directory is.
try:
    import tensorflow as tf
except ImportError:
    raise RuntimeError("Tensorflow must be installed to build the tensorflow wrapper.")

if "CUDA_HOME" not in os.environ:
    print("CUDA_HOME not found in the environment so building "
          "without GPU support. To build with GPU support "
          "please define the CUDA_HOME environment variable. "
          "This should be a path which contains include/cuda.h",
          file=sys.stderr)
    enable_gpu = False
else:
    enable_gpu = True

if platform.system() == 'Darwin':
    lib_ext = ".dylib"
else:
    lib_ext = ".so"

warp_rna_path = "../build"
if "WARP_RNA_PATH" in os.environ:
    warp_rna_path = os.environ["WARP_RNA_PATH"]
if not os.path.exists(os.path.join(warp_rna_path, "libwarprna" + lib_ext)):
    print(("Could not find libwarprna.so in {}.\n"
           "Build warp-rna and set WARP_RNA_PATH to the location of"
           " libwarprna.so (default is '../build')").format(warp_rna_path),
          file=sys.stderr)
    sys.exit(1)

root_path = os.path.realpath(os.path.dirname(__file__))

tf_include = tf.sysconfig.get_include()
tf_src_dir = tf.sysconfig.get_lib()
tf_includes = [tf_include, tf_src_dir]
include_dirs = tf_includes + [os.path.join(root_path, '../include')]

if LooseVersion(tf.__version__) >= LooseVersion('1.4'):
    nsync_dir = '../../external/nsync/public'
    if LooseVersion(tf.__version__) >= LooseVersion('1.10'):
        nsync_dir = 'external/nsync/public'
    include_dirs += [os.path.join(tf_include, nsync_dir)]

if os.getenv("TF_CXX11_ABI") is not None:
    TF_CXX11_ABI = os.getenv("TF_CXX11_ABI")
else:
    warnings.warn("Assuming tensorflow was compiled without C++11 ABI. "
                  "It is generally true if you are using binary pip package. "
                  "If you compiled tensorflow from source with gcc >= 5 and didn't set "
                  "-D_GLIBCXX_USE_CXX11_ABI=0 during compilation, you need to set "
                  "environment variable TF_CXX11_ABI=1 when compiling this bindings. "
                  "Also be sure to touch some files in src to trigger recompilation. "
                  "Also, you need to set (or unsed) this environment variable if getting "
                  "undefined symbol: _ZN10tensorflow... errors")
    TF_CXX11_ABI = "0"

extra_compile_args = ['-std=c++11', '-fPIC', '-D_GLIBCXX_USE_CXX11_ABI=' + TF_CXX11_ABI]
# current tensorflow code triggers return type errors, silence those for now
extra_compile_args += ['-Wno-return-type']
if LooseVersion(tf.__version__) >= LooseVersion('1.4'):
    extra_compile_args += tf.sysconfig.get_compile_flags()

extra_link_args = []
if LooseVersion(tf.__version__) >= LooseVersion('1.4'):
    extra_link_args += tf.sysconfig.get_link_flags()

if (enable_gpu):
    extra_compile_args += ['-DWARPRNA_ENABLE_GPU']
    include_dirs += [os.path.join(os.environ["CUDA_HOME"], 'include')]

    # mimic tensorflow cuda include setup so that their include command work
    if not os.path.exists(os.path.join(root_path, "include")):
        os.mkdir(os.path.join(root_path, "include"))

    cuda_inc_path = os.path.join(root_path, "include/cuda")
    if not os.path.exists(cuda_inc_path) or os.readlink(cuda_inc_path) != os.environ["CUDA_HOME"]:
        if os.path.exists(cuda_inc_path):
            os.remove(cuda_inc_path)
        os.symlink(os.environ["CUDA_HOME"], cuda_inc_path)
    include_dirs += [os.path.join(root_path, 'include')]

# Ensure that all expected files and directories exist.
for loc in include_dirs:
    if not os.path.exists(loc):
        print(("Could not find file or directory {}.\n"
               "Check your environment variables and paths?").format(loc),
              file=sys.stderr)
        sys.exit(1)

lib_srcs = ['src/warp_rna_op.cc']

ext = setuptools.Extension('warprna_tensorflow.kernels',
                           sources = lib_srcs,
                           language = 'c++',
                           include_dirs = include_dirs,
                           library_dirs = [warp_rna_path],
                           runtime_library_dirs = [os.path.realpath(warp_rna_path)],
                           libraries = ['warp_rna'],
                           extra_compile_args = extra_compile_args,
                           extra_link_args = extra_link_args)

class build_tf_ext(orig_build_ext):
    def build_extensions(self):
        if LooseVersion(tf.__version__) < LooseVersion('1.4'):
            self.compiler.compiler_so.remove('-Wstrict-prototypes')
        orig_build_ext.build_extensions(self)

def discover_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

# Read the README.md file for the long description. This lets us avoid
# duplicating the package description in multiple places in the source.
README_PATH = os.path.join(os.path.dirname(__file__), "README.md")
with open(README_PATH, "r") as handle:
    # Extract everything between the first set of ## headlines
    LONG_DESCRIPTION = re.search("#.*([^#]*)##", handle.read()).group(1).strip()

setuptools.setup(
    name = "warp_rna",
    version = "0.1",
    description = "TensorFlow wrapper for warp-rna",
    url="https://github.com/1ytic/warp-rna",
    long_description = LONG_DESCRIPTION,
    author = "Mingkun Huang",
    author_email = "mingkunhuang95@gmail.com",
    license = "Apache",
    packages = ["warp_rna"],
    ext_modules = [ext],
    cmdclass = {'build_ext': build_tf_ext},
    test_suite = 'setup.discover_test_suite',
)
