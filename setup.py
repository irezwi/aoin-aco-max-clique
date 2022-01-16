import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aoin-aco-max-clique",
    version="0.0.1",
    author="Ireneusz Żwirek, Wojciech Czarnecki",
    description="University project for Nature Inspired Optimization Algorithms course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irezwi/aoin-aco-max-clique",
    project_urls={
        "Bug Tracker": "https://github.com/irezwi/aoin-aco-max-clique/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)