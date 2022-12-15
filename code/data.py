import pandas as pd


CSV_file = "../database/data.csv"
type_buitenmuur = "Buitenmuur"
type_muur_aangrenzend = "Binnenmuur"
type_muur_aangrenzend_boven_onder = "Bovenburen"
type_vloer_bg = "Vloer-BG"


def load_data_building():
    df_building = pd.read_csv(CSV_file, sep=',', skiprows=2).set_index("Naam")

    df_building_outside = df_building[df_building["Type"] == type_buitenmuur]           # Data gebouw naar buitenlucht
    df_building_adjacent_sideways = df_building[df_building["Type"] == type_muur_aangrenzend]    # Data aangrenzende woning zij
    df_building_adjacent_above_below = df_building[df_building["Type"] == type_muur_aangrenzend_boven_onder]  # Data aangrenzende woning boven
    df_building_ground = df_building[df_building["Type"] == type_vloer_bg]              # Data grond

    return df_building_outside, df_building_adjacent_sideways, df_building_adjacent_above_below, df_building_ground


def calc_variables_ventilation(volume, sp_ceff, qis, a_surf, a_tot):
    c_eff = volume * sp_ceff                 # Calc opslagcapaciteit [Wh/K]
    qi = qis * a_surf                        # Calc volumestroom infiltration [m³/s]
    qv = 0.0009 * a_tot                    # Calc volumestroom ventilation [m³/s]

    return c_eff, qi, qv


def calc_fiak(t_in, t_adj, t_out_corr, t_corr1):
    fiak = ((t_in-t_adj) / (t_in-t_out_corr))
    fiak2 = (((t_in + t_corr1) - t_adj) / (t_in - t_out_corr))

    return fiak, fiak2


def calc_figk(t_in, t_corr2, t_average, t_out_corr):
    figk = ((t_in + t_corr2)-t_average)/(t_in-t_out_corr)

    return figk


def calc_heatloss_outside(df_building_outside):
    df_h_outside = pd.DataFrame(df_building_outside["Eff Opp. [m]"] * (
                df_building_outside["U-Waarde contructie"]
                + df_building_outside["U-Waarde Thermische bruggen"]) *
                                df_building_outside["fk"])

    h_outside = df_h_outside.sum()
    return h_outside[0]


def calc_heatloss_adjacent(df_building_adjacent, fiak):
    df_h_adjacent = pd.DataFrame(df_building_adjacent["Eff Opp. [m]"] * (
                df_building_adjacent["U-Waarde contructie"]
                + df_building_adjacent["U-Waarde Thermische bruggen"]) * fiak)

    h_adjacent = df_h_adjacent.sum()
    return h_adjacent[0]

def calc_heatloss_adjacent(df_building_adjacent, fiak):
    df_h_adjacent = pd.DataFrame(df_building_adjacent["Eff Opp. [m]"] * (
                df_building_adjacent["U-Waarde contructie"]
                + df_building_adjacent["U-Waarde Thermische bruggen"]) * fiak)

    h_adjacent = df_h_adjacent.sum()
    return h_adjacent[0]



def calc_heatloss_ground(df_building_ground, bhulp, dv, figk, fgw):
    df_h_ground = pd.DataFrame(df_building_ground["Eff Opp. [m]"]
                               * (0.9671 / (-7.455 + (10.76 + bhulp) ** 0.5532
                                            + (9.773 + dv) ** 0.6027
                                            + (0.0265 + df_building_ground["U-Waarde contructie"]
                                               + df_building_ground["U-Waarde Thermische bruggen"]) ** -0.9226)
                                  + -0.0203) * figk * fgw)
    h_ground = df_h_ground.sum() * 1.45
    return h_ground[0]


def calc_heatloss_ventilation(cp, qi, z, qv, fv):
    h_infiltration = cp * qi * z
    h_filtration = cp * qv * fv

    h_ventilation = h_infiltration + h_filtration

    return h_ventilation

