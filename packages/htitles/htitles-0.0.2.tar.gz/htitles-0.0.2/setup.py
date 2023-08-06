from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='htitles',
    version='0.0.2',
    author='FrostWreath',
    author_email='',
    description='A cool package to change the python terminal text easily',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=[''],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[''],
    entry_points={
        'console_scripts': [
            'script_name = htitles.module_name:main',
        ],
    },
)