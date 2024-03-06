import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
import scipy.signal as signal


def adder(a: int, b: int) -> Tuple[int, int]:
    s = a + b
    c = 1 if (s & (1 << 32)) else 0
    return c, (s & ((1 << 32) - 1))


if __name__ == "__main__":
    MASH_ORDER = 3
    ITERATIONS = 65536
    DDS_T = 1024
    input = 1 << 8
    output = np.zeros(ITERATIONS, dtype=np.int32)

    # initial values
    s = np.array([0] * MASH_ORDER)
    c = np.array([0] * MASH_ORDER)
    last_s = np.array([0] * MASH_ORDER)
    q = np.array([0] * MASH_ORDER)
    f = np.array([0] * MASH_ORDER)

    for i in range(ITERATIONS):
        phase = i % DDS_T
        input = int((np.sin(2 * np.pi * phase / DDS_T) + 1) * (1 << 31))

        # ripple
        c[0], s[0] = adder(input, last_s[0])
        c[1], s[1] = adder(s[0], last_s[1])
        c[2], s[2] = adder(s[1], last_s[2])

        # noise cancelation logic
        f[2] = c[2]
        f[1] = c[1] - q[1] + f[2]
        f[0] = c[0] - q[0] + f[1]

        # update
        last_s[0] = s[0]
        last_s[1] = s[1]
        last_s[2] = s[2]
        q[0] = f[1]
        q[1] = f[2]
        q[2] = 0

        output[i] = f[0] + 3  # + (2**(MASH_ORDER - 1) - 1) to shift to positive

    # Design LPF
    order = 3  # Filter order
    fcutoff = 0.05
    b, a = signal.butter(order, fcutoff, 'low')

    # Apply LPF
    filtered_signal = signal.lfilter(b, a, output)
    print(f"Butterworth order: {order:d}, cutoff: {fcutoff:f}")
    print(f"average: {np.average(filtered_signal[100:]):e}")
    print(f"varance: {np.var(filtered_signal[100:]):e}")

    t = np.arange(0, ITERATIONS, 1)

    # Compute FFT of output and filtered_signal
    fft_output = np.fft.fft(output)
    fft_filtered_signal = np.fft.fft(filtered_signal)

    # Compute frequency axis
    freq = np.fft.fftfreq(len(output))

    # Create a new figure
    plt.figure(figsize=(12, 6))

    # Plot output
    plt.subplot(1, 2, 1)
    plt.plot(t, output, label='Output Signal')
    plt.plot(t, filtered_signal, label='Filtered Signal')
    plt.title('Output')
    plt.grid(True)

    # Plot FFT of output
    plt.subplot(1, 2, 2)
    plt.stem(freq, np.abs(fft_output))
    plt.stem(freq, np.abs(fft_filtered_signal), 'r')
    plt.title('FFT of Output')
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
