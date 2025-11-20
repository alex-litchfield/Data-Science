from ucimlrepo import fetch_ucirepo 
import pandas as pd
import h5py
import json
import yaml

# Fetches Iris Data from https://doi.org/10.24432/C56C76
def fetchIris():
    # Fetching dataset  
    iris = fetch_ucirepo(id = 53) 
    # Merging features and targets into one pandas dataframe
    featuresAndTargets = pd.concat([iris.data.features, iris.data.targets], axis = 1)
    # Converting the metadata into a python dictionary because original data contains non hdf5 compatible types
    metadataDictionary = dict(iris.metadata)
    # Convert variables from a dataframe to a dictionary
    variablesDictionary = iris.variables.to_dict(orient = "records")
    return featuresAndTargets, metadataDictionary, variablesDictionary

# Fetches AMZN data from the "AMZN.csv" file
def fetchAMZN(inputDataFile, inputMetadataFile):
    # Converting data from AMZN file to pandas dataframe
    AMZNdata = pd.read_csv(inputDataFile)
    # Fetching metadata from yaml file
    with open(inputMetadataFile, "r") as f:
        AMZNmetadata = yaml.safe_load(f)
    return AMZNdata, AMZNmetadata

# Builds the new HDF5 file for the AMZN dataset
def buildFile(outputFile, standardData, metadataDictionary, variablesDictionary):
    with h5py.File(outputFile, "w") as h5:
        # Places metadata into the file
        if outputFile == "iris.h5":
            # Creating an hdf5 attribute for each value in the original metadata
            for key, value in metadataDictionary.items():
                h5.attrs[key] = json.dumps(value)
            # Convert to JSON strings only AFTER converting the structures
            h5.attrs["variables"] = json.dumps(variablesDictionary)
            # Creating dataset group and placing data
            grp = h5.create_group("Iris_table")
        elif outputFile == "AMZN.h5":
            # Creating an hdf5 attribute for each value in the original metadata
            h5.attrs["Custom Dataset Authors"] = json.dumps(metadataDictionary["Authors"])
            h5.attrs["Dataset Source"] = json.dumps(metadataDictionary["Provenance"]["Dataset Source"])
            h5.attrs["variables"] = json.dumps(metadataDictionary["AZMN Metadata"])
            metadataDictionary["Data & Metadata Origin from Kaggle"]["Temporal Coverage End Date"] = metadataDictionary["Data & Metadata Origin from Kaggle"]["Temporal Coverage End Date"].isoformat()
            for key, value in metadataDictionary["AZMN Metadata"].items():
                h5.attrs[key] = json.dumps(value)
            for key, value in metadataDictionary["Data & Metadata Origin from Kaggle"].items():
                h5.attrs[key] = json.dumps(value)
            # Creating dataset group and placing data
            grp = h5.create_group("AMZN_table")
        # Places data into the file
        for col in standardData.columns:
            data = standardData[col].values
            # If the object is a string handle it as a list. Otherwise, make a new dataset directly
            if standardData[col].dtype == object:
                new_dtype = h5py.string_dtype(encoding="utf-8")
                newList = [str(i) for i in data]
                newDataset = grp.create_dataset(col, data = newList, dtype = new_dtype)
            else:
                newDataset = grp.create_dataset(col, data = data)
            # Adds metadata to the columns
            newDataset.attrs["original_dtype"] = str(standardData[col].dtype)
        # Informs the user of a successful file conversion
        print("HDF5 file created successfully:", outputFile)

# Prints standard data and metadata found in the new HDF5 file
def printFileContents(readFile):
    with h5py.File(readFile, "r") as f:
        # Prints HDF5 File attributes (metadata)
        print("\nDISPLAYING HDF5 FILE ATTRIBUTES (Metadata):\n")
        for key, value in f.attrs.items():
            print(key, ":", value, "\n")
        # Prints HDF File data and groupings
        print("\nDISPLAYING HDF5 FILE GROUPS & DATASETS (Standard Data)\n")
        for groupName in f:
            print("GROUP:", groupName)
            for dataset_name in f[groupName]:
                print("  DATASET", groupName, "/", dataset_name)
                print("    Values:")
                print("    ", f[groupName][dataset_name][()])
                print("    Attributes:", dict(f[groupName][dataset_name].attrs), "\n")

# Converting iris to hdf5
featuresAndTargets, metadataDictionary, variablesDictionary = fetchIris()
buildFile("iris.h5", featuresAndTargets, metadataDictionary, variablesDictionary)
printFileContents("iris.h5")

# Converting AMZN.csv to hdf5
AMZNdata, AMZNmetadata = fetchAMZN("./AMZN_AIP/AMZN.csv", "./AMZN_AIP/metadata.yaml")
buildFile("AMZN.h5", AMZNdata, AMZNmetadata, None)
printFileContents("AMZN.h5")