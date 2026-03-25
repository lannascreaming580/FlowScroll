from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QTextEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from FlowScroll.core.config import cfg
from FlowScroll.ui.helpers import create_card, create_h_line


class WorkModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("工作模式")
        self.setFixedSize(480, 480)

        self.setStyleSheet("""
            QDialog { background-color: #0F172A; font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; }
            QLabel { font-size: 13px; color: #E2E8F0; }
            QRadioButton { color: #E2E8F0; font-size: 14px; font-weight: 600; spacing: 12px; min-height: 24px; }
            QTextEdit { border: 1px solid #334155; border-radius: 8px; padding: 10px; background: #1E293B; font-size: 14px; color: #F8FAFC; }
            QTextEdit:focus { border: 1px solid #3B82F6; }
            QPushButton { background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 8px 16px; color: #F8FAFC; font-weight: 600; font-size: 13px; }
            QPushButton:hover { background-color: #334155; border-color: #475569; }
            QPushButton#BtnPrimary { background-color: #3B82F6; color: #FFFFFF; border: none; padding: 10px 24px; font-size: 14px; border-radius: 10px; }
            QPushButton#BtnPrimary:hover { background-color: #2563EB; }
            QPushButton#BtnPrimary:pressed { background-color: #1D4ED8; }
            QFrame#Card { background-color: #1E293B; border-radius: 16px; border: 1px solid #334155; }
            QFrame#Separator { background-color: #334155; max-height: 1px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        card, card_layout = create_card()

        # --- Filter mode radios ---
        card_layout.addWidget(
            QLabel(
                "<span style='font-weight: 600; color: #E2E8F0;'>应用过滤模式</span>"
            )
        )

        self.button_group = QButtonGroup(self)

        self.radio_global = QRadioButton("全局模式")
        self.radio_global.setCursor(Qt.PointingHandCursor)
        self.button_group.addButton(self.radio_global, 0)
        card_layout.addWidget(self.radio_global)

        self.radio_blacklist = QRadioButton("黑名单模式")
        self.radio_blacklist.setCursor(Qt.PointingHandCursor)
        self.button_group.addButton(self.radio_blacklist, 1)
        card_layout.addWidget(self.radio_blacklist)

        self.radio_global.setChecked(cfg.filter_mode == 0)
        self.radio_blacklist.setChecked(cfg.filter_mode == 1)

        card_layout.addWidget(create_h_line())

        # --- Blacklist text ---
        hint_lbl = QLabel(
            "<span style='font-weight: 600; color: #E2E8F0;'>黑名单</span>"
            "<br><span style='color: #94A3B8; font-size: 12px;'>"
            "每行输入一个应用名称关键词，不区分大小写。<br>"
            "例如输入 <b>potplayer</b> 即可在该播放器中禁用滚动。</span>"
        )
        hint_lbl.setWordWrap(True)
        card_layout.addWidget(hint_lbl)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("\n".join(cfg.filter_list))
        self.text_edit.setMinimumHeight(120)
        self.text_edit.setEnabled(cfg.filter_mode != 0)
        self.button_group.idClicked.connect(
            lambda mid: self.text_edit.setEnabled(mid != 0)
        )
        card_layout.addWidget(self.text_edit)

        layout.addWidget(card)

        # --- Save button ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton("确定")
        btn_save.setObjectName("BtnPrimary")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def save_and_close(self):
        cfg.filter_mode = self.button_group.checkedId()
        cfg.filter_list = [
            line.strip()
            for line in self.text_edit.toPlainText().split("\n")
            if line.strip()
        ]
        self.accept()
