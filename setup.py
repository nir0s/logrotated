from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


install_requires = [
    "click==6.6",
    "jinja2==2.8"
]

setup(
    name='logrotated',
    version="0.0.3",
    url='https://github.com/nir0s/logrotated',
    author='nir0s',
    author_email='nir36g@gmail.com',
    license='LICENSE',
    platforms='All',
    description='A logrotate human friendly interface.',
    long_description=read('README.rst'),
    packages=find_packages(exclude=[]),
    package_data={'logrotated': ['resources/logrotate']},
    entry_points={
        'console_scripts': [
            'rotatethis = logrotated.logrotated:main',
        ]
    },
    install_requires=install_requires
)
