import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    # username => aagarwal1996

setuptools.setup(
    name="synthetic-combinations",
    version="0.0.1",
    author="Abhineet Agarwal, Anish Agarwal, Suhas Vijaykumar",
    author_email="aa3797@berkeley.edu",
    description="Imputing counterfactual outcomes for combinatorial interventions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aagarwal1996/synthetic-combinations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    install_requires=[
        "celer==0.7.2",
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "contourpy==1.0.7",
        "cycler==0.11.0",
        "Cython==0.29.34",
        "download==0.3.5",
        "fonttools==4.39.3",
        "idna==3.4",
        "joblib==1.2.0",
        "kiwisolver==1.4.4",
        "libsvmdata==0.4.1",
        "matplotlib==3.7.1",
        "numpy==1.24.2",
        "packaging==23.0",
        "pandas==1.5.3",
        "Pillow==9.5.0",
        "pyparsing==3.0.9",
        "python-dateutil==2.8.2",
        "pytz==2023.3",
        "requests==2.28.2",
        "scikit-learn==1.2.2",
        "scipy==1.10.1",
        "seaborn==0.12.2",
        "six==1.16.0",
        "threadpoolctl==3.1.0",
        "tqdm==4.65.0",
        "urllib3==1.26.15",
        "xarray==2023.3.0"
    ],
    python_requires='>=3.6',
)
