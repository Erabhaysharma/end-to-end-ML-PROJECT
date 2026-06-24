#the setup.py help us too create ml projt in the form of the pakage]
#by the using of setup.py we can make a packege and even deploy it on pipi so
#anyone can use it in therir project
from setuptools import find_packages,setup
from typing import List
HYPHEN_E_DOT = "-e ."

def get_requirements(file_path):
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements
setup(
    name="e to e ml project",
    version="0.0.1",
    author="AbhayKumarSharma",
    author_email="abhaysharma75547@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)