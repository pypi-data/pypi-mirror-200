# Copyright 2021 Rosalind Franklin Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


from setuptools import setup, find_packages
from glob import glob
from pathlib import Path

# read contents of readme
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    version="0.1.0post1",
    name="ot2rec_report",
    description="Generate reports for Ot2Rec",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rosalindfranklininstitute/ot2rec_report.git",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    data_files=[("templates", glob("src/ot2rec_report/templates/*ipynb"))],
    test_suite="tests",
    license="Apache License, Version 2.0",
    zip_safe=False,
    install_requires=[
        "jupyterlab",
        "jupyter",
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "networkx",
        "pydot",
        "icecream",
        "pyyaml",
        "papermill",
        "seaborn",
        "mrcfile",
        "tifffile",
        "magicgui[pyqt5]",
        "networkx",
        "pydot",
        "black[jupyter]",
    ],
    entry_points={"console_scripts": ["o2r.report.run=ot2rec_report.main:main"]},
)
