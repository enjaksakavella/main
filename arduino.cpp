//char neutral = 0x80;
char neutral = 0x78; // magic number (120) found with physical testing, at least for forward
char command_word = neutral;
int dac_word = 0;
//int dac0_word = 0;  // forward
//int dac1_word = 0;  // turn


void setup() {
  pinMode(DAC1, OUTPUT);
  pinMode(8, OUTPUT); // pwm pin to low-pass filter. because DAC0 broke.
  Serial.begin(115200);
}

void loop() {
  if (SerialUSB) {
    if (SerialUSB.available() > 0) {
      command_word = SerialUSB.read();
      SerialUSB.write(command_word);
      dac_word = 0x7F & command_word; // 01111111
      //dac_word = dac_word*2;  // put back when voltage limiting of pwm pin 8 is done with hardware
      if ((command_word & 0x80) == 0) { // 10000000, byte commands forward movement
        dac_word = dac_word*2;
        analogWrite(DAC1, dac_word);
      }
      else {
        //dac_word = int(float(dac_word)*1.335+42); // some purkka for demo, values determined by electrical measurements
        dac_word = int(float(dac_word)*1.5+87);
        analogWrite(8, dac_word);
      }
    }
  }
  else {
    analogWrite(DAC1, neutral);
    analogWrite(8, int(float(120)*1.335+42));
    //analogWrite(8, neutral);
  }
}

// voltages with dac: 2.699, 1.560, 0.540