import os
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.utils import platform
from kivy.core.window import Window

# Configuración de ventana para pruebas en PC
if platform != 'android':
    Window.size = (360, 680)

class GeneradorBoleta(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        self.nombre = "Lucas Silva"
        self.rut = "150873330016"
        self.ruta_imagen = None

        # --- ENCABEZADO ---
        self.add_widget(Label(text="Silva's Lima Electricidad", font_size='20sp', bold=True, color=(0,0,0,1) if platform != 'android' else (1,1,1,1)))
        self.add_widget(Label(text="Técnico en máquinas de coser", font_size='14sp', size_hint_y=None, height=30))

        # --- INPUTS ---
        self.input_precio = TextInput(hint_text="Precio ($)", multiline=False, input_filter='float', size_hint_y=None, height=45)
        self.add_widget(self.input_precio)

        self.input_detalle = TextInput(hint_text="Detalle del trabajo", size_hint_y=None, height=45)
        self.add_widget(self.input_detalle)

        # BOTÓN VISUALIZAR
        btn_ver = Button(text="👁 Visualizar Boleta", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        btn_ver.bind(on_release=self.actualizar)
        self.add_widget(btn_ver)

        # --- ÁREA DE LA BOLETA (FONDO BLANCO) ---
        self.area_boleta = BoxLayout(orientation='vertical', padding=20, size_hint_y=None, height=300)
        with self.area_boleta.canvas.before:
            Color(1, 1, 1, 1) # Fondo Blanco
            self.rect = Rectangle(size=self.area_boleta.size, pos=self.area_boleta.pos)
        self.area_boleta.bind(size=self._update_rect, pos=self._update_rect)

        self.boleta = Label(
            text="Complete los datos y toque 'Visualizar'",
            color=(0, 0, 0, 1), # TEXTO NEGRO
            halign='left',
            valign='top',
            markup=True,
            font_name='Roboto',
            line_height=1.2
        )
        self.boleta.bind(size=self.boleta.setter('text_size'))
        self.area_boleta.add_widget(self.boleta)
        self.add_widget(self.area_boleta)

        # --- BOTONES DE ACCIÓN ---
        btn_guardar = Button(text="📥 Guardar en Galería", size_hint_y=None, height=50)
        btn_guardar.bind(on_release=self.guardar)
        self.add_widget(btn_guardar)

        btn_wsp = Button(text="📲 Enviar por WhatsApp", size_hint_y=None, height=60, background_color=(0.1, 0.8, 0.3, 1))
        btn_wsp.bind(on_release=self.enviar_whatsapp)
        self.add_widget(btn_wsp)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generar_texto(self):
        precio = self.input_precio.text.strip()
        detalle = self.input_detalle.text.strip()
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")

        if not precio or not detalle:
            return "[color=ff0000]⚠️ Error: Falta precio o detalle[/color]"

        # Limitar detalle para que no rompa el diseño
        detalle_formateado = detalle[:25]
        
        return (
            f"[b]BOLETA TÉCNICA[/b]\n"
            f"[size=18]{self.nombre}[/size]\n"
            f"RUT: {self.rut}\n"
            f"Fecha: {fecha}\n"
            f"[b]------------------------------------[/b]\n"
            f"DETALLE: {detalle_formateado}\n"
            f"TOTAL: [b]${precio}[/b]\n"
            f"[b]------------------------------------[/b]\n"
            f"Garantía: 15 días\n"
            f"¡Gracias por su confianza!"
        )

    def actualizar(self, *args):
        self.boleta.text = self.generar_texto()

    def guardar(self, *args):
        if not self.input_precio.text or not self.input_detalle.text:
            self.boleta.text = "[color=ff0000]⚠️ Primero ingresa los datos[/color]"
            return

        nombre_archivo = f"boleta_{datetime.datetime.now().strftime('%H%M%S')}.png"
        
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = os.path.join(primary_external_storage_path(), 'Download')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            path = os.path.join(dir_path, nombre_archivo)
        else:
            path = nombre_archivo

        # Exportar el área blanca
        self.area_boleta.export_to_png(path)
        self.ruta_imagen = path
        self.boleta.text += "\n\n[color=008800][b]✅ Guardada en Descargas[/b][/color]"

    def enviar_whatsapp(self, *args):
        if not self.ruta_imagen or not os.path.exists(self.ruta_imagen):
            self.boleta.text += "\n\n[color=ff0000]⚠️ Guarda la boleta primero[/color]"
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                String = autoclass('java.lang.String')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                
                file = File(self.ruta_imagen)
                uri = Uri.fromFile(file)
                
                shareIntent = Intent(Intent.ACTION_SEND)
                shareIntent.setType("image/png")
                shareIntent.putExtra(Intent.EXTRA_STREAM, uri)
                shareIntent.setPackage("com.whatsapp")
                
                currentActivity = PythonActivity.mActivity
                currentActivity.startActivity(shareIntent)
            except Exception as e:
                self.boleta.text = f"Error al compartir: {str(e)}"
        else:
            print(f"Simulación: Enviando {self.ruta_imagen} por WhatsApp...")

class BoletaApp(App):
    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        return GeneradorBoleta()

if __name__ == "__main__":
    BoletaApp().run()
