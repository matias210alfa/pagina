import json
import os
from datetime import datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ColorProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

# --- PALETA MINIMALISTA CLARA ---
BG_LIGHT = get_color_from_hex("#F5F5F7")      # Fondo claro
BG_CARD = get_color_from_hex("#FFFFFF")       # Tarjetas blancas
TEXT_MAIN = get_color_from_hex("#1D1D1F")     # Texto principal
TEXT_SEC = get_color_from_hex("#86868B")      # Texto secundario
ACCENT_BLUE = get_color_from_hex("#007AFF")   # Azul iOS
SOFT_GREEN = get_color_from_hex("#34C759")    # Verde suave
SOFT_RED = get_color_from_hex("#FF3B30")      # Rojo suave

Window.clearcolor = BG_LIGHT
DATA_FILE = "pequeno_contador_data.json"

def get_data_path():
    try:
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), DATA_FILE)
    except ImportError:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE)

def load_data():
    path = get_data_path()
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    path = get_data_path()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def format_curr(amount):
    return f"$ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class TransactionItem(BoxLayout):
    def __init__(self, t, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(65)
        self.padding = [dp(15), dp(10)]
        self.spacing = dp(10)
        
        # Círculo de color según tipo
        is_inc = t["type"] == "ingreso"
        color = SOFT_GREEN if is_inc else SOFT_RED
        
        info = BoxLayout(orientation="vertical")
        info.add_widget(Label(text=t["concept"], color=TEXT_MAIN, font_size=dp(15), halign="left", text_size=(dp(200), None)))
        info.add_widget(Label(text=t["date"][:10], color=TEXT_SEC, font_size=dp(11), halign="left", text_size=(dp(200), None)))
        self.add_widget(info)
        
        amt = Label(text=f"{'+' if is_inc else '-'}{format_curr(t['amount'])}", 
                    color=color, bold=True, font_size=dp(14), size_hint_x=None, width=dp(100), halign="right")
        self.add_widget(amt)
        
        del_btn = Button(text="×", color=TEXT_SEC, background_color=(0,0,0,0), size_hint_x=None, width=dp(30), on_release=lambda x: on_delete(t["id"]))
        self.add_widget(del_btn)

class PequenoContadorApp(App):
    bal_semanal = StringProperty("$ 0,00")
    bal_mensual = StringProperty("$ 0,00")

    def build(self):
        self.title = "Pequeño Contador"
        self.transactions = load_data()
        
        main = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))
        
        # Header
        main.add_widget(Label(text="Pequeño Contador", font_size=dp(24), bold=True, color=TEXT_MAIN, size_hint_y=None, height=dp(40)))
        
        # Tarjetas de Balances
        bals = BoxLayout(size_hint_y=None, height=dp(100), spacing=dp(10))
        
        # Tarjeta Semanal (Más grande)
        sem_card = self._create_card("ESTA SEMANA", self.bal_semanal, size_hint_x=0.6)
        # Tarjeta Mensual (Más pequeña)
        mes_card = self._create_card("ESTE MES", self.bal_mensual, size_hint_x=0.4)
        
        bals.add_widget(sem_card)
        bals.add_widget(mes_card)
        main.add_widget(bals)
        
        # Botones de acción
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        btns.add_widget(Button(text="+ Ingreso", background_color=SOFT_GREEN, background_normal="", bold=True, on_release=lambda x: self._open_form("ingreso")))
        btns.add_widget(Button(text="- Egreso", background_color=SOFT_RED, background_normal="", bold=True, on_release=lambda x: self._open_form("egreso")))
        main.add_widget(btns)
        
        # Lista
        main.add_widget(Label(text="Actividad Reciente", color=TEXT_SEC, font_size=dp(13), halign="left", text_size=(dp(300), None), size_hint_y=None, height=dp(30)))
        self.scroll = ScrollView()
        self.list_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
        main.add_widget(self.scroll)
        
        self._update_ui()
        return main

    def _create_card(self, title, prop, size_hint_x):
        card = BoxLayout(orientation="vertical", padding=dp(15), size_hint_x=size_hint_x)
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*BG_CARD)
            self.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(15)])
        card.bind(pos=self._update_rect, size=self._update_rect)
        
        card.add_widget(Label(text=title, color=TEXT_SEC, font_size=dp(10), halign="left", text_size=(dp(150), None)))
        lbl_val = Label(text="", color=TEXT_MAIN, font_size=dp(18), bold=True, halign="left", text_size=(dp(150), None))
        
        # Vincular la propiedad al texto del label
        if "SEMANA" in title:
            self.bind(bal_semanal=lbl_val.setter("text"))
        else:
            self.bind(bal_mensual=lbl_val.setter("text"))
            
        card.add_widget(lbl_val)
        return card

    def _update_rect(self, instance, value):
        for instr in instance.canvas.before.children:
            if isinstance(instr, RoundedRectangle):
                instr.pos = instance.pos
                instr.size = instance.size

    def _update_ui(self):
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0)
        inicio_sem = hoy - timedelta(days=hoy.weekday())
        inicio_sem = inicio_sem.replace(hour=0, minute=0)
        
        sum_sem = 0
        sum_mes = 0
        
        self.list_layout.clear_widgets()
        for t in self.transactions:
            f_t = datetime.fromisoformat(t["date"])
            val = t["amount"] if t["type"] == "ingreso" else -t["amount"]
            
            if f_t >= inicio_mes: sum_mes += val
            if f_t >= inicio_sem: sum_sem += val
            
            # Solo mostrar los últimos 20 en la lista principal para minimalismo
            if len(self.list_layout.children) < 20:
                self.list_layout.add_widget(TransactionItem(t, self._delete_trans))
        
        self.bal_semanal = format_curr(sum_sem)
        self.bal_mensual = format_curr(sum_mes)

    def _open_form(self, tipo):
        content = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        amt_in = TextInput(hint_text="Monto", input_filter="float", multiline=False, font_size=dp(20))
        con_in = TextInput(hint_text="Concepto", multiline=False)
        save_btn = Button(text="Guardar", background_color=ACCENT_BLUE, background_normal="", size_hint_y=None, height=dp(50))
        
        content.add_widget(Label(text=f"Nuevo {tipo.capitalize()}", color=TEXT_MAIN, bold=True))
        content.add_widget(amt_in)
        content.add_widget(con_in)
        content.add_widget(save_btn)
        
        popup = ModalView(size_hint=(0.8, 0.5), background_color=[0,0,0,0.5])
        popup.add_widget(content)
        
        def save(instance):
            if amt_in.text and con_in.text:
                new_t = {
                    "id": str(datetime.now().timestamp()),
                    "date": datetime.now().isoformat(),
                    "type": tipo,
                    "amount": float(amt_in.text),
                    "concept": con_in.text
                }
                self.transactions.insert(0, new_t)
                save_data(self.transactions)
                self._update_ui()
                popup.dismiss()
        
        save_btn.bind(on_release=save)
        popup.open()

    def _delete_trans(self, t_id):
        self.transactions = [t for t in self.transactions if t["id"] != t_id]
        save_data(self.transactions)
        self._update_ui()

if __name__ == "__main__":
    PequenoContadorApp().run()
