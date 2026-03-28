import base64
import json
import urllib.request

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from FlowScroll.constants import (
    WEBDAV_DIALOG_DEFAULT_HEIGHT,
    WEBDAV_DIALOG_DEFAULT_WIDTH,
    WEBDAV_DIALOG_MIN_HEIGHT,
    WEBDAV_DIALOG_MIN_WIDTH,
)
from FlowScroll.core.config import CONFIG_FILE, cfg
from FlowScroll.i18n import tr
from FlowScroll.services.credential_service import credential_service
from FlowScroll.ui.styles import get_webdav_dialog_style


class WebDAVSyncDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("webdav.title"))
        self.setMinimumSize(WEBDAV_DIALOG_MIN_WIDTH, WEBDAV_DIALOG_MIN_HEIGHT)
        self.setSizeGripEnabled(True)

        self.setStyleSheet(get_webdav_dialog_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(QLabel(tr("webdav.url_label")))
        self.edit_url = QLineEdit(cfg.webdav_url)
        self.edit_url.setPlaceholderText("https://...")
        layout.addWidget(self.edit_url)

        layout.addWidget(QLabel(tr("webdav.username_label")))
        self.edit_user = QLineEdit(cfg.webdav_username)
        layout.addWidget(self.edit_user)

        layout.addWidget(QLabel(tr("webdav.password_label")))
        saved_password = credential_service.load_password()
        self.edit_pwd = QLineEdit(saved_password)
        self.edit_pwd.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pwd)

        if not credential_service.is_keyring_available:
            hint = QLabel(tr("webdav.keyring_unavailable_hint"))
            hint.setStyleSheet("color: #F59E0B; font-size: 11px;")
            hint.setWordWrap(True)
            layout.addWidget(hint)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_save = QPushButton(tr("webdav.save"))
        btn_save.clicked.connect(self.save_config)

        btn_upload = QPushButton(tr("webdav.upload"))
        btn_upload.setObjectName("BtnPrimary")
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.clicked.connect(self.upload_config)

        btn_download = QPushButton(tr("webdav.download"))
        btn_download.setObjectName("BtnSuccess")
        btn_download.setCursor(Qt.PointingHandCursor)
        btn_download.clicked.connect(self.download_config)

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_upload)
        btn_layout.addWidget(btn_download)

        layout.addStretch()
        layout.addLayout(btn_layout)

        adaptive_height = max(WEBDAV_DIALOG_DEFAULT_HEIGHT, self.sizeHint().height())
        self.resize(WEBDAV_DIALOG_DEFAULT_WIDTH, adaptive_height)

    def get_full_url(self):
        url = self.edit_url.text().strip()
        if not url.endswith("/"):
            url += "/"
        return url + "FlowScroll_config.json"

    def get_auth_header(self):
        user = self.edit_user.text().strip()
        pwd = self.edit_pwd.text().strip()
        auth_str = f"{user}:{pwd}"
        encoded = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"

    def save_config(self):
        cfg.webdav_url = self.edit_url.text().strip()
        cfg.webdav_username = self.edit_user.text().strip()
        password = self.edit_pwd.text().strip()

        if password:
            saved = credential_service.save_password(password)
            if not saved:
                QMessageBox.warning(
                    self,
                    tr("webdav.notice_title"),
                    tr("webdav.password_session_only"),
                )
        else:
            credential_service.delete_password()

        QMessageBox.information(
            self,
            tr("webdav.notice_title"),
            tr("webdav.saved_notice"),
        )
        self.accept()

    def upload_config(self):
        url = self.get_full_url()
        auth = self.get_auth_header()

        try:
            sync_data = cfg.to_dict_for_sync()
            data = json.dumps(sync_data, ensure_ascii=False, indent=4).encode("utf-8")

            req = urllib.request.Request(url, data=data, method="PUT")
            req.add_header("Authorization", auth)
            req.add_header("Content-Type", "application/json")

            with urllib.request.urlopen(req) as response:
                if response.status in (200, 201, 204):
                    QMessageBox.information(
                        self,
                        tr("webdav.success_title"),
                        tr("webdav.upload_success"),
                    )
                else:
                    QMessageBox.warning(
                        self,
                        tr("webdav.failed_title"),
                        tr("webdav.upload_failed_status", status=response.status),
                    )
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("webdav.error_title"),
                tr("webdav.connect_failed", error=str(e)),
            )

    def download_config(self):
        url = self.get_full_url()
        auth = self.get_auth_header()

        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("Authorization", auth)

            with urllib.request.urlopen(req) as response:
                remote_data = json.loads(response.read().decode("utf-8"))

            local_webdav_url = cfg.webdav_url
            local_webdav_username = cfg.webdav_username

            cfg.from_dict(remote_data)

            cfg.webdav_url = local_webdav_url
            cfg.webdav_username = local_webdav_username

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg.to_dict(), f, ensure_ascii=False, indent=4)

            QMessageBox.information(
                self,
                tr("webdav.success_title"),
                tr("webdav.download_success"),
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("webdav.error_title"),
                tr("webdav.download_failed", error=str(e)),
            )
