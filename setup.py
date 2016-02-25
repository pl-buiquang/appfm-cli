from setuptools import setup, find_packages

setup(
    name='CPM CLI',
    version='0.1',
    py_modules=['cpm'],
    install_requires=[
        'Click',
        'pyzmq'
    ],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        cpm=cpm:cli
    ''',
)
