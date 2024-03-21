import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Parameters
    N = 2  # Number of stages
    M = 1  # Differential delay
    R = 32  # Interpolation factor
    Fs = 96000  # Sampling frequency in Hz
    f_signal = 440  # Frequency of the sine wave in Hz
    duration = 1  # Duration of the signal in seconds

    # Generate the input signal (440Hz sine wave)
    t = np.linspace(0, duration, int(Fs * duration), endpoint=False)
    t_upsampled = np.linspace(
        0, duration, int(Fs * duration * R),
        endpoint=False)
    assert len(t) == len(t_upsampled) / R
    x = np.sin(2 * np.pi * f_signal * t)
    up_sampled = np.zeros(len(x) * R)
    up_sampled[::R] = x

    comb = np.array([0]*N)
    intr = np.array([0]*N)
    output = np.zeros(len(x)*R)
    for i in range(len(x)*R):  # i: upsampled signal index
        if i % R == 0:
            comb_in = x[i//R]
            s = np.zeros(N)
            s[0] = comb_in - comb[0]
            for j in range(1, N):
                s[j] = s[j-1] - comb[j]
            intr_in = s[-1]
            # Update sensitive list
            comb = np.roll(s, 1)
            comb[0] = comb_in
        else:
            intr_in = 0

        intr = intr + np.concatenate([[intr_in], intr[:-1]])

        output[i] = intr[-1]

    plt.plot(output)
    plt.title('Output Signal')
    plt.show()
