from setuptools import setup, find_packages

# requirement file
with open('requirements.txt') as f:
    required = f.read().splitlines()

# readme file
with open('README.md') as f:
    readme = f.read()


setup(
    name='texttidy',
    version='0.0.2',
    description='No frills text data cleaning methods. Stada means to tidy in Swedish.',
    long_description=readme,
    long_description_content_type="text/md",
    url='https://github.com/jhags/text-stada',
    author='J Hagstrom',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(include=['texttidy', 'texttidy.*']),
    package_data={
        "texttidy": [
            "data/*.json",
            "data/*.txt"
            ]
    },
    install_requires=required,
    tests_require=['pytest', 'pytest-cov', 'coveralls'],
    python_requires='>=3.7',
)