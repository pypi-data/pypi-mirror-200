import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="simplysklearn", 
    version="0.1.1",
    author="Kim Hyun Bin",
    author_email="KIMH0004@e.ntu.edu.sg",
    description="Python package to automate machine learning process to showcase metric values for nearly all Scikit-Learn's models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanilladucky/simplysklearn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)