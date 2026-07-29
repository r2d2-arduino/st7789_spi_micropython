from st7789_spi_fb import ST7789_SPI_FB
from pio_spi import PIO_SPI

# standart SPI dosn't work with dma
piospi = PIO_SPI( sck = 10, mosi = 11 )

CS_PIN  = 13 #pico
DC_PIN  = 20
RST_PIN = 21
BLK_PIN = 15 # Or None

tft = ST7789_SPI_FB( piospi, CS_PIN, DC_PIN,  RST_PIN, BLK_PIN,
                     height = 320, width = 240, bgr = 0, dma = True )
#tft.invert_display( True ) # If the display doesn't work correctly: Try to set inversion

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

import time
start = time.ticks_ms()

tft.fill(COLOR_BLACK) # Fill the screen with black color

tft.ellipse(SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1, (SCREEN_WIDTH >> 1) - 1, (SCREEN_WIDTH >> 1) - 1, COLOR_BLUE)

tft.ellipse(SCREEN_WIDTH >> 2, SCREEN_HEIGHT - (SCREEN_HEIGHT >> 2) + 16, SCREEN_WIDTH >> 2, SCREEN_WIDTH >> 2, COLOR_YELLOW, True)

tft.rect(10, 10, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_RED)

tft.rect(10, SCREEN_HEIGHT // 3, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_MAGENTA, True)

for y in range(SCREEN_HEIGHT // 8):
    tft.line(0, 0, SCREEN_WIDTH - 1, y * 8 , COLOR_GREEN)

tft.show()

print(time.ticks_diff(time.ticks_ms(), start), 'ms')
#s2    95 ms
#s3m8  45
#pico2 63
#dma   11 + 20 = 31