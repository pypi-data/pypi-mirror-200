
import codecs
import os

from setuptools import setup, find_packages

module_dir = os.path.dirname(__file__)

with codecs.open(os.path.join(module_dir, "README.rst"), encoding="utf8") as f:
    long_description = f.read()


classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
  "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3",
  "Operating System :: OS Independent",
  "Topic :: Software Development :: Libraries",
  "Topic :: Software Development :: Libraries :: Python Modules"]

setup(
    name = "doublebellycluster",
    version = "0.0.4",
    author = "George Pavlov",
    author_email = "pavlovgeorgem@yandex.ru",
    url = "",
    description='Библиотека кластеризации   ...',
    long_description=long_description, 
    license="LGPLv3",
    classifiers=classifiers,
    keywords='clustering voronoi intra_distance clustering-share-devide', 
    packages=find_packages(),
    install_requires=['requests'],
    project_urls={"Source code": "https://github.com/ivknv/yadisk",
                    "Documentation (EN)": "https://yadisk.readthedocs.io/en/latest"},
      
    python_requires='>=3.5'
)