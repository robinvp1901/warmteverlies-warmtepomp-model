import pandas as pd

type_buitenmuur = "Buitenmuur"
type_muur_aangrenzend = "Binnenmuur"
type_vloer_bg = "Vloer-BG"

df = pd.read_csv("../database/data.csv", sep=',', skiprows=2).set_index('Naam')
df_building_outside = df[df["Type"] == type_buitenmuur]
df_building_adjacent = df[df["Type"] == type_muur_aangrenzend]
df_building_ground = df[df["Type"] == type_vloer_bg]


#  H_outside
df_H_outside = pd.DataFrame(df_building_outside["Eff Opp. [m]"] * (df_building_outside["U-Waarde contructie"] + df_building_outside["U-Waarde Thermische bruggen"]) * df_building_outside["fk"])
print(df_H_outside)
H_outside = df_H_outside.sum()
print(H_outside[0])


# H_adjacent
temp_i = 20
temp_e0 = -9
temp_a = 15
Ve_temp = 257.9
SpCeff = 50
Ceff = SpCeff * Ve_temp


Htot = 1.0
tauw = Ceff / Htot

delta_temp_e_tauw = 0.016 * tauw - 0.8
temp_e = temp_e0 + delta_temp_e_tauw
fiak = ((temp_i-temp_a)/(temp_i-temp_e))

df_H_adjacent = pd.DataFrame(df_building_adjacent["Eff Opp. [m]"] * (df_building_adjacent["U-Waarde contructie"] + df_building_adjacent["U-Waarde Thermische bruggen"]) * fiak)
H_adjacent = df_H_adjacent.sum()
print(H_adjacent[0])


# H_ground
dv = 0
Bhulp = 10.00860215

df_H_ground = pd.DataFrame(df_building_ground["Eff Opp. [m]"]
                           * (0.9671 / (-7.455 + (10.76 + Bhulp) ** 0.5532
                                        + (9.773 + dv) ** 0.6027
                                        + (0.0265 + df_building_ground["U-Waarde contructie"] + df_building_ground["U-Waarde Thermische bruggen"]) ** -0.9226)
                              + -0.0203) * df_building_ground["figk"] * df_building_ground["fgw"])
H_ground = df_H_ground.sum()
print(H_ground[0])


# H_ventilation

Au_temp = 99.396
Atot_temp = 51.194

cp = 1200
qis = 190 * 10**-5
qi = Au_temp * qis
z = 0.5

qv = Atot_temp * 0.0009
fv = 1

H_infiltration = cp * qi * z
H_filtration = cp * qv * fv

H_ventilation = pd.DataFrame(H_infiltration + H_filtration)
print("H_ventilation = " + H_ventilation + "W/K")
