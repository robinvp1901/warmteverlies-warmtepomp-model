# importeer libraries
# ==================
from knmy import knmy
import pandas as pd

# Database
# ========

CSV_file = "../database/data.csv"
type_buitenmuur = "Buitenmuur"
type_muur_aangrenzend = "Binnenmuur"
type_vloer_bg = "Vloer-BG"



# Variables model
# ===============

#     Variable temperatuur
T_in = 20               # Ontwerpbinnentemperatuur  [°C]
T_corr1 = 3             # Correctie temperatuur delta1 [°C]
T_corr2 = -1            # Correctie temperatuur delta2 [°C]
Year = 2021             # Jaar

#     Variable warmtecapaciteit woning
SpCeff = 50             # Specifieke capaciteit [Wh/(m³·K)]

#   Parameters aangrenzende woning
T_n = 15                # Temperatuur aangrenzenden woning [°C]
cz = 1                  # Zekeheids klasse [-]

#     Parameters luchtverversing
T_corr_lucht = 0        # Correctie luchttemperatuur [°C]
Swd = 1200              # Soortelijk warmte [J/(m³·K)]
z_inf = 0.5             # Fractie infiltratie [-]
qis = 0.0019            # Luchtstroom infiltratie [m³/s per m²]
fv = 1                  # Correctiefactor inblaastemperaturen [-]

#     Parameters constructie woning
dv = 0                  # Diepte onder maaiveld [m]


# load year temp
# ==============

def load_data_temp():
    df_temp = knmy.get_daily_data(stations=[260],
                                   start=20210101,
                                   end=20211231,
                                   variables=['TEMP'],
                                   parse=True)[3:]

    df_temp = pd.DataFrame(df_temp[0])
    df_temp.drop(columns=['STN', 'TN', 'TX', 'T10N'],
                 inplace=True, axis=1)
    df_temp.set_index("YYYYMMDD",
                      inplace=True)
    df_temp = df_temp.rename_axis('')
    df_temp["TG"] = df_temp["TG"] * 0.1

    return df_temp


# load data house
# ===============
def load_data_building():
    df_building = pd.read_csv(CSV_file, sep=',', skiprows=2)

    df_building_outside = df_building[df_building["Type"] == type_buitenmuur]               #     Data gebouw naar buitenlucht
    df_building_adjacent = df_building[df_building["Type"] == type_muur_aangrenzend]        #     Data aangrenzende woning
    df_building_ground = df_building[df_building["Type"] == type_vloer_bg]                  #     Data grond

    return df_building_outside, df_building_adjacent, df_building_ground

# Calc dimensions
# ===============
def calc_dimensions():
    #    Volume
    df_building[df_building["Naam"] == Muur]
    # volume_building = df1 * df2 *df3 + df1 * df2 *df3       # calc volume [m³]

#    Surface outside
    surf_outside = df1 *df2 + df3 + df4 # calc [m²]

#    Surface living
    # calc [m²]

#    Lengte outside
    # calc B_par [m]

    return volume_building, Au, Atot, B_par

# Save data to list

# Calc variables
# ==============
def calc_variables(volume_building, Au, Atot):

    opslagcapaciteit_building = volume_building * SpCeff        #     Calc opslagcapaciteit [Wh/K]
    volumestroom_infiltration = qis * Au                        #     Calc volumestroom infiltration [m³/s]
    volumestroom_ventilation = 0.0009 * Atot                    #     Calc volumestroom ventilation [m³/s]

    return opslagcapaciteit_building, volumestroom_infiltration, volumestroom_ventilation

# Calc specific heatloss
# ======================

#     Calc specific heatloss to outside
#      Load data
#      Formula Surf. * (U-par-delta-U-par) * fk

#     Calc specific heatloss to neighbours
#      Load data
#      Formula Surf. * (U-par-delta-U-par) * fk

#     Calc specific heatloss to grond
#      Load data
#      Formula =Surf *(0,9671/(-7,455+(10,76+Bhulp)^0,5532+(9,773+Maaiveld)^0,6027+(0,0265+D79+delta_U)^-0,9226)+-0,0203)*fgw*fiak

#     Calc specific heatloss ventilation
#      Load data
#      Formula1 cp*qi*z
#      Formula2 cp*qv*fv

#       Save calc to date frame



