from setuptools import setup, find_packages

setup(
    name='maphis', 
    packages=find_packages(exclude=['maphis.bin']),
    include_package_data=True,
    exclude_package_data={'': ["*.pt", "Tesseract-OCR/*"]},
    setup_requires=['setuptools_scm'],
    install_requires=[
        "platformdirs",
        "numpy",
        "scikit-image",
        "PySide6",
        "opencv-python",
        "Pillow",
        "imagecodecs",
        "numba",
        "openpyxl",
        "scikit-learn",
        "scipy",
        "pytesseract",
        "mouse",
        "torch",
        "arthseg",
        "pyparsing",
        "requests"
    ])
