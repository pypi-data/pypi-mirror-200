from setuptools import setup, find_packages

setup(
    name='echobox',
    version='1.5.25',
    keywords=('echobox'),
    description='echobox',
    license='Apache 2.0',
    install_requires=[
        'six',
        'ruamel.yaml==0.16.13',
        'ruamel.yaml.clib==0.2.2',
        'Jinja2',
        'netaddr',
        'requests',
        'tzlocal==2.1',
        'redis',
        'configparser==3.7.4',
    ],

    scripts=[],

    author='kiuber',
    author_email='kiuber.zhang@gmail.com',
    url='',

    packages=find_packages(),
    platforms='any',
)
