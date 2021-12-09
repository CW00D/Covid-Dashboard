import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="Covid_Dashboard_Package_cw00d", 
    version="1.0.0",
    author="Christian Wood",
    author_email="christian.f.wood@gmail.com",
    description="A covid dashboard to display covid data for the users local area.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CW00D/Covid-Dashboard.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
