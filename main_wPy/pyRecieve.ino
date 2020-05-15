const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
float recieved;

char messageFromPC[buffSize] = {0};

//=============

void pyRecieve ( ) {
  getDataFromPC();
  replyToPC();
}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      inputBuffer[bytesRecvd] = 0;
      recieved = atof(inputBuffer);
      
      storeRecieved();
      
      //Serial.print("row: ");Serial.println(row); //Debugging message
      row ++;
      
      if (row > 5) {
        row = 0;
        recvDone = 1;
      }
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============

void storeRecieved() {
    //uint16_t actGoal = map(recieved, 0, 85, 100, 4000);
    path[row] = recieved;
  
}

//=============

void replyToPC() {
  if (recvDone == 1) {
    Serial.print("<");Serial.print(actGoal[0]);Serial.println(">");
    Serial.print("<");Serial.print(actGoal[1]);Serial.println(">");
    Serial.print("<");Serial.print(actGoal[2]);Serial.println(">");
    Serial.print("<");Serial.print(actGoal[3]);Serial.println(">");
    Serial.print("<");Serial.print(actGoal[4]);Serial.println(">");
    Serial.print("<");Serial.print(actGoal[5]);Serial.println(">");
  }
}

//=============

void getSpecific() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      inputBuffer[bytesRecvd] = 0;
      tempRecv = inputBuffer;
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}
