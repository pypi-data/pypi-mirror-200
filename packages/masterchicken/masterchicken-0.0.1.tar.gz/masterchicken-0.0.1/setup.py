from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='masterchicken',
    version='0.0.1',
    description='A basic calculator in "class mathcal:" and csv file reader',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://organicchicken.netlify.app/',
    author='PythonChicken123',
    author_email='wave6013@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)