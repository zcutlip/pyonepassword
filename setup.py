import os
import re

from setuptools import find_packages, setup
from setuptools.command.egg_info import egg_info


def project_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path


old_cwd = os.getcwd()
proj_path = project_path()
os.chdir(proj_path)

about = {}

with open(os.path.join(proj_path, "pyonepassword", "__about__.py"), "r") as fp:
    exec(fp.read(), about)

with open(os.path.join(proj_path, "README.md"), "r") as fp:
    long_description = fp.read()

GITHUB_URL = "https://github.com/zcutlip/pyonepassword"
# links on PyPI should have absolute URLs
# this awful regex looks for [any text](any url), making sure there's no 'http:'
# in the url part
# it then inserts https://github.com/zcutlip/pyonepassword/blobl/main/
# after between the '(' and the relative URL
# believe it or not this also works with directories such as examples/item_editing/
# Github redirects from blob/main/ to tree/main/ in this case
# source: https://github.com/pypa/readme_renderer/issues/163#issuecomment-1679601106
long_description = re.sub(
    r"(\[[^\]]+\]\()((?!https?:)[^\)]+)(\))",
    lambda m: m.group(1) + GITHUB_URL + "/blob/main/" +
    m.group(2) + m.group(3),
    long_description,
)


packages = find_packages(
    where=".", include=["pyonepassword", "pyonepassword.*"])


# Stale *.egg-info items don't get cleaned automatically
# and can result in things being packaged that shouldn't be or not packaged
# that should be
class CleanEggInfoCommand(egg_info):
    def run(self):
        import glob
        import shutil
        rm_list = glob.glob('*.egg-info')
        print("egg_info: removing egg-info")
        for rm_path in rm_list:
            print("rm_path")
            shutil.rmtree(rm_path)
        super().run()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    license="MIT",
    author="Zachary Cutlip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcutlip/pyonepassword",
    packages=packages,

    python_requires='>=3.9',
    install_requires=[
        "python-singleton-metaclasses"
    ],
    package_data={'pyonepassword': ['data/**', 'py.typed']},
    entry_points={"console_scripts":
                  ["opconfig=pyonepassword.opconfig_main:main"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    cmdclass={
        # TODO: this breaks building in tox>=4.0
        # disabling for now
        # 'egg_info': CleanEggInfoCommand
    },
)

os.chdir(old_cwd)
