from setuptools import setup, find_packages

setup(
    name='relative2absolute',
    version='0.1.0',
    description='Convert relative imports in a Python package to absolute imports.',
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
)
