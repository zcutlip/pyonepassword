from setuptools import setup
about = {}
with open("pyonepassword/__about__.py") as fp:
    exec(fp.read(), about)

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      url="TBD",
      packages=['pyonepassword'],
      python_requires='>=3.7',
      install_requires=[],
      package_data={'pyonepassword': ['config/*']},
      )
