from machine import SPI
from st7789_spi import ST7789_SPI

spi = SPI( 2, baudrate = 20_000_000, polarity = 1, phase = 1 )
# If it doesn't work: try changing the polarity and phase to 0

# Set pins here
cs_pin  = 1
dc_pin  = 2
rst_pin = 4

tft = ST7789_SPI( spi, cs_pin, dc_pin,  rst_pin)
tft.invert_display( True ) # If it doesn't work correctly: change to False

def file_exists(filename):
    import os
    try:
        os.stat(filename)
        return True
    except OSError:
        print("File not found:", filename)
        return False

tft.set_rotation(0)  # 0..3 - Rotates the screen clockwise
tft.fill_screen(0x0000) # Fill the screen with black color


filename = 'images/road240x320.raw'
if file_exists(filename):
    import time
    start = time.ticks_ms()

    tft.draw_raw_image(filename, 0, 0, 240, 320)

    print((time.ticks_ms()-start), 'ms')
