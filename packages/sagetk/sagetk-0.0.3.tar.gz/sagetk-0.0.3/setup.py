from setuptools import setup, find_packages

setup(
    name='sagetk',
    version='0.0.3',
    description='A Python library for creating GUIs in HTML/CSS like  syntax',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Chanda Fungamwango Mark',
    author_email='chandamark386@gmail.com',
    url='',
    license='MIT',
    keywords='sagetk,GUIs,html, gui,tkinter,tk',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['pillow']
)
