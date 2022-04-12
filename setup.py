from setuptools import setup, find_packages


setup(name='api_test',
      version='1.0',
      description="API testing",
      author='PyFlyBoy',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          "pytest==6.2.4",
          "pytest-html==3.1.1",
          "requests==2.27.1",
          "requests-oauthlib==1.3.0",
          "PyMySQL==1.0.2",
      ]
      )