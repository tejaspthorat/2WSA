import tkinter as tk
import threading
import serial
import math
from concurrent.futures import ThreadPoolExecutor

factor = 1

class UARTDisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UART Data Display")

        self.canvas = tk.Canvas(self, width=1200 / factor, height=800 / factor)
        self.canvas.pack()
        self.clear_canvas()
        self.draw_static_elements()

        self.uart = serial.Serial('COM7', 115200)
        self.executor = ThreadPoolExecutor(max_workers=6)

        self.read_thread = threading.Thread(target=self.read_uart_data)
        self.read_thread.daemon = True
        self.read_thread.start()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 1200, 800, fill="black")

    def draw_static_elements(self):
        # Draw initial static elements
        self.draw_circle(600 / factor, 400 / factor, 100 / factor, "black")

    def draw_sector(self, center_x, center_y, radius, start_angle, end_angle, color):
        self.canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=end_angle - start_angle,
            fill=color, outline=color
        )

    def draw_donut_sector(self, center_x, center_y, inner_radius, outer_radius, start_angle, end_angle, color):
        self.draw_sector(center_x, center_y, outer_radius, start_angle, end_angle, color)
        self.draw_sector(center_x, center_y, inner_radius, start_angle, end_angle, "black")

    def draw_circle(self, center_x, center_y, radius, color):
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color, width=16)

    def read_uart_data(self):
        while True:
            if self.uart.in_waiting > 0:
                print("Reading")
                data = self.uart.readline().decode().strip()
                self.uart.flush()
                try:
                    values = list(map(int, data.split('\t')))
                    print(values)
                    values = list(map(lambda x: int(x), data.split('\t')))
                    self.update_display(values)
                except ValueError:
                    print("Error parsing UART data:", data)

    def update_display(self, value):
        self.after(0, self._update_display,value)

    def _update_display(self,values):
        
        self.clear_canvas()

        # Left Front
        if values[5] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 150, 180, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 150, 180, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 150, 180, "red")
        else:
            if values[5] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 150, 180, "green")
            if values[5] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 150, 180, "yellow")
            if values[5] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 150, 180, "red")
                
        # Left Rear
        
        if values[4] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 183, 225, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 183, 225, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 183, 225, "red")
        else:
            if values[4] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 183, 225, "green")
            if values[4] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 183, 225, "yellow")
            if values[4] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 183, 225, "red")
        
        # Rear Left
                
        if values[3] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -92, -132, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -92, -132, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -92, -132, "red")
        else:
            if values[3] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -92, -132, "green")
            if values[3] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -92, -132, "yellow")
            if values[3] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -92, -132, "red")

        # Rear Right
        if values[2] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -48, -88, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -48, -88, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -48, -88, "red")
        else:
            if values[2] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -48, -88, "green")
            if values[2] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -48, -88, "yellow")
            if values[2] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -48, -88, "red")

        # Right Rear
        
        if values[1] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -3, -45, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -3, -45, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -3, -45, "red")
        else:
            if values[1] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, -3, -45, "green")
            if values[1] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, -3, -45, "yellow")
            if values[1] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, -3, -45, "red")
        # Right Front
                
        if values[0] == -1:
            self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 0, 30, "green")
            self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 0, 30, "yellow")
            self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 0, 30, "red")
        else:
            if values[0] > 500:
                self.draw_donut_sector(600 / factor, 400 / factor, 240 / factor, 280 / factor, 0, 30, "green")
            if values[0] > 250:
                self.draw_donut_sector(600 / factor, 400 / factor, 170 / factor, 230 / factor, 0, 30, "yellow")
            if values[0] > 100:
                self.draw_donut_sector(600 / factor, 400 / factor, 120 / factor, 160 / factor, 0, 30, "red")
        
        self.draw_circle(600 / factor, 400 / factor, 100 / factor, "black")

if __name__ == "__main__":
    app = UARTDisplayApp()
    app.mainloop()
