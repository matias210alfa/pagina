"""
Caja Chica - Aplicación de contabilidad sencilla
Desarrollada con Python + Kivy para Android (APK)
"""

import json
import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

# Colors
BG_PRIMARY = get_color_from_hex("#0f0f23")
BG_SECONDARY = get_color_from_hex("#1a1a2e")
BG_CARD = get_color_from_hex("#16213e")
TEXT_PRIMARY = get_color_from_hex("#e8e8f0")
TEXT_SECONDARY = get_color_from_hex("#a0a0b8")
TEXT_MUTED = get_color_from_hex("#6b6b80")
ACCENT_GREEN = get_color_from_hex("#00d68f")
ACCENT_RED = get_color_from_hex("#ff6b6b")
ACCENT_GREEN_BG = get_color_from_hex("#0d2e24")
ACCENT_RED_BG = get_color_from_hex("#2e1515")
WHITE = get_color_from_hex("#ffffff")

Window.clearcolor = BG_PRIMARY

DATA_FILE = "caja_chica_data.json"


def get_data_path():
    """Get platform-appropriate data path."""
    try:
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), DATA_FILE)
    except ImportError:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE)


def load_transactions():
    path = get_data_path()
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_transactions(transactions):
    path = get_data_path()
    with open(path, "w") as f:
        json.dump(transactions, f, indent=2)


def format_currency(amount):
    """Format number as ARS currency."""
    formatted = f"{abs(amount):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {formatted}"


def format_date(iso_string):
    """Format date for display."""
    try:
        dt = datetime.fromisoformat(iso_string)
        now = datetime.now()
        diff = now - dt
        if diff.days == 0:
            return dt.strftime("%H:%M")
        if diff.days == 1:
            return "Ayer"
        if diff.days < 7:
            return f"Hace {diff.days} días"
        return dt.strftime("%d %b")
    except (ValueError, TypeError):
        return ""


class RoundedButton(Button):
    """Custom button with rounded appearance."""
    pass


class TransactionItem(BoxLayout):
    """Single transaction row in the list."""

    def __init__(self, transaction, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(12), dp(8)]
        self.spacing = dp(10)
        self.transaction = transaction
        self.on_delete_callback = on_delete

        is_income = transaction["type"] == "ingreso"
        accent = ACCENT_GREEN if is_income else ACCENT_RED

        # Type icon
        icon_text = "↑" if is_income else "↓"
        icon_label = Label(
            text=icon_text,
            font_size=dp(20),
            bold=True,
            color=accent,
            size_hint_x=None,
            width=dp(40),
        )
        self.add_widget(icon_label)

        # Info section
        info_box = BoxLayout(orientation="vertical", spacing=dp(2))
        concept_label = Label(
            text=transaction["concept"],
            font_size=dp(14),
            color=TEXT_PRIMARY,
            halign="left",
            valign="center",
            text_size=(dp(150), None),
            shorten=True,
            shorten_from="right",
        )
        date_label = Label(
            text=format_date(transaction["date"]),
            font_size=dp(11),
            color=TEXT_MUTED,
            halign="left",
            valign="center",
            text_size=(dp(150), None),
        )
        info_box.add_widget(concept_label)
        info_box.add_widget(date_label)
        self.add_widget(info_box)

        # Amount
        sign = "+" if is_income else "-"
        amount_label = Label(
            text=f"{sign}{format_currency(transaction['amount'])}",
            font_size=dp(14),
            bold=True,
            color=accent,
            size_hint_x=None,
            width=dp(120),
            halign="right",
            text_size=(dp(120), None),
        )
        self.add_widget(amount_label)

        # Delete button
        del_btn = Button(
            text="✕",
            font_size=dp(12),
            color=TEXT_MUTED,
            background_color=(0, 0, 0, 0),
            size_hint_x=None,
            width=dp(35),
            on_release=self._delete,
        )
        self.add_widget(del_btn)

    def _delete(self, *args):
        self.on_delete_callback(self.transaction["id"])


class TransactionForm(ModalView):
    """Modal form to add a transaction."""

    def __init__(self, trans_type, on_save, **kwargs):
        super().__init__(**kwargs)
        self.trans_type = trans_type
        self.on_save_callback = on_save
        self.size_hint = (0.9, None)
        self.height = dp(340)
        self.background_color = (0, 0, 0, 0.6)
        self.auto_dismiss = True

        is_income = trans_type == "ingreso"
        accent = ACCENT_GREEN if is_income else ACCENT_RED
        accent_bg = ACCENT_GREEN_BG if is_income else ACCENT_RED_BG

        container = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(14),
        )

        from kivy.graphics import Color, RoundedRectangle
        with container.canvas.before:
            Color(*BG_SECONDARY)
            self._bg_rect = RoundedRectangle(
                pos=container.pos, size=container.size, radius=[dp(20)]
            )
        container.bind(
            pos=lambda *a: setattr(self._bg_rect, "pos", container.pos),
            size=lambda *a: setattr(self._bg_rect, "size", container.size),
        )

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(40))
        type_label = Label(
            text=f"{'+ Ingreso' if is_income else '− Egreso'}",
            font_size=dp(16),
            bold=True,
            color=accent,
            halign="left",
            text_size=(dp(200), None),
        )
        close_btn = Button(
            text="✕",
            font_size=dp(14),
            color=TEXT_SECONDARY,
            background_color=(0, 0, 0, 0),
            size_hint_x=None,
            width=dp(40),
            on_release=self.dismiss,
        )
        header.add_widget(type_label)
        header.add_widget(close_btn)
        container.add_widget(header)

        # Amount label
        amount_lbl = Label(
            text="MONTO",
            font_size=dp(11),
            color=TEXT_SECONDARY,
            halign="left",
            text_size=(dp(300), None),
            size_hint_y=None,
            height=dp(20),
        )
        container.add_widget(amount_lbl)

        # Amount input
        self.amount_input = TextInput(
            hint_text="0.00",
            input_filter="float",
            font_size=dp(24),
            foreground_color=TEXT_PRIMARY,
            background_color=BG_CARD,
            cursor_color=accent,
            hint_text_color=TEXT_MUTED,
            padding=[dp(12), dp(10)],
            size_hint_y=None,
            height=dp(50),
            multiline=False,
        )
        container.add_widget(self.amount_input)

        # Concept label
        concept_lbl = Label(
            text="CONCEPTO",
            font_size=dp(11),
            color=TEXT_SECONDARY,
            halign="left",
            text_size=(dp(300), None),
            size_hint_y=None,
            height=dp(20),
        )
        container.add_widget(concept_lbl)

        # Concept input
        placeholder = "Ej: Venta de repuesto" if is_income else "Ej: Compra de materiales"
        self.concept_input = TextInput(
            hint_text=placeholder,
            font_size=dp(15),
            foreground_color=TEXT_PRIMARY,
            background_color=BG_CARD,
            cursor_color=accent,
            hint_text_color=TEXT_MUTED,
            padding=[dp(12), dp(10)],
            size_hint_y=None,
            height=dp(45),
            multiline=False,
        )
        container.add_widget(self.concept_input)

        # Save button
        btn_text = "Guardar Ingreso" if is_income else "Guardar Egreso"
        self.save_btn = Button(
            text=btn_text,
            font_size=dp(16),
            bold=True,
            color=WHITE,
            background_color=accent,
            background_normal="",
            size_hint_y=None,
            height=dp(48),
            on_release=self._save,
        )
        container.add_widget(self.save_btn)

        self.add_widget(container)

        Clock.schedule_once(lambda dt: setattr(self.amount_input, "focus", True), 0.3)

    def _save(self, *args):
        try:
            amount = float(self.amount_input.text)
        except (ValueError, TypeError):
            return
        concept = self.concept_input.text.strip()
        if amount <= 0 or not concept:
            return
        self.on_save_callback(self.trans_type, amount, concept)
        self.dismiss()


class CajaChicaApp(App):
    """Main application."""

    balance = NumericProperty(0)
    balance_text = StringProperty("$ 0,00")
    balance_color = ColorProperty(ACCENT_GREEN)
    balance_status = StringProperty("Balance positivo")

    def build(self):
        self.title = "Caja Chica"
        self.transactions = load_transactions()
        self._update_balance()

        # Main layout
        self.root = BoxLayout(orientation="vertical", padding=[dp(16), dp(10)])

        from kivy.graphics import Color, Rectangle
        with self.root.canvas.before:
            Color(*BG_PRIMARY)
            self._root_bg = Rectangle(pos=self.root.pos, size=self.root.size)
        self.root.bind(
            pos=lambda *a: setattr(self._root_bg, "pos", self.root.pos),
            size=lambda *a: setattr(self._root_bg, "size", self.root.size),
        )

        # Title
        title = Label(
            text="Caja Chica",
            font_size=dp(22),
            bold=True,
            color=TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(50),
        )
        self.root.add_widget(title)

        # Balance card
        self._build_balance_card()

        # Action buttons
        self._build_action_buttons()

        # Transaction list
        self._build_transaction_list()

        return self.root

    def _build_balance_card(self):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(130),
            padding=[dp(20), dp(16)],
            spacing=dp(4),
        )

        from kivy.graphics import Color, RoundedRectangle
        with card.canvas.before:
            Color(*BG_CARD)
            self._card_bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(16)]
            )
        card.bind(
            pos=lambda *a: setattr(self._card_bg, "pos", card.pos),
            size=lambda *a: setattr(self._card_bg, "size", card.size),
        )

        saldo_label = Label(
            text="SALDO ACTUAL",
            font_size=dp(12),
            color=TEXT_SECONDARY,
            size_hint_y=None,
            height=dp(25),
        )
        card.add_widget(saldo_label)

        self.balance_label = Label(
            text=self.balance_text,
            font_size=dp(36),
            bold=True,
            color=self.balance_color,
            size_hint_y=None,
            height=dp(50),
        )
        card.add_widget(self.balance_label)

        self.status_label = Label(
            text=self.balance_status,
            font_size=dp(12),
            color=TEXT_MUTED,
            size_hint_y=None,
            height=dp(25),
        )
        card.add_widget(self.status_label)

        self.root.add_widget(card)
        self.root.add_widget(BoxLayout(size_hint_y=None, height=dp(12)))

    def _build_action_buttons(self):
        btn_row = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(12),
        )

        income_btn = Button(
            text="+ Ingreso",
            font_size=dp(16),
            bold=True,
            color=ACCENT_GREEN,
            background_color=ACCENT_GREEN_BG,
            background_normal="",
            on_release=lambda *a: self._show_form("ingreso"),
        )
        expense_btn = Button(
            text="− Egreso",
            font_size=dp(16),
            bold=True,
            color=ACCENT_RED,
            background_color=ACCENT_RED_BG,
            background_normal="",
            on_release=lambda *a: self._show_form("egreso"),
        )

        btn_row.add_widget(income_btn)
        btn_row.add_widget(expense_btn)
        self.root.add_widget(btn_row)
        self.root.add_widget(BoxLayout(size_hint_y=None, height=dp(16)))

    def _build_transaction_list(self):
        # Header
        self.list_header = Label(
            text="Movimientos",
            font_size=dp(17),
            bold=True,
            color=TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(35),
            halign="left",
            text_size=(dp(300), None),
        )

        # Empty state
        self.empty_label = Label(
            text="No hay movimientos aún\nUsa los botones de arriba para\nregistrar tu primer movimiento",
            font_size=dp(14),
            color=TEXT_MUTED,
            halign="center",
            valign="middle",
        )

        # Scrollable list
        self.scroll_view = ScrollView()
        self.list_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=[0, dp(4)],
        )
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll_view.add_widget(self.list_layout)

        self._refresh_list()

    def _refresh_list(self):
        # Remove old list widgets
        for widget in [self.list_header, self.empty_label, self.scroll_view]:
            if widget.parent:
                widget.parent.remove_widget(widget)

        self.list_layout.clear_widgets()

        if not self.transactions:
            self.root.add_widget(self.empty_label)
        else:
            self.root.add_widget(self.list_header)
            for t in self.transactions:
                item = TransactionItem(t, on_delete=self._delete_transaction)

                from kivy.graphics import Color, RoundedRectangle
                with item.canvas.before:
                    Color(*BG_CARD)
                    bg = RoundedRectangle(
                        pos=item.pos, size=item.size, radius=[dp(12)]
                    )
                item.bind(
                    pos=lambda inst, val, bg=bg: setattr(bg, "pos", val),
                    size=lambda inst, val, bg=bg: setattr(bg, "size", val),
                )
                self.list_layout.add_widget(item)
            self.root.add_widget(self.scroll_view)

    def _show_form(self, trans_type):
        form = TransactionForm(trans_type, on_save=self._add_transaction)
        form.open()

    def _add_transaction(self, trans_type, amount, concept):
        transaction = {
            "id": str(int(datetime.now().timestamp() * 1000)),
            "date": datetime.now().isoformat(),
            "type": trans_type,
            "amount": amount,
            "concept": concept,
        }
        self.transactions.insert(0, transaction)
        save_transactions(self.transactions)
        self._update_balance()
        self._refresh_list()

    def _delete_transaction(self, trans_id):
        self.transactions = [t for t in self.transactions if t["id"] != trans_id]
        save_transactions(self.transactions)
        self._update_balance()
        self._refresh_list()

    def _update_balance(self):
        self.balance = sum(
            t["amount"] if t["type"] == "ingreso" else -t["amount"]
            for t in self.transactions
        )
        self.balance_text = format_currency(self.balance)
        if self.balance < 0:
            self.balance_text = f"-{self.balance_text}"
        self.balance_color = ACCENT_GREEN if self.balance >= 0 else ACCENT_RED
        self.balance_status = (
            "Balance positivo" if self.balance >= 0 else "Balance negativo"
        )

        if hasattr(self, "balance_label"):
            self.balance_label.text = self.balance_text
            self.balance_label.color = self.balance_color
        if hasattr(self, "status_label"):
            self.status_label.text = self.balance_status


if __name__ == "__main__":
    CajaChicaApp().run()
