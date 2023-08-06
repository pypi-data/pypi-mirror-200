from setuptools import setup, find_namespace_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'uniconnapps-connector-proto~=0.0.1a1',
    'PyJWT~=2.4.0'
]


setup(
  name="uniconnapps-connector",
  packages=find_namespace_packages(include=['uniconnapps.*']),
  version='0.0.1a3',
  description="uniconnapps-connector",
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Uniconnapps',
  author_email='oss-maintainers@uniconnapps.com',
  #url="https://github.com/uniconnapps/uca-connector-sdk-python",
  install_requires=requirements,
  python_requires=">= 3.7",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11"
  ],
  license='Apache License 2.0',
  zip_safe=False
)
