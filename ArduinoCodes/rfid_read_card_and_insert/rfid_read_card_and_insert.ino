
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
byte nuidPICC[4];
#define SERVER_IP "192.168.1.75"

#ifndef STASSID
#define STASSID "ALCLB28D68D4"
#define STAPSK  "idatech@#25"
#endif
#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN D2
#define RST_PIN D1
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
 String mycard;
 String mycard2;
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
   Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  Serial.println("Approximate your card to the reader...");
  Serial.println();
 
  
}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  mycard=content.substring(1);
//  if (content.substring(1) == "BD 31 15 2B") //change here the UID of the card/cards that you want to give access
//  {
//    Serial.println("Authorized access");
//    Serial.println();
//    delay(3000);
//  }
// 
// else   {
//    Serial.println(" Access denied");
//    delay(3000);
//  }
  Serial.println(mycard);
  mycard2=mycard;
  Serial.println(mycard2);
  dataTranfer();
 
} 

void dataTranfer() {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://" SERVER_IP "/api/"); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    String httpRequestData = "{[ card:\""+mycard2+"\",identifier:\"idatechiot\",alcohol:24.25]}";           
   
    int httpCode = http.POST("{\"card\":\""+mycard2+"\",\"alcohol\":20,\"identifier\":\"idatechiot\"}");

//http.POST("{\"card\":\""+mycard2+"\",\"alcohol\":20,\"identifier\":\"idatechiot\"}");

    
Serial.println(httpRequestData);
    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }

  delay(10000);
}
