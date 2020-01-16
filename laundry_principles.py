import pandas as pd
import Aisle
import easygui, time, datetime
from subprocess import Popen

BRAND_DICT = {"Pantene": ["PANT"],
              "Dove": ["DOVE"],
              "Head & Shoulders": ["H&S ", "OLD SPC 2N1 SWAGGER SHMP"],
              "Herbal Essences": ["HERB ES"],
              "OGX": ["OGX"],
              "El Vive": ["LORL"],
              "Purex": ["PUREX"],
              "Gain": ["GAIN"],
              "PC": ["PC 2X LIQ","PC 4X LIQ", "PC LIQ", "PC LQ", "PC FAB", "PC FREE", "PC ORIGINAL SINGLE DOSE"],
              "Arm & Hammer": ["A&H", "ARM & HAMMER"],
              "Sunlight": ["SNLGHT", "SUNLIGHT", "SUNL "],
              "Persil": ["PERSIL"],
              "NN": ["NN "],
              "Ivory Snow": ["IVORY SNOW"],
              "Downy": ["DOWNY U", "DOWNY FP"],
              "Woolite": ["WOOLITE"],
              "Tide": ["TIDE P", "TIDE L"],
              "Tide Simply": ["TIDE SMP"]}
SUBBRAND_DICT = {"Dove Dermacare": ["DOVE DRMCR"],
                 "Pantene Daily Moisture Renewal": ["PANT DLY M"],
                 "Pantene Repair and Protect": ["PANT RPR"],
                 "Head & Shoulders Classic Clean": ["H&S 2N1 CLS", "H&S CLSC"],
                 "Head & Shoulders Dry Scalp": ["H&S 2N1 DRY", "H&S DRY"],
                 "Herbal Essences Biorenew": ["HRB ES BIO", "HRB ES CCMBR", "HRB ES REPAIR", "HRB ES MOISTURE COCO",
                                              "HRB ES VOL COFFEE", "HRB ES RNW MCLR", "HRB ES RV GRPFRT",
                                              "HRB ES SMOOTH"],
                 "Head & Shoulders Dry": ["H&S DRY", "H&S 2N1 DRY"],
                 "Head & Shoulders Men": ["H&S 2N1 MEN", "H&S MEN"],
                 "Head & Shoulders Women": ["H&S 2N1 CHARCOAL", "H&S RPR&PRT SHAMPOO", "H&S VOLUME BOOST SHMP",
                                             "H&S SMTH & SLKY SHAMPOO", "H&S SMTH & SLKY CONDTIONR",
                                             "H&S DEEP MOISTURE COND", "H&S DEEP MOISTURE SHMP"]}
GOLDEN_DICT = {"All SKUs": ["8087817704", "8087818122", "8087806220", "8087818116", "8087818115",
                            "8087818121", "8087818119", "8087818118", "8087818619", "8087818617",
                            "8087818616", "8087818620", "8087818621", "8087818239", "8087818105",
                            "8087818109", "8087817226"],
               "Top Shelf": ["8087817704", "8087818122", "8087806220", "8087818116", "8087818115",
                             "8087818121", "8087818119", "8087818118"],
               "Bottom Shelf": ["8087817704", "8087818122", "8087806220", "8087818116", "8087818115",
                                "8087818121", "8087818119", "8087818118"],
               "Middle Shelves": ["8087818619", "8087818617", "8087818616", "8087818620", "8087818621"]}

DOSE_DICT = {"Unit Dose": ["PAKS", "FLINGS", "DOSE", "PACS", "PODS"],
             "Powder": ["PWD", "POWDER"],
             "Beads": ["UNSTOPABLES"],
             "Sunlight Powder": ["SNLGHT LEMON FRESH PWD"],
             "Tide Unit Dose": ["TIDE LIQUID PODS", "TIDE LQ PODS", "TIDE PODS"],
             "Arm & Hammer Unit Dose": ["A&H OXI TRPL PWR PAKS", "A&H 3 IN 1 POWER PAKS"],
             "Gain Unit Dose": ["GAIN FLINGS"],
             "PC Unit Dose": ["PC FREE SINGLE DOSE", "PC ORIGINAL SINGLE DOSE"],
             "Sunlight Unit Dose": ["SUNL PWRCRE SNGLDOSE", "SUNL PWRONE SNGL DOSE", "SUNL PWRONE SNGLDOSE", "SUNLIGHT PACS"],
             "Tide Powder": ["TIDE POWDER", "TIDE PWDR"]}

if __name__ == "__main__":
    print("Program is starting. One moment please.")
    easygui.msgbox(msg="Please pick a folder to store your output files.", ok_button=("Pick Folder..."))
    output_folder = easygui.diropenbox()
    easygui.msgbox(msg="Please pick a POG file", ok_button=("Pick File..."))
    pog_file = easygui.fileopenbox(title="Pick a Pog csv", filetypes=".csv")
    start_time = time.time()
    hair_pog = pd.read_csv(pog_file)
    headers = ["Planogram"]
    principle_template = pd.DataFrame(index=[0], columns=headers)

    #Calling principles from the aisle class and making a df out of the results
    for i in hair_pog.drop_duplicates(subset=["POG_NAME"]).index:  # select each unique POG ID
        id = hair_pog.at[i, "POG_NAME"]
        print(id)
        if ' LAUNDRY_DETERGENT_40X72_ECONO_DISCOUNT_WEST ' in str(id):
            pass
        aisle = Aisle.Aisle(hair_pog, id)
        # testing each principle
        principle1 = aisle.is_in_vertical_block(BRAND_DICT["Purex"])
        principle2 = aisle.is_in_vertical_block(BRAND_DICT["Gain"])
        principle3 = aisle.is_in_vertical_block(BRAND_DICT["PC"])
        principle4 = aisle.is_in_vertical_block(BRAND_DICT["Arm & Hammer"])
        principle5 = aisle.is_in_vertical_block(BRAND_DICT["Sunlight"])
        principle6 = aisle.is_in_vertical_block(BRAND_DICT["Persil"])
        principle7 = aisle.is_in_vertical_block(BRAND_DICT["NN"])
        principle8 = aisle.is_in_vertical_block(BRAND_DICT["Ivory Snow"])
        principle9 = aisle.is_in_vertical_block(BRAND_DICT["Downy"])
        principle10 = aisle.is_in_vertical_block(BRAND_DICT["Woolite"])
        principle11 = aisle.is_leading_aisle(BRAND_DICT["Tide"])
        principle12 = aisle.is_at_eye_level(DOSE_DICT["Arm & Hammer Unit Dose"])
        principle13 = aisle.is_at_eye_level(DOSE_DICT["Tide Unit Dose"])
        principle14 = aisle.is_at_eye_level(DOSE_DICT["Gain Unit Dose"])
        principle15 = aisle.is_at_eye_level(DOSE_DICT["PC Unit Dose"])
        principle16 = aisle.is_at_eye_level(DOSE_DICT["Sunlight Unit Dose"])
        principle17 = aisle.is_on_bottom_shelf(DOSE_DICT["Sunlight Powder"])
        principle18 = aisle.is_on_bottom_shelf(DOSE_DICT["Tide Powder"])
        principle19 = not aisle.is_not_in_between(BRAND_DICT["Tide Simply"],BRAND_DICT["Sunlight"],BRAND_DICT["Purex"])
        principle20 = aisle.is_on_shelf(DOSE_DICT["Beads"])
        principle21 = aisle.is_in_vertical_block(BRAND_DICT["Tide"])

        # writing each principle to the appropriate header
        principle_template.at[id, "Planogram"] = id
        principle_template.at[id, "Purex in Vertical Block"] = principle1
        principle_template.at[id, "Gain in Vertical Block"] = principle2
        principle_template.at[id, "PC in Vertical Block"] = principle3
        principle_template.at[id, "Arm & Hammer in Vertical Block"] = principle4
        principle_template.at[id, "Sunlight in Vertical Block"] = principle5
        principle_template.at[id, "Persil in Vertical Block"] = principle6
        principle_template.at[id, "NN in Vertical Block"] = principle7
        principle_template.at[id, "Ivory Snow in Vertical Block"] = principle8
        principle_template.at[id, "Downy in Vertical Block"] = principle9
        principle_template.at[id, "Woolite in Vertical Block"] = principle10
        principle_template.at[id, "Tide Leads the Aisle"] = principle11
        principle_template.at[id, "A&H Unit Dose at Eye Level"] = principle12
        principle_template.at[id, "Tide Unit Dose at Eye Level"] = principle13
        principle_template.at[id, "Gain Unit Dose at Eye Level"] = principle14
        principle_template.at[id, "PC Unit Dose at Eye Level"] = principle15
        principle_template.at[id, "Sunlight Unit Dose at Eye Level"] = principle16
        principle_template.at[id, "Sunlight Powder on Bottom Shelf"] = principle17
        principle_template.at[id, "Tide Powder on Bottom Shelf"] = principle18
        principle_template.at[id, "Tide Simply is between Sunlight and Purex"] = principle19
        principle_template.at[id, "Beads are on Shelf"] = principle20
        principle_template.at[id, "Tide in Vertical Block"] = principle21

    try:
        principle_template.to_csv(str(output_folder) + "\\output_file.csv")
        Popen(str(output_folder) + "\\output_file.csv", shell=True)
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        easygui.msgbox("You cannot open two excel files with the same name.")
