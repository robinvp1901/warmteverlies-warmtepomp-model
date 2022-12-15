# importeer libraries
# ==================
from temp import load_data_temp
from data import load_data_building, calc_heatloss_outside,\
    calc_heatloss_adjacent, calc_heatloss_ground, calc_heatloss_ventilation
from data import calc_variables_ventilation, calc_fiak, calc_figk
from dimensions import calc_volume, calc_surface, calc_bhulp


# Variables model
# ===============

#     Parameters import temperatuur
stationnumber = 260     # Stationummer KNMI
startdate = 20210101    # Start datum temperatuur
enddate = 20211231      # Eind datum temperatuur

#     Parameters temperatuur
t_in = 20               # Ontwerpbinnentemperatuur  [°C]
t_out = -9              # Ontwerpbuitentemperatuur  [°C]
t_corr1 = 3             # Correctie temperatuur delta1 [°C]
t_corr2 = -1            # Correctie temperatuur delta2 [°C]
t_average = 9           # Jaarlijks gemiddelde [°C]

#     Parameters warmtecapaciteit woning
sp_ceff = 50            # Specifieke capaciteit [Wh/(m³·K)]

#   Parameters aangrenzende woning
t_adj = 15              # Temperatuur aangrenzende woning [°C]
cz = 1                  # Zekeheids klasse [-]

#     Parameters luchtverversing
# t_corr_air = 0        # Correctie luchttemperatuur [°C]
cp = 1200              # Soortelijk warmte [J/(m³·K)]
z = 0.5             # Fractie infiltratie [-]
qis = 0.0019            # Luchtstroom infiltratie [m³/s per m²]
fv = 1                  # Correctiefactor inblaastemperaturen [-]

#     Parameters constructie woning
dv = 0                  # Diepte onder maaiveld [m]
fgw = 1                 #


# Start parameters
# ===============
tauw = 50


# load year temp
# ==============
load_data_temp(stationnumber, startdate, enddate)


# load data house
# ===============
df_building_outside, df_building_adjacent_sideways, df_building_adjacent_above_below, df_building_ground =\
    load_data_building()

# Calc dimensions
# ===============
volume = calc_volume(df_building_outside)
a_surf = calc_surface(df_building_outside)
bhulp, a_tot = calc_bhulp(df_building_outside, df_building_ground, df_building_adjacent_above_below)

# Calc variables
# ==============
c_eff, qi, qv = calc_variables_ventilation(volume, sp_ceff, qis, a_surf, a_tot)


#       Save calc to date frame

for i in range(10):

    # Calc variables
    # ==============

    t_out_corr = t_out + (0.016 * tauw * 0.8)
    fiak, fiak2 = calc_fiak(t_in, t_adj, t_out_corr, t_corr1)
    figk = calc_figk(t_in, t_corr2, t_average, t_out_corr)

    # Calc specific heatloss
    # ======================
    h_outside = calc_heatloss_outside(df_building_outside)  # Calc specific heatloss to outside
    h_adjacent_sideways = calc_heatloss_adjacent(df_building_adjacent_sideways, fiak)  # Calc specific heatloss to neighbours
    h_adjacent_above_below = calc_heatloss_adjacent(df_building_adjacent_above_below, fiak2)  # Calc specific heatloss to neighbours
    h_ground = calc_heatloss_ground(df_building_ground, bhulp, dv, figk, fgw)  # Calc specific heatloss to grond
    h_ventilation = calc_heatloss_ventilation(cp, qi, z, qv, fv)  # Calc specific heatloss ventilation

    h_tot = h_outside + h_adjacent_sideways + h_adjacent_above_below + h_ground + h_ventilation

    # Update tauw
    # ===========
    tauw = c_eff / h_tot

print(h_outside)
print(h_adjacent_sideways)
print(h_adjacent_above_below)
print(h_ground)
print(h_ventilation)
print(h_tot)

warmteverlies = h_tot * (t_in-t_out_corr)
print(warmteverlies)
