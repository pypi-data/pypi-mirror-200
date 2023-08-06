
from setuptools import setup, find_packages

requirements = open('requirements.txt').read().splitlines()

setup(
    name='dms_ci',
    version='0.1.1',
    url='https://github.com/rouskinlab/DMS_CI',
    author='Yves Martin',
    author_email='yves@martin.yt',
    packages=find_packages(),    
    package_dir={'dms_ci': 'dms_ci'},
    install_requires=requirements,
)