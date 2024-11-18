void setup() {
  Serial.begin(9600);  
  delay(2000);  //tempo para o sensor inicializar

}

void loop() {
  
  int sensorArenoso = analogRead(A0);
  int sensorArgiloso = analogRead(A1);
  int sensorOrganico = analogRead(A2);

  //converte os valores para porcentagem (assumindo 1023 -> 0% e 0 -> 100%)
  float porcentagemArenoso = ((1023 - sensorArenoso) / 1023.0) * 100.0;
  float porcentagemArgiloso = ((1023 - sensorArgiloso) / 1023.0) * 100.0;
  float porcentagemOrganico = ((1023 - sensorOrganico) / 1023.0) * 100.0;
  
  Serial.print(porcentagemArenoso);
  Serial.print(",");
  Serial.print(porcentagemArgiloso);
  Serial.print(",");
  Serial.println(porcentagemOrganico);

  delay(2000); 
}
