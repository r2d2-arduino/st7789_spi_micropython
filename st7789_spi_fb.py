"""
ST7789_SPI_FB v 0.1.6
Display driver for ST7789 (with Framebuffer)

Display: ST7789
Connection: SPI
Colors: 16-bit
Controllers: Esp32-family
 
Project path: https://github.com/r2d2-arduino/st7789_spi_micropython
MIT License

Author: Arthur Derkach 
"""

from machine import Pin
from time import sleep_ms
from framebuf import FrameBuffer, RGB565

class ST7789_SPI_FB(FrameBuffer):
    
    def __init__(self, spi, cs_pin, dc_pin, rst_pin, width = 240, height = 320,
                 offset_x = 0, offset_y = 0):
        """ Constructor
        Args
        spi  (object): SPI
        cs_pin  (int): CS pin number (Chip Select)
        dc_pin  (int): DC pin number (command/parameter mode)
        rst_pin (int): RST pin number (Reset)
        width   (int): Screen width in pixels (less)
        height  (int): Screen height in pixels
        offset_x(int): Offset X
        offset_y(int): Offset Y        
        """        
        self.spi = spi
        self.cs  = Pin(cs_pin, Pin.OUT, value = 1)
        self.dc  = Pin(dc_pin, Pin.OUT, value = 0) 
        self.rst = Pin(rst_pin, Pin.OUT, value = 1)
        
        self.rotation = 0
        
        self.width  = width
        self.height = height
        
        self.font = None
        
        self.offset_x = offset_x
        self.offset_y = offset_y        
        
        # Buffer initialization
        self.buffsize = width * height * 2
        self.buffer = bytearray( self.buffsize )
        super().__init__( self.buffer, self.width, self.height, RGB565 )        
        
        self.init()

    def write_command(self, cmd):
        """ Sending a command to the display
        Args
        cmd (int): Command number, example: 0x2E
        """        
        self.dc.value(0)  # Устанавливаем DC в командный режим
        self.cs.value(0)
        self.spi.write(bytes([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        """ Sending data to the display
        Args
        data (int): Data byte, example: 0xF8
        """        
        self.dc.value(1)  
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def init(self):
        """ Initial display settings """
        self.reset()

        self.write_command(0x01)  # Display reset
        sleep_ms(150)
        
        self.write_command(0x11)  # Sleep OUT
        sleep_ms(150)
        
        self.write_command(0x3A)  # Pixel Format Set
        self.write_data(bytes([0x55]))  # 16-bit color
        
        self.write_command(0x20)  # Inversion OFF
        
        self.set_rotation( 0 ) # Sreen position - 0 degree
        
        self.write_command(0x29)  # Display ON
        
    def reset( self ):
        """ Display reset """
        self.rst.value(0)
        sleep_ms(10)
        self.rst.value(1)
        sleep_ms(120)    
    
    def set_rotation(self, rotation = 0):
        """
        Set orientation of Display
        Params
        rotation (int):  0 = 0 degree, 1 = 90 degrees, 2 = 180 degrees, 3 = 270 degrees
        """
        if rotation > 3 or rotation < 0:
            print("Incorrect rotation value")
            return False
        
        bgr = 0
        
        old_rotation = self.rotation
        self.rotation = rotation
        if self.rotation == 0: # 0 deg
            self.memory_access_control(0, 0, 0, 0, bgr, 0)
        elif self.rotation == 1: # 90 deg
            self.memory_access_control(0, 1, 1, 0, bgr, 0)
        elif self.rotation == 2: # 180 deg
            self.memory_access_control(1, 1, 0, 0, bgr, 0)
        elif self.rotation == 3: # 270 deg            
            self.memory_access_control(1, 0, 1, 0, bgr, 0)
        
        # Change height <-> width for 90 and 270 degrees           
        if ( ((rotation & 1) and not (old_rotation & 1))
             or ((not (rotation & 1)) and (old_rotation & 1)) ):
            
            height = self.height
            self.height = self.width
            self.width = height
            
            offset_buf = self.offset_x
            self.offset_x = self.offset_y
            self.offset_y = offset_buf            
            
            super().__init__(self.buffer, self.width, self.height, RGB565)

    def memory_access_control(self, my = 0, mx = 0, mv = 0, ml = 0, bgr = 0, mh = 0):
        """ MADCTL. This command defines read/write scanning direction of frame memory. """
        self.write_command(0x36)
        data =  0
        data += mh << 2 # Display Data Latch Data Order
        data += bgr<< 3 # RGB-BGR Order: 0 - RGB, 1 - BGR
        data += ml << 4 # Line Address Order
        data += mv << 5 # Row/Column exchange
        data += mx << 6 # Column address order
        data += my << 7 # Row address order
        #print(data)
        self.write_data(bytearray([data]))
        
    """ Dispay functions """

    def invert_display(self, on = True):
        """ Enables or disables color inversion on the display.
        Args
        on (bool): True = Enable inversion, False = Disable inversion
        """
        if on:
            self.write_command(0x21)  
        else:
            self.write_command(0x20)

    def idle_mode(self, on = True):
        """ Enables or disables idle mode on the display.
        Args
        on (bool): True = Enable idle mode, False = Disable idle mode
        """
        if on:
            self.write_command(0x39)
        else:
            self.write_command(0x38)

    def set_adaptive_brightness(self, mode = 0, ecnhctrl = 0, enchance = 0):
        """ Set adaptive brightness
        Args
        mode (int):
            0 - CABC OFF
            1 - User Interface Image
            2 - Still Picture
            3 - Moving Image
        ecnhctrl (int):
            0 - Color Enhancement Off
            1 - Color Enhancement On
        enchance (int):
            0 - Low
            1 - Medium
            2 - High
        """
        data = mode
        data += enchance << 4
        data += ecnhctrl << 7
        
        if 0 <= mode < 4 and 0 <= enchance <= 3 and 0 <= ecnhctrl <= 1:
            self.write_command(0x55)
            self.write_data(bytearray([data]))
        else:
            print('Error value in def set_adaptive_brightness')
            
    def vert_scroll(self, top_fix: int, scroll_height: int, bot_fix: int):
        """ Vertical scroll settings
        Args
        top_fix (int): Top fixed rows
        scroll_height (int): Scrolling height rows
        bot_fix (int): Bottom fixed rows
        
        top_fix + bot_fix + scroll_height - must be  equal height of screen
        """
        screen_height = self.height
        if self.rotation & 1:
            screen_height = self.width
            
        sum = top_fix + bot_fix + scroll_height
        
        if sum == screen_height:
            self.write_command(0x33)
            #Top fixed rows
            self.write_data(bytearray([(top_fix >> 8) & 0xff, top_fix & 0xff]))
            #Scrolling height rows
            self.write_data(bytearray([(scroll_height >> 8) & 0xff, scroll_height & 0xff]))
            #Bottom fixed rows
            self.write_data(bytearray([(bot_fix >> 8) & 0xff, bot_fix & 0xFF]))
            
        else:
            print('Incorrect sum in vertical scroll ', sum, ' <> ', screen_height)
            
    def vert_scroll_start_address(self, start = 0):
        """ Set vertical scroll start address, and run scrolling
        Args
        start (int): start row        
        """
        self.write_command(0x37)
        self.write_data(bytearray([(start >> 8) & 0xFF, start & 0xFF]))
        
    def scroll(self, delay = 5):
        """ Scrolling on the screen at a given speed.
        Args
        delay (int): Delay between scrolling actions
        """
        height = self.height
        if self.rotation & 1:
            height = self.width
            
        for y in range(height):
            self.vert_scroll_start_address(y + 1)
            sleep_ms(delay)        
        
    def tearing_effect(self, on = True):
        """ Activate "Tearing effect"
        Args
        on (bool): True = Enable effect, False = Disable effect
        """        
        if on:
            self.write_command(0x35)
        else:
            self.write_command(0x34)

    """ IMAGE AREA """
    
    @micropython.viper
    def draw_raw_image(self, filename, x:int, y:int, width:int, height:int):
        """ Draw RAW image (RGB565 format) on display
        Args
        filename (string): filename of image, example: "rain.bmp"
        x (int) : Start X position
        y (int) : Start Y position
        width (int) : Width of raw image
        height (int) : Height of raw image
        """
        with open( filename, 'rb' ) as f:
            buffer = ptr16( self.buffer )
            screen_width = int( self.width )

            for row in range( height ):
                image_data = f.read( width * 2 )
                image_buffer = ptr16( image_data )
                offset = x + ( row + y ) * screen_width

                col = 0
                while col < width:
                    buffer[ offset + col ] = image_buffer[ col ]
                    col += 1

        
    def draw_bmp(self, filename, x = 0, y = 0):
        """ Draw BMP image on display
        Args
        filename (string): filename of image, example: "rain.bmp"
        x (int) : Start X position
        y (int) : Start Y position
        """
        with open( filename, 'rb' ) as f:        
            if f.read(2) == b'BM':  #header
                dummy    = f.read(8) #file size(4), creator bytes(4)
                offset   = int.from_bytes(f.read(4), 'little')
                dummy    = f.read(4) #hdrsize
                width    = int.from_bytes(f.read(4), 'little')
                height   = int.from_bytes(f.read(4), 'little')
                planes   = int.from_bytes(f.read(2), 'little')
                depth    = int.from_bytes(f.read(2), 'little')
                compress = int.from_bytes(f.read(4), 'little')

                if planes == 1 and depth == 24 and compress == 0: #compress method == uncompressed
                    rowsize = (width * 3 + 3) & ~3
                    
                    if height < 0:
                        height = -height

                    frameWidth, frameHeight = width, height
                    
                    if x + frameWidth > self.width:
                        frameWidth = self.width - x
                        
                    if y + frameHeight > self.height:
                        frameHeight = self.height - y

                    f.seek(offset)
                    
                    self._send_bmp_to_framebuff(f, x, y, frameHeight, frameWidth, offset, rowsize)

            
    @micropython.viper           
    def _send_bmp_to_framebuff( self, f, x: int, y: int, frameHeight: int, frameWidth: int, offset: int, rowsize: int ):
        """ Send bmp-file to display
        Args
        f (object File) : Image file
        frameHeight (int): Height of image frame
        frameWidth (int): Width of image frame
        offset (int): Internal byte offset of image-file
        rowsize (int): Internal byte rowsize of image-file        
        """
        buffer = ptr8(self.buffer)
        screen_width = int(self.width)
        buffsize = int(self.buffsize)
        main_offset = buffsize - (y * screen_width + frameWidth + x) * 2
        
        for row in range(frameHeight):
            buff_offset = main_offset - row * screen_width * 2
            # Start position of new row in image-file
            pos = offset + row * rowsize
                                    
            if int(f.tell()) != pos:
                f.seek(pos)
            
            # Reading one row from image-file
            bgr_row = f.read(3 * frameWidth)
            image_buffer = ptr8(bgr_row)
            
            for col in range(frameWidth):
                #Getting color bytes
                red   = image_buffer[ col * 3     ]
                green = image_buffer[ col * 3 + 1 ]
                blue  = image_buffer[ col * 3 + 2 ]
                
                # Sending new bit-masks directly to registers
                buffer[buff_offset + col * 2    ] = (blue & 0xF8 ) | ( green & 0xFC ) >> 5  # color hi
                buffer[buff_offset + col * 2 + 1] = (green & 0x1C ) << 3 | red >> 3  # color low

        
    """ TEXT AREA """
        
    def set_font(self, font):
        """ Set font for text
        Args
        font (module): Font module generated by font_to_py.py
        """
        self.font = font
        
    def draw_text(self, text, x, y, color):
        """ Draw text on display
        Args
        x (int) : Start X position
        y (int) : Start Y position
        color (int): RGB565 2-byte color, example 0xF81F
        """
        x_start = x
        screen_height = self.height
        screen_width = self.width
        
        
        font = self.font        
        if font == None:
            print("Font not set")
            return False
        
        for char in text:
            if char == "\n": # New line
                x = screen_width
                continue
            
            if char == "\t": #replace tab to space
                char = " "
            
            glyph = font.get_ch(char)
            glyph_height = glyph[1]
            glyph_width = glyph[2]
            
            if char == " ": # double size for space
                x += glyph_width
                
            if x + glyph_width > screen_width:
                x = x_start
                y += glyph_height
                
            if y + glyph_height > screen_height: # End of screen
                break                
  
            self.draw_bitmap(glyph, x, y, color)
            x += glyph_width              
                
    @micropython.viper
    def draw_bitmap(self, bitmap, x:int, y:int, color:int):
        """ Draw one bitmap (glyph) on display
        Args
        bitmap (tuple) : Bitmap data [data, height, width]
        x (int) : Start X position
        y (int) : Start Y position
        color (int): RGB565 2-byte color, example 0xF81F
        """
        data   = ptr8(bitmap[0]) #memoryview of bitmap
        height = int(bitmap[1])
        width  = int(bitmap[2])
        screen_width  = int(self.width)
        
        buffer = ptr8(self.buffer)
        
        color_hi  = color & 0xFF
        color_low = (color >> 8) & 0xFF
        
        i = 0
        for h in range(height):
            ypos = (h + y) * screen_width * 2

            bit_len = 0
            while bit_len < width:
                byte = data[i]
                pos = ypos + (bit_len + x) * 2
                #Drawing pixels when bit = 1
                if (byte >> 7) & 1:                    
                    buffer[ pos     ] = color_hi
                    buffer[ pos + 1 ] = color_low        
                if (byte >> 6) & 1:                   
                    buffer[ pos + 2 ] = color_hi
                    buffer[ pos + 3 ] = color_low                    
                if (byte >> 5) & 1:                    
                    buffer[ pos + 4 ] = color_hi
                    buffer[ pos + 5 ] = color_low                      
                if (byte >> 4) & 1:                    
                    buffer[ pos + 6 ] = color_hi
                    buffer[ pos + 7 ] = color_low                    
                if (byte >> 3) & 1:                    
                    buffer[ pos + 8 ] = color_hi
                    buffer[ pos + 9 ] = color_low                     
                if (byte >> 2) & 1:                    
                    buffer[ pos + 10 ] = color_hi
                    buffer[ pos + 11 ] = color_low                     
                if (byte >> 1) & 1:                    
                    buffer[ pos + 12 ] = color_hi
                    buffer[ pos + 13 ] = color_low                     
                if byte & 1:                    
                    buffer[ pos + 14 ] = color_hi
                    buffer[ pos + 15 ] = color_low                     
                
                bit_len += 8
                i += 1
        
    @staticmethod
    def color565(red, green, blue):
        """ Convert 8,8,8 bits RGB to 16 bits  """
        return ( (green & 0x1c) << 11 | (blue & 0xf8) << 5 | (red & 0xf8) | (green & 0xe0) >> 5 )

    def show(self):
        ''' Displays the contents of the buffer on the screen '''
        self.cs.value(0)
        
        x0 = self.offset_x
        y0 = self.offset_y        
        x1 = self.offset_x + self.width - 1
        y1 = self.offset_y + self.height - 1
        
        dc = self.dc
        spi = self.spi
        
        dc.value(0) # command mode
        spi.write(b'\x2a')
        dc.value(1) # data mode
        spi.write(bytearray([(x0 >> 8) & 0xff, x0 & 0xff, (x1 >> 8) & 0xff, x1 & 0xff]))
        
        dc.value(0) # command mode
        spi.write(b'\x2b')
        dc.value(1) # data mode
        spi.write(bytearray([(y0 >> 8) & 0xff, y0 & 0xff, (y1 >> 8) & 0xff, y1 & 0xff]))
        
        dc.value(0) # command mode
        spi.write(b'\x2c') # Memory write
        dc.value(1) # data mode 
        spi.write( memoryview(self.buffer) )
        
        self.cs.value(1)
        