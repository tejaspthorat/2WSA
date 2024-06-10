#include <Arduino.h>

#include <AsyncSonarLib.h>

void PingRecieved(AsyncSonar&);
void TimeOut0(AsyncSonar&);
void TimeOut1(AsyncSonar&);
void TimeOut2(AsyncSonar&);
void TimeOut3(AsyncSonar&);
void TimeOut4(AsyncSonar&);
void TimeOut5(AsyncSonar&);

int8_t temp = 25.0;

float speedAir = 331.3 * sqrt((1+ 273.15 + (float)temp)/ 273.15); // in m/s 

AsyncSonar sonarA0(2, PingRecieved, TimeOut0);
AsyncSonar sonarA1(3, PingRecieved, TimeOut1);
AsyncSonar sonarA2(4, PingRecieved, TimeOut2);
AsyncSonar sonarA3(5, PingRecieved, TimeOut3);
AsyncSonar sonarA4(6, PingRecieved, TimeOut4);
AsyncSonar sonarA5(7, PingRecieved, TimeOut5);

int data[6]= {-1, -1, -1, -1, -1, -1};
float distances[6] = {-1, -1, -1, -1, -1, -1};
bool isSet[6] = {false, false, false, false, false, false};

// ping complete callback
// (this example shows how to access sonar from callback)

void printIfReady() {
    if (isSet[0] && isSet[1] && isSet[2] && isSet[3] && isSet[4] && isSet[5]) {
      bool flag = false;
      for (int i = 0; i < 6; i++) {
        Serial.print(data[i]);
        Serial.print("\t");
        isSet[i] = false;
        if(data[i] < 250) {
          flag = true;
        }
      }
      if (flag) {
        analogWrite(9, 170);
      } else {
        analogWrite(9, 255);
      }
    Serial.println();
  }

}

void PingRecieved(AsyncSonar& sonar)
{
    if(&sonar == &sonarA0) {
      data[0] = (int)sonar.GetFilteredMM() - 50; 
      if (data[0] < 0) { data[0] = -1; }
      isSet[0] = true;
    }
    else if(&sonar == &sonarA1) {
      data[1] = (int)sonar.GetFilteredMM() - 160; 
      if (data[1] < 0) { data[1] = -1; }
      isSet[1] = true;
    }
    else if(&sonar == &sonarA2) {
      data[2] = (int)sonar.GetFilteredMM() - 150;
      if (data[2] < 0) { data[2] = -1; }
      isSet[2] = true;
    }
    else if(&sonar == &sonarA3) {
      data[3] = (int)sonar.GetFilteredMM() - 150;
      if (data[3] < 0) { data[3] = -1; }
      isSet[3] = true;
    }
    else if(&sonar == &sonarA4) {
      data[4] = (int)sonar.GetFilteredMM() - 160; 
      if (data[4] < 0) { data[4] = -1; }
      isSet[4] = true;
    }
    else if(&sonar == &sonarA5) {
      data[5] = (int)sonar.GetFilteredMM() - 50; 
      if (data[5] < 0) { data[5] = -1; }
      isSet[5] = true;
    }

  printIfReady();
}



// timeout callbacks
// (this example shows how to use different callbacks for each sensor)
void TimeOut0(AsyncSonar& sonar) { data[0] = -1; isSet[0] = true; printIfReady(); }
void TimeOut1(AsyncSonar& sonar) { data[1] = -1; isSet[1] = true; printIfReady(); }
void TimeOut2(AsyncSonar& sonar) { data[2] = -1; isSet[2] = true; printIfReady(); }
void TimeOut3(AsyncSonar& sonar) { data[3] = -1; isSet[3] = true; printIfReady(); }
void TimeOut4(AsyncSonar& sonar) { data[4] = -1; isSet[4] = true; printIfReady(); }
void TimeOut5(AsyncSonar& sonar) { data[5] = -1; isSet[5] = true; printIfReady(); }

void setup()
{
	Serial.begin(115200);

	sonarA0.SetTemperatureCorrection(temp);
	sonarA1.SetTemperatureCorrection(temp);
	sonarA2.SetTemperatureCorrection(temp);
	sonarA3.SetTemperatureCorrection(temp);
	sonarA4.SetTemperatureCorrection(temp);
	sonarA5.SetTemperatureCorrection(temp);

  sonarA0.SetTimeOut(10);
  sonarA1.SetTimeOut(10);
  sonarA2.SetTimeOut(10);
  sonarA3.SetTimeOut(10);
  sonarA4.SetTimeOut(10);
  sonarA5.SetTimeOut(10);

	sonarA0.Start(500);
	sonarA1.Start(500);
	sonarA2.Start(500);
	sonarA3.Start(500);
	sonarA4.Start(500);
	sonarA5.Start(500);

  pinMode(9, OUTPUT);
}

void loop()
{
	// this is where magic begins
	sonarA0.Update(&sonarA0);
  delay(20);
	sonarA1.Update(&sonarA1);
  delay(20);
	sonarA2.Update(&sonarA2);
  delay(20);
	sonarA3.Update(&sonarA3);
  delay(20);
	sonarA4.Update(&sonarA4);
  delay(20);
	sonarA5.Update(&sonarA5);
  delay(20);
  //Serial.println(speedAir);

}