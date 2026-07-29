from machine import SPI, Pin
from st7789_spi import ST7789_SPI
from time import ticks_ms, ticks_diff

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

start = ticks_ms()

tft.fill(COLOR_BLACK) # Fill the screen with black color

tft.draw_circle(SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1, SCREEN_WIDTH >> 1, COLOR_BLUE, 2)

tft.fill_circle(SCREEN_WIDTH >> 2, SCREEN_HEIGHT - (SCREEN_HEIGHT >> 2) + 16, SCREEN_WIDTH >> 2, COLOR_YELLOW)

tft.draw_rect(10, 10, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_RED, 2)

tft.fill_rect(10, SCREEN_HEIGHT // 3, (SCREEN_WIDTH >> 1) - 20, SCREEN_HEIGHT >> 2, COLOR_MAGENTA)

for y in range(SCREEN_HEIGHT // 8):
    tft.draw_line(0, 0, SCREEN_WIDTH - 1, y * 8 , COLOR_GREEN)


print(ticks_diff(ticks_ms(), start), 'ms') 

#esp32 4,991 ms
#s3m8  3,625
#pico2 805