from setuptools import find_packages, setup

setup(
    name="hashflow",
    packages=find_packages(include=['hashflow']),
    version='0.1.0',
    description='Library implementing the Hashflow API',
    author='Hashflow Foundation',
    license='MIT',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)