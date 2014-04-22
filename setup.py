from setuptools import setup, find_packages
from glob import glob
import re

package_name = 'hardware_changes'
version_str = re.search(r'^__version__\s+=\s+[\'"]([\d.]+)[\'"]',
        open('%s/version.py' % (package_name, )).read(),
        re.M).group(1)

setup(name=package_name,
        version=version_str,
        description='NGTS hardware changes',
        author='Simon Walker',
        author_email='s.r.walker101@googlemail.com',
        url='http://github.com/NGTS/hardware-changes-python.git',
        packages=find_packages(),
        long_description=open('README.markdown').read(),
        install_requires=['flask',
            'gunicorn',
            ]
        )
