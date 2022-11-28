import os

from setuptools import find_packages, setup


def project_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path


old_cwd = os.getcwd()

print(os.path.abspath(os.path.curdir))
proj_path = project_path()
os.chdir(proj_path)
print(os.path.abspath(os.path.curdir))

about = {}

# TODO: remove this when we get this working in github actions
# In tox env, in githubaction, why are we not finding these files?
print("List dir:")
pyonepassword_dir = os.path.join(
    os.path.abspath(os.path.curdir), "pyonepassword")
print(os.listdir(pyonepassword_dir))

with open(os.path.join(proj_path, "pyonepassword", "__about__.py"), "r") as fp:
    exec(fp.read(), about)

with open(os.path.join(proj_path, "README.md"), "r") as fp:
    long_description = fp.read()


packages = find_packages(where=".", include=["pyonepassword.*"])
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
)

os.chdir(old_cwd)
