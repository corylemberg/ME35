from machine import Pin
import asyncio

class SevenSeg:
    def __init__(self):
        # Initialize the GPIO pins for the segments
        self.segments = {
            'A': Pin(6, Pin.OUT),
            'B': Pin(7, Pin.OUT),
            'C': Pin(8, Pin.OUT),
            'D': Pin(9, Pin.OUT),
            'E': Pin(10, Pin.OUT),
            'F': Pin(11, Pin.OUT),
            'G': Pin(12, Pin.OUT),
        }
        
        # Define the segment patterns for numbers 0-9 and letters a-d
        self.patterns = {
            '0': '1111101',  # BDEFAG (G off)   BDEFAGC
            '1': '1000001',  # B C (A, D, E, F, G off)
            '2': '1110110',  # B D E G A (C, F off)
            '3': '1100111',  # B C D G A (E, F off)
            '4': '1001011',  # C F G (A, B, D, E off)
            '5': '0101111',  # B D F G A (C, E off)
            '6': '0111111',  # B D E F G A (C off)
            '7': '1000101',  # B C (D, E, F, G off)
            '8': '1111111',  # B D E F G A (none off)
            '9': '1101111',  # B C D F G A (E off)
            '10': '1011111',  # B D E F G A (C off)
            '11': '0111011',  # C D E F G (A, B off)
            '12': '0111100',  # B D E (A, C, F, G off)
            '13': '1110011',  # B C D E G (A, F off)
        }

        self.human = 0
        self.hitBy = 0

    def display(self, char):
        # Turn off all segments first
        self._clear_segments()
        
        # Get the segment pattern for the character
        pattern = self.patterns.get(char)
        if pattern is not None:
            for segment, state in zip(self.segments.keys(), pattern):
                if state == '1':
                    self.segments[segment].on()
                else:
                    self.segments[segment].off()
        else:
            print(f"Character '{char}' not supported.")
    
    async def snake(self):
        delay = 0.1
        self._clear_segments()
        while True:
            while self.human:
                self.segments['A'].on()
                await asyncio.sleep(delay)
                self.segments['A'].off()
                self.segments['B'].on()
                await asyncio.sleep(delay)
                self.segments['B'].off()
                self.segments['G'].on()
                await asyncio.sleep(delay)
                self.segments['G'].off()
                self.segments['E'].on()
                await asyncio.sleep(delay)
                self.segments['E'].off()
                self.segments['D'].on()
                await asyncio.sleep(delay)
                self.segments['D'].off()
                self.segments['C'].on()
                await asyncio.sleep(delay)
                self.segments['C'].off()
                self.segments['G'].on()
                await asyncio.sleep(delay)
                self.segments['G'].off()
                self.segments['F'].on()
                await asyncio.sleep(delay)
                self.segments['F'].off()
                if self.hitBy:
                    for i in range(3):
                        self.display(str(self.hitBy))
                        await asyncio.sleep(0.1)
                        self._clear_segments()
                        await asyncio.sleep(0.1)
                self.hitBy = 0
            await asyncio.sleep(0)
            

    def _clear_segments(self):
        for segment in self.segments.values():
            segment.off()