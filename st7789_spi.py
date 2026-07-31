"""
ST7789_SPI v 0.1.1
Display driver for ST7789

Display: ST7789
Connection: SPI
Color: 16-bit
Controllers: Esp32-family, RP2-family
 
Project path: https://github.com/r2d2-arduino/st7789_spi_micropython
MIT License

Author: Arthur Derkach 
"""

from st7789_spi_base import ST7789_SPI_BASE
from tft_draw.draw_spi_c16 import DRAW_SPI_C16

class ST7789_SPI ( ST7789_SPI_BASE, DRAW_SPI_C16 ):
    
    def __init__( self, spi, cs_pin, dc_pin, rst_pin, blk_pin = None,
                  width = 240, height = 320, offset_x = 0, offset_y = 0,
                  bgr = False ):
        """ Constructor
        Args
        spi  (object): SPI
        cs_pin  (int): Chip Select pin number
        dc_pin  (int): Data/Command pin number
        rst_pin (int): Reset pin number 
        blk_pin (int): Backlight pin number
        width   (int): Screen width in pixels (less)
        height  (int): Screen height in pixels
        offset_x(int): Offset X
        offset_y(int): Offset Y
        bgr    (bool): Color order: False = RGB, True = BGR
        """
        
        super().__init__( spi, cs_pin, dc_pin, rst_pin, blk_pin,
                          width, height, offset_x, offset_y, bgr )
        
        DRAW_SPI_C16.__init__( self, self.spi, self.cs, self.dc,
                               self.width, self.height, self.offset_x, self.offset_y )
        
        self.init()
