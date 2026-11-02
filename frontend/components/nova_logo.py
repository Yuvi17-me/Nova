import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QLinearGradient,
    QRadialGradient,
    QPainterPath,
)


class NovaLogoWidget(QWidget):
    """
    Custom Vector Nova Celestial Emblem.
    Features a radiant cosmic orbital core with concentric elliptical arcs
    and a bright stellar nucleus. Completely distinct from Gemini's 4-point star.
    """

    def __init__(self, size=28, parent=None):
        super().__init__(parent)
        self.size = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        center = QPointF(w / 2.0, h / 2.0)
        radius = min(w, h) / 2.0

        # ----------------------------------------------------
        # Outer Subtle Ambient Glow
        # ----------------------------------------------------
        glow = QRadialGradient(center, radius)
        glow.setColorAt(0.0, QColor(99, 102, 241, 70))    # Indigo glow
        glow.setColorAt(0.7, QColor(56, 189, 248, 25))    # Cyan edge
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

        # ----------------------------------------------------
        # Primary Diagonal Orbit (Tilted Ellipse Arc)
        # ----------------------------------------------------
        painter.save()
        painter.translate(center)
        painter.rotate(-28)

        orbit_grad1 = QLinearGradient(-radius * 0.75, 0, radius * 0.75, 0)
        orbit_grad1.setColorAt(0.0, QColor(99, 102, 241, 230))  # Indigo
        orbit_grad1.setColorAt(0.5, QColor(129, 140, 248, 255)) # Soft violet
        orbit_grad1.setColorAt(1.0, QColor(56, 189, 248, 120))  # Cyan

        pen1 = QPen(QBrush(orbit_grad1), max(1.8, radius * 0.12))
        pen1.setCapStyle(Qt.RoundCap)
        painter.setPen(pen1)
        painter.setBrush(Qt.NoBrush)

        orbit_rect1 = QRectF(-radius * 0.72, -radius * 0.34, radius * 1.44, radius * 0.68)
        painter.drawEllipse(orbit_rect1)
        painter.restore()

        # ----------------------------------------------------
        # Secondary Counter-Orbit (Cross Arc)
        # ----------------------------------------------------
        painter.save()
        painter.translate(center)
        painter.rotate(42)

        orbit_grad2 = QLinearGradient(-radius * 0.65, 0, radius * 0.65, 0)
        orbit_grad2.setColorAt(0.0, QColor(56, 189, 248, 200))  # Cyan
        orbit_grad2.setColorAt(0.6, QColor(99, 102, 241, 160))  # Indigo
        orbit_grad2.setColorAt(1.0, QColor(168, 85, 247, 90))   # Purple

        pen2 = QPen(QBrush(orbit_grad2), max(1.4, radius * 0.09))
        pen2.setCapStyle(Qt.RoundCap)
        painter.setPen(pen2)
        painter.setBrush(Qt.NoBrush)

        orbit_rect2 = QRectF(-radius * 0.62, -radius * 0.28, radius * 1.24, radius * 0.56)
        painter.drawEllipse(orbit_rect2)
        painter.restore()

        # ----------------------------------------------------
        # Central Stellar Core (Supernova Nucleus)
        # ----------------------------------------------------
        core_radius = max(2.5, radius * 0.22)
        core_glow = QRadialGradient(center, core_radius * 1.8)
        core_glow.setColorAt(0.0, QColor(255, 255, 255, 255))   # Bright white center
        core_glow.setColorAt(0.4, QColor(165, 180, 252, 240))   # Ice indigo
        core_glow.setColorAt(0.8, QColor(99, 102, 241, 180))    # Electric indigo
        core_glow.setColorAt(1.0, QColor(99, 102, 241, 0))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(core_glow))
        painter.drawEllipse(center, core_radius * 1.6, core_radius * 1.6)

        # Micro white star point
        painter.setBrush(QBrush(QColor(255, 255, 255, 240)))
        painter.drawEllipse(center, core_radius * 0.6, core_radius * 0.6)
