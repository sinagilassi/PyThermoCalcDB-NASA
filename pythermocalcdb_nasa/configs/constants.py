# import libs

# SECTION: PyThermoDBLink/PyThermoDB
DATASOURCE = "datasource"
EQUATIONSOURCE = "equationsource"


# SECTION: constants
R_J_molK = 8.314462618  # universal gas constant in J/mol.K
T_ref_K = 298.15  # reference temperature in K
P_ref_Pa = 101325.0  # reference pressure in Pa

# SECTION: NASA polynomial types
NASA7_MIN = "nasa7_min"
NASA7_MAX = "nasa7_max"
NASA9_MIN = "nasa9_min"
NASA9_MAX = "nasa9_max"

NASA_POLY_TYPES = (
    NASA7_MIN,
    NASA7_MAX,
    NASA9_MIN,
    NASA9_MAX
)

TEMPERATURE_BREAK_NASA7_K = 1000.0  # temperature break for NASA7 polynomials in K
TEMPERATURE_BREAK_NASA9_K = 1000.0  # temperature break for NASA7 polynomials in K
