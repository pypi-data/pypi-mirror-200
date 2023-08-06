#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'openai', 'python-dotenv', 'tiktoken']

test_requirements = [ ]

setup(
    author="Ivan Vrbovčan",
    author_email='ivan.vrbovcan@nomendi6.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Generate project documentation using GPT.",
    entry_points={
        'console_scripts': [
            'create_doc=create_doc.__main__:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='create_doc',
    name='create_doc',
    packages=find_packages(include=['create_doc', 'create_doc.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Nomendi6/create_doc',
    version='0.1.5',
    zip_safe=False,
)
