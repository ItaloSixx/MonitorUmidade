import flet as ft
import random
import time
from datetime import datetime
import plotly.graph_objects as go
import serial

class SensorData:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.values = []
        self.timestamps = []
        
    def add_reading(self, value, timestamp):
        self.values.append(value)
        self.timestamps.append(timestamp)
        if len(self.values) > 30:
            self.values.pop(0)
            self.timestamps.pop(0)

def main(page: ft.Page):
    page.title = "Dashboard de Umidade"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 1500
    page.window.height = 800
    page.bgcolor = "#1a1a1a"  

    sensors = {
        "Solo Arenoso": SensorData("Solo Arenoso", "#d4a76a"),
        "Solo Argiloso": SensorData("Solo Argiloso", "#8b4513"),
        "Solo Orgânico": SensorData("Solo Orgânico", "#465945")
    }

    current_values = {name: ft.Text(size=28, color="#4a90e2") for name in sensors.keys()}

    sensor_columns = {}
    for name in sensors.keys():
        chart_container = ft.Container(
            content=ft.Image(
                src="",
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=10,
            ),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border_radius=10,
            padding=10,
            width=450, 
        )
        
        sensor_columns[name] = ft.Column(
            controls=[
                ft.Text(name, size=24, weight=ft.FontWeight.BOLD, color="#e0e0e0"),
                current_values[name],
                chart_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

    def create_chart(sensor_name, sensor_data):
        fig = go.Figure()

        if sensor_data.timestamps:
            time_labels = list(range(1, len(sensor_data.values) + 1))
            
            fig.add_trace(
                go.Scatter(
                    x=time_labels,
                    y=sensor_data.values,
                    name=sensor_name,
                    line=dict(
                        color=sensor_data.color,
                        width=3
                    ),
                    fill='tozeroy',
                    fillcolor=f'rgba{tuple(list(int(sensor_data.color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}'
                )
            )

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            showlegend=False,
            margin=dict(l=40, r=20, t=20, b=40),
            height=400,  
            width=450,  
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128,128,128,0.2)',
                tickangle=45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128,128,128,0.2)',
                range=[0, 100],
                tickfont=dict(size=12)
            )
        )

        return fig

    def update_ui():
        for name, sensor in sensors.items():
            if sensor.values:
                current_values[name].value = f"{sensor.values[-1]:.1f}%"

                fig = create_chart(name, sensor)
                
                import base64
                from io import BytesIO
                
                buffer = BytesIO()
                fig.write_image(buffer, format="png")
                buffer.seek(0)
                sensor_columns[name].controls[-1].content.src_base64 = base64.b64encode(buffer.read()).decode()

        page.update()

    def get_sensor_reading():
        try:
            arduino = None
            arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  
            line = arduino.readline().decode('utf-8', errors='ignore').strip()  
            if line:
                values = line.split(',')
                if len(values) == 3:
                    for idx, sensor in enumerate(sensors.values()):
                        value = float(values[idx])
                        sensor.add_reading(value, datetime.now())
            update_ui()
        except Exception as e:
            print(f"Erro ao ler do Arduino: {e}")
        finally:
            if arduino:
                arduino.close()


    def timer_callback():
        while True:
            get_sensor_reading()
            time.sleep(2)

    #layout principal
    title = ft.Text(
        "Monitoramento de Umidade do Solo",
        size=36,
        weight=ft.FontWeight.BOLD,
        color="#4a90e2",
        text_align=ft.TextAlign.CENTER
    )

    main_content = ft.Row(
        controls=[sensor_columns[name] for name in sensors.keys()],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,  
        spacing=30
    )

    page_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=title,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(bottom=30, top=10)
                ),
                main_content
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20
    )

    page.add(page_container)

    import threading
    threading.Thread(target=timer_callback, daemon=True).start()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
