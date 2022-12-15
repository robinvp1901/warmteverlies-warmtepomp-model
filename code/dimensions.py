names_volume_dim = [
    ('Muur-GZ-BG-01', 'Muur-VG-BG-02', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-VG-01-02', 'Muur-GZ-01-01'),
    ("Lengte [m]", "Lengte [m]", "Breedte [m]", "Lengte [m]", "Lengte [m]", "Breedte [m]")]

# first 3 dim BG, second 3 dim 1e floor

names_surf_dim = [
    ('Muur-GZ-BG-01', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-GZ-01-01',
     'Muur-VG-BG-02', 'Muur-VG-BG-02', 'Muur-VG-01-02', 'Muur-VG-01-02',
     'Muur-AG-BG-03', 'Muur-AG-BG-03', 'Muur-AG-01-03', 'Muur-AG-01-03',
     "Vloer-VD-01", "Vloer-VD-01"),
    ("Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]",)]

name_living_BG = [('Vloer-KR-BG', 'Vloer-KR-BG'), ("Lengte [m]", "Breedte [m]")]
name_living_1e = [('Vloer-SS-02', 'Vloer-SS-02'), ("Lengte [m]", "Breedte [m]")]


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

    surf_gz = surf_dim[0] * surf_dim[1] + surf_dim[2] * surf_dim[3]
    surf_vg = surf_dim[4] * surf_dim[5] + surf_dim[6] * surf_dim[7]
    surf_ag = surf_dim[8] * surf_dim[9] + surf_dim[10] * surf_dim[11]

    a_surf = surf_gz + surf_vg + surf_ag

    return a_surf


def calc_bhulp(df_building_outside, df_building_ground, df_building_adjacent_above_below):

    a_living = (df_building_ground.loc['Vloer-KR-BG']['Eff Opp. [m]']
                + df_building_adjacent_above_below.loc['Vloer-SS-02']['Eff Opp. [m]'])

    a_tot = a_living * 0.55

    outside_length = (df_building_outside.loc['Muur-GZ-01-01']["Lengte [m]"]
                      + df_building_outside.loc['Muur-VG-01-02']["Lengte [m]"]
                      + df_building_outside.loc['Muur-AG-01-03']["Lengte [m]"])

    bhulp = 2 * a_living / outside_length

    if bhulp <= 2:
        bhulp = 2
        return bhulp, a_tot

    elif bhulp >= 50:
        bhulp = 50
        return bhulp, a_tot

    else:
        return bhulp, a_tot
