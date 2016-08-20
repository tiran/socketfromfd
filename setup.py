from setuptools import setup

requirements = []
# test requirements
test_requires = ['coverage', 'pytest'] + requirements
test_pep8_requires = ['flake8', 'pep8-naming']
test_docs_requires = ['docutils', 'markdown']

setup(
    name='socketfromfd',
    description='socket.fromfd() with auto-detection of family and type',
    version='0.1.dev1',
    license='Apache License, Version 2.0',
    author='Christian Heimes',
    author_email='christian@python.org',
    url='https://github.com/tiran/socketfromfd',
    py_modules=['socketfromfd'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=requirements,
    tests_require=test_requires,
    extras_require={
        'test': test_requires,
        'test_docs': test_docs_requires,
        'test_pep8': test_pep8_requires,
    },
)
