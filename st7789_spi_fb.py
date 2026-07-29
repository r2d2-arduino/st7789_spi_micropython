"""
ST7789_SPI_FB v 0.3.2
Display driver for ST7789 ( with Framebuffer and DMA )

Display: ST7789
Connection: SPI
Colors: 16-bit
Controllers: Esp32-family
 
Project path: https://github.com/r2d2-arduino/st7789_spi_micropython
MIT License

Author: Arthur Derkach 
"""

from machine import Pin, PWM
from time import sleep_ms
from tft_draw.draw_fb_c16 import DRAW_FB_C16

class ST7789_SPI_FB( DRAW_FB_C16 ):
    
    def __init__( self, spi, cs_pin, dc_pin, rst_pin, blk_pin = None,
                  width = 240, height = 320, offset_x = 0, offset_y = 0,
                  bgr = False, dma = False ):
        """ Constructor
        Args
        spi  (object): SPI
        cs_pin  (int): Chip Select pin number
        dc_pin  (int): Data/Command pin number
        rst_pin (int): Reset pin number 
        blk_pin (int): Backlight pin number
        width   (int): Screen width in pixels (less)
        height  (int): Screen height in pixels
        bgr     (int): Color order: 0 = RGB, 1 = BGR
        offset_x(int): Offset X
        offset_y(int): Offset Y
        dma (bool): Enable DMA ( for pico only )
        """        
        self.spi = spi
        self.cs  = Pin(cs_pin, Pin.OUT, value = 1)
        self.dc  = Pin(dc_pin, Pin.OUT, value = 0) 
        self.rst = Pin(rst_pin, Pin.OUT, value = 1)
        self.blk = None
        
        self.controller_name = self.read_controller_name()

        if blk_pin is not None:
            self.blk = Pin(blk_pin, Pin.OUT, value = 1)
            
            self.blk_pwm = PWM(self.blk)
            self.blk_pwm.freq( 2000 )
            
            if self.controller_name == 'RP2':
                self.blk_pwm.duty_u16( 65535 )
            else:
                self.blk_pwm.duty( 1023 )
        
        self.width  = width
        self.height = height
        
        self.bgr = 0
        if bgr:
            self.bgr = 1
            
        self.rotation = 0
        
        self._font = None
        
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # DMA section
        self.dma_enabled = False
        self.dma_is_running = False
        
        if dma:
            if self.controller_name == 'RP2':
                self.dma_enabled = True
                self.init_dma()
            else:
                print('DMA is supported only for RP2')
                
        # DRAW parent
        super().__init__( self.width, self.height )       
        
        self.init()

    def write_command( self, cmd ):
        """ Sending a command to the display
        Args
        cmd (int): Command number, example: 0x2E
        """
        self.wait_dma()
        
        self.dc.value(0)  # Устанавливаем DC в командный режим
        self.cs.value(0)
        self.spi.write( bytes([cmd]) )
        self.cs.value(1)

    def write_data( self, data ):
        """ Sending data to the display
        Args
        data (int): Data byte, example: 0xF8
        """
        self.wait_dma()
        
        self.dc.value(1)  
        self.cs.value(0)
        self.spi.write( data )
        self.cs.value(1)

    def init( self ):
        """ Initial display settings """
        self.reset()

        self.write_command(0x01)  # Display reset
        sleep_ms(150)
        
        self.write_command(0x11)  # Sleep OUT
        sleep_ms(150)
        
        self.write_command(0x3A)  # Pixel Format Set
        if self.pixel_format == 12:
            self.write_data(bytearray([0x44]))
        elif self.pixel_format == 16:
            self.write_data(bytearray([0x55]))
        else: # 18 bit
            self.write_data(bytearray([0x66]))
        
        self.write_command(0x20)  # Inversion OFF
        
        self.set_rotation( 0 ) # Sreen position - 0 degree
        self.invert_display(False) # inversion off
        
        self.write_command(0x29)  # Display ON
        
    def reset( self ):
        """ Display reset """
        self.rst.value(0)
        sleep_ms(10)
        self.rst.value(1)
        sleep_ms(120)    
    
    @staticmethod
    def read_controller_name():
        from os import uname
        
        """ Reading controller name """
        info = uname()
        sysname = info.sysname

        controller = 'Undefined'
        if sysname == 'esp32':
            if 'ESP32S3' in info.machine:
                controller = 'ESP32-S3'
            elif 'ESP32C3' in info.machine:
                controller = 'ESP32-C3'
            else:
                controller = 'ESP32'
        elif sysname == 'rp2':
            controller = 'RP2'

        return controller
            
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
        if self.rotation == 0: # 0 deg
            self.memory_access_control(0, 0, 0, 0, self.bgr, 0)
        elif self.rotation == 1: # 90 deg
            self.memory_access_control(0, 1, 1, 0, self.bgr, 0)
        elif self.rotation == 2: # 180 deg
            self.memory_access_control(1, 1, 0, 0, self.bgr, 0)
        elif self.rotation == 3: # 270 deg            
            self.memory_access_control(1, 0, 1, 0, self.bgr, 0)
        
        # Change height <-> width for 90 and 270 degrees           
        if ( ((rotation & 1) and not (old_rotation & 1))
             or ((not (rotation & 1)) and (old_rotation & 1)) ):
            
            self.swap_dimensions()

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
        
    """ Dispay functions """

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
                if self.controller_name == 'RP2':
                    self.blk_pwm.duty_u16( duty * 64 )
                else:
                    self.blk_pwm.duty( duty )
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
        
        x0 += offx
        x1 += offx
        
        y0 += offy
        y1 += offy
        
        dcon = self.dc.on
        dcoff = self.dc.off
        spwrite = self.spi.write
        
        dcoff( ) # command mode
        spwrite( b'\x2a' )
        dcon( ) # data mode
        spwrite(bytearray([(x0 >> 8) & 0xff, x0 & 0xff, (x1 >> 8) & 0xff, x1 & 0xff]))
        
        dcoff( ) # command mode
        spwrite( b'\x2b' )
        dcon( ) # data mode
        spwrite(bytearray([(y0 >> 8) & 0xff, y0 & 0xff, (y1 >> 8) & 0xff, y1 & 0xff]))
        
        dcoff( ) # command mode
        spwrite( b'\x2c' )
        dcon( )

    def init_dma( self ):
        ''' Create DMA'''
        from rp2 import DMA
        from machine import mem32
        
        mem32[0x50000000 + 0x464] = (
            0x1  # aborting the channel seems to help restart DMA without a full power cycle
        )
        
        while mem32[0x50000000 + 0x464] != 0:
            continue
        
        self.dma = DMA()
        self.dma_ctrl = self.dma.pack_ctrl(
            size = 0,
            inc_write = False,
            irq_quiet = False,
            treq_sel = 0,
            bswap = True,
        )
        
        self.dma.active(0)
    
    def wait_dma(self):
        """ Blocks execution until the DMA has finished transmitting the current frame """
        if self.dma_is_running:
            while self.dma.active():
                pass
            
            self.cs.value(1)
            self.dma_is_running = False

    def show( self ):
        ''' Displays the contents of the buffer on the screen '''
        if self.dma_enabled:
            self.show_dma()
        else:
            self.show_fb()
        
    def show_fb( self ):
        ''' Displays the contents of the buffer on the screen '''
        self.cs.value(0)
        
        self.set_window( 0, 0, self.width - 1, self.height - 1)
        self.spi.write( self.buffer )
        
        self.cs.value(1)        
        
    def show_dma(self):
        """ Sending a buffer via DMA without blocking the processor """
        self.wait_dma() #Make sure the bus is free
        
        self.cs.value(0)
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Configuring DMA
        self.dma.config(
            read = self.buffer,
            write = self.spi.display_machine,
            count = self.buffsize,
            ctrl = self.dma_ctrl,
            trigger=True,
        )

        # Starting background transfer
        self.dma_is_running = True
        self.dma.active(1)