import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import next_fast_len
from scipy.signal import freqz


def cic_interpolator(num_stages, num_samples_stage, interpolation_ratio):
    # Define CIC filter parameters
    N = num_stages
    M = num_samples_stage
    R = interpolation_ratio

    numerator = np.array([1] + [0] * (R * M - 1) + [-1])
    b = numerator
    denominator = np.array([1, -1])
    a = denominator
    for _ in range(N-1):
        b = np.convolve(b, numerator)
        a = np.convolve(a, denominator)

    return b, a


if __name__ == "__main__":
    N = 2
    M = 1
    R = 32

    b, a = cic_interpolator(N, M, R)

    # Compute the frequency response of the filter
    w, h = freqz(b, a, worN=next_fast_len(8000))

    print(f"h[0]: {np.abs(h[1]):.2f} = {20 * np.log10(abs(h[1])):.2f} dB")
    print(
        f"h[1/32]: {np.abs(h[len(h)//32]):.2f} = {20 * np.log10(abs(h[len(h)//32])):.2f} dB")

    # Plot the frequency response
    plt.figure()
    plt.plot(w / np.pi, 20 * np.log10(abs(h)), 'b')
    plt.title('CIC Interpolator Frequency Response')
    plt.xlabel('Frequency [rad/sample]')
    plt.ylabel('Amplitude [dB]')
    plt.grid(True)
    plt.show()
