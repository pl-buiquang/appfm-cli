from setuptools import setup

setup(
    name='CPM CLI',
    version='0.1',
    py_modules=['cpm'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cpm=cpm:cli
    ''',
)