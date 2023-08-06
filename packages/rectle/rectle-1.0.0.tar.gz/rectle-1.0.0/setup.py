import setuptools
from rectle.version import Version


setuptools.setup(name='rectle',
                 version=Version('1.0.0').number,
                 description='Rectle module',
                 long_description='Rectle module',
                 author='Rectle',
                 author_email='contact@rectle.com',
                 url='http://rectle.com',
                 py_modules=['rectle'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='rectle',
                 classifiers=['Development Status :: 1 - Planning'])
