import rospy
from std_msgs.msg import Int32, Int16

def distance_callback(data):
    # Callback function that gets executed when data is received on the subscribed topic
    rospy.loginfo(f"Received Distance: {data.data}")

def lmd_callback(data):
    # Callback function that gets executed when data is received on the subscribed topic
    rospy.loginfo(f"Received Distance: {data.data}")

def distance_listener():
    # Initialize the ROS node
    rospy.init_node('distance_listener_node', anonymous=True)

    # Subscribe to the 'tfmini_pro/distance' topic
    rospy.Subscriber('tfmini_pro/distance', Int32, distance_callback)
    
    # Keep the node running and listening for messages
    rospy.spin()

def lmd_listener():
    rospy.init_node('lmd_listener_node', anonymous=True)
    rospy.Subscriber('land_mine', Int16, lmd_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        # distance_listener()
        lmd_listener()
    except rospy.ROSInterruptException:
        pass
