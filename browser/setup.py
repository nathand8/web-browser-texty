import setuptools

setuptools.setup(
    name="browser-pkg-u0777729-nathan-davis", # Replace with your own username
    version="0.0.1",
    author="Nathan Davis",
    author_email="u0777729@utah.edu",
    description="A minimal browser built in Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# Run afterwards: pip install -e .