import setuptools

setuptools.setup(
    name="vcl-parser",                      # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Vishwesswaran Gopal",                     # Full name of the author
    description="A python package that can be used to parse .vcl files.",
    long_description=".vcl files are a custom configuration file type that can store game information.",  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.11.1',                # Minimum version requirement of the package
    py_modules=["vcl-parser"],             # Name of the python package
    package_dir={'VCL':'../vcl_python/vcl_module'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)