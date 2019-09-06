from setuptools import setup

setup(
    name='snpcc',
    version='0.1',
    py_modules=['snpcc'],
    install_requires=[
        'snapcast',
    ],
    entry_points='''
        [console_scripts]
        snpcc=snpcc:main
    ''',
)
