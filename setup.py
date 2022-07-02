from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='inejsonstat',
    version='1.0.12',
    packages=['inejsonstat'],
    install_requires=['inejsonstat',
    'numpy',
    'requests',
    'terminaltables',
    'click',
    'cython',
    'pandas',
    'pyyaml',
    'unidecode',
    'datetime'],
    url='https://github.com/Mlgpigeon/inejsonstat.git',
    license='MIT License',
    author='Luis María Salete Cuartero',
    author_email='luismasc16@gmail.com',
    description='Library to interact with the INE JSON-Stat API',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
