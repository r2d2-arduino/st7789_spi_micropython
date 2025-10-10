from machine import SPI
from st7789_spi import ST7789_SPI
import LibreBodoni24 as bigFont

spi = SPI( 2, baudrate = 20_000_000, polarity = 1, phase = 1 )
# If it doesn't work: try changing the polarity and phase to 0

# Set pins here
cs_pin  = 1
dc_pin  = 2
rst_pin = 4

tft = ST7789_SPI( spi, cs_pin, dc_pin,  rst_pin)
tft.invert_display( True ) # If it doesn't work correctly: change to False

COLOR_BLACK   = tft.color565( 0, 0, 0 )
COLOR_BLUE    = tft.color565( 0, 0, 255 )
COLOR_RED     = tft.color565( 255, 0, 0 )
COLOR_GREEN   = tft.color565( 0, 255, 0 )
COLOR_CYAN    = tft.color565( 0, 255, 255 )
COLOR_MAGENTA = tft.color565( 255, 0, 255 )
COLOR_YELLOW  = tft.color565( 255, 255, 0 )
COLOR_WHITE   = tft.color565( 255, 255, 255 )
COLOR_GRAY    = tft.color565( 112, 160, 112 )

tft.set_font(bigFont)
tft.set_rotation(0) # 0..3 - Rotates the screen clockwise

tft.fill_screen(COLOR_BLACK) # Fill the screen with black color

import time
start = time.ticks_ms()

text = " Lorem ipsum dolor sit amet,\n consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n Duis aute irure dolor\
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n Excepteur sint occaecat cupidatat non proident, \
        sunt in culpa qui officia deserunt mollit anim id est laborum."

tft.draw_text(text, 10, 20, COLOR_WHITE, COLOR_BLACK)

print((time.ticks_ms()-start), 'ms')
