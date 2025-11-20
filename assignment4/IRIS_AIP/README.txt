IRIS HDF5 DATASET README
------------------------

Title:
    Iris Dataset (Fisher 1936) (HDF5 - Archival Information Package)

Creators / Contributors:
    R. A. Fisher (original creator)
    UCI Machine Learning Repository (data distributor)

Source:
    UCI Machine Learning Repository (Dataset ID 53)
    DOI: 10.24432/C56C76
    URL: https://archive.ics.uci.edu/ml/datasets/iris

Description:
    The classic Iris dataset contains 150 samples of iris flowers, including
    sepal length, sepal width, petal length, petal width, and species.
    It is converted from UCI ML Repository format to a single HDF5 file.

Data Structure:
    Iris_table/
        sepal_length  : float
        sepal_width   : float
        petal_length  : float
        petal_width   : float
        species       : string

Metadata:
    - Original metadata extracted from ucimlrepo and embedded in the HDF5 file
    - Column attributes include:
        - original_dtype
    - Variables metadata included as HDF5 attribute "variables"
    - Public domain dataset as provided by UCI ML Repository.

Preservation Information:
    - PREMIS metadata: premis.xml
    - File checksums: manifest.txt (SHA-256)

Conversion Workflow:
    - Python with pandas, h5py, ucimlrepo
    - Conversion script: conversion.py
    - Conversion date (UTC): 2025-11-19T00:00:00Z