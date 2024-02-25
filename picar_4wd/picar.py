import picar_4wd as fc
from picar_4wd.speed import Speed
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time
import signal
import sys
import numpy as np
class picar():
    def __init__(self):
        self.orientation_angles = set([0, 90, 180, 270])
        self.orientation = 0
        self.position = (0,int(50/2)-1)
        self.max_angle_bound = 80
        self.angles = np.array([i for i in range(-int(self.max_angle_bound), int(self.max_angle_bound) + 10, 10)])
        self.servo_angle = 0
        self.env_map = np.zeros((50,50))
        self.env_map_inst = np.zeros((50,50))
        signal.signal(signal.SIGINT, self.handle_signal)
        
    def handle_signal(self, signum, frame):
        fc.stop()
        sys.exit(0)
    
    def get_x(self):
        return self.position[0]
    def get_y(self):
        return self.position[1]
    def scan_step(self):
        angle_steps = self.angles.copy()
        scan_reversed = False
        if self.servo_angle == self.max_angle_bound:
            angle_steps = np.flip(angle_steps)
            scan_reversed = True
        scan_list = []
        for angle in angle_steps:
            time.sleep(0.05)
            dist = fc.get_distance_at(angle)
            self.servo_angle = angle
            scan_list.append(dist)
        if scan_reversed:
            scan_list.reverse()
        return np.array(scan_list)
    def map_car(self):
        self.env_map = self.env_map_inst.copy()
        self.env_map[int(self.get_y())][int(self.get_x())] = 8
        self.env_map_inst = np.zeros((50,50))
        cosines = np.cos(np.radians(self.angles+self.orientation))
        sines = np.sin(np.radians(self.angles+self.orientation))
        num_scans = 0
        while num_scans < 1:
            scan = self.scan_step()
            prevIdx = -1
            prev = 0
            prev_row = -1
            prev_col = -1
            scan_sines = scan * sines
            scan_cosines = scan * cosines
            for i in range(len(scan)):
                if scan[i] < 0:
                    prev = 0
                    continue
                row = int(self.position[1] - scan_sines[i]/6)
                col = int(self.position[0] + scan_cosines[i]/6)
                if self.env_map[row][col] == 8:
                    continue
                if row < 0 or col < 0 or col >= 50 or row >= 50:
                    prev = 0
                    continue
                
                self.env_map[row][col] = 1
                self.env_map_inst[row][col] = 1
                if prev > 0:
                    if col == prev_col:
                        for j in range(prev_row, row):
                            self.env_map[j][col] = 1
                            self.env_map_inst[row][col] = 1
                    else:
                        slope = (row - prev_row) / (col - prev_col)
                        for j in range(min(prev_col, col), max(prev_col, col)):
                            y = int(prev_row + slope * (j - prev_col))
                            self.env_map[y][j] = 1
                            self.env_map_inst[row][col] = 1
                prevIdx = i+1
                prev = 1
                prev_row = row
                prev_col = col
            num_scans += 1
        np.savetxt("env_map_test_txt.npy", self.env_map, delimiter=" ", fmt='%i')
    def print_env_map(self):
        print(self.env_map.shape)
        np.save("env_map_test.npy", self.env_map)
        np.savetxt("env_map_test_txt.npy", self.env_map, delimiter=" ", fmt='%i')
    def get_env_map(self):
        return self.env_map
    


picar1 = picar()
picar1.map_car()
picar1.print_env_map()