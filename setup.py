#!/usr/bin/env python3

# see http://bugs.python.org/issue8876
# this is just a quick hack so we can test build in vagrant
import os
if os.environ.get('USER','') == 'vagrant':
  del os.link

from setuptools import setup, find_packages

def requirements():
    with open('./requirements.txt', 'r') as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#') and not l.startswith('-e')]

reqs = requirements()
reqs.append("thingstance==0.1.0")

setup(name='thingstance.org',
      version='0.1.0',
      description='Thingstance Flask Application',
      author='Thingstance.org',
      author_email='paul.downey@whatfettle.com',
      url='https://github.com/thingstance/thing',
      download_url = 'https://github.com/thingstance/thingstance.org/tarball',
      packages=find_packages(exclude=['tests']),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.4',
        ),
      install_requires=reqs,
      dependency_links=[
        "git+ssh://git@github.com/thingstance/thingstance.git@0.1.0#egg=thingstance-0.1.0"
      ],
      scripts = ['bin/run.sh']
)

# crikey this bit below was painful
# see http://mike.zwobble.org/2013/05/adding-git-or-hg-or-svn-dependencies-in-setup-py/
# git@github.com:thingstance/thingstance.git
# git+ssh://git@github.com/thingstance/thingstance.git
