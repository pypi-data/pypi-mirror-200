import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "pyJoules",
    "os0",
    "logging3"
]
extras = {"protobuf": ["protobuf<5.0.0dev"]}    

setuptools.setup(
    name="softwareappenergycalc",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Sudeshna Mitra",                     # Full name of the author
    description="Software Application Energy Calculation  Package",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    #packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],                                    # Information to filter the project on PyPi website
    #python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["softwareappenergycalc"],             # Name of the python package
    package_dir={'':'softwareappenergycalc'},     # Directory of the source code of the package
    #install_requires=dependencies                    # Install other dependencies if any
    #packages=packages,
    #namespace_packages=namespaces,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
