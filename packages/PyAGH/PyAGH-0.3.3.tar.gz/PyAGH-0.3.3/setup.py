from setuptools import setup,find_packages,Extension
import os

os.environ["CC"] = "g++"  # 指定编译器为 g++
os.environ["CXX"] = "g++"
__VERSION__ = '0.3.3'
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))  ##
BASE_DIR = os.path.dirname(__file__)
os.chdir(BASE_DIR)



setup(

    name='PyAGH',  # package name
    version= __VERSION__,  # package version
    description='A package for calculating kinship matrix',  # package description
    author='Zhao Wei',
    author_email='852322127@qq.com',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=3.5  ',
    setup_requires = ["pybind11 >= 2.9.2"],
    install_requires=["numpy >= 1.19.0",
                      "pandas >=1.1.0",
                      "sympy",
                      "scipy >= 1.7.3",
                      "polars >= 0.13.51",
                      "pybind11>= 2.9.2",
                      "matplotlib",
                      "numba"
                      ],
    include_package_data=True,
    license='MIT License',
    platforms=["all"],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: C++',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
    ext_modules=[Extension(name='FUNC',  # 模块名称
                            sources=['scrc/function_c.cpp']  # 源码
                           )],
    package_data={
        '':['data/*'],
               },

)