from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path('README.md').parent
long_description = (this_directory / "README.md").read_text()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name='masterchicken',
    version='0.0.2',
    description='A basic calculator in "class mathcal:" and csv file reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://organicchicken.netlify.app/',
    author='PythonChicken123',
    author_email='wave6013@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['chicken', 'laserchicken', 'netlify', 'calculator'],
    packages=find_packages(),
    install_requires=[]
)
