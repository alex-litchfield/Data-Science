AMZN HDF5 DATASET README
------------------------

Title:
    Amazon (AMZN) Historical Stock Dataset (HDF5 - Archival Information Package)

Creators / Contributors:
    Timothy Grashaw
    Alex Litchfield
    Ruikang Lin

Source:
    JacksonCrow, "Nasdaq historical data" on Kaggle.
    URL: https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset
    DOI: https://doi.org/10.34740/kaggle/dsv/1054465

Description:
    Historical stock information Amazon (AMZN) converted from CSV into a single HDF5 object. 
    The HDF5 file stores each table column as an HDF5 dataset inside the group "/AMZN_table".

Data Structure
    AMZN_table/
        Date        : trading date (ISO date strings)
        Open        : opening price (float)
        High        : maximum price during the day (float)
        Low         : minimum price during the day (float)
        Close       : close price adjusted for splits (float)
        Adj Close   : adjusted close for dividends & splits (float)
        Volume      : number of shares (integer)

Metadata:
    - File-level descriptive metadata embedded as HDF5 attributes (converted from metadata.yaml)
    - Column-level metadata stored as dataset attributes:
        - original_dtype
    - Original dataset license: CC0: Public Domain (as provided by source)

Preservation information:
    - PREMIS file: premis.xml
    - Fixity recorded in manifest.txt (SHA-256).

Conversion workflow:
    - Python with pandas, h5py, PyYAML
    - Conversion script: conversion.py
    - Conversion date (UTC): 2025-11-19T00:00:00Z