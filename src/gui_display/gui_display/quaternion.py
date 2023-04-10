import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
import threading
import tkinter as tk
import math
from tf_transformations import *


class SubscriberThread(threading.Thread):
    def __init__(self, node, gauges):
        super().__init__()
        self.node = node
        self.gauges = gauges

    def run(self):
        def callback(msg):
            orientation_q = msg.orientation
            orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
            (r, p, y) = euler_from_quaternion(orientation_list)
            roll = r*(180/math.pi)
            pitch = p*(180/math.pi)
            yaw = y*(180/math.pi)
            self.gauges[0].update(roll)
            self.gauges[1].update(pitch)
            self.gauges[2].update(yaw)

        sub = self.node.create_subscription(
            Imu, '/imu/data', callback, 10)

        while rclpy.ok():
            rclpy.spin_once(self.node)


class Gauge(tk.Canvas):
    def __init__(self, master, label, size=5, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=150*size, height=190*size)
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.size = size
        self.draw_gauge()
        #self.create_text(75*self.size, 10*self.size, text=label, fill='white', font=("Helvetica", 12*self.size, "bold"))
        self.label = label
        self.create_text(75*self.size, 170*self.size, text=self.label, fill='white', font=("Helvetica", 8*self.size, "bold"))


    def draw_gauge(self):
        self.delete('all')
        self.create_oval(20*self.size, 20*self.size, 130*self.size, 130*self.size, outline='white', width=3)
        for i in range(-180, 181, 30):
            angle = math.radians(i)
            x1 = 75*self.size + 55*self.size * math.sin(angle)
            y1 = 75*self.size + 55*self.size * math.cos(angle)
            x2 = 75*self.size + 65*self.size * math.sin(angle)
            y2 = 75*self.size + 65*self.size * math.cos(angle)
            self.create_line(x1, y1, x2, y2, fill='yellow', width=2)
            if i != 0:
                self.create_text(x2, y2, text=str(abs(i))+'°', fill='white', font=("Helvetica", 8*self.size, "bold"))
            else:
                self.create_text(x2, y2, text='0°', fill='white', font=("Helvetica", 8*self.size, "bold"))

    def update(self, value):
        self.delete('needle')
        self.create_line(75*self.size, 75*self.size, 75*self.size + 55*self.size * math.sin(math.radians(-value)), 75*self.size + 55*self.size * math.cos(math.radians(-value)), tags='needle', fill='red', width=3*self.size)




def main():
    rclpy.init()

    node = Node('imu_subscriber')
    root = tk.Tk()
    root.geometry('2400x900')
    root.title('IMU Gauges')

    gauges = [
        Gauge(root, 'Roll', bg='black'),
        Gauge(root, 'Pitch', bg='black'),
        Gauge(root, 'Yaw', bg='black')
    ]

    for i, gauge in enumerate(gauges):
        gauge.grid(row=0, column=i, padx=5, pady=5)

    thread = SubscriberThread(node, gauges)
    thread.start()

    tk.mainloop()


if __name__ == '__main__':
    main()

