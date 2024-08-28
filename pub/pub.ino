/*
   rosserial Publisher Example
   Prints "hello world!"
   This intend to connect to a Wifi Access Point
   and a rosserial socket server.
   You can launch the rosserial socket server with
   roslaunch rosserial_server socket.launch
   The default port is 11411

*/
#include <ESP8266WiFi.h>
#include <ros.h>
#include <std_msgs/Int16.h>

//const char* ssid     = "TP-Link_3BB5";
//const char* password = "40378145";
//// Set the rosserial socket server IP address
//IPAddress server(192, 168, 0, 117);

const char* ssid     = "clover1";
const char* password = "cloverwifi";
// Set the rosserial socket server IP address
IPAddress server(192,168,11,1);
// Set the rosserial socket server port
const uint16_t serverPort = 11411;

ros::NodeHandle nh;

std_msgs::Int16 land_mine;
ros::Publisher lmd_sense("land_mine", &land_mine);

void setup()
{
  // Use ESP8266 serial to monitor the process
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect the ESP8266 the the wifi AP
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Set the connection to rosserial socket server
  nh.getHardware()->setConnection(server, serverPort);
  nh.initNode();

  // Another way to get IP
  Serial.print("IP = ");
  Serial.println(nh.getHardware()->getLocalIP());

  nh.advertise(lmd_sense);
}

void loop()
{

  if (nh.connected()) {
    Serial.println("Connected");
    // Say hello


    if (analogRead(A0) > 100) {
      land_mine.data = 1;
    }
    else {
      land_mine.data = 0;
    }
    Serial.println(land_mine.data);
    lmd_sense.publish( &land_mine );
  } else {
    Serial.println("Not Connected");
  }
  nh.spinOnce();
  // Loop exproximativly at 1Hz
  delay(10);
  Serial.flush();
}
