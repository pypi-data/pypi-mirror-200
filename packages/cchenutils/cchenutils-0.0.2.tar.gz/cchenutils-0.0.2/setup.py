from setuptools import setup, find_packages

setup(
    name = 'cchenutils',
    version = '0.0.2',
    keywords = ('chench'),
    description = 'cc personal use',
    license = 'MIT License',
    install_requires = [],
    include_package_data=True,
    zip_safe=True,

    author = 'chench',
    author_email = 'phantomkidding@gmail.com',

    packages = find_packages(),
    platforms = 'any',
)