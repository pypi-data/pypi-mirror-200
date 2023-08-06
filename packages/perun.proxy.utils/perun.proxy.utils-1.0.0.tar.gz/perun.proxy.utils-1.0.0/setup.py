import setuptools

setuptools.setup(
    name="perun.proxy.utils",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/proxyidp-scripts.git",
    description="Module with utilities and monitoring probes",
    include_package_data=True,
    packages=setuptools.find_namespace_packages(include=["perun.*"]),
    install_requires=[
        "setuptools",
        "pymongo~=4.3",
        "asyncssh~=2.13",
        "docker~=6.0",
        "beautifulsoup4~=4.12",
    ],
)
