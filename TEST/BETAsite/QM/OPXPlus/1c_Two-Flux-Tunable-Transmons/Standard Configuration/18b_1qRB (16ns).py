"""
Performs a 1 qubit randomized benchmarking to measure the 1 qubit gate fidelity. This version is using directly the 'I'
& 'Q' data and should be used when there is no single-shot readout
"""
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from scipy.optimize import curve_fit
from configuration import *
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from qualang_tools.bakery.randomized_benchmark_c1 import c1_table
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import fetching_tool, progress_counter
from qm.simulate import SimulationConfig
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool

inv_gates = [int(np.where(c1_table[i, :] == 0)[0][0]) for i in range(24)]
max_circuit_depth = 1000
num_of_sequences = 40
n_avg = 60
seed = 345323
cooldown_time = 5000
qb = "q2_xy"
rr = "rr2"

# qmm = QuantumMachinesManager(host=qop_ip, port=9800, octave=octave_config, cluster_name=cluster_name)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)



def generate_sequence():
    cayley = declare(int, value=c1_table.flatten().tolist())
    inv_list = declare(int, value=inv_gates)
    current_state = declare(int)
    step = declare(int)
    sequence = declare(int, size=max_circuit_depth + 1)
    inv_gate = declare(int, size=max_circuit_depth + 1)
    i = declare(int)
    rand = Random(seed=seed)

    assign(current_state, 0)
    with for_(i, 0, i < max_circuit_depth, i + 1):
        assign(step, rand.rand_int(24))
        assign(current_state, cayley[current_state * 24 + step])
        assign(sequence[i], step)
        assign(inv_gate[i], inv_list[current_state])

    return sequence, inv_gate


def play_sequence(sequence_list, depth):
    i = declare(int)
    with for_(i, 0, i <= depth, i + 1):
        with switch_(sequence_list[i], unsafe=True):
            with case_(0):
                wait(pi_len // 4, qb)
            with case_(1):
                play("x180", qb)
            with case_(2):
                play("y180", qb)
            with case_(3):
                play("y180", qb)
                play("x180", qb)
            with case_(4):
                play("x90", qb)
                play("y90", qb)
            with case_(5):
                play("x90", qb)
                play("-y90", qb)
            with case_(6):
                play("-x90", qb)
                play("y90", qb)
            with case_(7):
                play("-x90", qb)
                play("-y90", qb)
            with case_(8):
                play("y90", qb)
                play("x90", qb)
            with case_(9):
                play("y90", qb)
                play("-x90", qb)
            with case_(10):
                play("-y90", qb)
                play("x90", qb)
            with case_(11):
                play("-y90", qb)
                play("-x90", qb)
            with case_(12):
                play("x90", qb)
            with case_(13):
                play("-x90", qb)
            with case_(14):
                play("y90", qb)
            with case_(15):
                play("-y90", qb)
            with case_(16):
                play("-x90", qb)
                play("y90", qb)
                play("x90", qb)
            with case_(17):
                play("-x90", qb)
                play("-y90", qb)
                play("x90", qb)
            with case_(18):
                play("x180", qb)
                play("y90", qb)
            with case_(19):
                play("x180", qb)
                play("-y90", qb)
            with case_(20):
                play("y180", qb)
                play("x90", qb)
            with case_(21):
                play("y180", qb)
                play("-x90", qb)
            with case_(22):
                play("x90", qb)
                play("y90", qb)
                play("x90", qb)
            with case_(23):
                play("-x90", qb)
                play("y90", qb)
                play("-x90", qb)


with program() as rb:
    depth = declare(int)
    saved_gate = declare(int)
    m = declare(int)
    n = declare(int)
    n_st = declare_stream()
    I = declare(fixed)
    Q = declare(fixed)
    I_st = declare_stream()
    Q_st = declare_stream()
    # update_frequency("q2_xy", 0)
    with for_(n, 0, n < n_avg, n + 1):
        save(n, n_st)
        with for_(m, 0, m < num_of_sequences, m + 1):
            sequence_list, inv_gate_list = generate_sequence()

            with for_(depth, 1, depth <= max_circuit_depth, depth + 1):
                # Replacing the last gate in the sequence with the sequence's inverse gate
                # The original gate is saved in 'saved_gate' and is being restored at the end
                assign(saved_gate, sequence_list[depth])
                assign(sequence_list[depth], inv_gate_list[depth - 1])

                wait(cooldown_time)

                align()

                play_sequence(sequence_list, depth)
                
                align()
                # Qubit-1
                # measure("readout", "rr1", None, dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q))
                # measure("readout", "rr2", None)
                # Qubit-2
                # measure("readout", "rr1", None)
                measure("readout", rr, None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I))
     
                save(I, I_st)
                assign(sequence_list[depth], saved_gate)
        

    with stream_processing():
        I_st.buffer(max_circuit_depth).buffer(num_of_sequences).average().save("I")
        n_st.save("iteration")

# job = qmm.simulate(config, rb, SimulationConfig(10000))
# job.get_simulated_samples().con1.plot()
# plt.show()

qm = qmm.open_qm(config)

job = qm.execute(rb)

# Get results from QUA program
results = fetching_tool(job, data_list=["I", "iteration"], mode="live")
# Live plotting
fig = plt.figure()
interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

x = np.linspace(1, max_circuit_depth, max_circuit_depth)
while results.is_processing():
    # Fetch results
    I, iteration = results.fetch_all()
    # Progress bar
    progress_counter(iteration, n_avg, start_time=results.get_start_time())
    # Plot results
    plt.cla()
    plt.plot(x, np.average(I, axis=0), ".", label="I")
    plt.xlabel("Number of Clifford gates")
    plt.legend()
    plt.pause(1.0)


def power_law(m, a, b, p):
    return a * (p**m) + b


data = I
value = np.average(data, axis=0)  # Can change to Q
error = np.std(data, axis=0)
pars, cov = curve_fit(
    f=power_law,
    xdata=x,
    ydata=value,
    p0=[0.5, 0.5, 0.9],
    bounds=(-np.inf, np.inf),
    maxfev=2000,
)
plt.figure()
plt.errorbar(x, value, yerr=error, marker=".")
plt.plot(x, power_law(x, *pars), linestyle="--", linewidth=2)

stdevs = np.sqrt(np.diag(cov))

print("#########################")
print("### Fitted Parameters ###")
print("#########################")
print(f"A = {pars[0]:.3} ({stdevs[0]:.1}), B = {pars[1]:.3} ({stdevs[1]:.1}), p = {pars[2]:.3} ({stdevs[2]:.1})")
print("Covariance Matrix")
print(cov)

one_minus_p = 1 - pars[2]
r_c = one_minus_p * (1 - 1 / 2**1)
r_g = r_c / 1.875  # 1.875 is the average number of gates in clifford operation
r_c_std = stdevs[2] * (1 - 1 / 2**1)
r_g_std = r_c_std / 1.875

print("#########################")
print("### Useful Parameters ###")
print("#########################")
print(
    f"Error rate: 1-p = {np.format_float_scientific(one_minus_p, precision=2)} ({stdevs[2]:.1})\n"
    f"Clifford set infidelity: r_c = {np.format_float_scientific(r_c, precision=2)} ({r_c_std:.1})\n"
    f"Gate infidelity: r_g = {np.format_float_scientific(r_g, precision=2)}  ({r_g_std:.1})"
)

plt.title("r_c: %s%%, r_g: %s%%" %(r_c*100, r_g*100))
plt.show()

np.savez(save_dir/"rb_values", value)