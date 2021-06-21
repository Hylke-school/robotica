import config
import spidev
from numpy import fft, array, argmax, absolute, delete
import time

spi = spidev.SpiDev(config.SPI_BUS, config.ADC_CHANNEL)
spi.max_speed_hz = config.SPIDEV_BAUD_RATE


class Microphone:
    def __init__(self):

        pass

    @staticmethod
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

    def get_data(self):
        # adc = read_adc(0)
        # print(adc)
        samples = []
        for i in range(config.MIC_SAMPLE_SIZE):
            samples.append(self.read_adc(config.ADC_CHANNEL))
            time.sleep(config.MIC_SAMPLING_PERIOD)
        samples = array(samples)

        spectrum = fft.rfft(samples)
        spectrum = delete(spectrum, 0)

        results = absolute(spectrum)
        freq = fft.rfftfreq(n=config.MIC_SAMPLE_SIZE, d=config.MIC_SAMPLING_PERIOD)

        index = argmax(results)
        frequency = freq[index]
        # Fixing the scale of read frequency.
        frequency = frequency - (frequency * 0.66)

        # print("frequency = " + str(frequency))
        # plt.plot(freq, results)
        # plt.xlabel("frequency, Hz")
        # plt.ylabel("Amplitude, units")
        # plt.show()
        # time.sleep(0.2)
        return frequency
