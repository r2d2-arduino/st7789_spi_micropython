from machine import SPI
from st7789_spi import ST7789_SPI

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

tft.fill_screen(COLOR_BLACK) # Fill the screen with black color

import time
start = time.ticks_ms()

tft.draw_circle(SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1, SCREEN_WIDTH >> 1, COLOR_BLUE, 2)

tft.fill_circle(SCREEN_WIDTH >> 2, SCREEN_HEIGHT - (SCREEN_HEIGHT >> 2) + 16, SCREEN_WIDTH >> 2, COLOR_YELLOW)

tft.draw_rect(10, 10, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_RED, 2)

tft.fill_rect(10, SCREEN_HEIGHT // 3, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_MAGENTA)

for y in range(SCREEN_HEIGHT // 8):
    tft.draw_line(0, 0, SCREEN_WIDTH, y * 8 , COLOR_GREEN)

print(time.ticks_diff(time.ticks_ms(), start), 'ms')
