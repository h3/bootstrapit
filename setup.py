from setuptools import setup, find_packages

VERSION = '0.0.1'

install_requires = [
   #'simplejson',
   #'PyYAML',
]

setup(
    name="bootstrapit",
    version=VERSION,
    url="https://github.com/h3/bootstrapit",
    license="BSD",
    description="Bootstrapit",
    author='Maxime Haineault & Maxime Barbier',
    packages=find_packages(exclude=['tests']),
#   package_dir={'': '.'},
    install_requires = [],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development'
    ],
)
