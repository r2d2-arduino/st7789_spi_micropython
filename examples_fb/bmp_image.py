from machine import SPI
from st7789_spi_fb import ST7789_SPI_FB

# For Esp32:    sck=Pin(18), mosi=Pin(23), miso=Pin(19)
# For Esp32-S2: sck=Pin(36), mosi=Pin(35), miso=Pin(37)
# If the display doesn't work: try changing the polarity and phase to 0
spi = SPI( 2, baudrate = 20_000_000, polarity = 1, phase = 1 )

# Set pins here
CS_PIN  = 1
DC_PIN  = 2
RST_PIN = 4
BLK_PIN = 6 # Set to None if the display doesn't have a backlight pin

tft = ST7789_SPI_FB( spi, CS_PIN, DC_PIN,  RST_PIN, BLK_PIN, height = 320, width = 240)
#tft.invert_display( True ) # If the display doesn't work correctly: Try to set inversion

def file_exists(filename):
    import os
    try:
        os.stat(filename)
        return True
    except OSError:
        print("File not found:", filename)
        return False

tft.set_rotation(0)  # 0..3 - Rotates the screen
tft.fill(0x0000) # Fill the screen with black color

filename = 'images/grass240x320.bmp'

if file_exists(filename):
    import time
    start = time.ticks_ms()

    tft.draw_bmp(filename, 0, 0)
    tft.show()
    print((time.ticks_ms()-start), 'ms') # 522

