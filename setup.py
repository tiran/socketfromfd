import subprocess

from setuptools import setup

requirements = []
# test requirements
test_requires = ['coverage', 'pytest'] + requirements
test_pep8_requires = ['flake8', 'pep8-naming']
test_docs_requires = ['docutils', 'markdown']

try:
    cmd = ['pandoc', '--from=markdown', '--to=rst', 'README.md']
    long_description = subprocess.check_output(cmd).decode('utf-8')
except (subprocess.CalledProcessError, OSError) as e:
    print(e)
    long_description = ''


setup(
    name='socketfromfd',
    description='socket.fromfd() with auto-detection of family and type',
    long_description=long_description,
    version='0.1.0',
    license='Apache License, Version 2.0',
    author='Christian Heimes',
    author_email='christian@python.org',
    url='https://github.com/tiran/socketfromfd',
    py_modules=['socketfromfd'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking',
        'Topic :: Software Development :: Libraries',
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
