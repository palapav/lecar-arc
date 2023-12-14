# https://github.com/Azure/AzurePublicDataset?tab=readme-ov-file

import pandas as pd

df = pd.read_csv("azurefunctions-accesses-2020.csv.bz2")
df["AnonBlobName"].to_csv("requests.txt", index=False, header=False)
