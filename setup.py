from setuptools import setup

setup(
    name='listigator',
    packages=['listigator'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy'
    ],
)