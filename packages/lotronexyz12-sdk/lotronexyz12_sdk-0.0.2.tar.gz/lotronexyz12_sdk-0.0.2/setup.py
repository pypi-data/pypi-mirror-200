import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lotronexyz12_sdk",
    version="0.0.2",
    author="Alex",
    author_email="",
    description="LOTR coding test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.10.9',
    install_requires=[
        'requests'
    ],
    keywords=''
)