from st7789_spi_fb import ST7789_SPI_FB
from pio_spi import PIO_SPI
import resources.LibreBodoni24 as bigFont
from time import sleep_ms
from resources.bitmaps import suncloud

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

tft.set_font(bigFont)
tft.tearing_effect()
tft.fill(COLOR_BLACK)
tft.show()

def rainbow( ):

    for y in range(0, 32):
        red = tft.rgb( y * 6 + 64, 0, 0 )
        yellow = tft.rgb(  y * 6 + 64, y * 6 + 64, 0 )
        green = tft.rgb(  0, y * 6 + 64, 0 )
        blue = tft.rgb(  0, 0, y * 6 + 64 )
        purple = tft.rgb( y * 6 + 64, 0, y * 6 + 64 )
        
        tft.rect(0, y * 2,       SCREEN_WIDTH, 2, red, True)      
        tft.rect(0, y * 2 + 64,  SCREEN_WIDTH, 2, yellow, True)
        tft.rect(0, y * 2 + 128, SCREEN_WIDTH, 2, green, True)        
        tft.rect(0, y * 2 + 192, SCREEN_WIDTH, 2, blue, True)
        tft.rect(0, y * 2 + 256, SCREEN_WIDTH, 2, purple, True)

    tft.show()

#bitmap
size = 16
for y in range( SCREEN_HEIGHT // size ):
    for x in range(  SCREEN_WIDTH // size ):
        tft.draw_bitmap(suncloud, x * size, y * size, COLOR_CYAN)        
tft.show()
sleep_ms(500)

#red gradient
for y in range(0, 32):
    color = tft.rgb( y * 8, 0, 0 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True)
    
tft.show()
sleep_ms(500)

#green gradient
for y in range(0, 32):
    color = tft.rgb( 0, y * 8, 0 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True) 
tft.show()
sleep_ms(500)

#blue gradient
for y in range(0, 32):
    color = tft.rgb( 0, 0, y * 8 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True) 
tft.show()
sleep_ms(500)


text = "	Lorem ipsum dolor sit amet,\n consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n Duis aute irure dolor\
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n Excepteur sint occaecat cupidatat non proident, \
        sunt in culpa qui officia deserunt mollit anim id est laborum."

tft.set_rotation(1)
tft.fill(COLOR_RED)
tft.draw_text(text, 0, 0, COLOR_YELLOW)
tft.show()
sleep_ms(500)

tft.set_rotation(2)
tft.fill(COLOR_BLUE)
tft.draw_text(text, 0, 0, COLOR_WHITE)
tft.show()
sleep_ms(500)

tft.set_rotation(3)
tft.fill(COLOR_GREEN)
tft.draw_text(text, 0, 0, COLOR_MAGENTA)
tft.show()
sleep_ms(500)

tft.set_rotation(0)
tft.fill(COLOR_BLACK)
tft.draw_text(text, 0, 0, COLOR_WHITE)
tft.show()
sleep_ms(500)

rainbow()
sleep_ms(500)

tft.vert_scroll(0, tft.height, 0)
for _ in range(3):
    for line in range(SCREEN_HEIGHT):
        tft.vert_scroll_start_address(line + 1)
        sleep_ms(3) 
