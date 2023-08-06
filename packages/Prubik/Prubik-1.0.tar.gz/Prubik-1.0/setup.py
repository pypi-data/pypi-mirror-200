from setuptools import setup, find_packages

setup(
    name = 'Prubik',
    version = '1.0',
    author='0xRezA',
    author_email = 'gg.test1386@gmail.com',
    description = 'Build Your Own Rubika Bot !',
    keywords = ['Rubika', 'Rubika Bot'],
    packages = find_packages(),
    install_requires = ['websocket-client', 'pycryptodome', 'urllib3'],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)