import setuptools

# To publish on pypi:
# 1) Change version and delete sdist and bdist_wheel
# 2) python3 setup.py sdist bdist_wheel
# 3) twine upload --repository pypi dist/*

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='zcross',  
     version='0.0.17',
     scripts=[] ,
     author="Michele Renda",
     author_email="michele.renda@cern.ch",
     description="An utility to read low-pressure gaseous cross sections data",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/micrenda/zcross-python",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
         "Operating System :: OS Independent",
     ],
     install_requires=[
          'matplotlib',
          'pint',
          'pyxb',
          'bibtexparser',
     ],
     python_requires='>=3.0',
     entry_points = {
        'console_scripts': ['zcross-xml=zcross.zcross_xml:main', 'zcross-plot=zcross.zcross_plot:main'],
    }
 )
