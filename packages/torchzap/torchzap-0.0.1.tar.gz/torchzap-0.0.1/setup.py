import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torchzap",
    version="0.0.1",  # Latest version .
    author="tompz",
    author_email="mailto@gmail.com",
    description="PyTorch Zap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/",
    packages=setuptools.find_packages(),
    install_requires=['fire', 'pandas', 'codefast>=0.9.9', 'pydantic'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
