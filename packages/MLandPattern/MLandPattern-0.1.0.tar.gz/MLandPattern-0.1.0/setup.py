from setuptools import find_packages, setup

setup(
    name="MLandPattern",
    packages=find_packages(include=['numpy', 'pandas', 'scipy', 'matplotlib']),
    version='0.1.0',
    description="Machine Learning and Pattern recognition Library",
    author="Pablo Munoz Salazar",
    license="ISC",
)