from setuptools import setup, find_packages

setup(
    name="Code_laguilhon",
    version="0.0.11",
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
        "tkinter==8.5",
        "Pillow==8.3.2",
        "webbrowser",
        "fpdf==1.7.2",
        "numpy==1.21.0",
        "matplotlib==3.4.2",
        "pandas==1.3.1",
        "scikit-image==0.18.2",
        "opencv-python-headless==4.5.3.56",
        "tensorflow==2.6.0",
        "keras==2.6.0",
        "skimage==0.19.1",
        "cv2==4.5.4",
    ],
    python_requires=">=3.7",
)