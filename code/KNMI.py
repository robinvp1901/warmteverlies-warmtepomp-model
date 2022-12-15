from knmy import knmy
import pandas as pd

df_temp = knmy.get_daily_data(stations=[260],
                                           start=20210101,
                                           end=20211231,
                                           variables=['TEMP'],
                                  parse=True)[3:]

df_temp =pd.DataFrame(df_temp[0])
df_temp.drop(columns=['STN', 'TN', 'TX', 'T10N'], inplace=True, axis=1)
df_temp.set_index("YYYYMMDD", inplace=True)
df = df_temp.rename_axis('')
df["TG"] = df["TG"] * 0.1
print(df["TG"])

