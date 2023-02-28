from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in invictus/__init__.py
from invictus import __version__ as version

setup(
	name="invictus",
	version=version,
	description="Travel Management",
	author="Thirvusoft",
	author_email="thirvusoft@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
