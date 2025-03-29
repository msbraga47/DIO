import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QKeyEvent
from timer_cubo import CubeTimer



class TimerCube(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("icon.ico"))


        self.setWindowTitle("Cube Timer - Matheus Braga")
        self.resize(1280, 720)

        # Instância do cronômetro
        self.cube_timer = CubeTimer()

        # Layout principal
        layout = QVBoxLayout()

        # Label do tempo
        self.timer_label = QLabel("0.00", self)
        self.timer_label.setStyleSheet("font-size: 150px; font-weight: bold;")
        layout.addWidget(self.timer_label)

        # Botão para iniciar/parar o tempo
        self.start_button = QPushButton("Iniciar", self)
        self.set_button_style(self.start_button, "#1c256b")
        self.start_button.clicked.connect(self.toggle_timer)
        self.start_button.pressed.connect(self.button_pressed)
        self.start_button.released.connect(self.button_released)
        self.start_button.enterEvent = self.button_enter
        self.start_button.leaveEvent = self.button_leave
        layout.addWidget(self.start_button)

        # Lista de tempos
        self.times_list = QListWidget(self)
        layout.addWidget(self.times_list)

        # Botão para gerar embaralhamento
        self.scramble_button = QPushButton("Gerar Embaralhamento", self)
        self.set_button_style(self.scramble_button, "#1c256b")
        self.scramble_button.clicked.connect(self.show_scramble)
        layout.addWidget(self.scramble_button)

        # Label do embaralhamento
        self.scramble_label = QLabel("Clique para gerar um embaralhamento", self)
        layout.addWidget(self.scramble_label)

        # Label da média
        self.average_label = QLabel("Média: -", self)
        layout.addWidget(self.average_label)

        # Timer para atualizar o tempo na tela
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.setLayout(layout)

        # Estado do cronômetro
        self.timer_running = False
        self.start_time = 0

    def toggle_timer(self):
        """Inicia ou para o cronômetro."""
        if not self.timer_running:
            self.start_time = time.time()
            self.timer.start(1)
            self.start_button.setText("Parar")
            self.set_button_style(self.start_button, "#313d9e")
        else:
            elapsed = round(time.time() - self.start_time, 3)
            self.cube_timer.times.append(elapsed)
            self.timer.stop()
            self.start_button.setText("Iniciar")
            self.set_button_style(self.start_button, "#1c256b")
            self.update_time_list()
            self.update_average()
        self.timer_running = not self.timer_running
        

    def update_timer(self):
        """Atualiza o tempo na tela em tempo real"""
        elapsed = round(time.time() - self.start_time, 3)
        self.timer_label.setText(str(elapsed))

    def update_time_list(self):
        """Atualiza a lista de tempos"""
        self.times_list.clear()
        for time_val in self.cube_timer.get_times():
            self.times_list.addItem(f"{time_val} s")

    def show_scramble(self):
        """Mostra um embaralhamento na tela"""
        scramble = self.cube_timer.scramble_cube()
        self.scramble_label.setText(scramble)

    def update_average(self):
        """Atualiza a média dos últimos 5 tempos."""
        average = self.cube_timer.get_average()
        if average:
            self.average_label.setText(f"Média: {average} s")
        else:
            self.average_label.setText("Média: -")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Space:
            if self.start_button.isVisible():
                    self.start_button.setStyleSheet("background-color: #428a42; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

    def set_button_style(self, button, color):
        """Define um estilo para os botões."""
        button.setStyleSheet(f"""
            background-color: {color};
            color: white;
            font-size: 16px;
            padding: 10px 20px; 
            border-radius: 10px; 
            border: none; 
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor) 

        # Efeito de transição de cor ao passar o mouse
        button.enterEvent = lambda event: button.setStyleSheet(f"""
            background-color: {self.adjust_color(color, 0.1)}; 
            color: white;
            font-size: 16px;
            padding: 10px 20px; 
            border-radius: 10px; 
            border: none; 
        """)
        button.leaveEvent = lambda event: button.setStyleSheet(f"""
            background-color: {color};
            color: white;
            font-size: 16px;
            padding: 10px 20px; 
            border-radius: 10px; 
            border: none; 
        """)

    def adjust_color(self, color, factor):
        """Ajusta a luminosidade da cor."""
        if not color.startswith("#"):
            return color  # Retorna a cor original se não for hexadecimal
        c = tuple(int(color[i:i+2], 16) for i in range(1, 7, 2))
        return '#' + ''.join(f'{hex(int(round(x + (255 - x) * factor)))[2:].zfill(2)}' for x in c)


    def button_pressed(self):
        self.start_button.setStyleSheet("background-color: #330808; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

    def button_released(self):
        if self.timer_running:
            self.start_button.setStyleSheet("background-color: #0d3e6e; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        else:
            self.start_button.setStyleSheet("background-color: #1c256b; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

    def button_enter(self, event):
        self.start_button.setStyleSheet("background-color: #555; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

    def button_leave(self, event):
        if self.timer_running:
            self.start_button.setStyleSheet("background-color: #0d3e6e; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        else:
            self.start_button.setStyleSheet("background-color: #1c256b; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerCube()
    window.show()
    sys.exit(app.exec())