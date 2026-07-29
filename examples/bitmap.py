from machine import SPI, Pin, SoftSPI
from st7789_spi import ST7789_SPI
from resources.bitmaps import rain

# For Esp32:    spi = 2, sck=Pin(18), mosi=Pin(23)
# For Esp32-S2: spi = 2, sck=Pin(36), mosi=Pin(35)
spi = SPI( 1, baudrate = 40_000_000, polarity = 1, phase = 1,
           sck = Pin(12), mosi = Pin(11) ) # Example for s3

# Set pins here
CS_PIN  = 10 #s3
DC_PIN  = 21
RST_PIN = 14
BLK_PIN = 17

tft = ST7789_SPI( spi, CS_PIN, DC_PIN,  RST_PIN, BLK_PIN,
                  height = 320, width = 240, bgr = 0)
#tft.invert_display( True )

SCREEN_WIDTH  = tft.width
SCREEN_HEIGHT = tft.height

COLOR_BLACK   = tft.rgb( 0, 0, 0 )
COLOR_BLUE    = tft.rgb( 0, 0, 255 )
COLOR_RED     = tft.rgb( 255, 0, 0 )
COLOR_GREEN   = tft.rgb( 0, 255, 0 )
COLOR_CYAN    = tft.rgb( 0, 255, 255 )
COLOR_MAGENTA = tft.rgb( 255, 0, 255 )
COLOR_YELLOW  = tft.rgb( 255, 255, 0 )
COLOR_WHITE   = tft.rgb( 255, 255, 255 )
COLOR_GRAY    = tft.rgb( 112, 160, 112 )

tft.fill(COLOR_BLACK) # Fill the screen with black color
    
colors = [COLOR_WHITE, COLOR_CYAN, COLOR_MAGENTA, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW]

import time
start = time.ticks_ms()

size = 16
for y in range( SCREEN_HEIGHT // size ):
    for x in range( SCREEN_WIDTH // size ):
        tft.draw_bitmap(rain, x * size, y * size, COLOR_CYAN, COLOR_BLACK)
              
print((time.ticks_ms()-start), 'ms') 

#esp32 400 ms
#s3m8  266
#pico2 152