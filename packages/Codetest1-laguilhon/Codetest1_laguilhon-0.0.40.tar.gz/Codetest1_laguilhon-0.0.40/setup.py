from setuptools import setup, find_packages

setup(
    name="Codetest1_laguilhon",
    version="0.0.40",
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
        "numpy>=1.21.2",
        "pandas>=1.3.3",
        "matplotlib>=3.4.3",
        "scikit-learn>=1.0",
        "scipy>=1.7.1",
        "tensorflow>=2.6.0",
        "keras>=2.6.0",
        "opencv-python-headless>=4.5.4.58",
        "pillow>=8.3.2",
        "fpdf>=1.7.2",
        "scikit-image>=0.18.3"
    ],

    python_requires=">=3.7",
)