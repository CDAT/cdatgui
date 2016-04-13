import pytest
import vcs, cdms2
from cdatgui.editors.secondary.editor.marker import MarkerEditorWidget

@pytest.fixture
def editor():
    editor = MarkerEditorWidget()
    marker = vcs.createmarker()
    editor.setMarkerObject(marker)
    return editor

def test_type(qtbot, editor):
    editor.updateType('triangle_up')
    assert editor.object.type == ['triangle_up']

def test_color(qtbot, editor):
    editor.updateColor(55)
    assert editor.object.color == [55]

def test_size(qtbot, editor):
    editor.updateSize(250)
    assert editor.object.size == [250]
