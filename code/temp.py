from knmy import knmy
import pandas as pd


def load_data_temp(stationnumber, startdate, enddate):
    df = knmy.get_daily_data(stations=[stationnumber],                                  # Station nummmer voorbeeld 260
                             start=startdate,                           # 20210101
                             end=enddate,                               # 20211231
                             variables=['TEMP'],
                             parse=True)[3:]

    df_temp = pd.DataFrame(df[0])
    df_temp.drop(columns=['STN', 'TN', 'TX', 'T10N'], inplace=True, axis=1)
    df_temp.set_index("YYYYMMDD", inplace=True)
    df_temp = df_temp.rename_axis('')
    df_temp["TG"] = df_temp["TG"] * 0.1

    return df_temp
