import pandas as pd

CSV_file = "../database/data.csv"
type_buitenmuur = "Buitenmuur"
type_muur_aangrenzend = "Binnenmuur"
type_vloer_bg = "Vloer-BG"

names_volume_dim = [
    ('Muur-GZ-BG-01', 'Muur-VG-BG-02', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-VG-01-02', 'Muur-GZ-01-01'),
    ("Lengte [m]", "Lengte [m]", "Breedte [m]", "Lengte [m]", "Lengte [m]", "Breedte [m]")]                             # first 3 dim BG, second 3 dim 1e floor

names_surf_dim = [
    ('Muur-GZ-BG-01', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-GZ-01-01',
                   'Muur-VG-BG-02', 'Muur-VG-BG-02', 'Muur-VG-01-02', 'Muur-VG-01-02',
                   'Muur-AG-BG-03', 'Muur-AG-BG-03', 'Muur-AG-01-03', 'Muur-AG-01-03'),
    ("Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
                   "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
                   "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
                   "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]")]

name_living_BG = [('Vloer-KR-BG', 'Vloer-KR-BG'),("Lengte [m]", "Breedte [m]")]
name_living_1e = [('Vloer-SS-02', 'Vloer-SS-02'),("Lengte [m]", "Breedte [m]")]

def load_data_building():
    df_building = pd.read_csv("../database/data.csv", sep=',', skiprows=2).set_index("Naam")

    df_building_outside = df_building[df_building["Type"] == type_buitenmuur] # Data gebouw naar buitenlucht
    df_building_adjacent = df_building[df_building["Type"] == type_muur_aangrenzend]  # Data aangrenzende woning
    df_building_ground = df_building[df_building["Type"] == type_vloer_bg]

    return df_building_outside, df_building_adjacent, df_building_ground

def calc_volume(df_building_outside):
    volume_dim = []
    for i, j in zip(names_volume_dim[0], names_volume_dim[1]):
        volume_dim.append(df_building_outside.loc[i][j])

    volume = volume_dim[0] * volume_dim[1] * volume_dim[2] + volume_dim[3] * volume_dim[4] * volume_dim[5]

    return volume

def calc_surface(df_building_outside):
    surf_dim = []
    for i, j in zip(names_surf_dim[0], names_surf_dim[1]):
        surf_dim.append(df_building_outside.loc[i][j])

    surf_GZ = surf_dim[0] * surf_dim[1] + surf_dim[2] * surf_dim[3]
    surf_VG = surf_dim[4] * surf_dim[5] + surf_dim[6] * surf_dim[7]
    surf_AG = surf_dim[8] * surf_dim[9] + surf_dim[10] * surf_dim[11]

    A_surf = surf_GZ + surf_VG + surf_AG

    return A_surf

def calc_bhulp(df_building_outside, df_building_ground, df_building_adjacent):

    A_living = df_building_ground.loc['Vloer-KR-BG']['Eff Opp. [m]'] + df_building_adjacent.loc['Vloer-SS-02']['Eff Opp. [m]']
    Outside_length = df_building_outside.loc['Muur-GZ-01-01']["Lengte [m]"] + df_building_outside.loc['Muur-VG-01-02']["Lengte [m]"] + df_building_outside.loc['Muur-AG-01-03']["Lengte [m]"]

    Bhulp = 2 * A_living / Outside_length

    if Bhulp <= 2:
        Bhulp = 2
        return Bhulp

    elif Bhulp >= 50:
        Bhulp = 50
        return Bhulp

    else:
        return Bhulp

if __name__ == '__main__':
    df_building_outside, df_building_adjacent, df_building_ground = load_data_building()
    calc_volume(df_building_outside)
    calc_surface(df_building_outside)
    calc_bhulp(df_building_outside, df_building_ground, df_building_adjacent)

