import time
from dynamixel_sdk import *

LOG_FILE = "registro_movimentos.txt"

class DynamixelMotor:
    def __init__(self, motor_id, port_handler):
        self.motor_id = motor_id
        self.port_handler = port_handler
        self.packet_handler = PacketHandler(2.0)
        self.ADDR_TORQUE_ENABLE = 64
        self.ADDR_GOAL_POSITION = 116
        self.ADDR_PROFILE_VELOCITY = 112
        self.ADDR_PROFILE_ACCELERATION = 108

    def enable_torque(self):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 1)

    def disable_torque(self):
        self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 0)

    def set_profile(self, acceleration, velocity):
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_ACCELERATION, acceleration)
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_VELOCITY, velocity)

    def set_goal_position(self, position):
        self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_GOAL_POSITION, int(position))


def reproduzir_movimentos():
    port_handler = PortHandler('COM3')

    if not port_handler.openPort():
        print("Erro ao abrir a porta.")
        return
    if not port_handler.setBaudRate(1000000):
        print("Erro ao configurar a baudrate.")
        return

    motores = {}

    try:
        with open(LOG_FILE, "r") as f:
            linhas = f.readlines()

        for linha in linhas:
            try:
                # Exemplo: 2025-05-22 16:45:10;MOTOR:1;POSICAO:1260
                partes = linha.strip().split(";")
                motor_id = int(partes[1].split(":")[1])
                posicao = int(partes[2].split(":")[1])

                if motor_id not in motores:
                    motores[motor_id] = DynamixelMotor(motor_id, port_handler)
                    motores[motor_id].enable_torque()
                    motores[motor_id].set_profile(acceleration=10, velocity=60)

                print(f"[Reproduzindo] Motor {motor_id} -> Posição {posicao}")
                motores[motor_id].set_goal_position(posicao)
                time.sleep(0.5)  # Delay entre movimentos

            except Exception as e:
                print(f"Erro ao processar linha: {linha.strip()} -> {e}")

    finally:
        for motor in motores.values():
            motor.disable_torque()
        port_handler.closePort()
        print("Porta fechada. Reprodução finalizada.")

if __name__ == "__main__":
    reproduzir_movimentos()
