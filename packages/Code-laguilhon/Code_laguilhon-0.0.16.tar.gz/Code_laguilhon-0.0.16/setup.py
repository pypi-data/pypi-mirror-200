from setuptools import setup, find_packages

setup(
    name="Code_laguilhon",
    version="0.0.16",
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
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
    "data": ["IMG/*", "f_annexe/*"]
    },
    include_package_data=True,
    install_requires=[
        "tkinter",
        "Pillow",
        "webbrowser",
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