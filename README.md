# st7789_spi_micropython
MicroPython driver for ST7789 SPI displays.

![Photo of st7789 display](/../main/photo/st7789.jpg)

## File Structure:
* **examples/** - a set of examples for using the library ST7789_SPI.
* **examples_fb/** - a set of examples for using the library ST7789_SPI_FB.
* **for_examples/** - related files for examples.
* **st7789_spi.py** - Main library ST7789_SPI. 
* **st7789_spi_fb.py** - Main library ST7789_SPI_FB. Framebuffer version, see details here: https://docs.micropython.org/en/latest/library/framebuf.html . This option is much faster, but requires more RAM ( 110kB+ ). Suitable for Esp32-S2, Esp32-S3.

## Minimum code to run:
```python
from machine import SPI, Pin
from st7789_spi import ST7789_SPI

spi = SPI( 2, baudrate = 20_000_000, polarity = 1, phase = 1 )
# For Esp32 it is:    sck=Pin(18), mosi=Pin(23), miso=Pin(19)
# For Esp32-S2 it is: sck=Pin(36), mosi=Pin(35), miso=Pin(37)

CS_PIN  = 1
DC_PIN  = 2
RST_PIN = 4
BLK_PIN = 6 # Set to None if the display doesn't have a backlight pin

tft = ST7789_SPI( spi, CS_PIN, DC_PIN, RST_PIN, BLK_PIN )

tft.fill_screen( tft.color565( 255, 0, 0 ) ) # Fills the entire screen with red
```

## Display functions:
* **set_rotation ( rotation = 0 )** - Set orientation of Display, 0 = 0 degrees, 1 = 90 degrees, 2 = 180 degrees, 3 = 270 degrees.
* **invert_display ( on = True )** - Enables or disables color inversion on display.
* **tearing_effect ( on = True )** - Activate "Tearing effect".
* **idle_mode ( on = True )** - Enables or disables idle mode on display.
* **scroll ( delay = 5 )** - Scrolling on the screen at a given speed.
* **set_backlight ( duty = 1023 )** - Set Backlight PWM Pin: 0 - Backlight Off; 1023 - Backlight Max.
* **show ( )** - Displays the contents of the buffer on the screen ( st7789_spi_fb only ).

## Image functions:
* **draw_raw_image ( filename, x, y, width, height )** - Draw RAW image (RGB565 format) on display.
* **draw_bmp ( filename, x = 0, y = 0 )** - Draw BMP image on display.
* **color565 ( red, green, blue )** - Convert 8,8,8 bits RGB to 16 bits.

## Text functions:
* **set_font ( font )** - Set font for text.
* **draw_text ( text, x, y, color )** - Draw text on display.
* **draw_bitmap ( bitmap, x, y, color )** - Draw one bitmap on display.

## Draw functions ( for st7789_spi only ):
* **fill_screen ( color )** - Fill whole screen.
* **fill_rect ( x, y, width, height, color )** - Draw filled rectangle.
* **draw_vline ( x, y, height, color, thickness = 1 )** - Draw vertical line.
* **draw_hline ( x, y, width, color, thickness = 1 )** - Draw horizontal line.
* **draw_rect ( x, y, width, height, color, thickness = 1 )** - Draw rectangle.
* **draw_line ( x0, y0, x1, y1, color )** - Draw line using Bresenham's Algorithm.
* **draw_circle ( x, y, radius, color, border = 1 )** - Draw circle.
* **fill_circle ( x, y, radius, color )** - Draw filled circle.
* **draw_pixel ( x, y, color )** - Draw one pixel on display.

## Tools
* **tools / font_to_py.py** - Used to convert ttf font to py-script. First of all, you need to install: `pip install freetype-py`. Then run a command similar to the example: `python font_to_py.py -x LibreBodoni-Bold.ttf 24 LibreBodoni24.py`. More details: https://github.com/peterhinch/micropython-font-to-py
* **tools / img2rgb565.py** - Used to convert BMP-image to RAW RGB565 format. Usage: `python img2rgb565.py <your_image>`. Raw images load faster and use less memory.
