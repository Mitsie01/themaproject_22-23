// Stepper driver for Arduino NANO

// Define Pins
int ENA = 7;
int DIR = 8;
int PUL = 9;
int led = 13;

/* Perform initialization and declarations inside setup() */
void setup()
{
  pinMode(ENA, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);
  pinMode(led, OUTPUT);
  TCCR1A=_BV(COM1A1)|_BV(COM1B1); /* set Fast PWM Mode */
  TCCR1B=_BV(WGM13)|_BV(CS11); /* Activate PWM Phase, frequency correction Mode */
}

void loop()
{
  float frequency=0; /* initially set frequency to zero */
  float count=10000;
  float count2=0;
  float readinput=0;
  
  while(1)
  {
    ICR1=count;
    count2=2*8*count;
    frequency= int(16000000/count2);
    OCR1A=int(count/2);
    
    count=10000;
    readinput=analogRead(A0);
    readinput=(readinput/0.0113);
    count=count+readinput;
    
    if(count>=100000)
      {
        count=10000;
      }
      delay(1000);
    }
}
