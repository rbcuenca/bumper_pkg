import rclpy
import RPi.GPIO as GPIO
from rclpy.node import Node
from std_msgs.msg import UInt8


class Bumper(Node):

    def __init__(self):

        super().__init__('bumper')

        self.bumpis = UInt8()
        self.bumpis.data = 0000
        self.bump1=26
        self.bump2=16
        self.bump3=20
        self.bump4=21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bump1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bump2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bump3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bump4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.bump1, GPIO.RISING, callback=self.interrupt, bouncetime=1000)
        GPIO.add_event_detect(self.bump2, GPIO.RISING, callback=self.interrupt, bouncetime=1000)
        GPIO.add_event_detect(self.bump3, GPIO.RISING, callback=self.interrupt, bouncetime=1000)
        GPIO.add_event_detect(self.bump4, GPIO.RISING, callback=self.interrupt, bouncetime=1000)

        self.publisher = self.create_publisher(UInt8, 'bumper', 10)
 
    def interrupt(self, channel):

        if channel == self.bump1:
            self.bumpis.data = 1
            self.get_logger().info("Bumper " + str(self.bumpis.data))
        if channel == self.bump2:
            self.bumpis.data = 2
            self.get_logger().info("Bumper " + str(self.bumpis.data))
        if channel == self.bump3:
            self.bumpis.data = 3
            self.get_logger().info("Bumper " + str(self.bumpis.data))
        if channel == self.bump4:
            self.bumpis.data = 4 
            self.get_logger().info("Bumper " + str(self.bumpis.data))
        
        self.publisher.publish(self.bumpis)


def main(args=None):
    rclpy.init(args=args)
    bumper = Bumper()
    rclpy.spin(bumper)
    bumper.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()