import json
import io
import os
from setuptools import setup

with open('./youhi/package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

def _get_long_description():
    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"), encoding="utf8") as f:
        return f.read()

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        'Framework :: Dash',
    ],
)
