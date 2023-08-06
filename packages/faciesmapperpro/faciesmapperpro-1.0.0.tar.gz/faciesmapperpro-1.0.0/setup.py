from setuptools import setup, find_packages


# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='faciesmapperpro',
      version='1.0.0',
      author='Srv',
      author_email='smukherjee10@slb.com',
      maintainer='Srv',
      maintainer_email='smukherjee10@slb.com',
      description="predicts facies from a given borehole image.",
      packages=find_packages(), # NEW: find packages automatically
      install_requires=requirements)