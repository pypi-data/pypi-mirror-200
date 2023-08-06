import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

test_deps = [
    'pytest',
    'pytest-timeout',
    'flake8',
    'pylint',
    'mypy',
]
extras = {
    'test': test_deps
}

setuptools.setup(
    name='terminal-formatter',
    version='0.0.2',
    author='Ruben Lipperts',
    author_email='',
    description='Simple terminal text formatter that helps with printing pretty stuff',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rlipperts/formatter',
    package_dir={'': 'src'},
    packages=['terminal_formatter'],
    package_data={'terminal_formatter': ['py.typed']},
    tests_require=test_deps,
    extras_require=extras,
    install_requires=[
        'pprintpp',
        'colored',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: General',
    ],
    python_requires='~=3.9',
)
