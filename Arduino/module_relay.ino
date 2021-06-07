float Vout;
int relay = 13 ;
int ACS = 0,max_Value,min_Value,i;
float VRMS,Amp,P=0.0,A=0.0,result,t;
int mVperAmp=64;
unsigned long time;
void setup() {
  Serial.begin(9600);
  pinMode(relay, OUTPUT ) ; 
  time=millis();
}

void loop() {
  //Serial.println(analogRead(ACS));
  if (Serial.available() > 0) 
  {
        String data = Serial.readStringUntil('\n');
        if(data=="1")
        {
           digitalWrite(relay, HIGH ) ;
           Vout=GetVPP();
           VRMS = (Vout/2.0) *0.707;  
           Amp = (VRMS * 1000)/mVperAmp;
            if(Amp>0.19)
            {
              P = (Amp*220.0)/1000.0 ;
            }
            else
            {
              P=0;
            }
            t=((millis() - time)/(1000.0*3600.0));
            A=P*t+A;
//            Serial.print("Điện năng tiêu thụ: ");
//            Serial.print(A,4);Serial.println("Wh");
        }
        else 
        {
          digitalWrite(relay, LOW ) ;
          Serial.println(A,4);
        }  
    }  
}
float GetVPP()
{
  float result;
  int readValue,maxValue=0,minValue=1024;
  uint32_t start_time=millis();
  while(millis()-start_time<500)
  {
    readValue=analogRead(ACS);
    //Serial.println(readValue);
    if(readValue>maxValue)
    {
      maxValue=readValue;
    }
    if(readValue<minValue)
    {
      minValue=readValue;
    }
  }
  result=((maxValue-minValue)*5.0)/1024.0;
  return result;
}
