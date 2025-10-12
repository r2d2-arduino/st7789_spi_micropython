from machine import SPI
from st7789_spi_fb import ST7789_SPI_FB
import LibreBodoni24 as bigFont
import time
from bitmaps import suncloud

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

tft.set_font(bigFont)
tft.tearing_effect()
tft.fill(COLOR_BLACK)
tft.show()

def rainbow( ):
    #red
    for y in range(0, 32):
        color = tft.color565( y * 6 + 64, 0, 0 )
        tft.rect(0, y * 2, SCREEN_WIDTH, 2, color, True)
    
    #red-green
    for y in range(0, 32):
        color = tft.color565(  y * 6 + 64, y * 6 + 64, 0 )
        tft.rect(0, y * 2 + 64, SCREEN_WIDTH, 2, color, True)
    
    #green
    for y in range(0, 32):
        color = tft.color565(  0, y * 6 + 64, 0 )
        tft.rect(0, y* 2 + 128, SCREEN_WIDTH, 2, color, True)

    #blue
    for y in range(0, 32):
        color = tft.color565(  0, 0, y * 6 + 64 )
        tft.rect(0, y * 2 + 192, SCREEN_WIDTH, 2, color, True)
        
    #red-blue
    for y in range(0, 32):
        color = tft.color565( y * 6 + 64, 0, y * 6 + 64 )
        tft.rect(0, y * 2 + 256, SCREEN_WIDTH, 2, color, True)

    tft.show()

#bitmap
size = 16
for y in range( SCREEN_HEIGHT // size ):
    for x in range(  SCREEN_WIDTH // size ):
        tft.draw_bitmap(suncloud, x * size, y * size, COLOR_YELLOW)        
tft.show()
time.sleep_ms(500)

#red gradient
for y in range(0, 32):
    color = tft.color565( y * 8, 0, 0 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True)
    
tft.show()
time.sleep_ms(500)

#green gradient
for y in range(0, 32):
    color = tft.color565( 0, y * 8, 0 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True) 
tft.show()
time.sleep_ms(500)

#blue gradient
for y in range(0, 32):
    color = tft.color565( 0, 0, y * 8 )
    tft.rect(0, y * 10, SCREEN_WIDTH, 10, color, True) 
tft.show()
time.sleep_ms(500)


text = "	Lorem ipsum dolor sit amet,\n consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n Duis aute irure dolor\
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n Excepteur sint occaecat cupidatat non proident, \
        sunt in culpa qui officia deserunt mollit anim id est laborum."

tft.set_rotation(1)
tft.fill(COLOR_RED)
tft.draw_text(text, 10, 20, COLOR_YELLOW)
tft.show()
time.sleep_ms(500)

tft.set_rotation(2)
tft.fill(COLOR_BLUE)
tft.draw_text(text, 10, 20, COLOR_WHITE)
tft.show()
time.sleep_ms(500)

tft.set_rotation(3)
tft.fill(COLOR_GREEN)
tft.draw_text(text, 10, 20, COLOR_MAGENTA)
tft.show()
time.sleep_ms(500)

tft.set_rotation(0)
tft.fill(COLOR_BLACK)
tft.draw_text(text, 10, 20, COLOR_WHITE)
tft.show()
time.sleep_ms(500)

rainbow()
time.sleep_ms(500)

tft.vert_scroll(0, tft.height, 0)
for _ in range(3):
    for line in range(SCREEN_HEIGHT):
        tft.vert_scroll_start_address(line + 1)
        time.sleep_ms(3) 
