from setuptools import setup, find_packages

setup(
    name="Codetest1_laguilhon",
    version="0.0.39",
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
   "numpy==1.19.3",        "pandas>=1.2.2",        "matplotlib>=3.3.4",        "scikit-learn>=0.24.1",        "scipy==1.6.2",        "tensorflow>=2.4.1",        "keras>=2.4.3",        "opencv-python-headless>=4.5.1.48",        "pillow>=8.2.0",        "fpdf>=1.7.2",        "scikit-image>=0.18.1"  
    ],

    python_requires=">=3.7",
)