#include <MightyZap.h>

//Defining number of actuators and stroke limits
#define numMotor 6
#define minStroke 50
#define maxStroke 4000

//Defining direction port, TX high/low
#define dir_1 28
#define dir_2 30
#define dir_3 32

//=============

//Defining variables
uint16_t actGoal[numMotor];
uint16_t actPos;
float in_conv[6];
bool Start = 0;
String tempRecv;

// Global recieving and storing variables
bool recvDone = 0;
float path[numMotor];
int row = 0;


// Defining communication port and command for the actuators
MightyZap m_zap(&Serial1, dir_1, HIGH);   // TX:18 RX: 19, Direction pin: 28, TX HIGH to send
MightyZap m_zap2(&Serial2, dir_2, HIGH); // TX:16 RX: 17, Direction pin: 30, TX HIGH to send
MightyZap m_zap3(&Serial3, dir_3, HIGH); // TX:14 RX: 15, Direction pin: 32, TX HIGH to send

//=============

void setup() {

  //In order to utilize the serial monitor
  Serial.begin(57600); // 57600, same as linear actuator

  //Baud rate 57600 for the actuators/serial ports
  m_zap.begin(32);
  m_zap2.begin(32);
  m_zap3.begin(32);

  //Declaring PID values
for (int count = 0; count < 6; count++) {
  m_zap.pidGain(count,pGain,20);
  m_zap.pidGain(count,iGain,18);
  m_zap.pidGain(count,dGain,32);
  m_zap2.pidGain(count,pGain,20);
  m_zap2.pidGain(count,iGain,18);
  m_zap2.pidGain(count,dGain,32);
  m_zap3.pidGain(count,pGain,20);
  m_zap3.pidGain(count,iGain,18);
  m_zap3.pidGain(count,dGain,32);
}

  // tell the PC the Arduino is ready
  Serial.println("<Arduino is ready>");
  
}

//=============

void loop( ) {
  while(Start == 0) {
    getSpecific();
    if (tempRecv == "Start") {
      //serialFlush();
      startSequence( );
      }
}
  control( );

}

//=============

void control ( ){ // Two loops: Recieve and store data, and actuaton and replying

  if (recvDone == 0) { //Recieve and store data loop
    getDataFromPC( );
  }
  else if (recvDone) { // data convert and actuate loop
    inputConv( ); // convert input to motor values
    if (Start == 1) {
      actuate( ); // actuate
    }
    recvDone = 0; //Start recieving new data 
  }
}

//=============

void inputConv( ) {

  // Serial.print("<");Serial.print("Reaced inputConv( )");Serial.println(">"); // Debugging text
  for (int count = 0; count < numMotor ; count++){
    actGoal[count] = map(path[count], 0, 96, minStroke, maxStroke);
  if (actGoal[count] <= maxStroke  && actGoal[count] >= minStroke) {
    }
    else {
      stopAct();
    }
  }
}

//=============

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}  
