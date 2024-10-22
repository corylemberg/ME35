from machine import I2C, Pin
from micropython import const
import time

# HT16K33 Command Constants
_HT16K33_OSCILATOR_ON = const(0x21)
_HT16K33_BLINK_CMD = const(0x80)
_HT16K33_BLINK_DISPLAYON = const(0x01)
_HT16K33_CMD_BRIGHTNESS = const(0xE0)
_HT16K33_KEY_READ_CMD = const(0x40)

# LED Lookup Table
ledLUT = (
    0x3A, 0x37, 0x35, 0x34,
    0x28, 0x29, 0x23, 0x24,
    0x16, 0x1B, 0x11, 0x10,
    0x0E, 0x0D, 0x0C, 0x02,
)

# Button Lookup Table
buttonLUT = (
    0x07, 0x04, 0x02, 0x22,
    0x05, 0x06, 0x00, 0x01,
    0x03, 0x10, 0x30, 0x21,
    0x13, 0x12, 0x11, 0x31,
)

class TrellisLEDs:
    def __init__(self, trellis_obj):
        self._parent = trellis_obj

    def __getitem__(self, x):
        if x < 0 or x >= self._parent._num_leds:
            raise ValueError(f"LED number must be between 0 and {self._parent._num_leds - 1}")
        led = ledLUT[x % 16] >> 4
        mask = 1 << (ledLUT[x % 16] & 0x0F)
        return bool(
            (
                (self._parent._led_buffer[x // 16][(led * 2) + 1] |
                 (self._parent._led_buffer[x // 16][(led * 2) + 2] << 8)) & mask) > 0
            )

    def __setitem__(self, x, value):
        if x < 0 or x >= self._parent._num_leds:
            raise ValueError(f"LED number must be between 0 and {self._parent._num_leds - 1}")
        led = ledLUT[x % 16] >> 4
        mask = 1 << (ledLUT[x % 16] & 0x0F)
        if value:
            self._parent._led_buffer[x // 16][(led * 2) + 1] |= mask & 0xFF
            self._parent._led_buffer[x // 16][(led * 2) + 2] |= mask >> 8
        else:
            self._parent._led_buffer[x // 16][(led * 2) + 1] &= ~mask
            self._parent._led_buffer[x // 16][(led * 2) + 2] &= ~mask >> 8
        if self._parent._auto_show:
            self._parent.show()

    def fill(self, on):
        fill = 0xFF if on else 0x00
        for buff in range(len(self._parent._i2c_devices)):
            for i in range(1, 17):
                self._parent._led_buffer[buff][i] = fill
        if self._parent._auto_show:
            self._parent.show()


class Trellis:
    def __init__(self, i2c, addresses=None):
        if addresses is None:
            addresses = [0x70]
        self._i2c_devices = []
        self._led_buffer = []
        self._buttons = []
        for i2c_address in addresses:
            self._i2c_devices.append(i2c_address)
            self._led_buffer.append(bytearray(17))
            self._buttons.append([bytearray(6), bytearray(6)])
        self._num_leds = len(self._i2c_devices) * 16
        self._temp = bytearray(1)
        self._blink_rate = None
        self._brightness = None
        self._auto_show = True
        self.led = TrellisLEDs(self)
        self.led.fill(False)
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self.blink_rate = 0
        self.brightness = 15

    def _write_cmd(self, byte):
        self._temp[0] = byte
        for device in self._i2c_devices:
            with I2C(device, I2C.MASTER) as i2c:
                i2c.writeto(device, self._temp)

    @property
    def blink_rate(self):
        return self._blink_rate

    @blink_rate.setter
    def blink_rate(self, rate):
        if not 0 <= rate <= 3:
            raise ValueError("Blink rate must be an integer in the range: 0-3")
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD | _HT16K33_BLINK_DISPLAYON | (rate << 1))

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if not 0 <= brightness <= 15:
            raise ValueError("Brightness must be an integer in the range: 0-15")
        brightness = brightness & 0x0F
        self._brightness = brightness
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | brightness)

    def show(self):
        for pos in range(len(self._i2c_devices)):
            with I2C(self._i2c_devices[pos], I2C.MASTER) as i2c:
                i2c.writeto(self._i2c_devices[pos], self._led_buffer[pos])

    @property
    def auto_show(self):
        return self._auto_show

    @auto_show.setter
    def auto_show(self, value):
        if value not in (True, False):
            raise ValueError("Auto show value must be True or False")
        self._auto_show = value

    def read_buttons(self):
        for i in range(len(self._buttons)):
            self._buttons[i][0] = bytearray(self._buttons[i][1])
        self._write_cmd(_HT16K33_KEY_READ_CMD)
        pos = 0
        for device in self._i2c_devices:
            with I2C(device, I2C.MASTER) as i2c:
                i2c.readfrom_into(device, self._buttons[pos][1])
                pos += 1
        pressed = []
        released = []
        for i in range(self._num_leds):
            if self._just_pressed(i):
                pressed.append(i)
            elif self._just_released(i):
                released.append(i)

        return pressed, released

    def _is_pressed(self, button):
        mask = 1 << (buttonLUT[button % 16] & 0x0F)
        return self._buttons[button // 16][1][(buttonLUT[button % 16] >> 4)] & mask

    def _was_pressed(self, button):
        mask = 1 << (buttonLUT[button % 16] & 0x0F)
        return self._buttons[button // 16][0][(buttonLUT[button % 16] >> 4)] & mask

    def _just_pressed(self, button):
        return self._is_pressed(button) and not self._was_pressed(button)

    def _just_released(self, button):
        return not self._is_pressed(button) and self._was_pressed(button)
