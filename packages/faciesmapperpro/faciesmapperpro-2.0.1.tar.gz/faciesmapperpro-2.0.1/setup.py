from setuptools import setup, find_packages


# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='faciesmapperpro',
      version='2.0.1',
      author='Srv',
      author_email='smukherjee10@slb.com',
      maintainer='Srv',
      maintainer_email='smukherjee10@slb.com',
      description="This version works within the Techlog environment. The dependency to have an external PNG and CSV file has been eliminated.",
      packages=['faciesmapperpro'], # NEW: find packages automatically
      install_requires=requirements)