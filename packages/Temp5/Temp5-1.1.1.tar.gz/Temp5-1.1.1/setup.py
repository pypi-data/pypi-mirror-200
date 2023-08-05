#In the name of GOD
from setuptools import setup, find_packages

long_desc = open("c:\\MTemp\\README.md").read()
setup(
    name='Temp5',
    version='1.1.1',
    description = "Temp5 Test ML Environment",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    license='MIT',
    author="Pooya Ghiami",
    author_email='pooyagheyami@gmail.com',
    packages=find_packages(
        where='src',
        include=['*'],
        ),
    package_dir={'': 'src'},
    package_data={
        "Temp5": ["*.txt"],
        "Temp5.Database": ["*.db"],
        "Temp5.Config":["*.ini"],
        "Temp5.Database.sqls":["*.sql"],
        "Temp5.locale.en":["*.mo","*.po"],
        "Temp5.Fount":["*.sql","*.ini","*.txt"]
        },
    include_package_data=True,
    scripts=['scripts/TEMP5.py'],
    url='https://github.com/Srcfount/Temp5/',
    keywords='MACHINELEARNING GUI SQL',
    install_requires=[
          'wxPython',
      ],
##    entry_points={
##        'console_scripts': [
##            'make = MPT5:make cmd1 cmd2'
##
##            ]
##        },
    #script_name='make cmd1 cmd2',
    #script_args=['cmd1','cmd2']
    

)
##
##import setuptools
##
##long_desc = open("README.md").read()
##required = ['wxpython'] # Comma seperated dependent libraries name
##
##setuptools.setup(
##    name="MPT5.1.0",
##    version="1.0.0", # eg:1.0.0
##    author="Pooya Ghiami",
##    author_email="pooyagheyami@gmail.com",
##    license="GNU",
##    description="MPT5 Test ML Environment",
##    long_description=long_desc,
##    #long_description_content_type="text/markdown",
##    url="https://github.com/Srcfount/MPT5/",
##    #packages = ['c:\\MPT5.1.0.0'],#setuptools.find_packages('src'), #['MPT5.1.0'],
##    # project_urls is optional
##    #project_urls={
##    #    "Bug Tracker": "<BUG_TRACKER_URL>",
##    #},
##    keywords="MACHINELEARNING GUI SQL",
##    install_requires=required,
##    packages=setuptools.find_packages(where="src"),
##    python_requires=">=3.6",
##)


##name string
##
##version string
##
##description string
##
##long_description string
##
##long_description_content_type string
##
##author string
##
##author_email string
##
##maintainer string
##
##maintainer_email string
##
##url string
##
##download_url string
##
##packages list
##
##py_modules list
##
##scripts list
##
##ext_package string
##
##ext_modules list
##
##classifiers list
##
##distclass Distribution subclass
##
##script_name string
##
##script_args list
##
##options dictionary
##
##license string
##
##license_file string deprecated
##
##license_files list
##
##keywords string or list
##
##platforms list
##
##cmdclass dictionary
##
##data_files list deprecated
##
##package_dir dictionary
##
##requires string or list deprecated
##
##obsoletes list deprecated
##
##provides list
