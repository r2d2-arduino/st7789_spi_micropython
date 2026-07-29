from st7789_spi_fb import ST7789_SPI_FB
from pio_spi import PIO_SPI
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

def file_exists(filename):
    import os
    try:
        os.stat(filename)
        return True
    except OSError:
        print("File not found:", filename)
        return False

tft.set_rotation(0)  # 0..3 - Rotates the screen
tft.fill(0x0000) # Fill the screen with black color

filename = 'resources/grass240x320.bmp'

if file_exists(filename):

    start = ticks_ms()

    tft.draw_bmp(filename, 0, 0)
    tft.show()
    print((ticks_ms()-start), 'ms')
#s2    522 ms
#s3m8  324
#pico2 364
#dma   320 + 20 = 342