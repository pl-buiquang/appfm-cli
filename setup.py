from setuptools import setup

setup(
    name='CPM CLI',
    version='0.1',
    py_modules=['client'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cpm=client:cli
    ''',
)