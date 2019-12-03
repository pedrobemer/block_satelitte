import numpy as np
import numpy.matlib
import math

def update_to_float_format(float_number):
    if (float_number[0] != '-'):
        phi_error_list = list(float_number)
        phi_error_list[1] = '.'
    else:
        phi_error_list = list(float_number)
        phi_error_list[2] = '.'

    float_number = "".join(phi_error_list)
    try:
        float_number, _ = float_number.split("\n")
    except ValueError:
            pass

    return float(float_number)

n_repetitions = 10
barker_code = np.real([-1.0000 - 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j, 
                       -1.0000 - 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j,
                       1.0000 + 1.0000j, -1.0000 - 1.0000j, -1.0000 - 1.0000j,
                       1.0000 + 1.0000j, -1.0000 - 1.0000j,  1.0000 + 1.0000j, 
                       -1.0000 - 1.0000j])

preamble = np.matlib.repmat(barker_code, 1, n_repetitions)[0]

filename = "ex2_iq1.txt"
f = open(filename, "r")

for line in f:
    try:
        _, k, preamble_real, _, preamble_imag = line.split(" ")
    except ValueError:
        continue
    else:  
        k,_ = k.split(":")
        k = int(k)
        preamble_real = update_to_float_format(preamble_real)
        _, preamble_imag = preamble_imag.split("j")
        preamble_imag = update_to_float_format(preamble_imag)
        mag_rec_preamble = math.sqrt(preamble_real**2 + preamble_imag**2)
        phase_rec_preamble = math.atan2(preamble_imag, preamble_real)
        phase_tx_preamble = math.atan2(0,preamble[k])
        phase_error = phase_tx_preamble - phase_rec_preamble
        noise_real = preamble[k] - preamble_real
        noise_imag = 0 - preamble_imag
        mag_noise = math.sqrt(noise_real**2 + noise_imag**2)
        power_tx_preamble = preamble[k]**2
        power_rec_preamble = mag_rec_preamble**2
        power_noise = mag_noise**2
        snr_watts = power_rec_preamble/power_noise
        print(preamble_real," + ",preamble_imag,"j")
        print("Received Phase:",phase_rec_preamble)
        print("Tranmitted Phase:", phase_tx_preamble)
        print("Phase Error:", phase_error)
        print("Received Magnitude:", mag_rec_preamble)
        print("Power Received Preamble(in Watts):", power_rec_preamble)
        print("Power Noise(in Watts):", power_noise)
        print("SNR(in Watts):",snr_watts)
        snr_db = 10*(math.log10(snr_watts))
        print("SNR(in dB):", snr_db)
