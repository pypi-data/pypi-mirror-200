import io
import os
import re
from setuptools import setup

script_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_folder)

# Find version info from module (without importing the module):
with open('pillowscreenx/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name='PillowScreenX',
    version=version,
    url='https://github.com/4akhilkumar/pillowscreenx',
    author='Sai Akhil Kumar Reddy N',
    author_email='4akhilkumar@gmail.com',
    description=('PillowScreenX is a powerful screenshot capturing tool that leverages the power of the Pillow library to provide high-quality screenshot captures.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='HPND',
    packages=['PillowScreenX'],
    keywords="Python, PillowScreenX, Screenshots, Path",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    zip_safe=True
)
