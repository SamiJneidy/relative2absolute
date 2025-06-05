from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='relative2absolute',
    version='0.1.3',
    description='Convert relative imports in a Python package to absolute imports.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sami Jneidy',
    author_email='samihanijneidy@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'relative2absolute=relative2absolute.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    readme = "README.md"
)