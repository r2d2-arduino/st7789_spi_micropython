from machine import SPI
from st7789_spi import ST7789_SPI
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

tft = ST7789_SPI( spi, CS_PIN, DC_PIN,  RST_PIN, BLK_PIN, height = 320, width = 240)
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
    color = tft.color565( y * 8, 0, 0 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)    
time.sleep_ms(500)

#green gradient
for y in range(0, 32):
    color = tft.color565( 0, y * 8, 0 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)
time.sleep_ms(500)

#blue gradient
for y in range(0, 32):
    color = tft.color565( 0, 0, y * 8 )
    tft.fill_rect(0, y * 10, SCREEN_WIDTH, 10, color)
time.sleep_ms(500)

def rainbow( ):
    #red
    for y in range(0, 32):
        color = tft.color565( y * 6 + 64, 0, 0 )
        tft.fill_rect(0, y * 2, SCREEN_WIDTH, 2, color)
    
    #red-green
    for y in range(0, 32):
        color = tft.color565(  y * 6 + 64, y * 6 + 64, 0 )
        tft.fill_rect(0, y * 2 + 64, SCREEN_WIDTH, 2, color)
    
    #green
    for y in range(0, 32):
        color = tft.color565(  0, y * 6 + 64, 0 )
        tft.fill_rect(0, y* 2 + 128, SCREEN_WIDTH, 2, color)

    #blue
    for y in range(0, 32):
        color = tft.color565(  0, 0, y * 6 + 64 )
        tft.fill_rect(0, y * 2 + 192, SCREEN_WIDTH, 2, color)
        
    #red-blue
    for y in range(0, 32):
        color = tft.color565( y * 6 + 64, 0, y * 6 + 64 )
        tft.fill_rect(0, y * 2 + 256, SCREEN_WIDTH, 2, color)

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
tft.vert_scroll(0, tft.height, 0)
for _ in range(3):
    for line in range(SCREEN_HEIGHT):
        tft.vert_scroll_start_address(line + 1)
        time.sleep_ms(3) 
