void actuate() {
    
    m_zap.goalPosition(6, actGoal[0]);
    m_zap.goalPosition(1, actGoal[1]);
    //Serial.print("<");Serial.print("Act: ");Serial.print(count);Serial.print("| Pos: ");Serial.print(actGoal[count]);Serial.println(">"); // Debugging text

  for (int count = 2; count < 4; count++) {
    m_zap2.goalPosition(count, actGoal[count]);
    //Serial.print("<");Serial.print("Act: ");Serial.print(count);Serial.print("| Pos: ");Serial.print(actGoal[count]);Serial.println(">"); // Debugging text
  }
  for (int count = 4; count < 6; count++) {
    m_zap3.goalPosition(count, actGoal[count]);
    //Serial.print("<");Serial.print("Act: ");Serial.print(count);Serial.print("| Pos: ");Serial.print(actGoal[count]);Serial.println(">"); // Debugging text
  }
    
 //Serial.print("<");Serial.print("Act done");Serial.println(">");
}

void startSequence( ) {

  uint16_t startPos = map(48, 0, 96, minStroke, maxStroke);
  
  m_zap.goalPosition(6, startPos);
  m_zap.goalPosition(1, startPos);
   
  for (int count = 2; count < 4; count++) {
    m_zap2.goalPosition(count, startPos);
   // Serial.print("<");Serial.print("Act: ");Serial.print(count);Serial.print("| Pos: ");Serial.print(actGoal[count]);Serial.println(">"); // Debugging text
  }
  for (int count = 4; count < 6; count++) {
    m_zap3.goalPosition(count, startPos);
    // Serial.print("<");Serial.print("Act: ");Serial.print(count);Serial.print("| Pos: ");Serial.print(actGoal[count]);Serial.println(">"); // Debugging text
  }

  
    delay(1000);
    Start = 1;
    Serial.println("<Start>");
}
