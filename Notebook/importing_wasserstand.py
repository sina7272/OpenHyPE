import pandas as pd
import sqlalchemy
import numpy as np
import credential as  creds 

data_in_dir = r"../data/"

katalog_fname = r"opendata.gw_wasserstand.csv"

katalog_pfname = data_in_dir + katalog_fname
df = pd.read_csv(katalog_pfname, sep=";")

df['datum_messung'] = pd.to_datetime(
    df['datum_messung'].astype(str), format='%Y%m%d')


# # df1 = df.iloc[:1000000, :]
# df1 = df.iloc[1000000:2000000, :]

# print(df1.shape)


df_split = np.array_split(df, 20)

postgresurl = creds.URL


engine = sqlalchemy.create_engine(postgresurl)

print("connect to DB")

df_split[8].to_sql(con=engine, name="wasserstand2",
                   schema="sina", if_exists="append", index=False)

# 8 is error

# for x in range(9):

#     df_split[x].to_sql(con=engine, name="wasserstand2",
#                        schema="sina", if_exists="append", index=False)

#     print("data {} is in DB now".format(x))

print("All Data is done now")
