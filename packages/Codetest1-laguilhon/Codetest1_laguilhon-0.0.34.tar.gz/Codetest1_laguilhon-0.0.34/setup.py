from setuptools import setup, find_packages

setup(
    name="Codetest1_laguilhon",
    version="0.0.34",
    author="laguilhon",
    author_email="lea.aguilhon@gmail.com",
    description="Test de package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=["src/data/IMG","src/data/f_annexes","src/data/Code"],

    install_requires=[
        "tk",
        "Pillow",
        "fpdf>=1.7.2,<2",
        "numpy>=1.22.0,<=1.23.9",
        "matplotlib",
        "pandas",
        "scikit-image<0.20.0",
        "opencv-python-headless",
        "tensorflow==2.12.0",
        "keras>=2.12.0,<2.13",
        "scipy>=1.7.0,<1.9.0",
    ],

    

    python_requires=">=3.7",
)