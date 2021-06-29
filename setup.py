from setuptools import setup, find_packages
about = {}

with open("pyonepassword/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    license="MIT",
    author="Zachary Cutlip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcutlip/pyonepassword",
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[],
    package_data={'pyonepassword': ['config/*']},
    entry_points={"console_scripts":
                  ["opconfig=pyonepassword.opconfig_main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
