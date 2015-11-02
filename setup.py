from setuptools import setup, find_packages
import admin_extras

install_requires = [
    'Django>=1.7',
    'markdown2',
]

tests_require = [
    'nose',
    'coverage',
]

long_description = open('README.rst').read()

setup(
    name='Django-admin-extras',
    version=admin_extras.__versionstr__,
    description='Application that contains useful extras for django admin',
    long_description=long_description,
    author='Michal Dub',
    author_email='michalmam@centrum.cz',
    license='BSD',
    url='https://github.com/MichalMaM/django-admin-extras',

    packages=find_packages(
        where='.',
        exclude=('doc', 'tests',)
    ),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,

    test_suite='tests.run_tests.run_all',
    tests_require=tests_require,
)
