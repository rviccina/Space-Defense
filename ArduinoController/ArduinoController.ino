const int analogPin = A0;
const int ButtonPin = 12;

int outputValue = 0;
int inputValue = 0;
String button_state = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ButtonPin, INPUT);
}

void loop() {
  delay(50);
  if(digitalRead(ButtonPin) == HIGH){
    button_state = "T";
  }
  else{
    button_state = "F";
  }
  // put your main code here, to run repeatedly:
  inputValue = analogRead(analogPin);// read value from sensor
  outputValue = map(inputValue,0,1023,0,360); // conver from 0-1023
  String value = String(outputValue);
  Serial.println(button_state + value);
}
