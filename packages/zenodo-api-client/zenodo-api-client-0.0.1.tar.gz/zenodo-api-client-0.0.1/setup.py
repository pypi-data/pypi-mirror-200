from setuptools import setup

setup(
    name='zenodo-api-client',
    version='0.0.1',
    package_dir={'':'src'},
    packages=['zenodo_client'],
    install_requires=['requests']
)
