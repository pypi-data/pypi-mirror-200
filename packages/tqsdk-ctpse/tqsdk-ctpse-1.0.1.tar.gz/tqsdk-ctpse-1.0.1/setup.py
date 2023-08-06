# -*- coding: utf-8 -*-
__author__ = 'chengzhi'

import setuptools

# from py-spy/setup.py
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel, get_platform

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package (we have platform specific lib)
            if self.plat_name != "any":
                self.root_is_pure = False
                plat_name = (self.plat_name or get_platform()).replace('-', '_').replace('.', '_')
                if plat_name == "linux_x86_64" or plat_name == "manylinux1_x86_64":
                    self.distribution.package_data[""] = ["LinuxDataCollect64.so"]
                elif plat_name == "win32":
                    self.distribution.package_data[""] = ["WinDataCollect32.dll"]
                elif plat_name == "win_amd64":
                    self.distribution.package_data[""] = ["WinDataCollect64.dll"]

        def get_tag(self):
            # this set's us up to build generic wheels.
            python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't contain any python source
            python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None

setuptools.setup(
    name='tqsdk-ctpse',
    version="1.0.1",
    description='TianQin SDK - ctpse lib',
    author='TianQin',
    author_email='tianqincn@gmail.com',
    url='https://www.shinnytech.com/tqsdk',
    packages=setuptools.find_packages(),
    python_requires='>=3',
    cmdclass={'bdist_wheel': bdist_wheel},
)
