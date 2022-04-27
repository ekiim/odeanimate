from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="odeanimate",
    version="0.0.1",
    description=(
        "A module for useful quick mathematical calculation,"
        "plotting and animation."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://git.ekiim.com/ekiim/odeanimate",  # Optional
    author="Miguel Alejandro Salgado Zapien",  # Optional
    author_email="ekiim@ekiim.xyz",  # Optional
    classifiers=[  # Optional
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="numerical",  # Optional
    packages=find_packages(),  # Required
    python_requires=">=3.9",
    install_requires=["matplotlib", "ffmpeg-python"],  # Optional
    project_urls={  # Optional
        "Source": "https://git.ekiim.xyz/ekiim/odeanimate",
    },
)
