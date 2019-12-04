import matplotlib.pyplot as plt

#Update the phi error to the float notation in python
def update_phi_error_str(phi_error):
    if (phi_error[0] != '-'):
        phi_error_list = list(phi_error)
        phi_error_list[1] = '.'
        phi_error = "".join(phi_error_list)
        phi_error, _ = phi_error.split("\n")
    else:
        phi_error_list = list(phi_error)
        phi_error_list[2] = '.'
        phi_error = "".join(phi_error_list)
        phi_error, _ = phi_error.split("\n")
    return phi_error


#Global Variables
da_bw = "0.5"
filename = "ex1_bw_"+da_bw+".txt"
phi_error_data = []
phi_error_preamble = []
phi_error_pilot = []

f = open(filename, "r")
for line in f:
    try:
        _, important = line.split("Data")
    except ValueError:
        try:
            _, important = line.split("Pilot")
        except ValueError: 
            try:
                _, important = line.split("Preamble")
            except ValueError:
                continue
            else:
                # print(important)
                try:
                    _, phi_error = important.split("Phase Error: ")
                except ValueError:
                    continue
                phi_error = update_phi_error_str(phi_error)
                # print(float(phi_error))
                phi_error_preamble.append(float(phi_error))
        else:
            # print(important)
            try:
                _, phi_error = important.split("Phase Error: ")
            except ValueError:
                continue
            # print(phi_error)
            phi_error = update_phi_error_str(phi_error)
            # print(float(phi_error))
            phi_error_pilot.append(float(phi_error))

    else:
        # print(important)
        try:
            _, phi_error = important.split("Phase Error: ")
        except ValueError:
            continue
        phi_error = update_phi_error_str(phi_error)
        # print(float(phi_error))
        phi_error_data.append(float(phi_error))
        # print(phi_error_data)
        
pilot_len = len(phi_error_pilot)
preamble_len = len(phi_error_preamble)
data_len = len(phi_error_data)
# print(a)
# print(phi_error_pilot[a-1])
plt.figure(1)
plt.plot(range(pilot_len), phi_error_pilot)
plt.xlabel("Samples")
plt.ylabel("Phase Error (radians)")
plt.title("Phase Error for the Pilot Symbols with a BW of " + da_bw)
plt.figure(2)
plt.plot(range(preamble_len), phi_error_preamble)
plt.xlabel("Samples")
plt.ylabel("Phase Error (radians)")
plt.title("Phase Error for the Preamble Symbols with BW of " + da_bw)
plt.figure(3)
plt.plot(range(100000), phi_error_data[0:100000])
plt.xlabel("Samples")
plt.ylabel("Phase Error (radians)")
plt.title("Phase Error for the Payload Symbols with BW of " + da_bw)
plt.show()
