from PySide import QtGui
from .graphics_method_editor import GraphicsMethodEditorWidget
from .secondary.editor.marker import MarkerEditorWidget
from .secondary.editor.line import LineEditorWidget
import vcs

class Cdat1dEditor(GraphicsMethodEditorWidget):
    """Configures a meshfill graphics method."""

    def __init__(self, parent=None):
        """Initialize the object."""
        super(Cdat1dEditor, self).__init__(parent=parent)

        self.button_layout.takeAt(0).widget().deleteLater()
        self.button_layout.takeAt(0).widget().deleteLater()

        marker_button = QtGui.QPushButton("Edit Marker")
        marker_button.clicked.connect(self.editMarker)

        line_button = QtGui.QPushButton("Edit Line")
        line_button.clicked.connect(self.editLine)

        self.button_layout.insertWidget(0, line_button)
        self.button_layout.insertWidget(0, marker_button)

        self.marker_editor = None
        self.line_editor = None

    def editMarker(self):
        if not self.marker_editor:
            self.marker_editor = MarkerEditorWidget()
            self.marker_editor.savePressed.connect(self.updateMarker)

        mark_obj = vcs.createmarker(mtype=self.gm.marker, color=self.gm.markercolor, size=self.gm.markersize)
        self.marker_editor.setMarkerObject(mark_obj)
        self.marker_editor.raise_()
        self.marker_editor.show()

    def editLine(self):
        if not self.line_editor:
            self.line_editor = LineEditorWidget()
            self.line_editor.savePressed.connect(self.updateLine)
        line_obj = vcs.createline(ltype=self.gm.line, color=self.gm.linecolor, width=self.gm.linewidth)
        self.line_editor.setLineObject(line_obj)
        self.line_editor.raise_()
        self.line_editor.show()

    def updateMarker(self, name):
        self.gm.marker = self.marker_editor.object.type[0]
        self.gm.markercolor = self.marker_editor.object.color[0]
        self.gm.markersize = self.marker_editor.object.size[0]

    def updateLine(self, name):
        self.gm.line = self.line_editor.object.type[0]
        self.gm.linecolor = self.line_editor.object.color[0]
        self.gm.line = self.line_editor.object.width[0]
