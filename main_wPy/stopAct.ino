void stopAct( ) {
//Stop actuators in current position
//Serial.println("Stop state active");
  while (Start == 1) {
    getSpecific();
      if (tempRecv == "Reset") {
        Start = 0;
        //Serial.println("Reset recv");
      }
  }
}
