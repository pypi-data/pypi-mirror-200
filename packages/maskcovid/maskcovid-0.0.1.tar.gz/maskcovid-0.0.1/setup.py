import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maskcovid",
    version="0.0.1",
    author="Izuru Inose",
    author_email="i.inose0304@gmail.com",
    description="maskcovid is a PyPI tool that predicts the number of people infected by day and up to one month from the date Japan began its liberal mask-wearing policy in the current Covid-19 epidemic.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i-inose/maskcovid",
    project_urls={
        "Bug Tracker": "https://github.com/i-inose/maskcovid",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['maskcovid'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'maskcovid = maskcovid:main'
        ]
    },
)
