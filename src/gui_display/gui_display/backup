import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
import threading
import tkinter as tk
import math
from tf_transformations import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class SubscriberThread(threading.Thread):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def run(self):
        def callback(msg):
        	orientation_q = msg.orientation
        	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        	(r, p, y) = euler_from_quaternion(orientation_list)
        	(self.roll, self.pitch, self.yaw) =(r*(180/math.pi), p*(180/math.pi), y*(180/math.pi))

        sub = self.node.create_subscription(
            Imu, '/imu/data', callback, 10)

        while rclpy.ok():
            rclpy.spin_once(self.node)

    def get_rpy(self):
        return self.roll, self.pitch, self.yaw

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('IMU Data')
        self.geometry('800x800')
        self.roll_label = tk.Label(self, text='Roll: 0')
        self.roll_label.config(font=('Tahoma',30),width=10)
        self.roll_label.place(relx=400,rely= 50)
        self.roll_label.pack()
        self.pitch_label = tk.Label(self, text='Pitch: 0')
        self.pitch_label.config(font=('Tahoma',30),width=10)
        self.pitch_label.pack()
        self.yaw_label = tk.Label(self, text='Yaw: 0')
        self.yaw_label.config(font=('Tahoma',30),width=10)
        self.yaw_label.pack()

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 10000)
        self.ax.set_ylim(-180, 180)
        self.ax.set_title('RPY Data')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('RPY (deg)')
        self.line_roll, = self.ax.plot([], [], label='Roll')
        self.line_pitch, = self.ax.plot([], [], label='Pitch')
        self.line_yaw, = self.ax.plot([], [], label='Yaw')
        self.ax.legend()
        self.roll_data = []
        self.pitch_data = []
        self.yaw_data = []
        self.time_data = []
        
        self.animation = None
    
       
        
    def update_labels(self, roll, pitch, yaw):
        self.roll_label.configure(text=f'Roll: {roll:.2f}')
        self.pitch_label.configure(text=f'Pitch: {pitch:.2f}')
        self.yaw_label.configure(text=f'Yaw: {yaw:.2f}')
        self.roll_data.append(roll)
        self.pitch_data.append(pitch)
        self.yaw_data.append(yaw)
        self.time_data.append(len(self.time_data))
        if len(self.roll_data) > 100000:
            self.roll_data.pop(0)
            self.pitch_data.pop(0)
            self.yaw_data.pop(0)
            self.time_data.pop(0)
            
        self.line_roll.set_data(self.time_data, self.roll_data)
        self.line_pitch.set_data(self.time_data, self.pitch_data)
        self.line_yaw.set_data(self.time_data, self.yaw_data)
        
        if self.animation is None:
            self.animation = self.fig.canvas.new_timer(interval=50)
            self.animation.add_callback(self.animate)
            self.animation.start()
        self.ax.set_xlim(0, len(self.time_data))
        
    def animate(self):
        self.canvas.draw()
     

def main():
    rclpy.init()

    node = Node('imu_subscriber')
    thread = SubscriberThread(node)
    thread.start()

    gui = GUI()

    def update_gui_labels():
        roll, pitch, yaw = thread.get_rpy()
        gui.update_labels(roll, pitch, yaw)
        gui.after(100, update_gui_labels)
        

    gui.after(100, update_gui_labels)
    gui.mainloop()

    thread.join()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
