from extractname import ExtractName
from iofile import IoFile
import pandas as pd

################################################################
###       extraction de tout les utilisateurs                ###
################################################################
extractname: ExtractName = ExtractName("list_users.csv")
data: pd.DataFrame = extractname.get_users_list()
extractname.show_data()

################################################################
###              test sur chaque utilisateurs                ###
################################################################



