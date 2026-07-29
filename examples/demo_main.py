from machine import SPI, Pin
from st7789_spi import ST7789_SPI
import resources.LibreBodoni24 as bigFont
import time
from resources.bitmaps import suncloud

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

tft.set_font(bigFont)
tft.tearing_effect()
tft.fill_screen(COLOR_BLACK)

#bitmap
colors = [COLOR_WHITE, COLOR_CYAN, COLOR_MAGENTA, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW]
size = 16

for i in range(len(colors)):
    color = colors[i]
    for y in range(20):
        for x in range(15):
            tft.draw_bitmap(suncloud, x * size, y * size, color, COLOR_BLACK)

#red gradient
for y in range(0, 32):
    color = tft.rgb( y * 8, 0, 0 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)    
time.sleep_ms(500)

#green gradient
for y in range(0, 32):
    color = tft.rgb( 0, y * 8, 0 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)
time.sleep_ms(500)

#blue gradient
for y in range(0, 32):
    color = tft.rgb( 0, 0, y * 8 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)
time.sleep_ms(500)

def rainbow( ):
    #red
    for y in range(0, 32):
        red = tft.rgb( y * 6 + 64, 0, 0 )
        yellow = tft.rgb(  y * 6 + 64, y * 6 + 64, 0 )
        green = tft.rgb(  0, y * 6 + 64, 0 )
        blue = tft.rgb(  0, 0, y * 6 + 64 )
        purple = tft.rgb( y * 6 + 64, 0, y * 6 + 64 )
        
        tft.fill_rect(0, y * 2,       SCREEN_WIDTH, 2, red)
        tft.fill_rect(0, y * 2 + 64,  SCREEN_WIDTH, 2, yellow)
        tft.fill_rect(0, y * 2 + 128, SCREEN_WIDTH, 2, green)
        tft.fill_rect(0, y * 2 + 192, SCREEN_WIDTH, 2, blue)
        tft.fill_rect(0, y * 2 + 256, SCREEN_WIDTH, 2, purple)

text = "	Lorem ipsum dolor sit amet,\n consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n Duis aute irure dolor\
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n Excepteur sint occaecat cupidatat non proident, \
        sunt in culpa qui officia deserunt mollit anim id est laborum."

tft.set_rotation(1)
tft.fill_screen(COLOR_RED)
tft.draw_text(text, 10, 20, COLOR_YELLOW, COLOR_RED)
time.sleep_ms(500)

tft.set_rotation(2)
tft.fill_screen(COLOR_BLUE)
tft.draw_text(text, 10, 20, COLOR_WHITE, COLOR_BLUE)
time.sleep_ms(500)

tft.set_rotation(3)
tft.fill_screen(COLOR_GREEN)
tft.draw_text(text, 10, 20, COLOR_MAGENTA, COLOR_GREEN)
time.sleep_ms(500)

tft.set_rotation(0)
tft.fill_screen(COLOR_BLACK)
tft.draw_text(text, 10, 20, COLOR_WHITE, COLOR_BLACK)
time.sleep_ms(500)

rainbow()
time.sleep_ms(500)

tft.vert_scroll(0, tft.height, 0)
for _ in range(3):
    for line in range(SCREEN_HEIGHT):
        tft.vert_scroll_start_address(line + 1)
        time.sleep_ms(3) 
