import time
import keyboard
from datetime import datetime
from dynamixel_sdk import *

LOG_FILE = "registro_movimentos.txt"

class DynamixelMotor:
    def __init__(self, motor_id, port_handler):
        self.motor_id = motor_id
        self.port_handler = port_handler
        self.packet_handler = PacketHandler(2.0)
        self.ADDR_TORQUE_ENABLE = 64
        self.ADDR_GOAL_POSITION = 116
        self.ADDR_PRESENT_POSITION = 132
        self.ADDR_PROFILE_VELOCITY = 112
        self.ADDR_PROFILE_ACCELERATION = 108
        self.goal_position = self.get_present_position() or 0

    def enable_torque(self):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 1)

    def disable_torque(self):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 0)

    def set_profile(self, acceleration, velocity):
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_ACCELERATION, acceleration)
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_VELOCITY, velocity)

    def set_goal_position(self, position):
        self.goal_position = position
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_GOAL_POSITION, int(position))
        self.log_movimento(position)

    def get_present_position(self):
        position, _, _ = self.packet_handler.read4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PRESENT_POSITION)
        return position

    def log_movimento(self, position):
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp};MOTOR:{self.motor_id};POSICAO:{position}\n")

def controle_motor_individual(motor_id, motores):
    incremento = 40
    motor = motores[motor_id]
    print(f"\n➡️ Controlando Motor {motor_id} (↑ aumenta, ↓ diminui, ESC volta ao menu)")

    try:
        while True:
            if keyboard.is_pressed('up'):
                motor.goal_position += incremento
                motor.set_goal_position(motor.goal_position)
                print(f"[Motor {motor_id}] ↑ Posição: {motor.goal_position}")
                time.sleep(0.2)

            if keyboard.is_pressed('down'):
                motor.goal_position -= incremento
                motor.set_goal_position(motor.goal_position)
                print(f"[Motor {motor_id}] ↓ Posição: {motor.goal_position}")
                time.sleep(0.2)

            if keyboard.is_pressed('esc'):
                print("🔙 Voltando ao menu...")
                break

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Encerrando controle...")

def main():
    port_handler = PortHandler('COM3')

    if not port_handler.openPort():
        print("Erro ao abrir a porta.")
        return
    if not port_handler.setBaudRate(1000000):
        print("Erro ao configurar a baudrate.")
        return

    motores = {
        1: DynamixelMotor(1, port_handler),
        2: DynamixelMotor(2, port_handler),
        3: DynamixelMotor(3, port_handler),
        4: DynamixelMotor(4, port_handler),
        #5: DynamixelMotor(5, port_handler),
        6: DynamixelMotor(6, port_handler),
        7: DynamixelMotor(7, port_handler),
    }

    for motor in motores.values():
        motor.enable_torque()
        motor.set_profile(acceleration=10, velocity=60)

    # Zera o arquivo de log no início da sessão
    open(LOG_FILE, "w").close()

    try:
        while True:
            print("\n=== Controle de Motores Dynamixel ===")
            print("Escolha um motor para controlar:")
            print("1 - Motor 1")
            print("2 - Motor 2")
            print("3 - Motor 3")
            print("4 - Motor 4")
            print("5 - Motor 5")
            print("6 - Motor 6")
            print("7 - Motor 7")
            print("0 - Sair")
            opcao = input("Digite o número do motor: ")

            if opcao == '0':
                print("Encerrando...")
                break

            try:
                motor_id = int(opcao)
                if motor_id in motores:
                    controle_motor_individual(motor_id, motores)
                else:
                    print("Motor inválido.")
            except ValueError:
                print("Entrada inválida.")

    finally:
        for motor in motores.values():
            motor.disable_torque()
        port_handler.closePort()
        print("Porta fechada.")

if __name__ == "__main__":
    main()
