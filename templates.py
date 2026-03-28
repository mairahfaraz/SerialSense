templates = {
    "Line Follower": {
        "L298N": """
// Line Follower with L298N Motor Driver
// Pin Structure:
// ENA=9(PWM), IN1=7, IN2=8 — Left Motor
// ENB=3(PWM), IN3=5, IN4=4 — Right Motor
// IR_LEFT=A0, IR_RIGHT=A1

#define ENA 9
#define IN1 7
#define IN2 8
#define ENB 3
#define IN3 5
#define IN4 4
#define IR_LEFT A0
#define IR_RIGHT A1
#define MOTOR_SPEED 180

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(IR_LEFT, INPUT); pinMode(IR_RIGHT, INPUT);
  Serial.begin(9600);
}

void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, MOTOR_SPEED);
}

void turnLeft() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, MOTOR_SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, MOTOR_SPEED);
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void loop() {
  int left = digitalRead(IR_LEFT);
  int right = digitalRead(IR_RIGHT);
  if (left == LOW && right == LOW) moveForward();
  else if (left == HIGH && right == LOW) turnLeft();
  else if (left == LOW && right == HIGH) turnRight();
  else stopMotors();
}
""",
        "L293D": """
// Line Follower with L293D
// Same pin logic as L298N but L293D has lower current capacity (600mA vs 2A)
// Use same template as L298N — just note lower current limit in feedback
""",
        "TB6612FNG": """
// Line Follower with TB6612FNG
// PWMA=9, AIN1=7, AIN2=8 — Left Motor
// PWMB=3, BIN1=5, BIN2=4 — Right Motor
// STBY=6 (must be HIGH to enable motors)

#define PWMA 9
#define AIN1 7
#define AIN2 8
#define PWMB 3
#define BIN1 5
#define BIN2 4
#define STBY 6
#define IR_LEFT A0
#define IR_RIGHT A1
#define MOTOR_SPEED 180

void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(STBY, OUTPUT);
  digitalWrite(STBY, HIGH);
  pinMode(IR_LEFT, INPUT); pinMode(IR_RIGHT, INPUT);
  Serial.begin(9600);
}

void moveForward() {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, MOTOR_SPEED);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, MOTOR_SPEED);
}

void turnLeft() {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); analogWrite(PWMA, MOTOR_SPEED);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, MOTOR_SPEED);
}

void turnRight() {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, MOTOR_SPEED);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH); analogWrite(PWMB, MOTOR_SPEED);
}

void stopMotors() {
  analogWrite(PWMA, 0); analogWrite(PWMB, 0);
}

void loop() {
  int left = digitalRead(IR_LEFT);
  int right = digitalRead(IR_RIGHT);
  if (left == LOW && right == LOW) moveForward();
  else if (left == HIGH && right == LOW) turnLeft();
  else if (left == LOW && right == HIGH) turnRight();
  else stopMotors();
}
""",
        "L9110S": """
// Line Follower with L9110S
// A-1A=7, A-1B=6 — Left Motor (no separate enable pin)
// B-1A=5, B-1B=4 — Right Motor
// Speed controlled by PWM on direction pins directly

#define A1A 7
#define A1B 6
#define B1A 5
#define B1B 4
#define IR_LEFT A0
#define IR_RIGHT A1
#define MOTOR_SPEED 180

void setup() {
  pinMode(A1A, OUTPUT); pinMode(A1B, OUTPUT);
  pinMode(B1A, OUTPUT); pinMode(B1B, OUTPUT);
  pinMode(IR_LEFT, INPUT); pinMode(IR_RIGHT, INPUT);
  Serial.begin(9600);
}

void moveForward() {
  analogWrite(A1A, MOTOR_SPEED); digitalWrite(A1B, LOW);
  analogWrite(B1A, MOTOR_SPEED); digitalWrite(B1B, LOW);
}

void turnLeft() {
  digitalWrite(A1A, LOW); analogWrite(A1B, MOTOR_SPEED);
  analogWrite(B1A, MOTOR_SPEED); digitalWrite(B1B, LOW);
}

void turnRight() {
  analogWrite(A1A, MOTOR_SPEED); digitalWrite(A1B, LOW);
  digitalWrite(B1A, LOW); analogWrite(B1B, MOTOR_SPEED);
}

void stopMotors() {
  digitalWrite(A1A, LOW); digitalWrite(A1B, LOW);
  digitalWrite(B1A, LOW); digitalWrite(B1B, LOW);
}

void loop() {
  int left = digitalRead(IR_LEFT);
  int right = digitalRead(IR_RIGHT);
  if (left == LOW && right == LOW) moveForward();
  else if (left == HIGH && right == LOW) turnLeft();
  else if (left == LOW && right == HIGH) turnRight();
  else stopMotors();
}
""",
        "DRV8833": """
// Line Follower with DRV8833
// AIN1=9(PWM), AIN2=8 — Left Motor
// BIN1=6(PWM), BIN2=5 — Right Motor
// No separate enable pin — speed via PWM on IN1

#define AIN1 9
#define AIN2 8
#define BIN1 6
#define BIN2 5
#define IR_LEFT A0
#define IR_RIGHT A1
#define MOTOR_SPEED 180

void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT);
  pinMode(IR_LEFT, INPUT); pinMode(IR_RIGHT, INPUT);
  Serial.begin(9600);
}

void moveForward() {
  analogWrite(AIN1, MOTOR_SPEED); digitalWrite(AIN2, LOW);
  analogWrite(BIN1, MOTOR_SPEED); digitalWrite(BIN2, LOW);
}

void turnLeft() {
  digitalWrite(AIN1, LOW); analogWrite(AIN2, MOTOR_SPEED);
  analogWrite(BIN1, MOTOR_SPEED); digitalWrite(BIN2, LOW);
}

void turnRight() {
  analogWrite(AIN1, MOTOR_SPEED); digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, LOW); analogWrite(BIN2, MOTOR_SPEED);
}

void stopMotors() {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, LOW);
}

void loop() {
  int left = digitalRead(IR_LEFT);
  int right = digitalRead(IR_RIGHT);
  if (left == LOW && right == LOW) moveForward();
  else if (left == HIGH && right == LOW) turnLeft();
  else if (left == LOW && right == HIGH) turnRight();
  else stopMotors();
}
"""
    },

    "Bluetooth Controlled": {
        "L298N": """
// Bluetooth Controlled with L298N
// ENA=9(PWM), IN1=7, IN2=8 — Left Motor
// ENB=3(PWM), IN3=5, IN4=4 — Right Motor
// BT_RX=10, BT_TX=11 (SoftwareSerial)
// Commands: F=forward, B=backward, L=left, R=right, S=stop, +=speed up, -=speed down

#include <SoftwareSerial.h>
SoftwareSerial bluetooth(10, 11);

#define ENA 9
#define IN1 7
#define IN2 8
#define ENB 3
#define IN3 5
#define IN4 4
int motorSpeed = 180;

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  bluetooth.begin(9600);
  Serial.begin(9600);
}

void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, motorSpeed);
}

void moveBackward() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, motorSpeed);
}

void turnLeft() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, motorSpeed);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, motorSpeed);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, motorSpeed);
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void loop() {
  if (bluetooth.available()) {
    char cmd = bluetooth.read();
    if (cmd == 'F') moveForward();
    else if (cmd == 'B') moveBackward();
    else if (cmd == 'L') turnLeft();
    else if (cmd == 'R') turnRight();
    else if (cmd == 'S') stopMotors();
    else if (cmd == '+') { motorSpeed = min(255, motorSpeed + 20); }
    else if (cmd == '-') { motorSpeed = max(0, motorSpeed - 20); }
  }
}
""",
        "L293D": "// Same as L298N template — L293D uses identical control logic, lower current capacity.",
        "TB6612FNG": """
// Bluetooth Controlled with TB6612FNG
// PWMA=9, AIN1=7, AIN2=8 — Left Motor
// PWMB=3, BIN1=5, BIN2=4 — Right Motor
// STBY=6 must be HIGH
// BT_RX=10, BT_TX=11

#include <SoftwareSerial.h>
SoftwareSerial bluetooth(10, 11);

#define PWMA 9
#define AIN1 7
#define AIN2 8
#define PWMB 3
#define BIN1 5
#define BIN2 4
#define STBY 6
int motorSpeed = 180;

void setup() {
  pinMode(AIN1, OUTPUT); pinMode(AIN2, OUTPUT); pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT); pinMode(BIN2, OUTPUT); pinMode(PWMB, OUTPUT);
  pinMode(STBY, OUTPUT); digitalWrite(STBY, HIGH);
  bluetooth.begin(9600);
  Serial.begin(9600);
}

void moveForward() {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, motorSpeed);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, motorSpeed);
}

void moveBackward() {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); analogWrite(PWMA, motorSpeed);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH); analogWrite(PWMB, motorSpeed);
}

void turnLeft() {
  digitalWrite(AIN1, LOW); digitalWrite(AIN2, HIGH); analogWrite(PWMA, motorSpeed);
  digitalWrite(BIN1, HIGH); digitalWrite(BIN2, LOW); analogWrite(PWMB, motorSpeed);
}

void turnRight() {
  digitalWrite(AIN1, HIGH); digitalWrite(AIN2, LOW); analogWrite(PWMA, motorSpeed);
  digitalWrite(BIN1, LOW); digitalWrite(BIN2, HIGH); analogWrite(PWMB, motorSpeed);
}

void stopMotors() {
  analogWrite(PWMA, 0); analogWrite(PWMB, 0);
}

void loop() {
  if (bluetooth.available()) {
    char cmd = bluetooth.read();
    if (cmd == 'F') moveForward();
    else if (cmd == 'B') moveBackward();
    else if (cmd == 'L') turnLeft();
    else if (cmd == 'R') turnRight();
    else if (cmd == 'S') stopMotors();
  }
}
""",
        "L9110S": "// Same logic as line follower L9110S but with SoftwareSerial bluetooth commands instead of sensor reads.",
        "DRV8833": "// Same logic as line follower DRV8833 but with SoftwareSerial bluetooth commands instead of sensor reads."
    },

    "Obstacle Avoider": {
        "L298N": """
// Obstacle Avoider with L298N + HC-SR04 Ultrasonic Sensor
// ENA=9, IN1=7, IN2=8 — Left Motor
// ENB=3, IN3=5, IN4=4 — Right Motor
// TRIG=12, ECHO=11

#define ENA 9
#define IN1 7
#define IN2 8
#define ENB 3
#define IN3 5
#define IN4 4
#define TRIG 12
#define ECHO 11
#define MOTOR_SPEED 180
#define OBSTACLE_DISTANCE 20

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  Serial.begin(9600);
}

long getDistance() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  return pulseIn(ECHO, HIGH) * 0.034 / 2;
}

void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, MOTOR_SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, MOTOR_SPEED);
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void loop() {
  long distance = getDistance();
  Serial.println(distance);
  if (distance > OBSTACLE_DISTANCE) moveForward();
  else { stopMotors(); delay(300); turnRight(); delay(500); }
}
""",
        "L293D": "// Same as L298N obstacle avoider template.",
        "TB6612FNG": "// Same logic as L298N obstacle avoider but use PWMA/AIN1/AIN2 and PWMB/BIN1/BIN2 with STBY=HIGH.",
        "L9110S": "// Same logic as L298N obstacle avoider but use A1A/A1B and B1A/B1B with analogWrite on direction pins.",
        "DRV8833": "// Same logic as L298N obstacle avoider but use AIN1/AIN2 and BIN1/BIN2 with PWM on IN1 pins."
    },

    "IR Remote Controlled": {
        "L298N": """
// IR Remote Controlled with L298N + IR Receiver
// ENA=9, IN1=7, IN2=8 — Left Motor
// ENB=3, IN3=5, IN4=4 — Right Motor
// IR_RECEIVER=2

#include <IRremote.h>
#define IR_RECEIVER 2
#define ENA 9
#define IN1 7
#define IN2 8
#define ENB 3
#define IN3 5
#define IN4 4
#define MOTOR_SPEED 180

IRrecv irrecv(IR_RECEIVER);
decode_results results;

// Replace these hex codes with your remote's actual codes
#define BTN_FORWARD 0xFF629D
#define BTN_BACKWARD 0xFFA857
#define BTN_LEFT 0xFF22DD
#define BTN_RIGHT 0xFFC23D
#define BTN_STOP 0xFF02FD

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  irrecv.enableIRIn();
  Serial.begin(9600);
}

void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, MOTOR_SPEED);
}

void moveBackward() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, MOTOR_SPEED);
}

void turnLeft() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, MOTOR_SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, MOTOR_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, MOTOR_SPEED);
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void loop() {
  if (irrecv.decode(&results)) {
    long code = results.value;
    Serial.println(code, HEX);
    if (code == BTN_FORWARD) moveForward();
    else if (code == BTN_BACKWARD) moveBackward();
    else if (code == BTN_LEFT) turnLeft();
    else if (code == BTN_RIGHT) turnRight();
    else if (code == BTN_STOP) stopMotors();
    irrecv.resume();
  }
}
""",
        "L293D": "// Same as L298N IR template.",
        "TB6612FNG": "// Same logic as L298N IR but use PWMA/AIN1/AIN2 and PWMB/BIN1/BIN2 with STBY=HIGH.",
        "L9110S": "// Same logic as L298N IR but use A1A/A1B and B1A/B1B.",
        "DRV8833": "// Same logic as L298N IR but use AIN1/AIN2 and BIN1/BIN2."
    },

    "Sumo Robot": {
        "L298N": """
// Sumo Robot with L298N + 2x HC-SR04 + IR Edge Sensors
// ENA=9, IN1=7, IN2=8 — Left Motor
// ENB=3, IN3=5, IN4=4 — Right Motor
// FRONT_TRIG=12, FRONT_ECHO=11
// EDGE_LEFT=A0, EDGE_RIGHT=A1

#define ENA 9
#define IN1 7
#define IN2 8
#define ENB 3
#define IN3 5
#define IN4 4
#define FRONT_TRIG 12
#define FRONT_ECHO 11
#define EDGE_LEFT A0
#define EDGE_RIGHT A1
#define ATTACK_SPEED 255
#define SEARCH_SPEED 150
#define ENEMY_DISTANCE 40
#define EDGE_THRESHOLD 500

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(FRONT_TRIG, OUTPUT); pinMode(FRONT_ECHO, INPUT);
  pinMode(EDGE_LEFT, INPUT); pinMode(EDGE_RIGHT, INPUT);
  Serial.begin(9600);
  delay(3000); // Sumo rules: 3 second delay before start
}

long getDistance() {
  digitalWrite(FRONT_TRIG, LOW); delayMicroseconds(2);
  digitalWrite(FRONT_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(FRONT_TRIG, LOW);
  return pulseIn(FRONT_ECHO, HIGH) * 0.034 / 2;
}

void attack() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, ATTACK_SPEED);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); analogWrite(ENB, ATTACK_SPEED);
}

void reverse() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); analogWrite(ENA, ATTACK_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, ATTACK_SPEED);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, SEARCH_SPEED);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); analogWrite(ENB, SEARCH_SPEED);
}

void stopMotors() {
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}

void loop() {
  int edgeLeft = analogRead(EDGE_LEFT);
  int edgeRight = analogRead(EDGE_RIGHT);

  // Edge detection — reverse if near ring boundary
  if (edgeLeft < EDGE_THRESHOLD || edgeRight < EDGE_THRESHOLD) {
    reverse(); delay(400);
    turnRight(); delay(300);
    return;
  }

  long distance = getDistance();
  if (distance < ENEMY_DISTANCE) attack();
  else turnRight(); // Search for opponent
}
""",
        "L293D": "// Same as L298N sumo template.",
        "TB6612FNG": "// Same logic as L298N sumo but use PWMA/AIN1/AIN2 and PWMB/BIN1/BIN2 with STBY=HIGH.",
        "L9110S": "// Same logic as L298N sumo but use A1A/A1B and B1A/B1B.",
        "DRV8833": "// Same logic as L298N sumo but use AIN1/AIN2 and BIN1/BIN2."
    }
}

def get_template(robot_type, motor_driver):
    try:
        return templates[robot_type][motor_driver]
    except KeyError:
        return "No template available for this combination."