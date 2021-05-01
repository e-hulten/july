import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="july",
    version="0.0.1",
    author="Edvard Hultén",
    author_email="edvard.hulten@gmail.com",
    description="Make beautiful heatmaps of daily data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/e-hulten/july/",
    keywords=[
        "heatmap",
        "visualisation",
        "calendar",
        "daily",
        "matplotlib",
        "github plot",
    ],
    classifiers=[
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
