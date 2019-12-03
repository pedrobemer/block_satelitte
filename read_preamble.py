import numpy as np
import numpy.matlib
import math
import cmath
import matplotlib.pyplot as plt


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
frame = 0
snr_db = []
for line in f:
    try:
        _, k, preamble_real, _, preamble_imag = line.split(" ")
    except ValueError:
        continue
    else:  
        k,_ = k.split(":")
        k = int(k)
        print(k,"-th Preamble Symbol")
        print("Transmitted Preamble:", preamble[k],  " + 0j")

        # Get from txt the imaginary and real part from the received preamble
        preamble_real = update_to_float_format(preamble_real)
        _, preamble_imag = preamble_imag.split("j")
        preamble_imag = update_to_float_format(preamble_imag)
        print("Preamble Symbols rotated:",preamble_real," + ",preamble_imag,"j")

        mag_rec_preamble = math.sqrt(preamble_real**2 + preamble_imag**2)
        phase_rec_preamble = math.atan2(preamble_imag, preamble_real)
        print("Received Phase:",phase_rec_preamble)

        phase_tx_preamble = math.atan2(0,preamble[k])
        power_tx_preamble = preamble[k]**2
        print("Tranmitted Phase:", phase_tx_preamble)

        phase_error = phase_tx_preamble - phase_rec_preamble
        print("Phase Error:", phase_error)
        # power_rec_preamble = mag_rec_preamble**2
        # power_rec_preamble = 
        # snr_watts = power_rec_preamble/power_noise
        
        fix_phase = complex(0,phase_error)
        received_sym = complex(preamble_real, preamble_imag)
        received_symbol_derotated = cmath.exp(fix_phase)*received_sym
        mag_rec_preamble_derotated = math.sqrt(received_symbol_derotated.real**2
                                               + received_symbol_derotated.imag**2)
        if (k == 0):  
            power_rec_preamble_derotated = 0.0 
        power_rec_preamble_derotated = power_rec_preamble_derotated + mag_rec_preamble_derotated**2

        print("Preamble Symbols derotated:", received_symbol_derotated)
        print("Received Magnitude(Symbols derotated):", mag_rec_preamble_derotated)
        print("Power Received derotated Preamble(in Watts):", power_rec_preamble_derotated)

        noise_real = preamble[k] - received_symbol_derotated.real
        noise_imag = 0 - received_symbol_derotated.imag
        mag_noise = math.sqrt(noise_real**2 + noise_imag**2)
        if (k == 0):
            power_noise = 0.0    
        power_noise = power_noise + mag_noise**2
        print("Power Noise(in Watts):", power_noise)


        if (k == 129):
            snr_watts = power_rec_preamble_derotated/power_noise
            print("Frame ",frame, "SNR(in Watts):",snr_watts)
            # snr_db = 10*(math.log10(snr_watts))
            snr_db.append(10*(math.log10(snr_watts)))
            print("Frame ",frame,"SNR(in dB):", 10*(math.log10(snr_watts)))
            frame = frame + 1

        print("\n") 

        # if(power_rec_preamble_derotated != 0):
        #     try:
        #         snr_watts = power_rec_preamble_derotated/power_noise    
        #     except (ZeroDivisionError or ValueError):
        #         snr_watts = "inf"
        #         print("SNR(in Watts):",snr_watts) 
        #     else:            
        #         print("SNR(in Watts):",snr_watts)
        #         snr_db = 10*(math.log10(snr_watts))
        #         print("SNR(in dB):", snr_db)
        #         print("\n")
        # else:
        #     print("Symbol Error")

n_frames = len(snr_db)
plt.figure(1)
plt.plot(range(n_frames), snr_db)
plt.xlabel("Frame")
plt.ylabel("SNR in dB")
plt.show()