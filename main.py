import time

import spidev
from numpy import fft, array, argmax, absolute, delete

spi_ch = 0

# Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

# sampling
samplingPeriod = 1 / 16384
sampleSize = 256


def read_adc(adc_ch):
    # Make sure ADC channel is 0 or 1
    if adc_ch != 0:
        adc_ch = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + adc_ch) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    return adc


# Report the channel 0 and channel 1 voltages to the terminal
try:
    while True:
        # adc = read_adc(0)
        # print(adc)
        samples = []
        for i in range(sampleSize):
            samples.append(read_adc(0))
            time.sleep(samplingPeriod)
        samples = array(samples)

        spectrum = fft.rfft(samples)
        spectrum = delete(spectrum, 0)

        results = absolute(spectrum)
        freq = fft.rfftfreq(n=sampleSize, d=samplingPeriod)

        index = argmax(results)
        frequency = freq[index]
        frequency = frequency - (frequency * 0.66)
        print("frequency = " + str(frequency))
        # plt.plot(freq, results)
        # plt.xlabel("frequency, Hz")
        # plt.ylabel("Amplitude, units")
        # plt.show()
        # time.sleep(0.2)


finally:
    # GPIO.cleanup()
    print("success?")
