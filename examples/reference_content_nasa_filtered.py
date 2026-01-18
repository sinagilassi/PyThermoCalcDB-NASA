# reference content
REFERENCE_CONTENT = """
REFERENCES:
  CUSTOM-REF-1:
    DATABOOK-ID: 1
    TABLES:
      NASA9-1:
        TABLE-ID: 1
        DESCRIPTION: This table provides the 9-coefficient NASA polynomial parameters, from 200 to 1000 K.
        EQUATIONS:
          EQ-1:
            BODY:
            - res['nasa9-1 | nasa9_200_1000_K | 1'] = parms['a1 | a1 | 1'] + parms['a2 | a2 | 1'] + parms['a3 | a3 | 1'] + parms['a4 | a4 | 1'] + parms['a5 | a5 | 1'] + parms['a6 | a6 | 1'] + parms['a7 | a7 | 1'] + parms['b1 | b1 | 1'] + parms['b2 | b2 | 1'] + args['temperature | T | K'] + parms['Molecular-Weight | MW | 1']
            BODY-INTEGRAL: None
            BODY-FIRST-DERIVATIVE: None
            BODY-SECOND-DERIVATIVE: None
        STRUCTURE:
          COLUMNS: [Name, Formula, State, Formula-Raw, Phase-Flag, Molecular-Weight, Enthalpy-of-Formation, Minimum-Temperature, Maximum-Temperature, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, Eq]
          SYMBOL: [None, None, None, None, None, MW, EnFo_IG, Tmin, Tmax, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, nasa9_200_1000_K]
          UNIT: [None, None, None, None, None, g/mol, J/mol, K, K, J/mol, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        VALUES:
        - [methane, CH4, g, C   1.00H   4.00    0.00    0.00    0.00, 0, 16.04246, -74600, 200, 1000, 10016.198, -176654.573, 2785.47782, -12.0193547, 0.039146259, -3.61e-05, 2.02e-08, -4.96e-12, -23310.1156, 89.0107539, 1]
        - [methanol, CH4O, g, C   1.00H   4.00O   1.00    0.00    0.00, 0, 32.04186, -200940, 200, 1000, 11435.277, -241663.747, 4032.13812, -20.4640954, 0.069036793, -7.6e-05, 4.6e-08, -1.16e-11, -44332.5697, 140.013886, 1]
        - [carbon dioxide, CO2, g, C   1.00O   2.00    0.00    0.00    0.00, 0, 44.0095, -393510, 200, 1000, 9365.469, 49437.8364, -626.429208, 5.30181336, 0.002503601, -2.12e-07, -7.69e-10, 2.85e-13, -45281.8986, -7.0487901, 1]
        - [ethanol, C2H6O, g, C   2.00H   6.00O   1.00    0.00    0.00, 0, 46.06844, -234950, 200, 1000, 14541.926, -234281.0005, 4479.20556, -27.44830238, 0.10886825, -0.000130531, 8.44e-08, -2.23e-11, -50222.4115, 176.4836305, 1]
        - [benzene, C6H6, g, C   6.00H   6.00    0.00    0.00    0.00, 0, 78.11184, 82880, 200, 1000, 14194.791, -168282.654, 4412.51452, -37.2206393, 0.164191815, -0.000202322, 1.31e-07, -3.45e-11, -10392.5432, 217.2442068, 1]
        - [dihydrogen, H2, g, H   2.00    0.00    0.00    0.00    0.00, 0, 2.01588, 0, 200, 1000, 8468.102, 40783.2281, -800.918545, 8.21470167, -0.012697144, 1.75e-05, -1.2e-08, 3.37e-12, 2682.48438, -30.4378866, 1]
        - [dinitrogen, N2, g, N   2.00    0.00    0.00    0.00    0.00, 0, 28.01348, 0, 200, 1000, 8670.104, 22103.71497, -381.846182, 6.08273836, -0.008530914, 1.38e-05, -9.63e-09, 2.52e-12, 710.846086, -10.76003316, 1]
        - [dioxygen, O2, g, O   2.00    0.00    0.00    0.00    0.00, 0, 31.9988, 0, 200, 1000, 8680.104, -34255.6342, 484.700097, 1.119010961, 0.004293889, -6.84e-07, -2.02e-09, 1.04e-12, -3391.45487, 18.4969947, 1]
      NASA9-2:
        TABLE-ID: 2
        DESCRIPTION: This table provides the 9-coefficient NASA polynomial parameters, from 1000 to 6000 K.
        EQUATIONS:
          EQ-1:
            BODY:
            - res['nasa9-2 | nasa9_1000_6000_K | 1'] = parms['a1 | a1 | 1'] + parms['a2 | a2 | 1'] + parms['a3 | a3 | 1'] + parms['a4 | a4 | 1'] + parms['a5 | a5 | 1'] + parms['a6 | a6 | 1'] + parms['a7 | a7 | 1'] + parms['b1 | b1 | 1'] + parms['b2 | b2 | 1'] + args['temperature | T | K'] + parms['Molecular-Weight | MW | 1']
            BODY-INTEGRAL: None
            BODY-FIRST-DERIVATIVE: None
            BODY-SECOND-DERIVATIVE: None
        STRUCTURE:
          COLUMNS: [Name, Formula, State, Formula-Raw, Phase-Flag, Molecular-Weight, Enthalpy-of-Formation, Minimum-Temperature, Maximum-Temperature, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, Eq]
          SYMBOL: [None, None, None, None, None, MW, EnFo_IG, Tmin, Tmax, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, nasa9_1000_6000_K]
          UNIT: [None, None, None, None, None, g/mol, J/mol, K, K, J/mol, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        VALUES:
        - [methane, CH4, g, C   1.00H   4.00    0.00    0.00    0.00, 0, 16.04246, -74600, 1000, 6000, 10016.198, 3746265.7, -13888.5134, 20.5402982, -0.001944197, 4.32e-07, -4.06e-11, 1.64e-15, 75659.8868, -122.2977672, 1]
        - [methanol, CH4O, g, C   1.00H   4.00O   1.00    0.00    0.00, 0, 32.04186, -200940, 1000, 6000, 11435.277, 3411560.75, -13454.9745, 22.614046, -0.002141012, 3.73e-07, -3.5e-11, 1.37e-15, 56360.6386, -127.781226, 1]
        - [carbon dioxide, CO2, g, C   1.00O   2.00    0.00    0.00    0.00, 0, 44.0095, -393510, 1000, 6000, 9365.469, 117696.9434, -1788.801467, 8.29154353, -9.22e-05, 4.87e-09, -1.89e-12, 6.33e-16, -39083.4501, -26.52683962, 1]
        - [ethanol, C2H6O, g, C   2.00H   6.00O   1.00    0.00    0.00, 0, 46.06844, -234950, 1000, 6000, 14541.926, 4694781.59, -19297.89472, 34.4757599, -0.00323613, 5.78e-07, -5.56e-11, 2.23e-15, 86015.652, -203.4795998, 1]
        - [benzene, C6H6, g, C   6.00H   6.00    0.00    0.00    0.00, 0, 78.11184, 82880, 1000, 6000, 14194.791, 4549770.27, -22615.3394, 46.922072, -0.004196808, 7.87e-07, -7.92e-11, 3.3e-15, 139238.84, -286.7689812, 1]
        - [dihydrogen, H2, g, H   2.00    0.00    0.00    0.00    0.00, 0, 2.01588, 0, 1000, 6000, 8468.102, 560812.338, -837.149134, 2.97536304, 0.00125225, -3.74e-07, 5.94e-11, -3.61e-15, 5339.81585, -2.20276405, 1]
        - [dinitrogen, N2, g, N   2.00    0.00    0.00    0.00    0.00, 0, 28.01348, 0, 1000, 6000, 8670.104, 587712.406, -2239.249073, 6.06694922, -0.000613969, 1.49e-07, -1.92e-11, 1.06e-15, 12832.10415, -15.86639599, 1]
        - [dioxygen, O2, g, O   2.00    0.00    0.00    0.00    0.00, 0, 31.9988, 0, 1000, 6000, 8680.104, -1037939.022, 2344.830282, 1.819732036, 0.001267848, -2.19e-07, 2.05e-11, -8.19e-16, -16890.10929, 17.38716506, 1]
      NASA9-3:
        TABLE-ID: 2
        DESCRIPTION: This table provides the 9-coefficient NASA polynomial parameters, from 6000 to 20000 K.
        EQUATIONS:
          EQ-1:
            BODY:
            - res['nasa9-3 | nasa9_6000_20000_K | 1'] = parms['a1 | a1 | 1'] + parms['a2 | a2 | 1'] + parms['a3 | a3 | 1'] + parms['a4 | a4 | 1'] + parms['a5 | a5 | 1'] + parms['a6 | a6 | 1'] + parms['a7 | a7 | 1'] + parms['b1 | b1 | 1'] + parms['b2 | b2 | 1'] + args['temperature | T | K'] + parms['Molecular-Weight | MW | 1']
            BODY-INTEGRAL: None
            BODY-FIRST-DERIVATIVE: None
            BODY-SECOND-DERIVATIVE: None
        STRUCTURE:
          COLUMNS: [Name, Formula, State, Formula-Raw, Phase-Flag, Molecular-Weight, Enthalpy-of-Formation, Minimum-Temperature, Maximum-Temperature, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, Eq]
          SYMBOL: [None, None, None, None, None, MW, EnFo_IG, Tmin, Tmax, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2, nasa9_6000_20000_K]
          UNIT: [None, None, None, None, None, g/mol, J/mol, K, K, J/mol, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        VALUES:
        - [carbon dioxide, CO2, g, C   1.00O   2.00    0.00    0.00    0.00, 0, 44.0095, -393510, 6000, 20000, 9365.469, -1544406228, 1016836.139, -256.1377096, 0.033693639, -2.18e-06, 6.99e-11, -8.84e-16, -8043128.5, 2254.153243, 1]
        - [dihydrogen, H2, g, H   2.00    0.00    0.00    0.00    0.00, 0, 2.01588, 0, 6000, 20000, 8468.102, 496671613, -314744.812, 79.838875, -0.008414504, 4.75e-07, -1.37e-11, 1.61e-16, 2488354.66, -669.552419, 1]
        - [dinitrogen, N2, g, N   2.00    0.00    0.00    0.00    0.00, 0, 28.01348, 0, 6000, 20000, 8670.104, 831013916, -642073.354, 202.0264635, -0.03065092, 2.49e-06, -9.71e-11, 1.44e-15, 4938707.04, -1672.099736, 1]
        - [dioxygen, O2, g, O   2.00    0.00    0.00    0.00    0.00, 0, 31.9988, 0, 6000, 20000, 8680.104, 497529430, -286610.6874, 66.9035225, -0.006169959, 3.02e-07, -7.42e-12, 7.28e-17, 2293554.027, -553.062161, 1]
"""
