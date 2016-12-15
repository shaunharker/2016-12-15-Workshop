from setuptools import setup

setup(name='pyCHomP',
      version='0.1',
      description='Python Version of CHomP',
      url='https://github.com/shaunharker/pyCHomP',
      author='Shaun Harker',
      author_email='shaun.harker@rutgers.edu',
      license='MIT',
      packages=['pyCHomP'],
      install_requires=[
          'IPython'
      ],
      include_package_data=True,
      zip_safe=False)
