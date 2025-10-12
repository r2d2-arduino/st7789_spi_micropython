"""
ST7789_SPI v 0.1.7
Display driver for ST7789

Display: ST7789
Connection: SPI
Color: 16-bit
Controllers: Esp32-family, RP2-family
 
Project path: https://github.com/r2d2-arduino/st7789_spi_micropython
MIT License

Author: Arthur Derkach 
"""

from machine import Pin, PWM
from time import sleep_ms
from struct import pack

class ST7789_SPI:
    
    BUFFER_INTERNAL = 2097
    
    def __init__( self, spi, cs_pin, dc_pin, rst_pin, blk_pin = None,
                  width = 240, height = 320, offset_x = 0, offset_y = 0 ):
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
        """        
        self.spi = spi
        self.cs  = Pin(cs_pin,  Pin.OUT, value = 1)
        self.dc  = Pin(dc_pin,  Pin.OUT, value = 0) 
        self.rst = Pin(rst_pin, Pin.OUT, value = 1)
        self.blk = None
        
        if blk_pin is not None:
            self.blk = Pin(blk_pin, Pin.OUT, value = 1)
            
            self.blk_pwm = PWM(self.blk)
            self.blk_pwm.freq( 2000 )
            self.blk_pwm.duty( 1023 )
        
        self.width = width
        self.height = height
        
        self.rotation = 0
        
        self.font = None
        
        self.offset_x = offset_x
        self.offset_y = offset_y  
        
        self.init()

    def write_command( self, cmd ):
        """ Sending a command to the display
        Args
        cmd (int): Command number, example: 0x2E
        """        
        self.dc.value(0)  # Устанавливаем DC в командный режим
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data( self, data ):
        """ Sending data to the display
        Args
        data (int): Data byte, example: 0xF8
        """        
        self.dc.value(1)  
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def init( self ):
        """ Initial display settings """
        self.reset()
        
        self.write_command(0x01)  # Display reset
        sleep_ms(150)
        self.write_command(0x11)  # Sleep OUT
        sleep_ms(150)
        
        self.write_command(0x3A)  # Pixel Format Set
        self.write_data(bytearray([0x55]))  # 16-bit color
        
        self.set_rotation(0) # Sreen position - 0 degree
        
        self.invert_display(False) # inversion off
        
        self.write_command(0x29)  # Display ON

    def reset( self ):
        """ Display reset """
        self.rst.value(0)
        sleep_ms(10)
        self.rst.value(1)
        sleep_ms(120)

    def set_rotation( self, rotation = 0 ):
        """
        Set orientation of Display
        Params
        rotation (int):  0 = 0 degree, 1 = 90 degrees, 2 = 180 degrees, 3 = 270 degrees
        """
        if rotation > 3 or rotation < 0:
            print("Incorrect rotation value")
            return False
        
        old_rotation = self.rotation
        self.rotation = rotation
        
        bgr = 0
        
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
            
            hw_buf = self.height
            self.height = self.width
            self.width = hw_buf
            
            offset_buf = self.offset_x
            self.offset_x = self.offset_y
            self.offset_y = offset_buf

    def memory_access_control( self, my = 0, mx = 0, mv = 0, ml = 0, bgr = 0, mh = 0 ):
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

    def invert_display( self, on = True ):
        """ Enables or disables color inversion on the display.
        Args
        on (bool): True = Enable inversion, False = Disable inversion
        """
        if on:
            self.write_command(0x21)  
        else:
            self.write_command(0x20)   

    def idle_mode( self, on = True ):
        """ Enables or disables idle mode on the display.
        Args
        on (bool): True = Enable idle mode, False = Disable idle mode
        """
        if on:
            self.write_command(0x39)
        else:
            self.write_command(0x38)

    def set_adaptive_brightness( self, mode = 0, ecnhctrl = 0, enchance = 0 ):
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
            
    def vert_scroll( self, top_fix: int, scroll_height: int, bot_fix: int ):
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
            
    def vert_scroll_start_address( self, start = 0 ):
        """ Set vertical scroll start address, and run scrolling
        Args
        start (int): start row        
        """
        self.write_command(0x37)
        self.write_data(bytearray([(start >> 8) & 0xFF, start & 0xFF]))
        
    def scroll( self, delay = 5 ):
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
        
    def tearing_effect( self, on = True ):
        """ Activate "Tearing effect"
        Args
        on (bool): True = Enable effect, False = Disable effect
        """        
        if on:
            self.write_command(0x35)
        else:
            self.write_command(0x34)
            
    def set_backlight ( self, duty = 1023 ):
        """ Set Backlight PWM Pin
        Args
        duty (int): Duty value: 0..1023
        """
        if self.blk is not None:
            if 0 <= duty < 1024:
                self.blk_pwm.duty(duty)
            else:
                print("Duty value out of range: 0..1023")

    @micropython.viper
    def set_window( self, x0:int, y0:int, x1:int, y1:int ):
        """ Sets the starting position and the area of drawing on the display
        Args
        x0 (int): Start X position  ________
        y0 (int): Start Y position  |s---> |
        x1 (int): End X position    ||     |    
        y1 (int): End Y position    |v____e|  
        """
        offx = int( self.offset_x )
        offy = int( self.offset_y )
        
        dc = self.dc
        spi = self.spi
        
        dc.value( 0 ) # command mode
        spi.write( b'\x2a' )
        dc.value( 1 ) # data mode
        spi.write( pack( ">HH", x0 + offx, x1 + offx ) )
        
        dc.value( 0 ) # command mode
        spi.write( b'\x2b' )
        dc.value( 1 ) # data mode
        spi.write( pack( ">HH", y0 + offy, y1 + offy ) )
        
        dc.value( 0 ) # command mode
        spi.write( b'\x2c' )
        dc.value( 1 )
    
    # *** DRAW AREA ***
    
    def fill_rect( self, x, y, width, height, color ):
        """ Draw filled rectangle
        Args
        x (int): Start X position          xy----->
        y (int): Start Y position          |   w  .
        width (int): Width of rectangle  h |      .
        height (int): Height of rectangle   v.......
        color (int): RGB color
        """        
        self.cs.value(0)        
        self.set_window(x, y, x + width - 1, y + height - 1)
        
        if ( width * height < self.BUFFER_INTERNAL ):
            self.spi.write( pack( '<H', color ) * width * height )
        else:
            buffer = pack( '<H', color ) * width
            
            for _ in range( height ):
                self.spi.write( buffer )
                
        self.cs.value(1)
        
    def fill_screen( self, color ):
        """ Fill whole screen
        Args
        color (int): RGB color
        """        
        self.fill_rect( 0, 0, self.width, self.height, color )
        
    
    def draw_vline( self, x, y, height, color, thickness = 1 ):
        """ Draw vertical line
        Args
        x (int): Start X position      xy
        y (int): Start Y position     h |   
        height (int): Height of line    v   
        color (int): RGB color
        thickness (int): thickness of line
        """        
        self.fill_rect(x, y, thickness, height, color)

    def draw_hline( self, x, y, width, color, thickness = 1 ):
        """ Draw horizontal line 
        Args
        x (int): Start X position          xy----->
        y (int): Start Y position              w
        width (int): Width of line            
        color (int): RGB color
        thickness (int): thickness of line
        """         
        self.fill_rect(x, y, width, thickness, color)
    
    def draw_rect( self, x, y, width, height, color, thickness = 1 ):
        """ Draw rectangle 
        Args  
        x (int): Start X position          xy----->
        y (int): Start Y position          |   w  .
        height (int): Height of line    h  |      .
        width (int): Width of square       v.......  
        thickness (int): thickness of line   
        color (int): RGB color
        """ 
        self.fill_rect(x, y, width, thickness, color)                     
        self.fill_rect(x, y + height - thickness, width, thickness, color) 
        self.fill_rect(x, y, thickness, height, color)                     
        self.fill_rect(x + width - thickness, y, thickness, height, color) 
            
    @micropython.viper
    def draw_line( self, x0:int, y0:int, x1:int, y1:int, color:int ):
        """ Draw line using Bresenham's Algorithm
        Args
        x0 (int): Start X position   s
        y0 (int): Start Y position    \
        x1 (int): End X position       \ 
        y1 (int): End Y position        e
        color (int): RGB color
        """
        
        dx = int( abs(x1 - x0) )
        dy = int( abs(y1 - y0) )
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        dc = self.dc
        spi = self.spi
        
        offx = int(self.offset_x)
        offy = int(self.offset_y)
        
        x0 += offx
        x1 += offx
        y0 += offy
        y1 += offy        
        
        color_bytes = pack( '<H', color )
        
        x0_bytes = pack( ">HH", x0, x0 )
        y0_bytes = pack( ">HH", y0, y0 ) 
        
        self.cs.value(0)
                
        while True:
            dc.value( 0 ) # command mode
            spi.write( b'\x2a' )
            dc.value( 1 ) # data mode
            spi.write( x0_bytes )
            
            dc.value( 0 ) # command mode
            spi.write( b'\x2b' )
            dc.value( 1 ) # data mode
            spi.write( y0_bytes )
            
            dc.value( 0 ) # command mode
            spi.write( b'\x2c' )
            dc.value( 1 ) # data mode
            spi.write( color_bytes )
        
            if x0 == x1 and y0 == y1:
                break            
            
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
                x0_bytes = pack( ">HH", x0, x0 )
                
            if e2 < dx:
                err += dx
                y0 += sy
                y0_bytes = pack( ">HH", y0, y0 )

        self.cs.value(1)

    def draw_circle( self, x, y, radius, color, border = 1 ):
        """ Draw circle
        Args
        x (int): Start X position          
        y (int): Start Y position              
        radius (int): Radius of circle         
        border (int): border of circle   
        color (int): RGB color
        """
        if (x < 0 or y < 0 or x >= self.width or y >= self.height):
            print("Invalid params in draw_circle")
            return
        
        spi = self.spi
        set_window = self.set_window
        color_bytes = pack( '<H', color )
        
        self.cs.value(0)
        
        for r in range(radius - border, radius):
            # Bresenham algorithm
            x_pos = 0 - r
            y_pos = 0
            err = 2 - 2 * r
            while 1:
                set_window( x - x_pos, y + y_pos, x - x_pos, y + y_pos )
                spi.write( color_bytes )
                set_window( x + x_pos, y + y_pos, x + x_pos, y + y_pos )
                spi.write( color_bytes )
                set_window( x + x_pos, y - y_pos, x + x_pos, y - y_pos )
                spi.write( color_bytes )
                set_window( x - x_pos, y - y_pos, x - x_pos, y - y_pos )
                spi.write( color_bytes )
                
                e2 = err
                if (e2 <= y_pos):
                    y_pos += 1
                    err += y_pos * 2 + 1
                    if(0-x_pos == y_pos and e2 <= x_pos):
                        e2 = 0
                if (e2 > x_pos):
                    x_pos += 1
                    err += x_pos * 2 + 1
                if x_pos > 0:
                    break
                
        self.cs.value(1)
    
    def fill_circle( self, x, y, radius, color ):
        """ Draw filled circle
        Args
        x (int): Start X position          
        y (int): Start Y position              
        radius (int): Radius of circle
        color (int): RGB color
        """
        color_bytes = pack( '<H', color )
        self.cs.value(0) 
        for p in range(-radius, radius + 1):
            # Calculating the horizontal line
            dx = round( (radius**2 - p**2)**0.5 )
            if dx > 0:                       
                self.set_window(x - dx, y + p, x + dx - 1, y + p)
                self.spi.write( color_bytes * 2 * dx )
                    
        self.cs.value(1)      
        
    @micropython.viper
    def draw_pixel( self, x:int, y:int, color:int ):
        """ Draw one pixel on display
        Args
        x (int): X position on dispaly, example 100
        y (int): Y position on dispaly, example 200
        color (int): RGB color
        """        
        dc = self.dc
        spi = self.spi
        
        offx = int( self.offset_x )
        offy = int( self.offset_y )
        
        self.cs.value(0)
        dc.value(0) # command mode
        spi.write(b'\x2a')
        dc.value(1) # data mode
        spi.write( pack(">HH", x + offx, x + offx) )
        
        dc.value(0) # command mode
        spi.write(b'\x2b')
        dc.value(1) # data mode
        spi.write( pack(">HH", y + offy, y + offy) )
        
        dc.value(0) # command mode
        spi.write(b'\x2c')
        dc.value(1) # data mode
            
        #spi.write(bytearray([(color >> 8) & 0xff, color & 0xff]))
        spi.write( pack( '<H', color ) )
        
        self.cs.value(1)

    # *** IMAGE AREA ***
    
    def draw_raw_image( self, filename, x, y, width, height ):
        """ Draw RAW image (RGB565 format) on display
        Args
        filename (string): filename of image, example: "rain.bmp"
        x (int) : Start X position
        y (int) : Start Y position
        width (int) : Width of raw image
        height (int) : Height of raw image
        """
        with open( filename, 'rb' ) as f:
            self.cs.value( 0 )      
            self.set_window( x, y, x + width - 1, y + height - 1 ) # Set start position
            
            byte_width = width * 2
            total_bytes = height * byte_width
            
            if ( total_bytes < self.BUFFER_INTERNAL ):
                image_buffer = f.read( total_bytes )
                self.spi.write( image_buffer )
            else:
                for _ in range( height ):
                    image_buffer = f.read( byte_width )
                    self.spi.write( image_buffer )
                         
            self.cs.value( 1 )  # Chip disabled
        
    def draw_bmp( self, filename, x = 0, y = 0 ):
        """ Draw BMP image on display
        Args
        filename (string): filename of image, example: "rain.bmp"
        x (int) : Start X position
        y (int) : Start Y position
        """
        #f = open(filename, 'rb')
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
                    
                    self.cs.value(0)
                    self.set_window(x, y, x + frameWidth - 1, y + frameHeight - 1)
                    
                    self._send_bmp_to_display(f, frameHeight, frameWidth, offset, rowsize)
             
                    self.cs.value(1)
                    
    @micropython.viper           
    def _send_bmp_to_display( self, f, frameHeight: int, frameWidth: int, offset: int, rowsize: int ):
        """ Send bmp-file to display
        Args
        f (object File) : Image file
        frameHeight (int): Height of image frame
        frameWidth (int): Width of image frame
        offset (int): Internal byte offset of image-file
        rowsize (int): Internal byte rowsize of image-file        
        """
        spi_buffer = bytearray( frameWidth * 2 )
        row_buffer = ptr16( spi_buffer )

        for row in range( frameHeight ):
            # Start position of new row in image-file
            pos = offset + ( frameHeight - row - 1 ) * rowsize
            #pos = offset + row * rowsize
                                    
            if int( f.tell() ) != pos:
                f.seek( pos )

            # Reading one row from image-file
            bgr_row = f.read( frameWidth * 3 )
            image_buffer = ptr8( bgr_row )

            for col in range( frameWidth ):             
                #Getting color bytes
                red   = image_buffer[ col * 3     ]
                green = image_buffer[ col * 3 + 1 ]
                blue  = image_buffer[ col * 3 + 2 ]
                
                row_buffer[ col ] = (green & 0x1C) << 11 |  ((red & 0xF8) << 5 | (blue & 0xF8)) | (green & 0xE0) >> 5
            
            self.spi.write( spi_buffer )
    
    # *** TEXT AREA ***
    
    def set_font( self, font ):
        """ Set font for text
        Args
        font (module): Font module generated by font_to_py.py
        """
        self.font = font
        
    def draw_text( self, text, x, y, color, bg = 0x0000 ):
        """ Draw text on display (fast version)
        Args
        x (int) : Start X position
        y (int) : Start Y position
        color (int): RGB color
        bg (int) : Bacground, RGB color
        """        
        x_start = x
        glyph_height = 0
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
            
            if x + glyph_width >= screen_width: # End of row
                x = x_start
                y += glyph_height
                
            if y + glyph_height >= screen_height: # End of screen
                break
                
            self.draw_bitmap(glyph, x, y, color, bg)
            x += glyph_width
            
            if char == " " and (x + glyph_width) <= screen_width: # double size for space
                self.draw_bitmap(glyph, x, y, color, bg)
                x += glyph_width
                
        return ( x, y )
        
  
    @micropython.viper
    def draw_bitmap( self, bitmap, x:int, y:int, color:int, bg: int ):
        """ Draw one bitmap (glyph) on display (Fast version)
        Args
        bitmap (tuple) : Bitmap data [data, height, width]
        x (int) : Start X position
        y (int) : Start Y position
        color (int): RGB color
        bg (int) : Bacground, RGB color
        """
        data  = ptr8(bitmap[0]) #memoryview of bitmap
        height = int(bitmap[1]) 
        width  = int(bitmap[2])
        
        self.cs.value(0)
        self.set_window(x, y, x + width - 1, y + height - 1)
        
        spi_buffer = bytearray( height * width * 2 )
        bitmap_buffer = ptr16( spi_buffer )
        
        # Sending Color data        
        i = 0
        for row in range(height):
            dots_sum = 0                    
            while dots_sum < width:
                byte = data[i]
                i += 1
                dot = 0
                offset = (row * width + dots_sum)
                
                while dot < 8 and dot + dots_sum < width:
                    if (byte >> (7 - dot)) & 1: # main color
                        bitmap_buffer[ dot + offset ] = color
                    else: # background
                        bitmap_buffer[ dot + offset ] = bg
                    dot += 1                         
                dots_sum += 8
                
        self.spi.write(spi_buffer)     
        self.cs.value(1)
        
    @staticmethod
    @micropython.viper
    def color565( red:int, green:int, blue:int ) -> int:
        """ Convert 8,8,8 bits RGB to 16 bits  """
        return ( (green & 0x1c) << 11 | (blue & 0xf8) << 5 | (red & 0xf8) | (green & 0xe0) >> 5 )
