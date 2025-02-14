from pathlib import Path
import numpy as np
from set_octave import OctaveUnit, octave_declaration
from qualang_tools.config.waveform_tools import drag_gaussian_pulse_waveforms, flattop_gaussian_waveform, gaussian
from qualang_tools.units import unit


#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)

######################
# Network parameters #
######################
# Either using Cluster or Port:
cluster_name = "QPX_2"  # Write your cluster_name if version >= QOP220
qop_ip = "192.168.1.105"  # Write the QM router IP address
qop_port = None  # Write the QOP port if version < QOP220
# qop_ip = "qum.phys.sinica.edu.tw"  # Write the QM router IP address
# qop_port = 9800  # Write the QOP port if version < QOP220

###################
#   Data Saving   #
###################
# Path to save data
save_data = False
save_dir = r"D:\Ke Lab\SynologyDrive\09 Data\Fridge Data\Qubit\20231027_DR2_5XQ\01 Resonator Spectroscopy"
# save_dir = (Path().absolute()/"PYQUM"/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"data")

############################
# Set octave configuration #
############################
# Custom port mapping example
port_mapping = {
    ("con1", 1): ("octave1", "I1"),
    ("con1", 2): ("octave1", "Q1"),
    ("con1", 3): ("octave1", "I2"),
    ("con1", 4): ("octave1", "Q2"),
    ("con1", 5): ("octave1", "I3"),
    ("con1", 6): ("octave1", "Q3"),
    ("con1", 7): ("octave1", "I4"),
    ("con1", 8): ("octave1", "Q4"),
    ("con1", 9): ("octave1", "I5"),
    ("con1", 10): ("octave1", "Q5"),
}

# The Octave port is 11xxx, where xxx are the last three digits of the Octave internal IP that can be accessed from
# the OPX admin panel if you QOP version is >= QOP220. Otherwise, it is 50 for Octave1, then 51, 52 and so on.
octave_1 = OctaveUnit("octave1", qop_ip, port=11250, con="con1", clock="Internal", port_mapping=port_mapping)

# Add the octaves
octaves = [octave_1]
# Configure the Octaves
octave_config = octave_declaration(octaves)

#####################
# OPX configuration #
#####################

#############################################
#                  Qubits                   #
#############################################
qubit_LO_q1 = (4.200 -0.530) * u.GHz
qubit_LO_q2 = (4.200 -0.530) * u.GHz
qubit_LO_q3 = (4.200 -0.530) * u.GHz
qubit_LO_q4 = (4.200 -0.530) * u.GHz
qubit_LO_q5 = (4.200 -0.530) * u.GHz

# Qubits IF
qubit_IF = np.zeros(5)
qubit_IF[0] = (-347.022) * u.MHz #(4013-0.0088-0.0037 -4200) * u.MHz
qubit_IF[1] = (471.52 ) * u.MHz #(4156-0.119  -4200) * u.MHz
qubit_IF[2] = (-355) * u.MHz
qubit_IF[3] = (-44.4216-0.032) * u.MHz
qubit_IF[4] = (-44.4216-0.032) * u.MHz
# For comparing 2q:
# qubit_IF[1] = qubit_IF[0]

# Relaxation time
qubit1_T1 = int(12000 * u.ns)
qubit2_T1 = int(12000 * u.ns)
qubit3_T1 = int(12000 * u.ns)
qubit4_T1 = int(12000 * u.ns)
qubit5_T1 = int(12000 * u.ns)
thermalization_time = 5 * max(qubit1_T1, qubit2_T1, qubit3_T1, qubit4_T1, qubit5_T1)

# CW pulse parameter
const_len = 100
const_amp = 270 * u.mV
# Saturation_pulse
saturation_len = 1 * u.us
saturation_amp = 0.270
# Pi pulse parameters
pi_len = 32
pi_sigma = pi_len / 4
pi_amp_q1 = 0.1342
pi_amp_q2 = 0.2542
pi_amp_q3 = 0.5
pi_amp_q4 = 0.5
pi_amp_q5 = 0.5

# DRAG coefficients (# No DRAG when drag_coef_qi=0, it's just a gaussian.)
drag_coef_q1 = 0.68
drag_coef_q2 = 1.3
drag_coef_q3 = 0.5
drag_coef_q4 = 0
drag_coef_q5 = 0
anharmonicity_q1 = -(450.2-344.2)*2 * u.MHz
anharmonicity_q2 = -(470.7-369.2)*2 * u.MHz
anharmonicity_q3 = -(200) * u.MHz
anharmonicity_q4 = -(200) * u.MHz
anharmonicity_q5 = -(200) * u.MHz
AC_stark_detuning_q1 = -0.2 * u.MHz
AC_stark_detuning_q2 = 2.1 * u.MHz
AC_stark_detuning_q3 = 0 * u.MHz
AC_stark_detuning_q4 = 0 * u.MHz
AC_stark_detuning_q5 = 0 * u.MHz

# DRAG waveforms (x180)
x180_wf_q1, x180_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
x180_I_wf_q1, x180_Q_wf_q1 = x180_wf_q1, x180_der_wf_q1
x180_wf_q2, x180_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
x180_I_wf_q2, x180_Q_wf_q2 = x180_wf_q2, x180_der_wf_q2
x180_wf_q3, x180_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q3, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
x180_I_wf_q3, x180_Q_wf_q3 = x180_wf_q3, x180_der_wf_q3
x180_wf_q4, x180_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q4, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
x180_I_wf_q4, x180_Q_wf_q4 = x180_wf_q4, x180_der_wf_q4
x180_wf_q5, x180_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q5, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
x180_I_wf_q5, x180_Q_wf_q5 = x180_wf_q5, x180_der_wf_q5
# DRAG waveforms (x90)
x90_wf_q1, x90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1 / 2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
x90_I_wf_q1, x90_Q_wf_q1 = x90_wf_q1, x90_der_wf_q1
x90_wf_q2, x90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2 / 2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
x90_I_wf_q2, x90_Q_wf_q2 = x90_wf_q2, x90_der_wf_q2
x90_wf_q3, x90_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q3 / 2, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
x90_I_wf_q3, x90_Q_wf_q3 = x90_wf_q3, x90_der_wf_q3
x90_wf_q4, x90_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q4 / 2, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
x90_I_wf_q4, x90_Q_wf_q4 = x90_wf_q4, x90_der_wf_q4
x90_wf_q5, x90_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q5 / 2, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
x90_I_wf_q5, x90_Q_wf_q5 = x90_wf_q5, x90_der_wf_q5
# DRAG waveforms (-x90)
minus_x90_wf_q1, minus_x90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q1 / 2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
minus_x90_I_wf_q1, minus_x90_Q_wf_q1 = minus_x90_wf_q1, minus_x90_der_wf_q1
minus_x90_wf_q2, minus_x90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q2 / 2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
minus_x90_I_wf_q2, minus_x90_Q_wf_q2 = minus_x90_wf_q2, minus_x90_der_wf_q2
minus_x90_wf_q3, minus_x90_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q3 / 2, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
minus_x90_I_wf_q3, minus_x90_Q_wf_q3 = minus_x90_wf_q3, minus_x90_der_wf_q3
minus_x90_wf_q4, minus_x90_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q4 / 2, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
minus_x90_I_wf_q4, minus_x90_Q_wf_q4 = minus_x90_wf_q4, minus_x90_der_wf_q4
minus_x90_wf_q5, minus_x90_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q5 / 2, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
minus_x90_I_wf_q5, minus_x90_Q_wf_q5 = minus_x90_wf_q5, minus_x90_der_wf_q5
# DRAG waveforms (y180)
y180_wf_q1, y180_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
y180_I_wf_q1, y180_Q_wf_q1 = (-1) * y180_der_wf_q1, y180_wf_q1
y180_wf_q2, y180_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
y180_I_wf_q2, y180_Q_wf_q2 = (-1) * y180_der_wf_q2, y180_wf_q2
y180_wf_q3, y180_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q3, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
y180_I_wf_q3, y180_Q_wf_q3 = (-1) * y180_der_wf_q3, y180_wf_q3
y180_wf_q4, y180_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q4, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
y180_I_wf_q4, y180_Q_wf_q4 = (-1) * y180_der_wf_q4, y180_wf_q4
y180_wf_q5, y180_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q5, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
y180_I_wf_q5, y180_Q_wf_q5 = (-1) * y180_der_wf_q5, y180_wf_q5
# DRAG waveforms (y90)
y90_wf_q1, y90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1 / 2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
y90_I_wf_q1, y90_Q_wf_q1 = (-1) * y90_der_wf_q1, y90_wf_q1
y90_wf_q2, y90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2 / 2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
y90_I_wf_q2, y90_Q_wf_q2 = (-1) * y90_der_wf_q2, y90_wf_q2
y90_wf_q3, y90_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q3 / 2, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
y90_I_wf_q3, y90_Q_wf_q3 = (-1) * y90_der_wf_q3, y90_wf_q3
y90_wf_q4, y90_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q4 / 2, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
y90_I_wf_q4, y90_Q_wf_q4 = (-1) * y90_der_wf_q4, y90_wf_q4
y90_wf_q5, y90_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q5 / 2, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
y90_I_wf_q5, y90_Q_wf_q5 = (-1) * y90_der_wf_q5, y90_wf_q5
# DRAG waveforms (-y90)
minus_y90_wf_q1, minus_y90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q1 / 2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
minus_y90_I_wf_q1, minus_y90_Q_wf_q1 = (-1) * minus_y90_der_wf_q1, minus_y90_wf_q1
minus_y90_wf_q2, minus_y90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q2 / 2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
minus_y90_I_wf_q2, minus_y90_Q_wf_q2 = (-1) * minus_y90_der_wf_q2, minus_y90_wf_q2
minus_y90_wf_q3, minus_y90_der_wf_q3 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q3 / 2, pi_len, pi_sigma, drag_coef_q3, anharmonicity_q3, AC_stark_detuning_q3))
minus_y90_I_wf_q3, minus_y90_Q_wf_q3 = (-1) * minus_y90_der_wf_q3, minus_y90_wf_q3
minus_y90_wf_q4, minus_y90_der_wf_q4 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q4 / 2, pi_len, pi_sigma, drag_coef_q4, anharmonicity_q4, AC_stark_detuning_q4))
minus_y90_I_wf_q4, minus_y90_Q_wf_q4 = (-1) * minus_y90_der_wf_q4, minus_y90_wf_q4
minus_y90_wf_q5, minus_y90_der_wf_q5 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q5 / 2, pi_len, pi_sigma, drag_coef_q5, anharmonicity_q5, AC_stark_detuning_q5))
minus_y90_I_wf_q5, minus_y90_Q_wf_q5 = (-1) * minus_y90_der_wf_q5, minus_y90_wf_q5

##########################################
#               Flux line                #
##########################################
flux_settle_time = 100 * u.ns

max_frequency_point1 = 0
max_frequency_point2 = 0
max_frequency_point3 = 0
max_frequency_point4 = 0
max_frequency_point5 = 0

idle_q1 = max_frequency_point1 - 0.26
idle_q2 = max_frequency_point2 + 0.0
idle_q3 = max_frequency_point3 + 0.2
idle_q4 = max_frequency_point4 + 0.0
idle_q5 = max_frequency_point5 + 0.0

# Resonator frequency versus flux fit parameters according to resonator_spec_vs_flux
# amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset
amplitude_fit1, frequency_fit1, phase_fit1, offset_fit1 = [0, 0, 0, 0]
amplitude_fit2, frequency_fit2, phase_fit2, offset_fit2 = [0, 0, 0, 0]
amplitude_fit3, frequency_fit3, phase_fit3, offset_fit3 = [0, 0, 0, 0]
amplitude_fit4, frequency_fit4, phase_fit4, offset_fit4 = [0, 0, 0, 0]
amplitude_fit5, frequency_fit5, phase_fit5, offset_fit5 = [0, 0, 0, 0]

const_flux_len = 200
const_flux_amp = 0.45

##########################################
#               two-qubit                #
##########################################
cz_point_1_2_q2 = 0.14519591 # q1 - q2 = Ec
gft_cz_1_2_q2 = flattop_gaussian_waveform(cz_point_1_2_q2-idle_q2, 8 * u.ns, 8 * u.ns)
g_cz_1_2_q2 = 0.5 * abs(0.5-idle_q2) * gaussian(16, 16/4)

#############################################
#                Resonators                 #
#############################################
resonator_LO = 5.96 * u.GHz
# Resonators IF
resonator_IF = np.zeros(5)
resonator_IF[0] = int((-237) * u.MHz)
resonator_IF[1] = int((54.5) * u.MHz)
resonator_IF[2] = int((-124) * u.MHz) 
resonator_IF[3] = int((142.6) * u.MHz)
resonator_IF[4] = int((-50.5) * u.MHz)
# Above is for verifying wide-sweep results: -156, -38, 39, 137, 231

# Readout pulse parameters (optimal input for IQ-mixer: 125mV)
readout_len = 4000
readout_amp = np.zeros(5)
readout_amp[0] = 0.05
readout_amp[1] = 0.05
readout_amp[2] = 0.05
readout_amp[3] = 0.05
readout_amp[4] = 0.05

# TOF and depletion time
time_of_flight = 280  # must be a multiple of 4
depletion_time = int(1000/560) * u.us

opt_weights = False
if opt_weights:
    from qualang_tools.config.integration_weights_tools import convert_integration_weights

    weights_q1 = np.load("optimal_weights_q1.npz")
    opt_weights_real_q1 = convert_integration_weights(weights_q1["weights_real"])
    opt_weights_minus_imag_q1 = convert_integration_weights(weights_q1["weights_minus_imag"])
    opt_weights_imag_q1 = convert_integration_weights(weights_q1["weights_imag"])
    opt_weights_minus_real_q1 = convert_integration_weights(weights_q1["weights_minus_real"])
    weights_q2 = np.load("optimal_weights_q2.npz")
    opt_weights_real_q2 = convert_integration_weights(weights_q2["weights_real"])
    opt_weights_minus_imag_q2 = convert_integration_weights(weights_q2["weights_minus_imag"])
    opt_weights_imag_q2 = convert_integration_weights(weights_q2["weights_imag"])
    opt_weights_minus_real_q2 = convert_integration_weights(weights_q2["weights_minus_real"])
    weights_q3 = np.load("optimal_weights_q3.npz")
    opt_weights_real_q3 = convert_integration_weights(weights_q3["weights_real"])
    opt_weights_minus_imag_q3 = convert_integration_weights(weights_q3["weights_minus_imag"])
    opt_weights_imag_q3 = convert_integration_weights(weights_q3["weights_imag"])
    opt_weights_minus_real_q3 = convert_integration_weights(weights_q3["weights_minus_real"])
    weights_q4 = np.load("optimal_weights_q4.npz")
    opt_weights_real_q4 = convert_integration_weights(weights_q4["weights_real"])
    opt_weights_minus_imag_q4 = convert_integration_weights(weights_q4["weights_minus_imag"])
    opt_weights_imag_q4 = convert_integration_weights(weights_q4["weights_imag"])
    opt_weights_minus_real_q4 = convert_integration_weights(weights_q4["weights_minus_real"])
    weights_q5 = np.load("optimal_weights_q5.npz")
    opt_weights_real_q5 = convert_integration_weights(weights_q5["weights_real"])
    opt_weights_minus_imag_q5 = convert_integration_weights(weights_q5["weights_minus_imag"])
    opt_weights_imag_q5 = convert_integration_weights(weights_q5["weights_imag"])
    opt_weights_minus_real_q5 = convert_integration_weights(weights_q5["weights_minus_real"])
else:
    opt_weights_real_q1 = [(1.0, readout_len)]
    opt_weights_minus_imag_q1 = [(1.0, readout_len)]
    opt_weights_imag_q1 = [(1.0, readout_len)]
    opt_weights_minus_real_q1 = [(1.0, readout_len)]
    opt_weights_real_q2 = [(1.0, readout_len)]
    opt_weights_minus_imag_q2 = [(1.0, readout_len)]
    opt_weights_imag_q2 = [(1.0, readout_len)]
    opt_weights_minus_real_q2 = [(1.0, readout_len)]
    opt_weights_real_q3 = [(1.0, readout_len)]
    opt_weights_minus_imag_q3 = [(1.0, readout_len)]
    opt_weights_imag_q3 = [(1.0, readout_len)]
    opt_weights_minus_real_q3 = [(1.0, readout_len)]
    opt_weights_real_q4 = [(1.0, readout_len)]
    opt_weights_minus_imag_q4 = [(1.0, readout_len)]
    opt_weights_imag_q4 = [(1.0, readout_len)]
    opt_weights_minus_real_q4 = [(1.0, readout_len)]
    opt_weights_real_q5 = [(1.0, readout_len)]
    opt_weights_minus_imag_q5 = [(1.0, readout_len)]
    opt_weights_imag_q5 = [(1.0, readout_len)]
    opt_weights_minus_real_q5 = [(1.0, readout_len)]

# state discrimination
rotation_angle_q1 = (148.6 / 180) * np.pi
rotation_angle_q2 = (45.9 / 180) * np.pi
rotation_angle_q3 = (0 / 180) * np.pi
rotation_angle_q4 = (0 / 180) * np.pi
rotation_angle_q5 = (0 / 180) * np.pi
ge_threshold_q1 = 0.000909
ge_threshold_q2 = 0.000229
ge_threshold_q3 = 0
ge_threshold_q4 = 0
ge_threshold_q5 = 0

#############################################
#                  Config                   #
#############################################
config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                1: {"offset": 0.0},  # I readout line
                2: {"offset": 0.0},  # Q readout line
                3: {"offset": 0.0},  # I qubit1 XY
                4: {"offset": 0.0},  # Q qubit1 XY
                5: {"offset": 0.0},  # I qubit2 XY
                6: {"offset": 0.0},  # Q qubit2 XY
                7: {"offset": 0.0},  # I qubit3 XY
                8: {"offset": 0.0},  # Q qubit3 XY
                9: {"offset": 0.0},  # I qubit4 XY
                10: {"offset": 0.0},  # Q qubit4 XY
            },
            "digital_outputs": {
                1: {},
                3: {},
                5: {},
                7: {},
                10: {},
            },
            "analog_inputs": {
                1: {"offset": 0.006487780227661133+0.00832853277297247, "gain_db": 0},  # I from down-conversion
                2: {"offset": 0.004683707580566406+0.008599453735351563, "gain_db": 0},  # Q from down-conversion
            },
        },
    },
    "elements": {
        "rr1": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF[0],
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr2": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF[1],
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr3": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF[2],
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr4": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF[3],
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr5": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": resonator_IF[4],
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "q1_xy": {
            "mixInputs": {
                "I": ("con1", 3),
                "Q": ("con1", 4),
                "lo_frequency": qubit_LO_q1,
                "mixer": "octave_octave1_2",
            },
            "intermediate_frequency": qubit_IF[0],  # frequency at offset ch7 (max freq)
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
            },
        },
        "q2_xy": {
            "mixInputs": {
                "I": ("con1", 5),
                "Q": ("con1", 6),
                "lo_frequency": qubit_LO_q2,
                "mixer": "octave_octave1_3",
            },
            "intermediate_frequency": qubit_IF[1],  # frequency at offset ch8 (max freq)
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
            },
        },
        "q3_xy": {
            "mixInputs": {
                "I": ("con1", 7),
                "Q": ("con1", 8),
                "lo_frequency": qubit_LO_q3,
                "mixer": "octave_octave1_4",
            },
            "intermediate_frequency": qubit_IF[2],
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
            },
        },
        "q4_xy": {
            "mixInputs": {
                "I": ("con1", 9),
                "Q": ("con1", 10),
                "lo_frequency": qubit_LO_q4,
                "mixer": "octave_octave1_5",
            },
            "intermediate_frequency": qubit_IF[3],
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
        },
        # "q5_xy": {
        #     "mixInputs": {
        #         "I": ("con2", 1),
        #         "Q": ("con2", 2),
        #         "lo_frequency": qubit_LO_q5,
        #         "mixer": "octave_octave2_1",
        #     },
        #     "intermediate_frequency": qubit_IF[4],
        #     "operations": {
        #         "cw": "const_pulse",
        #         "saturation": "saturation_pulse",
        #         "x180": "x180_pulse_q5",
        #         "x90": "x90_pulse_q5",
        #         "-x90": "-x90_pulse_q5",
        #         "y90": "y90_pulse_q5",
        #         "y180": "y180_pulse_q5",
        #         "-y90": "-y90_pulse_q5",
        #     },
        # },
        # "q1_z": {
        #     "singleInput": {
        #         "port": ("con2", 5),
        #     },
        #     "operations": {
        #         "const": "const_flux_pulse",

        #     },
        # },
        # "q2_z": {
        #     "singleInput": {
        #         "port": ("con2", 6),
        #     },
        #     "operations": {
        #         "const": "const_flux_pulse",
        #         # options: gft_cz_pulse_1_2_q2, g_cz_pulse_1_2_q2
        #         "cz_1_2": "gft_cz_pulse_1_2_q2",
        #     },
        # },
        # "q3_z": {
        #     "singleInput": {
        #         "port": ("con2", 7),
        #     },
        #     "operations": {
        #         "const": "const_flux_pulse",
                
        #     },
        # },
        # "q4_z": {
        #     "singleInput": {
        #         "port": ("con2", 8),
        #     },
        #     "operations": {
        #         "const": "const_flux_pulse",

        #     },
        # },
        # "q5_z": {
        #     "singleInput": {
        #         "port": ("con2", 9),
        #     },
        #     "operations": {
        #         "const": "const_flux_pulse",
                
        #     },
        # },
        
    },
    "pulses": {
        # General:
        "const_flux_pulse": {
            "operation": "control",
            "length": const_flux_len,
            "waveforms": {
                "single": "const_flux_wf",
            },
        },
        "const_pulse": {
            "operation": "control",
            "length": const_len,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "saturation_pulse": {
            "operation": "control",
            "length": saturation_len,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
        },
        
        # Qubit-1:
        "x90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q1",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q1",
                "rotated_sin": "rotated_sine_weights_q1",
                "rotated_minus_sin": "rotated_minus_sine_weights_q1",
                "opt_cos": "opt_cosine_weights_q1",
                "opt_sin": "opt_sine_weights_q1",
                "opt_minus_sin": "opt_minus_sine_weights_q1",
            },
            "digital_marker": "ON",
        },
        # Qubit-2:
        "x90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q2",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q2",
                "rotated_sin": "rotated_sine_weights_q2",
                "rotated_minus_sin": "rotated_minus_sine_weights_q2",
                "opt_cos": "opt_cosine_weights_q2",
                "opt_sin": "opt_sine_weights_q2",
                "opt_minus_sin": "opt_minus_sine_weights_q2",
            },
            "digital_marker": "ON",
        },
        # Qubit-3:
        "x90_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
        },
        "readout_pulse_q3": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q3",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q3",
                "rotated_sin": "rotated_sine_weights_q3",
                "rotated_minus_sin": "rotated_minus_sine_weights_q3",
                "opt_cos": "opt_cosine_weights_q3",
                "opt_sin": "opt_sine_weights_q3",
                "opt_minus_sin": "opt_minus_sine_weights_q3",
            },
            "digital_marker": "ON",
        },
        # Qubit-4:
        "x90_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
        },
        "readout_pulse_q4": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q4",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q4",
                "rotated_sin": "rotated_sine_weights_q4",
                "rotated_minus_sin": "rotated_minus_sine_weights_q4",
                "opt_cos": "opt_cosine_weights_q4",
                "opt_sin": "opt_sine_weights_q4",
                "opt_minus_sin": "opt_minus_sine_weights_q4",
            },
            "digital_marker": "ON",
        },
        # Qubit-5:
        "x90_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
        },
        "readout_pulse_q5": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q5",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q5",
                "rotated_sin": "rotated_sine_weights_q5",
                "rotated_minus_sin": "rotated_minus_sine_weights_q5",
                "opt_cos": "opt_cosine_weights_q5",
                "opt_sin": "opt_sine_weights_q5",
                "opt_minus_sin": "opt_minus_sine_weights_q5",
            },
            "digital_marker": "ON",
        },

        # q1-q2:
        "gft_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": len(gft_cz_1_2_q2),
            "waveforms": {
                "single": "gft_cz_wf_1_2_q2",
            },
        },
        "g_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": len(g_cz_1_2_q2),
            "waveforms": {
                "single": "g_cz_wf_1_2_q2",
            },
        },

    },
    "waveforms": {
        # General:
        "const_wf": {"type": "constant", "sample": const_amp},
        "saturation_wf": {"type": "constant", "sample": saturation_amp},
        "const_flux_wf": {"type": "constant", "sample": const_flux_amp},
        "zero_wf": {"type": "constant", "sample": 0.0},

        # Qubit-1:
        "x90_I_wf_q1": {"type": "arbitrary", "samples": x90_I_wf_q1.tolist()},
        "x90_Q_wf_q1": {"type": "arbitrary", "samples": x90_Q_wf_q1.tolist()},
        "x180_I_wf_q1": {"type": "arbitrary", "samples": x180_I_wf_q1.tolist()},
        "x180_Q_wf_q1": {"type": "arbitrary", "samples": x180_Q_wf_q1.tolist()},
        "minus_x90_I_wf_q1": {"type": "arbitrary", "samples": minus_x90_I_wf_q1.tolist()},
        "minus_x90_Q_wf_q1": {"type": "arbitrary", "samples": minus_x90_Q_wf_q1.tolist()},
        "y90_I_wf_q1": {"type": "arbitrary", "samples": y90_I_wf_q1.tolist()},
        "y90_Q_wf_q1": {"type": "arbitrary", "samples": y90_Q_wf_q1.tolist()},
        "y180_I_wf_q1": {"type": "arbitrary", "samples": y180_I_wf_q1.tolist()},
        "y180_Q_wf_q1": {"type": "arbitrary", "samples": y180_Q_wf_q1.tolist()},
        "minus_y90_I_wf_q1": {"type": "arbitrary", "samples": minus_y90_I_wf_q1.tolist()},
        "minus_y90_Q_wf_q1": {"type": "arbitrary", "samples": minus_y90_Q_wf_q1.tolist()},
        "readout_wf_q1": {"type": "constant", "sample": readout_amp[0]},
        # Qubit-2:
        "x90_I_wf_q2": {"type": "arbitrary", "samples": x90_I_wf_q2.tolist()},
        "x90_Q_wf_q2": {"type": "arbitrary", "samples": x90_Q_wf_q2.tolist()},
        "x180_I_wf_q2": {"type": "arbitrary", "samples": x180_I_wf_q2.tolist()},
        "x180_Q_wf_q2": {"type": "arbitrary", "samples": x180_Q_wf_q2.tolist()},
        "minus_x90_I_wf_q2": {"type": "arbitrary", "samples": minus_x90_I_wf_q2.tolist()},
        "minus_x90_Q_wf_q2": {"type": "arbitrary", "samples": minus_x90_Q_wf_q2.tolist()},
        "y90_I_wf_q2": {"type": "arbitrary", "samples": y90_I_wf_q2.tolist()},
        "y90_Q_wf_q2": {"type": "arbitrary", "samples": y90_Q_wf_q2.tolist()},
        "y180_I_wf_q2": {"type": "arbitrary", "samples": y180_I_wf_q2.tolist()},
        "y180_Q_wf_q2": {"type": "arbitrary", "samples": y180_Q_wf_q2.tolist()},
        "minus_y90_I_wf_q2": {"type": "arbitrary", "samples": minus_y90_I_wf_q2.tolist()},
        "minus_y90_Q_wf_q2": {"type": "arbitrary", "samples": minus_y90_Q_wf_q2.tolist()},
        "readout_wf_q2": {"type": "constant", "sample": readout_amp[1]},
        # Qubit-3:
        "x90_I_wf_q3": {"type": "arbitrary", "samples": x90_I_wf_q3.tolist()},
        "x90_Q_wf_q3": {"type": "arbitrary", "samples": x90_Q_wf_q3.tolist()},
        "x180_I_wf_q3": {"type": "arbitrary", "samples": x180_I_wf_q3.tolist()},
        "x180_Q_wf_q3": {"type": "arbitrary", "samples": x180_Q_wf_q3.tolist()},
        "minus_x90_I_wf_q3": {"type": "arbitrary", "samples": minus_x90_I_wf_q3.tolist()},
        "minus_x90_Q_wf_q3": {"type": "arbitrary", "samples": minus_x90_Q_wf_q3.tolist()},
        "y90_I_wf_q3": {"type": "arbitrary", "samples": y90_I_wf_q3.tolist()},
        "y90_Q_wf_q3": {"type": "arbitrary", "samples": y90_Q_wf_q3.tolist()},
        "y180_I_wf_q3": {"type": "arbitrary", "samples": y180_I_wf_q3.tolist()},
        "y180_Q_wf_q3": {"type": "arbitrary", "samples": y180_Q_wf_q3.tolist()},
        "minus_y90_I_wf_q3": {"type": "arbitrary", "samples": minus_y90_I_wf_q3.tolist()},
        "minus_y90_Q_wf_q3": {"type": "arbitrary", "samples": minus_y90_Q_wf_q3.tolist()},
        "readout_wf_q3": {"type": "constant", "sample": readout_amp[2]},
        # Qubit-4:
        "x90_I_wf_q4": {"type": "arbitrary", "samples": x90_I_wf_q4.tolist()},
        "x90_Q_wf_q4": {"type": "arbitrary", "samples": x90_Q_wf_q4.tolist()},
        "x180_I_wf_q4": {"type": "arbitrary", "samples": x180_I_wf_q4.tolist()},
        "x180_Q_wf_q4": {"type": "arbitrary", "samples": x180_Q_wf_q4.tolist()},
        "minus_x90_I_wf_q4": {"type": "arbitrary", "samples": minus_x90_I_wf_q4.tolist()},
        "minus_x90_Q_wf_q4": {"type": "arbitrary", "samples": minus_x90_Q_wf_q4.tolist()},
        "y90_I_wf_q4": {"type": "arbitrary", "samples": y90_I_wf_q4.tolist()},
        "y90_Q_wf_q4": {"type": "arbitrary", "samples": y90_Q_wf_q4.tolist()},
        "y180_I_wf_q4": {"type": "arbitrary", "samples": y180_I_wf_q4.tolist()},
        "y180_Q_wf_q4": {"type": "arbitrary", "samples": y180_Q_wf_q4.tolist()},
        "minus_y90_I_wf_q4": {"type": "arbitrary", "samples": minus_y90_I_wf_q4.tolist()},
        "minus_y90_Q_wf_q4": {"type": "arbitrary", "samples": minus_y90_Q_wf_q4.tolist()},
        "readout_wf_q4": {"type": "constant", "sample": readout_amp[3]},
        # Qubit-5:
        "x90_I_wf_q5": {"type": "arbitrary", "samples": x90_I_wf_q5.tolist()},
        "x90_Q_wf_q5": {"type": "arbitrary", "samples": x90_Q_wf_q5.tolist()},
        "x180_I_wf_q5": {"type": "arbitrary", "samples": x180_I_wf_q5.tolist()},
        "x180_Q_wf_q5": {"type": "arbitrary", "samples": x180_Q_wf_q5.tolist()},
        "minus_x90_I_wf_q5": {"type": "arbitrary", "samples": minus_x90_I_wf_q5.tolist()},
        "minus_x90_Q_wf_q5": {"type": "arbitrary", "samples": minus_x90_Q_wf_q5.tolist()},
        "y90_I_wf_q5": {"type": "arbitrary", "samples": y90_I_wf_q5.tolist()},
        "y90_Q_wf_q5": {"type": "arbitrary", "samples": y90_Q_wf_q5.tolist()},
        "y180_I_wf_q5": {"type": "arbitrary", "samples": y180_I_wf_q5.tolist()},
        "y180_Q_wf_q5": {"type": "arbitrary", "samples": y180_Q_wf_q5.tolist()},
        "minus_y90_I_wf_q5": {"type": "arbitrary", "samples": minus_y90_I_wf_q5.tolist()},
        "minus_y90_Q_wf_q5": {"type": "arbitrary", "samples": minus_y90_Q_wf_q5.tolist()},
        "readout_wf_q5": {"type": "constant", "sample": readout_amp[4]},

        # q1-q2:
        "gft_cz_wf_1_2_q2": {"type": "arbitrary", "samples": gft_cz_1_2_q2},
        "g_cz_wf_1_2_q2": {"type": "arbitrary", "samples": g_cz_1_2_q2}

    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
    },
    "integration_weights": {
        # Default:
        "cosine_weights": {
            "cosine": [(1.0, readout_len)],
            "sine": [(0.0, readout_len)],
        },
        "sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(1.0, readout_len)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(-1.0, readout_len)],
        },

        # rotated q1:
        "rotated_cosine_weights_q1": {
            "cosine": [(np.cos(rotation_angle_q1), readout_len)],
            "sine": [(np.sin(rotation_angle_q1), readout_len)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-np.sin(rotation_angle_q1), readout_len)],
            "sine": [(np.cos(rotation_angle_q1), readout_len)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(np.sin(rotation_angle_q1), readout_len)],
            "sine": [(-np.cos(rotation_angle_q1), readout_len)],
        },
        # rotated q2:
        "rotated_cosine_weights_q2": {
            "cosine": [(np.cos(rotation_angle_q2), readout_len)],
            "sine": [(np.sin(rotation_angle_q2), readout_len)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-np.sin(rotation_angle_q2), readout_len)],
            "sine": [(np.cos(rotation_angle_q2), readout_len)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(np.sin(rotation_angle_q2), readout_len)],
            "sine": [(-np.cos(rotation_angle_q2), readout_len)],
        },
        # rotated q3:
        "rotated_cosine_weights_q3": {
            "cosine": [(np.cos(rotation_angle_q3), readout_len)],
            "sine": [(np.sin(rotation_angle_q3), readout_len)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-np.sin(rotation_angle_q3), readout_len)],
            "sine": [(np.cos(rotation_angle_q3), readout_len)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(np.sin(rotation_angle_q3), readout_len)],
            "sine": [(-np.cos(rotation_angle_q3), readout_len)],
        },
        # rotated q4:
        "rotated_cosine_weights_q4": {
            "cosine": [(np.cos(rotation_angle_q4), readout_len)],
            "sine": [(np.sin(rotation_angle_q4), readout_len)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(-np.sin(rotation_angle_q4), readout_len)],
            "sine": [(np.cos(rotation_angle_q4), readout_len)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(np.sin(rotation_angle_q4), readout_len)],
            "sine": [(-np.cos(rotation_angle_q4), readout_len)],
        },
        # rotated q5:
        "rotated_cosine_weights_q5": {
            "cosine": [(np.cos(rotation_angle_q5), readout_len)],
            "sine": [(np.sin(rotation_angle_q5), readout_len)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(-np.sin(rotation_angle_q5), readout_len)],
            "sine": [(np.cos(rotation_angle_q5), readout_len)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(np.sin(rotation_angle_q5), readout_len)],
            "sine": [(-np.cos(rotation_angle_q5), readout_len)],
        },

        # optimal weight for readout on q1:
        "opt_cosine_weights_q1": {
            "cosine": opt_weights_real_q1,
            "sine": opt_weights_minus_imag_q1,
        },
        "opt_sine_weights_q1": {
            "cosine": opt_weights_imag_q1,
            "sine": opt_weights_real_q1,
        },
        "opt_minus_sine_weights_q1": {
            "cosine": opt_weights_minus_imag_q1,
            "sine": opt_weights_minus_real_q1,
        },
        # optimal weight for readout on q2:
        "opt_cosine_weights_q2": {
            "cosine": opt_weights_real_q2,
            "sine": opt_weights_minus_imag_q2,
        },
        "opt_sine_weights_q2": {
            "cosine": opt_weights_imag_q2,
            "sine": opt_weights_real_q2,
        },
        "opt_minus_sine_weights_q2": {
            "cosine": opt_weights_minus_imag_q2,
            "sine": opt_weights_minus_real_q2,
        },
        # optimal weight for readout on q3:
        "opt_cosine_weights_q3": {
            "cosine": opt_weights_real_q3,
            "sine": opt_weights_minus_imag_q3,
        },
        "opt_sine_weights_q3": {
            "cosine": opt_weights_imag_q3,
            "sine": opt_weights_real_q3,
        },
        "opt_minus_sine_weights_q3": {
            "cosine": opt_weights_minus_imag_q3,
            "sine": opt_weights_minus_real_q3,
        },
        # optimal weight for readout on q4:
        "opt_cosine_weights_q4": {
            "cosine": opt_weights_real_q4,
            "sine": opt_weights_minus_imag_q4,
        },
        "opt_sine_weights_q4": {
            "cosine": opt_weights_imag_q4,
            "sine": opt_weights_real_q4,
        },
        "opt_minus_sine_weights_q4": {
            "cosine": opt_weights_minus_imag_q4,
            "sine": opt_weights_minus_real_q4,
        },
        # optimal weight for readout on q5:
        "opt_cosine_weights_q5": {
            "cosine": opt_weights_real_q5,
            "sine": opt_weights_minus_imag_q5,
        },
        "opt_sine_weights_q5": {
            "cosine": opt_weights_imag_q5,
            "sine": opt_weights_real_q5,
        },
        "opt_minus_sine_weights_q5": {
            "cosine": opt_weights_minus_imag_q5,
            "sine": opt_weights_minus_real_q5,
        },

    },

    "mixers": {
        # Control:
        "octave_octave1_2": [
            {
                "intermediate_frequency": qubit_IF[0],
                "lo_frequency": qubit_LO_q1,
                "correction": (1, 0, 0, 1),
            },
        ],
        "octave_octave1_3": [
            {
                "intermediate_frequency": qubit_IF[1],
                "lo_frequency": qubit_LO_q2,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave1_4": [
            {
                "intermediate_frequency": qubit_IF[2],
                "lo_frequency": qubit_LO_q3,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave1_5": [
            {
                "intermediate_frequency": qubit_IF[3],
                "lo_frequency": qubit_LO_q4,
                "correction": (1, 0, 0, 1),
            }
        ],
        "octave_octave2_1": [
            {
                "intermediate_frequency": qubit_IF[4],
                "lo_frequency": qubit_LO_q5,
                "correction": (1, 0, 0, 1),
            }
        ],

        # Readout:
        "octave_octave1_1": [
            {
                "intermediate_frequency": resonator_IF[0],
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF[1],
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF[2],
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF[3],
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
            {
                "intermediate_frequency": resonator_IF[4],
                "lo_frequency": resonator_LO,
                "correction": (1, 0, 0, 1),
            },
        ],

    },
}
