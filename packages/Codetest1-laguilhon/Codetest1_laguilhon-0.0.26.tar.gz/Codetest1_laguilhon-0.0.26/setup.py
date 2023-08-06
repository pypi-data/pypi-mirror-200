from setuptools import setup, find_packages

setup(
    name="Codetest1_laguilhon",
    version="0.0.26",
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
        "fpdf",
        "numpy",
        "matplotlib",
        "pandas",
        "scikit-image",
        "opencv-python-headless",
        "tensorflow",
        "keras",
    ],
    python_requires=">=3.7",
)