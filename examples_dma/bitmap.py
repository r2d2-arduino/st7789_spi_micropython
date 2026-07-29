from st7789_spi_fb import ST7789_SPI_FB
from pio_spi import PIO_SPI
from resources.bitmaps import rain
from time import ticks_ms

# standart SPI dosn't work with dma
piospi = PIO_SPI( sck = 10, mosi = 11 )

CS_PIN  = 13 #pico
DC_PIN  = 20
RST_PIN = 21
BLK_PIN = 15 # Or None

tft = ST7789_SPI_FB( piospi, CS_PIN, DC_PIN,  RST_PIN, BLK_PIN,
                     height = 320, width = 240, bgr = 0, dma = True )
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

start = ticks_ms()
size = 16
for y in range( SCREEN_HEIGHT // size ):
    for x in range(  SCREEN_WIDTH // size ):
        tft.draw_bitmap(rain, x * size, y * size, COLOR_CYAN)

tft.show() # s3 - 33 / pico2 - 51
print((ticks_ms()-start), 'ms')
#s2    95 ms
#s3m8  48
#pico2 73
#dma   22 + 20 = 42