from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QRadioButton,
    QButtonGroup,
    QTextEdit,
    QPushButton,
    QSlider,
    QFileDialog,
    QMessageBox,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from FlowScroll.core.config import cfg
from FlowScroll.ui.components import HotkeyEdit
from FlowScroll.ui.helpers import create_card, create_h_line
from FlowScroll.ui.styles import (
    get_dialog_stylesheet,
    get_checkbox_style,
    get_radiobutton_style,
    get_textedit_style,
    get_slider_style,
    get_value_label_style,
    get_hint_label_style,
)
from FlowScroll.constants import (
    REVERSE_DIALOG_WIDTH,
    REVERSE_DIALOG_HEIGHT,
    WORK_MODE_DIALOG_WIDTH,
    WORK_MODE_DIALOG_HEIGHT,
    INERTIA_DIALOG_WIDTH,
    INERTIA_DIALOG_HEIGHT,
)


class ReverseModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('滚轮方向')
        self.setMinimumSize(REVERSE_DIALOG_WIDTH, REVERSE_DIALOG_HEIGHT)
        self.setSizeGripEnabled(True)

        self.setStyleSheet(get_dialog_stylesheet() + get_checkbox_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        card, card_layout = create_card()

        hint_lbl = QLabel("可按个人习惯反转纵向/横向滚轮方向。")
        hint_lbl.setWordWrap(True)
        card_layout.addWidget(hint_lbl)

        card_layout.addWidget(create_h_line())

        self.chk_reverse_y = QCheckBox('反转纵向滚动 (Y轴)')
        self.chk_reverse_y.setChecked(cfg.reverse_y)
        self.chk_reverse_y.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.chk_reverse_y)

        self.chk_reverse_x = QCheckBox('反转横向滚动 (X轴)')
        self.chk_reverse_x.setChecked(cfg.reverse_x)
        self.chk_reverse_x.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.chk_reverse_x)

        layout.addWidget(card)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton('确定')
        btn_save.setObjectName('BtnPrimary')
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

        adaptive_height = max(REVERSE_DIALOG_HEIGHT, self.sizeHint().height())
        self.resize(REVERSE_DIALOG_WIDTH, adaptive_height)

    def save_and_close(self):
        cfg.reverse_y = self.chk_reverse_y.isChecked()
        cfg.reverse_x = self.chk_reverse_x.isChecked()
        self.accept()


class WorkModeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('工作模式')
        self.setMinimumSize(WORK_MODE_DIALOG_WIDTH, WORK_MODE_DIALOG_HEIGHT)
        self.setSizeGripEnabled(True)

        self.setStyleSheet(
            get_dialog_stylesheet() + get_radiobutton_style() + get_checkbox_style()
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        mode_card, mode_layout = create_card()
        mode_layout.setContentsMargins(16, 16, 16, 16)
        mode_layout.setSpacing(12)

        title = QLabel('滚动启用方式')
        title.setStyleSheet('font-size: 17px; font-weight: 700; color: #F8FAFC;')
        subtitle = QLabel(
            '你可以设置“按一下开关”或“按住才生效”。下方快捷键支持鼠标和键盘。'
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet('color: #94A3B8; font-size: 13px;')
        mode_layout.addWidget(title)
        mode_layout.addWidget(subtitle)

        self.activation_group = QButtonGroup(self)
        self._build_mode_block(
            mode_layout,
            mode_id=0,
            title='按一下开启 / 再按一下关闭',
            desc='适合长时间阅读或浏览网页，切换成本更低。',
            key_name='click',
            hotkey_value=cfg.activation_hotkey_click,
        )
        self._build_mode_block(
            mode_layout,
            mode_id=1,
            title='按住时生效 / 松开后关闭',
            desc='适合临时滚动，结束后自动恢复，不影响原有操作习惯。',
            key_name='hold',
            hotkey_value=cfg.activation_hotkey_hold,
        )
        self.radio_click_toggle.setChecked(cfg.activation_mode == 0)
        self.radio_hold.setChecked(cfg.activation_mode == 1)
        layout.addWidget(mode_card)

        policy_card, policy_layout = create_card()
        policy_layout.setContentsMargins(16, 16, 16, 16)
        policy_layout.setSpacing(10)

        self.chk_activation_compat_mode = QCheckBox('防误触模式（短按不触发，按住一会儿才触发）')
        self.chk_activation_compat_mode.setChecked(cfg.activation_compat_mode)
        self.chk_activation_compat_mode.setCursor(Qt.PointingHandCursor)
        self.chk_activation_compat_mode.toggled.connect(self._on_compat_mode_changed)
        policy_layout.addWidget(self.chk_activation_compat_mode)

        delay_row = QHBoxLayout()
        delay_row.setContentsMargins(8, 0, 0, 0)
        delay_row.setSpacing(10)
        self.delay_title = QLabel('触发等待时间')
        self.delay_title.setStyleSheet('color: #94A3B8; font-size: 13px;')
        self.delay_value_label = QLabel()
        self.delay_value_label.setStyleSheet(get_value_label_style())

        self.activation_delay_slider = QSlider(Qt.Horizontal)
        self.activation_delay_slider.setRange(0, 500)
        self.activation_delay_slider.setSingleStep(10)
        self.activation_delay_slider.setValue(int(cfg.activation_delay_ms))
        self.activation_delay_slider.valueChanged.connect(self._update_delay_label)
        self.activation_delay_slider.setCursor(Qt.PointingHandCursor)
        self.activation_delay_slider.setFixedHeight(22)

        delay_row.addWidget(self.delay_title)
        delay_row.addWidget(self.activation_delay_slider, 1)
        delay_row.addWidget(self.delay_value_label)
        policy_layout.addLayout(delay_row)

        self.compat_hint = QLabel(
            '建议 150~250ms，可减少“中键关标签页/关窗口”这类误触。'
        )
        self.compat_hint.setWordWrap(True)
        self.compat_hint.setContentsMargins(8, 0, 0, 0)
        self.compat_hint.setStyleSheet('color: #94A3B8; font-size: 12px;')
        policy_layout.addWidget(self.compat_hint)

        layout.addWidget(policy_card)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton('保存设置')
        btn_save.setObjectName('BtnPrimary')
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

        self._update_delay_label()
        self._on_compat_mode_changed(self.chk_activation_compat_mode.isChecked())

        adaptive_height = max(WORK_MODE_DIALOG_HEIGHT, self.sizeHint().height())
        self.resize(WORK_MODE_DIALOG_WIDTH, adaptive_height)

    def _build_mode_block(self, parent_layout, mode_id, title, desc, key_name, hotkey_value):
        block = QLabel()
        block.setFixedHeight(1)
        if parent_layout.count() > 0:
            parent_layout.addWidget(create_h_line())

        radio = QRadioButton(title)
        radio.setCursor(Qt.PointingHandCursor)
        self.activation_group.addButton(radio, mode_id)
        parent_layout.addWidget(radio)

        if mode_id == 0:
            self.radio_click_toggle = radio
        else:
            self.radio_hold = radio

        desc_lbl = QLabel(desc)
        desc_lbl.setWordWrap(True)
        desc_lbl.setContentsMargins(24, 0, 0, 0)
        desc_lbl.setStyleSheet('color: #94A3B8; font-size: 12px;')
        parent_layout.addWidget(desc_lbl)
        parent_layout.addLayout(self._create_hotkey_row(key_name, hotkey_value))

    def _create_hotkey_row(self, key_name, hotkey_value):
        wrapper = QVBoxLayout()
        wrapper.setContentsMargins(24, 0, 0, 0)
        wrapper.setSpacing(8)

        row = QHBoxLayout()
        row.setSpacing(8)

        edit = HotkeyEdit()
        edit.set_hotkey(hotkey_value)
        edit.setMaximumSequenceLength(1)
        row.addWidget(edit, 1)

        btn_clear = QPushButton('默认')
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.clicked.connect(edit.clear)
        row.addWidget(btn_clear)

        wrapper.addLayout(row)
        setattr(self, f'activation_hotkey_edit_{key_name}', edit)
        return wrapper

    def _update_delay_label(self):
        self.delay_value_label.setText(f'{self.activation_delay_slider.value()} ms')

    def _on_compat_mode_changed(self, checked):
        self.activation_delay_slider.setEnabled(checked)
        self.delay_title.setEnabled(checked)
        self.delay_value_label.setEnabled(checked)
        self.compat_hint.setEnabled(checked)

    def save_and_close(self):
        cfg.activation_mode = self.activation_group.checkedId()
        cfg.activation_hotkey_click = self.activation_hotkey_edit_click.hotkey_text()
        cfg.activation_hotkey_hold = self.activation_hotkey_edit_hold.hotkey_text()
        cfg.activation_compat_mode = self.chk_activation_compat_mode.isChecked()
        cfg.activation_delay_ms = int(self.activation_delay_slider.value())
        self.accept()


class AppFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('应用过滤模式')
        self.setMinimumSize(WORK_MODE_DIALOG_WIDTH, WORK_MODE_DIALOG_HEIGHT)
        self.setSizeGripEnabled(True)

        self.setStyleSheet(
            get_dialog_stylesheet() + get_radiobutton_style() + get_textedit_style()
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel('应用过滤规则')
        title.setStyleSheet('font-size: 17px; font-weight: 700; color: #F8FAFC;')
        subtitle = QLabel(
            '用黑名单或白名单指定哪些应用启用滚动增强，避免在不希望的应用里误触。'
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet('color: #94A3B8; font-size: 13px;')
        layout.addWidget(title)
        layout.addWidget(subtitle)

        mode_card, mode_layout = create_card()
        mode_layout.setContentsMargins(16, 16, 16, 16)
        mode_layout.setSpacing(10)

        mode_title = QLabel('过滤模式')
        mode_title.setStyleSheet('font-size: 15px; font-weight: 700; color: #E2E8F0;')
        mode_layout.addWidget(mode_title)

        self.button_group = QButtonGroup(self)

        self.radio_global = QRadioButton('全局模式')
        self.radio_global.setCursor(Qt.PointingHandCursor)
        self.button_group.addButton(self.radio_global, 0)
        mode_layout.addWidget(self.radio_global)

        desc_global = QLabel("该模式下滚动功能对所有应用生效（仍受全屏禁用影响）。")
        desc_global.setWordWrap(True)
        desc_global.setContentsMargins(24, 0, 0, 0)
        desc_global.setStyleSheet('color: #94A3B8; font-size: 12px;')
        mode_layout.addWidget(desc_global)

        mode_layout.addWidget(create_h_line())

        self.radio_blacklist = QRadioButton('黑名单模式')
        self.radio_blacklist.setCursor(Qt.PointingHandCursor)
        self.button_group.addButton(self.radio_blacklist, 1)
        mode_layout.addWidget(self.radio_blacklist)

        desc_blacklist = QLabel("每行一个应用关键词（不区分大小写），命中后禁用滚动增强。")
        desc_blacklist.setWordWrap(True)
        desc_blacklist.setContentsMargins(24, 0, 0, 0)
        desc_blacklist.setStyleSheet('color: #94A3B8; font-size: 12px;')
        mode_layout.addWidget(desc_blacklist)

        mode_layout.addWidget(create_h_line())

        self.radio_whitelist = QRadioButton('白名单模式')
        self.radio_whitelist.setCursor(Qt.PointingHandCursor)
        self.button_group.addButton(self.radio_whitelist, 2)
        mode_layout.addWidget(self.radio_whitelist)

        desc_whitelist = QLabel("每行一个应用关键词（不区分大小写），仅在命中应用内启用滚动增强。")
        desc_whitelist.setWordWrap(True)
        desc_whitelist.setContentsMargins(24, 0, 0, 0)
        desc_whitelist.setStyleSheet('color: #94A3B8; font-size: 12px;')
        mode_layout.addWidget(desc_whitelist)

        self.radio_global.setChecked(cfg.filter_mode == 0)
        self.radio_blacklist.setChecked(cfg.filter_mode == 1)
        self.radio_whitelist.setChecked(cfg.filter_mode == 2)
        layout.addWidget(mode_card)

        keyword_card, keyword_layout = create_card()
        keyword_layout.setContentsMargins(16, 16, 16, 16)
        keyword_layout.setSpacing(10)

        list_row = QHBoxLayout()
        list_row.setSpacing(12)

        left_col = QVBoxLayout()
        left_col.setSpacing(8)
        lbl_black = QLabel('黑名单关键词')
        lbl_black.setStyleSheet('color: #E2E8F0; font-weight: 600;')
        lbl_black.setAlignment(Qt.AlignHCenter)
        black_action_row = QHBoxLayout()
        black_action_row.setSpacing(8)
        black_action_row.setContentsMargins(0, 7, 0, 7)
        self.btn_import_black = QPushButton('导入')
        self.btn_import_black.setCursor(Qt.PointingHandCursor)
        self.btn_import_black.setObjectName('BtnSmall')
        self.btn_import_black.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_import_black.setFixedHeight(20)
        self.btn_import_black.setStyleSheet("min-height: 20px; padding-top: 1px; padding-bottom: 1px;")
        self.btn_import_black.clicked.connect(
            lambda: self._import_keywords_to(self.text_edit_blacklist)
        )
        black_action_row.addWidget(self.btn_import_black)
        self.btn_clear_black = QPushButton('清空')
        self.btn_clear_black.setCursor(Qt.PointingHandCursor)
        self.btn_clear_black.setObjectName('BtnSmall')
        self.btn_clear_black.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_clear_black.setFixedHeight(20)
        self.btn_clear_black.setStyleSheet("min-height: 20px; padding-top: 1px; padding-bottom: 1px;")
        self.btn_clear_black.clicked.connect(
            lambda: self._clear_keywords(self.text_edit_blacklist, '黑名单')
        )
        black_action_row.addWidget(self.btn_clear_black)
        self.text_edit_blacklist = QTextEdit()
        self.text_edit_blacklist.setPlainText('\n'.join(cfg.filter_blacklist))
        self.text_edit_blacklist.setMinimumHeight(140)
        left_col.addWidget(lbl_black)
        left_col.addLayout(black_action_row)
        left_col.addWidget(self.text_edit_blacklist)

        right_col = QVBoxLayout()
        right_col.setSpacing(8)
        lbl_white = QLabel('白名单关键词')
        lbl_white.setStyleSheet('color: #E2E8F0; font-weight: 600;')
        lbl_white.setAlignment(Qt.AlignHCenter)
        white_action_row = QHBoxLayout()
        white_action_row.setSpacing(8)
        white_action_row.setContentsMargins(0, 7, 0, 7)
        self.btn_import_white = QPushButton('导入')
        self.btn_import_white.setCursor(Qt.PointingHandCursor)
        self.btn_import_white.setObjectName('BtnSmall')
        self.btn_import_white.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_import_white.setFixedHeight(20)
        self.btn_import_white.setStyleSheet("min-height: 20px; padding-top: 1px; padding-bottom: 1px;")
        self.btn_import_white.clicked.connect(
            lambda: self._import_keywords_to(self.text_edit_whitelist)
        )
        white_action_row.addWidget(self.btn_import_white)
        self.btn_clear_white = QPushButton('清空')
        self.btn_clear_white.setCursor(Qt.PointingHandCursor)
        self.btn_clear_white.setObjectName('BtnSmall')
        self.btn_clear_white.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_clear_white.setFixedHeight(20)
        self.btn_clear_white.setStyleSheet("min-height: 20px; padding-top: 1px; padding-bottom: 1px;")
        self.btn_clear_white.clicked.connect(
            lambda: self._clear_keywords(self.text_edit_whitelist, '白名单')
        )
        white_action_row.addWidget(self.btn_clear_white)
        self.text_edit_whitelist = QTextEdit()
        self.text_edit_whitelist.setPlainText('\n'.join(cfg.filter_whitelist))
        self.text_edit_whitelist.setMinimumHeight(140)
        right_col.addWidget(lbl_white)
        right_col.addLayout(white_action_row)
        right_col.addWidget(self.text_edit_whitelist)

        list_row.addLayout(left_col, 1)
        list_row.addLayout(right_col, 1)
        keyword_layout.addLayout(list_row)

        hint = QLabel('支持从文本导入关键词；每行一条，建议使用稳定的应用名片段（如 chrome、code、potplayer）。')
        hint.setWordWrap(True)
        hint.setStyleSheet('color: #94A3B8; font-size: 12px;')
        keyword_layout.addWidget(hint)

        layout.addWidget(keyword_card)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton('保存设置')
        btn_save.setObjectName('BtnPrimary')
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

        adaptive_height = max(WORK_MODE_DIALOG_HEIGHT, self.sizeHint().height())
        self.resize(WORK_MODE_DIALOG_WIDTH, adaptive_height)

    @staticmethod
    def _parse_keywords(text):
        return [line.strip() for line in text.split('\n') if line.strip()]

    def _clear_keywords(self, target_edit: QTextEdit, list_name: str):
        reply = QMessageBox.question(
            self,
            '确认清空',
            f'确定要清空{list_name}关键词吗？此操作不可撤销。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            target_edit.clear()

    def _import_keywords_to(self, target_edit: QTextEdit):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '导入关键词',
            '',
            '文本文件 (*.txt *.csv *.log);;所有文件 (*.*)',
        )
        if not file_path:
            return

        with open(file_path, 'rb') as f:
            raw = f.read()

        try:
            content = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            content = raw.decode('gbk', errors='ignore')

        target_edit.setPlainText('\n'.join(self._parse_keywords(content)))

    def save_and_close(self):
        cfg.filter_mode = self.button_group.checkedId()
        cfg.filter_blacklist = self._parse_keywords(self.text_edit_blacklist.toPlainText())
        cfg.filter_whitelist = self._parse_keywords(self.text_edit_whitelist.toPlainText())
        self.accept()


class InertiaSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('惯性滚动设置')
        self.setMinimumSize(INERTIA_DIALOG_WIDTH, INERTIA_DIALOG_HEIGHT)
        self.setSizeGripEnabled(True)

        self.setStyleSheet(get_dialog_stylesheet() + get_slider_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel('惯性滚动参数')
        title.setStyleSheet('font-size: 17px; font-weight: 700; color: #F8FAFC;')
        subtitle = QLabel(
            '用于控制“松手后继续滑行”的手感。建议和“长按启用键时启用”搭配使用。'
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet('color: #94A3B8; font-size: 13px;')
        layout.addWidget(title)
        layout.addWidget(subtitle)

        card1, card_layout1 = create_card()
        card1.setStyleSheet(card1.styleSheet() + "QLabel{color:#E2E8F0;}")
        card_layout1.setContentsMargins(16, 16, 16, 16)
        card_layout1.setSpacing(10)

        friction_header = QHBoxLayout()
        friction_title = QLabel('阻尼 / 摩擦力')
        friction_title.setStyleSheet('font-size: 15px; font-weight: 700; color: #E2E8F0;')
        self.friction_value_label = QLabel()
        self.friction_value_label.setStyleSheet(get_value_label_style())
        friction_header.addWidget(friction_title)
        friction_header.addStretch()
        friction_header.addWidget(self.friction_value_label)
        card_layout1.addLayout(friction_header)

        friction_desc = QLabel("控制惯性滑行持续时间。数值越大，滑行越久。")
        friction_desc.setWordWrap(True)
        card_layout1.addWidget(friction_desc)

        friction_slider_row = QHBoxLayout()
        hint_style = get_hint_label_style()
        lbl_compact = QLabel('紧凑')
        lbl_compact.setStyleSheet(hint_style)
        lbl_loose = QLabel('松弛')
        lbl_loose.setStyleSheet(hint_style)

        self.friction_slider = QSlider(Qt.Horizontal)
        self.friction_slider.setRange(100, 3000)
        self.friction_slider.setValue(int(cfg.inertia_friction_ms))
        self.friction_slider.setSingleStep(50)
        self.friction_slider.setFixedHeight(22)
        self.friction_slider.setCursor(Qt.PointingHandCursor)
        self.friction_slider.valueChanged.connect(self._on_friction_changed)

        friction_slider_row.addWidget(lbl_compact)
        friction_slider_row.addWidget(self.friction_slider, 1)
        friction_slider_row.addWidget(lbl_loose)
        card_layout1.addLayout(friction_slider_row)

        layout.addWidget(card1)

        card2, card_layout2 = create_card()
        card2.setStyleSheet(card2.styleSheet() + "QLabel{color:#E2E8F0;}")
        card_layout2.setContentsMargins(16, 16, 16, 16)
        card_layout2.setSpacing(10)

        threshold_header = QHBoxLayout()
        threshold_title = QLabel('触发阈值')
        threshold_title.setStyleSheet('font-size: 15px; font-weight: 700; color: #E2E8F0;')
        self.threshold_value_label = QLabel()
        self.threshold_value_label.setStyleSheet(get_value_label_style())
        threshold_header.addWidget(threshold_title)
        threshold_header.addStretch()
        threshold_header.addWidget(self.threshold_value_label)
        card_layout2.addLayout(threshold_header)

        threshold_desc = QLabel("释放时鼠标速度超过阈值才触发惯性滑行。")
        threshold_desc.setWordWrap(True)
        card_layout2.addWidget(threshold_desc)

        threshold_slider_row = QHBoxLayout()
        lbl_slow = QLabel('低')
        lbl_slow.setStyleSheet(hint_style)
        lbl_fast = QLabel('高')
        lbl_fast.setStyleSheet(hint_style)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(30, 300)
        self.threshold_slider.setValue(int(cfg.inertia_threshold))
        self.threshold_slider.setSingleStep(5)
        self.threshold_slider.setFixedHeight(22)
        self.threshold_slider.setCursor(Qt.PointingHandCursor)
        self.threshold_slider.valueChanged.connect(self._on_threshold_changed)

        threshold_slider_row.addWidget(lbl_slow)
        threshold_slider_row.addWidget(self.threshold_slider, 1)
        threshold_slider_row.addWidget(lbl_fast)
        card_layout2.addLayout(threshold_slider_row)

        layout.addWidget(card2)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton('保存设置')
        btn_save.setObjectName('BtnPrimary')
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

        self._update_friction_label()
        self._update_threshold_label()

        adaptive_height = max(INERTIA_DIALOG_HEIGHT, self.sizeHint().height())
        self.resize(INERTIA_DIALOG_WIDTH, adaptive_height)

    def _update_friction_label(self):
        ms = self.friction_slider.value()
        self.friction_value_label.setText(f'{ms} ms')

    def _update_threshold_label(self):
        val = self.threshold_slider.value()
        self.threshold_value_label.setText(f'{val} px/s')

    def _on_friction_changed(self, _value):
        self._update_friction_label()

    def _on_threshold_changed(self, _value):
        self._update_threshold_label()

    def save_and_close(self):
        cfg.inertia_friction_ms = self.friction_slider.value()
        cfg.inertia_threshold = float(self.threshold_slider.value())
        self.accept()
