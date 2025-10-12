from machine import SPI
from st7789_spi_fb import ST7789_SPI_FB
from bitmaps import rain

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

tft.fill(COLOR_BLACK) # Fill the screen with black color
    
import time
start = time.ticks_ms()

size = 16
for y in range( SCREEN_HEIGHT // size ):
    for x in range(  SCREEN_WIDTH // size ):
        tft.draw_bitmap(rain, x * size, y * size, COLOR_CYAN)

tft.show()
print((time.ticks_ms()-start), 'ms') # 92
