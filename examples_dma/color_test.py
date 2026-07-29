from st7789_spi_fb import ST7789_SPI_FB
from pio_spi import PIO_SPI
import resources.LibreBodoni24 as bigFont
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

COLOR_BLACK   = tft.rgb( 0, 0, 0 )
COLOR_BLUE    = tft.rgb( 0, 0, 255 )
COLOR_RED     = tft.rgb( 255, 0, 0 )
COLOR_GREEN   = tft.rgb( 0, 255, 0 )
COLOR_CYAN    = tft.rgb( 0, 255, 255 )
COLOR_MAGENTA = tft.rgb( 255, 0, 255 )
COLOR_YELLOW  = tft.rgb( 255, 255, 0 )
COLOR_WHITE   = tft.rgb( 255, 255, 255 )
COLOR_GRAY    = tft.rgb( 112, 160, 112 )

tft.set_font(bigFont)
tft.set_rotation(0) # 0..3 - Rotates the screen

tft.fill(COLOR_BLACK) # Fill the screen with black color

row = 24

tft.draw_text('RED', 10, row * 0, COLOR_RED)
tft.draw_text('GREEN', 10, row * 1, COLOR_GREEN)
tft.draw_text('BLUE', 10, row * 2, COLOR_BLUE)
tft.draw_text('CYAN', 10, row * 3, COLOR_CYAN)
tft.draw_text('MAGENTA', 10, row * 4, COLOR_MAGENTA)
tft.draw_text('YELLOW', 10, row * 5, COLOR_YELLOW)
tft.draw_text('WHITE', 10, row * 6, COLOR_WHITE)
tft.draw_text('GRAY', 10, row * 7, COLOR_GRAY)
tft.draw_text('BLACK', 10, row * 8, COLOR_BLACK)

start = ticks_ms()

tft.show()
while tft.dma.active():
    pass
print('DMA speed:', (ticks_ms()-start), 'ms')
