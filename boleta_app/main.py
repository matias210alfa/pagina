import os
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.image import Image

if platform != 'android':
    Window.size = (400, 780)


def bg_widget(widget, color):
    with widget.canvas.before:
        Color(*color)
        r = Rectangle(size=widget.size, pos=widget.pos)
    widget.bind(size=lambda w, v: setattr(r, 'size', v),
                pos=lambda w, v: setattr(r, 'pos', v))
    return r


def make_label(text, **kw):
    defaults = dict(color=(0, 0, 0, 1), markup=True, halign='left', valign='middle')
    defaults.update(kw)
    lbl = Label(text=text, **defaults)
    lbl.bind(size=lbl.setter('text_size'))
    return lbl


class CeldaTabla(BoxLayout):
    def __init__(self, texto, bold=False, align='center', **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 30
        t = f"[b]{texto}[/b]" if bold else texto
        lbl = make_label(t, font_size='11sp', halign=align, valign='middle')
        self.add_widget(lbl)
        with self.canvas.after:
            Color(0.6, 0.6, 0.6, 1)
            self._line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.bind(pos=self._update_border, size=self._update_border)

    def _update_border(self, *args):
        self._line.rectangle = (self.x, self.y, self.width, self.height)


class GeneradorBoleta(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 6

        self.nombre = "Lucas Silva"
        self.rut = "150873330016"
        self.cel = "092165379"
        self.email = "matias201908@gmail.com"
        self.ubicacion = "Salto, Uruguay"
        self.ruta_imagen = None

        # Ruta del logo
        self.logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')

        # --- ENCABEZADO ---
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=170,
                           padding=[0, 5, 0, 5], spacing=2)
        header.add_widget(make_label("Diseñado por Lucas Silva",
                                     font_size='12sp', halign='center',
                                     size_hint_y=None, height=20))
        header.add_widget(make_label("[b]TÉCNICO EN[/b]", font_size='14sp',
                                     halign='center', size_hint_y=None, height=20))
        header.add_widget(make_label("[b]MÁQUINAS DE COSER[/b]", font_size='16sp',
                                     halign='center', size_hint_y=None, height=22))
        if os.path.exists(self.logo_path):
            header.add_widget(Image(source=self.logo_path, size_hint_y=None,
                                    height=80, allow_stretch=True))
        header.add_widget(make_label("Técnico habilitado por UTE",
                                     font_size='10sp', halign='center',
                                     size_hint_y=None, height=18))
        self.add_widget(header)

        # --- INPUTS ---
        row_precio = BoxLayout(size_hint_y=None, height=40, spacing=5)
        row_precio.add_widget(make_label("Precio:", font_size='14sp', bold=True,
                                         size_hint_x=0.3))
        self.input_precio = TextInput(hint_text="$", multiline=False,
                                      input_filter='float', size_hint_x=0.7,
                                      font_size='14sp')
        row_precio.add_widget(self.input_precio)
        self.add_widget(row_precio)

        row_detalle = BoxLayout(size_hint_y=None, height=70, spacing=5)
        row_detalle.add_widget(make_label("Detalle:", font_size='14sp', bold=True,
                                          size_hint_x=0.3, valign='top'))
        self.input_detalle = TextInput(hint_text="Descripción del trabajo",
                                       multiline=True, size_hint_x=0.7,
                                       font_size='13sp')
        row_detalle.add_widget(self.input_detalle)
        self.add_widget(row_detalle)

        # --- BOTÓN VISUALIZAR ---
        btn_ver = Button(text="👁  VISUALIZAR", size_hint_y=None, height=45,
                         font_size='15sp', bold=True,
                         background_color=(0.65, 0.65, 0.65, 1),
                         color=(0, 0, 0, 1))
        btn_ver.bind(on_release=self.actualizar)
        self.add_widget(btn_ver)

        # --- ÁREA DE LA BOLETA ---
        scroll = ScrollView(size_hint_y=1)
        self.area_boleta = BoxLayout(orientation='vertical', padding=12,
                                     spacing=4, size_hint_y=None)
        self.area_boleta.bind(minimum_height=self.area_boleta.setter('height'))
        bg_widget(self.area_boleta, (1, 1, 1, 1))

        self.boleta_titulo = make_label(
            "[b]BOLETA TÉCNICA (Vista Previa)[/b]",
            font_size='14sp', halign='center', size_hint_y=None, height=28)
        self.area_boleta.add_widget(self.boleta_titulo)

        # Logo en boleta
        if os.path.exists(self.logo_path):
            self.area_boleta.add_widget(Image(source=self.logo_path,
                                              size_hint_y=None, height=60,
                                              allow_stretch=True))

        # Info contacto
        info_row = BoxLayout(size_hint_y=None, height=60, spacing=5)
        info_left = BoxLayout(orientation='vertical', size_hint_x=0.55)
        info_left.add_widget(make_label(f"[b]{self.nombre}[/b]", font_size='12sp',
                                        size_hint_y=None, height=18))
        info_left.add_widget(make_label(f"Cel. {self.cel}", font_size='10sp',
                                        size_hint_y=None, height=16))
        info_left.add_widget(make_label(f"{self.email}", font_size='9sp',
                                        size_hint_y=None, height=16))
        info_row.add_widget(info_left)

        info_right = BoxLayout(orientation='vertical', size_hint_x=0.45)
        self.lbl_fecha = make_label("", font_size='10sp', halign='right',
                                    size_hint_y=None, height=18)
        info_right.add_widget(self.lbl_fecha)
        info_right.add_widget(make_label(self.ubicacion, font_size='10sp',
                                         halign='right', size_hint_y=None, height=16))
        info_right.add_widget(make_label(f"[b]RUT: {self.rut}[/b]",
                                         font_size='10sp', halign='right',
                                         size_hint_y=None, height=16))
        info_row.add_widget(info_right)
        self.area_boleta.add_widget(info_row)

        # Tabla
        self.tabla_container = BoxLayout(orientation='vertical', size_hint_y=None,
                                         height=65)
        self._crear_tabla_vacia()
        self.area_boleta.add_widget(self.tabla_container)

        # Totales
        self.lbl_subtotal = make_label("Subtotal: $0", font_size='11sp',
                                       halign='right', size_hint_y=None, height=20)
        self.area_boleta.add_widget(self.lbl_subtotal)
        self.lbl_total = make_label("[b]TOTAL: $0[/b]", font_size='13sp',
                                    halign='right', size_hint_y=None, height=22)
        self.area_boleta.add_widget(self.lbl_total)

        # Notas
        notas = BoxLayout(orientation='vertical', size_hint_y=None, height=40,
                          padding=[0, 5, 0, 0])
        notas.add_widget(make_label("[b]Notas:[/b]", font_size='10sp',
                                    size_hint_y=None, height=16))
        notas.add_widget(make_label("Plazo de validez: 15 días | Garantía: 15 días",
                                    font_size='9sp', size_hint_y=None, height=16))
        self.area_boleta.add_widget(notas)

        scroll.add_widget(self.area_boleta)
        self.add_widget(scroll)

        # --- BOTONES DE ACCIÓN ---
        btn_guardar = Button(text="⬇  DESCARGAR IMAGEN", size_hint_y=None,
                             height=50, font_size='14sp', bold=True,
                             background_color=(0.65, 0.65, 0.65, 1),
                             color=(0, 0, 0, 1))
        btn_guardar.bind(on_release=self.guardar)
        self.add_widget(btn_guardar)

        btn_wsp = Button(text="📲  COMPARTIR POR\nWHATSAPP LA IMAGEN",
                         size_hint_y=None, height=55, font_size='13sp', bold=True,
                         background_color=(0.18, 0.62, 0.25, 1),
                         color=(1, 1, 1, 1), halign='center')
        btn_wsp.bind(on_release=self.enviar_whatsapp)
        self.add_widget(btn_wsp)

    def _crear_tabla_vacia(self):
        self.tabla_container.clear_widgets()
        header = GridLayout(cols=4, size_hint_y=None, height=30, spacing=1)
        for txt in ["Cantidad", "Descripción", "Precio", "Total"]:
            header.add_widget(CeldaTabla(txt, bold=True))
        self.tabla_container.add_widget(header)

        row = GridLayout(cols=4, size_hint_y=None, height=30, spacing=1)
        for txt in ["1", "Mano de Obra", "$0", "$0"]:
            row.add_widget(CeldaTabla(txt))
        self.tabla_container.add_widget(row)

    def _crear_tabla(self, detalle, precio):
        self.tabla_container.clear_widgets()
        header = GridLayout(cols=4, size_hint_y=None, height=30, spacing=1)
        for txt in ["Cantidad", "Descripción", "Precio", "Total"]:
            header.add_widget(CeldaTabla(txt, bold=True))
        self.tabla_container.add_widget(header)

        desc = detalle[:22] if len(detalle) > 22 else detalle
        row = GridLayout(cols=4, size_hint_y=None, height=30, spacing=1)
        row.add_widget(CeldaTabla("1"))
        row.add_widget(CeldaTabla(desc))
        row.add_widget(CeldaTabla(f"${precio}"))
        row.add_widget(CeldaTabla(f"${precio}"))
        self.tabla_container.add_widget(row)

    def actualizar(self, *args):
        precio = self.input_precio.text.strip()
        detalle = self.input_detalle.text.strip()
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")

        if not precio or not detalle:
            self.boleta_titulo.text = "[color=ff0000]⚠️ Complete precio y detalle[/color]"
            return

        self.boleta_titulo.text = "[b]BOLETA TÉCNICA (Vista Previa)[/b]"
        self.lbl_fecha.text = fecha
        self._crear_tabla(detalle, precio)
        self.lbl_subtotal.text = f"Subtotal: ${precio}"
        self.lbl_total.text = f"[b]TOTAL: ${precio}[/b]"

    def guardar(self, *args):
        if not self.input_precio.text or not self.input_detalle.text:
            self.boleta_titulo.text = "[color=ff0000]⚠️ Primero ingresa los datos[/color]"
            return

        self.actualizar()
        nombre_archivo = f"boleta_{datetime.datetime.now().strftime('%H%M%S')}.png"

        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = os.path.join(primary_external_storage_path(), 'Download')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            path = os.path.join(dir_path, nombre_archivo)
        else:
            path = nombre_archivo

        self.area_boleta.export_to_png(path)
        self.ruta_imagen = path
        self.boleta_titulo.text = "[b]BOLETA TÉCNICA[/b] [color=008800]✅ Guardada[/color]"

    def enviar_whatsapp(self, *args):
        if not self.ruta_imagen or not os.path.exists(self.ruta_imagen):
            self.boleta_titulo.text = "[color=ff0000]⚠️ Guarda la boleta primero[/color]"
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
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
                self.boleta_titulo.text = f"[color=ff0000]Error: {e}[/color]"
        else:
            print(f"Simulación: Enviando {self.ruta_imagen} por WhatsApp...")


class BoletaApp(App):
    def build(self):
        self.title = "Boleta Técnica"
        Window.clearcolor = (0.96, 0.94, 0.90, 1)
        return GeneradorBoleta()


if __name__ == "__main__":
    BoletaApp().run()
