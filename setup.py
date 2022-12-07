import os

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

    # We need python3.9 in order to use importlib.resources.files in templates.py
    python_requires='>=3.8',
    install_requires=[
        # importlib.resources.files requires python >=3.9
        # if python 3.8, need to install 3rd importlib-resources
        "importlib-resources>=5.2.0; python_version<'3.9'"
    ],
    package_data={'pyonepassword': ['data/*', 'py.typed']},
    entry_points={"console_scripts":
                  ["opconfig=pyonepassword.opconfig_main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        # TODO: this breaks building in tox>=4.0
        # disabling for now
        # 'egg_info': CleanEggInfoCommand
    },
)

os.chdir(old_cwd)
