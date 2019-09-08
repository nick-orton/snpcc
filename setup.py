from setuptools import setup, find_packages

setup(
    name='snpcc',
    version='0.1',
    py_modules=['snpcc'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'snapcast',
        'click',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'snpcc=snpcc:cli',
        ],
    },
)
