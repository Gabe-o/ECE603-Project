#include <Arduino.h>
#include <AES.h>
#include <GCM.h>
#include <DES.h>

const int BUFFER_SIZE = 64;
char buffer[BUFFER_SIZE];
int bufferIndex = 0;

byte key[32] = {0}; // 32-byte key for AES-256
byte deskey[8] = {0}; // 8-byte key for DES
bool useAES = false; // Flag to determine encryption algorithm

AES256 aes256;
GCM<AES256> gcmAes256;

DES des;

void processCommand();
void encryptMessage(char* message);
void setNewKey(char* key);
void printKey();

void setup() {
  // from https://www.circuitbasics.com/how-to-set-up-uart-communication-for-arduino/
  pinMode(8, INPUT_PULLUP); // set push button pin as input
  pinMode(13, OUTPUT);      // set LED pin as output
  digitalWrite(13, LOW);    // switch off LED pin

  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  pinMode(2, OUTPUT); // This is the pin used by the AES library
  Serial.println("Ready for commands");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      buffer[bufferIndex] = '\0';
      processCommand();
      bufferIndex = 0;
    } else if (bufferIndex < BUFFER_SIZE - 1) {
      buffer[bufferIndex++] = c;
    }
  }
}

void processCommand() {
  if (strncmp(buffer, "ENC ", 4) == 0) {
    encryptMessage(buffer + 4);
  } else if (strncmp(buffer, "KEY ", 4) == 0) {
    setNewKey(buffer + 4);
  } else if (strcmp(buffer, "ALG AES") == 0) {
    useAES = true;
    Serial.println("Using AES encryption");
  } else if (strcmp(buffer, "ALG DES") == 0) {
    useAES = false;
    Serial.println("Using DES encryption");
  } else if (strcmp(buffer, "GETKEY") == 0) {
    printKey();
  } else {
    Serial.println("Unknown command");
  }
}

void encryptMessage(char* message) {
  int messageLen = strlen(message);
  byte ciphertext[messageLen];
  
  if (useAES) {
    byte iv[16] = {0}; // Initialization vector
    gcmAes256.setKey(key, 32);
    gcmAes256.setIV(iv, 16);
    gcmAes256.encrypt(ciphertext, (byte*)message, messageLen);
    
    // Serial.print("Encrypted (AES): ");
  } else {
    des.set_IV(0);
    des.encrypt(ciphertext, message, deskey);
    // byte nonce[12] = {0}; // Nonce for ChaCha
    // chacha.setKey(key, 32);
    // chacha.setIV(nonce, 12);
    // chacha.encrypt(ciphertext, (byte*)message, messageLen);
  }
  
  for (int i = 0; i < messageLen; i++) {
    Serial.print(ciphertext[i], HEX);
  }
  Serial.println();
}

void setNewKey(char* newKey) {
  if (useAES){
    int keyLen = strlen(newKey);
    if (keyLen > 32) keyLen = 32;
    memset(key, 0, 32);
    memcpy(key, newKey, keyLen);
  }
  else{
    int keyLen = strlen(newKey);
    if (keyLen > 8) keyLen = 8;
    memset(deskey, 0, 8); // Set the key for DES
    memcpy(deskey, newKey, keyLen);
  }
  Serial.println("New key set");
}

void printKey() {
  Serial.print("Current key: ");
  for (int i = 0; i < 32; i++) {
    Serial.print(key[i], HEX);
  }
  Serial.println();
}

