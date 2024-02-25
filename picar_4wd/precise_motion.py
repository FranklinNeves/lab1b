import picar_4wd as fc
import time

# def move_forward():
#     fc.forward(50) 
#     time.sleep(0.0495)
#     fc.stop()
#     time.sleep(0.05)

def move_forward(times=1):
    
    while times > 0:
        fc.forward(50)
        time.sleep(0.0495)
        fc.stop()
        times -= 1
        time.sleep(0.15)
    fc.stop()
    



def turn_right():
    fc.turn_right(90)
    time.sleep(.59)
    fc.stop()
    time.sleep(0.1)

def turn_left():
    fc.turn_left(90)
    time.sleep(.67)
    fc.stop()
    time.sleep(0.1)


# for i in range(1,31):
#     move_forward()
#     time.sleep(0.4)
# move_forward()
# time.sleep(1)
# turn_left()

# time.sleep(3)
# turn_right()

if __name__ == "__main__":
    move_forward(95)







