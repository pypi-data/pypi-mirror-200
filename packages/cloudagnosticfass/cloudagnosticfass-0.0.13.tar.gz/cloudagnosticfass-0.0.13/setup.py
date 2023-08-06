import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "google-auth >= 1.25.0, < 3.0dev",
    "google-api-core >= 1.31.5, <3.0.0dev,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0",
    "google-cloud-core >= 2.3.0, < 3.0dev",
    "google-resumable-media >= 2.3.2",
    "requests >= 2.18.0, < 3.0.0dev",
    "boto3",
    "botocore",
    "json-operator",
    "os0",
    "logging3"
]
extras = {"protobuf": ["protobuf<5.0.0dev"]}    
packages = [
    package for package in setuptools.find_packages() if package.startswith("google")
]

namespaces = ["google"]
if "google.cloud" in packages:
    namespaces.append("google.cloud")

# Determine which namespaces are needed.

setuptools.setup(
    name="cloudagnosticfass",                     # This is the name of the package
    version="0.0.13",                        # The initial release version
    author="Jagruti Sakhare",                     # Full name of the author
    description="Cloud Agnostic FaaS  Package",
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
    py_modules=["cloudagnosticfass","google"],             # Name of the python package
    package_dir={'':'cloudagnosticfass'},     # Directory of the source code of the package
    #install_requires=dependencies                    # Install other dependencies if any
    packages=packages,
    namespace_packages=namespaces,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)