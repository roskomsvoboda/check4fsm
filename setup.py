import os
import setuptools

from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError

from setuptools import setup  


class sdist(sdist_orig):

    def run(self):
        try:
            self.spawn(['python', '-m', 'dostoevsky', 'download', 'fasttext-social-network-model'])
        except DistutilsExecError:
            self.warn('listing directory failed')
        super().run()

def parse_requirements():
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, 'requirements.txt')) as f:
        lines = f.readlines()
    lines = [l for l in map(lambda l: l.strip(), lines) if l != '' and l[0] != '#']
    return lines


requirements = parse_requirements()

setuptools.setup(
    name='check4fsm',
    version='0.0.15',
    scripts=['check4fsm/Communication.py'],
    author="Stanisalv Kiselev",
    author_email="ristleell@gmail.com",
    description="Utilities package",
    url="https://gitlab.com/ristle/check4fsm.git",
    packages=setuptools.find_packages(),
    classifiers=[
        # "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    install_requires=requirements,
        cmdclass={
        'sdist': sdist
    }
)
