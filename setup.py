from os.path import dirname, join

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open(join(dirname(__file__), 'firetail_lambda/version.py'), 'r') as f:
    exec(f.read())

setuptools.setup(
    name='Firetail-Lambda',
    author='Riley Priddle',
    version=__version__,
    author_email='riley@firetail.io',
    description='Firetail Lambda Package',
    keywords='pypi, package',
    long_description=long_description,
    license='LGPLv3',
    long_description_content_type='text/markdown',
    url='https://github.com/firetail-io/firetail-py-lambda',
    project_urls={
        'Documentation': 'https://github.com/firetail-io/firetail-py-lambda',
        'Bug Reports':
        'https://github.com/firetail-io/firetail-py-lambda/issues',
        'Source Code': 'https://github.com/firetail-io/firetail-py-lambda',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest']
    },
)
