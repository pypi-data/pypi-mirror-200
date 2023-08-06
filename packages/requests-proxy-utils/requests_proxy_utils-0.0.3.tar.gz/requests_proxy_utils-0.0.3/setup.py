from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'A Library for using proxies with the requests library'
LONG_DESCRIPTION = 'A Library for using proxies with the requests library'

setup(
        name="requests_proxy_utils", 
        version=VERSION,
        author="Leon",
        author_email="leonwagner09@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
