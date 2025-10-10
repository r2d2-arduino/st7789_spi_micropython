from machine import SPI
from st7789_spi import ST7789_SPI
from bitmaps import rain

spi = SPI( 2, baudrate = 20_000_000, polarity = 1, phase = 1 )
# If it doesn't work: try changing the polarity and phase to 0

# Set pins here
cs_pin  = 1
dc_pin  = 2
rst_pin = 4

tft = ST7789_SPI( spi, cs_pin, dc_pin,  rst_pin, height = 320, width = 240)
tft.invert_display( True ) # If it doesn't work correctly: change to False

SCREEN_WIDTH  = tft.width
SCREEN_HEIGHT = tft.height

COLOR_BLACK   = tft.color565( 0, 0, 0 )
COLOR_BLUE    = tft.color565( 0, 0, 255 )
COLOR_RED     = tft.color565( 255, 0, 0 )
COLOR_GREEN   = tft.color565( 0, 255, 0 )
COLOR_CYAN    = tft.color565( 0, 255, 255 )
COLOR_MAGENTA = tft.color565( 255, 0, 255 )
COLOR_YELLOW  = tft.color565( 255, 255, 0 )
COLOR_WHITE   = tft.color565( 255, 255, 255 )
COLOR_GRAY    = tft.color565( 112, 160, 112 )

tft.fill_screen(COLOR_BLACK) # Fill the screen with black color
    
colors = [COLOR_WHITE, COLOR_CYAN, COLOR_MAGENTA, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW]

import time
start = time.ticks_ms()

size = 16
for i in range(len(colors)):
    color = colors[i]
    for y in range( SCREEN_HEIGHT // size ):
        for x in range( SCREEN_WIDTH // size ):
            tft.draw_bitmap(rain, x * size, y * size, color, COLOR_BLACK)
              
print((time.ticks_ms()-start), 'ms')
