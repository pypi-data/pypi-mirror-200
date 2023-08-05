import setuptools

setuptools.setup(
    name="generic-output-manager",
    version="0.0.6",
    author="Alida research team",
    author_email="engineering-alida-lab@eng.it",
    description="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "bda-service-utils",
        "minio",
        "alida-arg-parser>=0.0.35",
        "kafka-python>=2.0.2",
        ],
)
