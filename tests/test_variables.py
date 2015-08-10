import pytest
import mocks
import cdatgui
import vcs
import cdms2


@pytest.fixture
def cdmsfile():
    return cdms2.open(vcs.sample_data + "/clt.nc")


@pytest.fixture
def clt():
    return cdmsfile()("clt")


def test_cdms_file_tree_add_file(qtbot, cdmsfile):
    tree = cdatgui.variables.cdms_file_tree.CDMSFileTree()
    qtbot.addWidget(tree)

    tree.add_file(cdmsfile)

    # the item was added
    assert tree.topLevelItemCount() == 1

    tli = tree.topLevelItem(0)
    # it grabbed the filename correctly
    assert tli.text(1) == "clt.nc"

    # new files are expanded
    assert tli.isExpanded()

    # that it loaded the variables correctly
    assert tli.childCount() == 3

    file_variables = ["clt", "u", "v"]

    for i in range(tli.childCount()):
        child = tli.child(i)
        # that it placed the variables in
        # the order they were in the file
        assert file_variables.index(child.text(1)) == i

    # we can't add the same file twice
    with pytest.raises(ValueError):
        tree.add_file(cdmsfile)


def test_cdms_file_tree_get_selected(qtbot, cdmsfile):
    tree = cdatgui.variables.cdms_file_tree.CDMSFileTree()
    qtbot.addWidget(tree)

    tree.add_file(cdmsfile)

    # Nothing selected, should return None
    assert len(tree.get_selected()) == 0

    tli = tree.topLevelItem(0)
    clt = tli.child(0)
    clt.setSelected(True)

    selected_vars = tree.get_selected()

    # it returned the clt variable
    assert selected_vars[0].id == "clt"

    u = tli.child(1)
    u.setSelected(True)

    selected_vars = tree.get_selected()
    assert len(selected_vars) == 2
    assert selected_vars[0].id == "clt" and selected_vars[1].id == "u"


def test_cdms_var_list_add_var(qtbot, clt):
    varlist = cdatgui.variables.cdms_var_list.CDMSVariableList()
    qtbot.addWidget(varlist)

    varlist.add_variable(clt)

    # it has an item in the list
    assert varlist.count() == 1

    item = varlist.item(0)

    # it has the variable name as the text
    assert item.text() == "clt"


def test_cdms_var_list_get_var(qtbot, clt):
    varlist = cdatgui.variables.cdms_var_list.CDMSVariableList()

    varlist.add_variable(clt)

    # it's the same variable
    var = varlist.get_variable(0)
    assert var.id == "clt"


def test_cdms_file_chooser_browse(qtbot):
    chooser = cdatgui.variables.cdms_file_chooser.CDMSFileChooser()

    # it's on the file browser
    chooser.tabs.set_current_row(0)

    qtbot.addWidget(chooser)

    assert chooser.accepted_button.isEnabled() is False

    # Navigate the file browser to sample_data directory
    chooser.file_browser.set_root(vcs.sample_data)

    assert chooser.accepted_button.isEnabled() is False

    l = chooser.file_browser.dirs[0].list

    # Find clt.nc row
    l.setCurrentItem(l.findItems(u"clt.nc", 0)[0])

    assert chooser.accepted_button.isEnabled() is True

    assert chooser.get_selected()[0].id == vcs.sample_data + "/clt.nc"

    l.setCurrentItem(None)

    assert chooser.accepted_button.isEnabled() is False


def test_manager():
    man = cdatgui.variables.manager.Manager()
    clt = man.get_file(vcs.sample_data + "/clt.nc")

    # The file is the same as the one requested
    assert clt.id == vcs.sample_data + "/clt.nc"
    # Retrieving the same file returns the exact same object
    assert id(clt) == id(man.get_file(vcs.sample_data + "/clt.nc"))
    # Retrieving a nonexistant object gives an IOError
    with pytest.raises(IOError):
        man.get_file("/tmp/filedoesnotexist")
    # Will only retrieve correct file types
    with pytest.raises(IOError):
        man.get_file(__file__)


def test_add_dialog(qtbot):
    dia = cdatgui.variables.variable_add.AddDialog()
    qtbot.addWidget(dia)

    # No files selected yet
    assert len(dia.selected_variables()) == 0

    dia.chooser = mocks.CDMSFileChooser

    assert dia.tree.topLevelItemCount() == 0

    dia.added_files()

    # The tree should have clt.nc
    assert dia.tree.topLevelItemCount() == 1
    assert dia.tree.topLevelItem(0).text(1) == "clt.nc"

    # Select the "clt" variable
    dia.tree.topLevelItem(0).child(0).setSelected(True)
    assert len(dia.selected_variables()) == 1


def test_variable_widget(qtbot):
    w = cdatgui.variables.VariableWidget()
    qtbot.addWidget(w)

    w.add_dialog = mocks.VariableAddDialog

    # Fake the signal to check for new variables
    w.add_variable()

    # Make sure that we can select a variable
    with qtbot.waitSignal(w.selectedVariable,
                          timeout=1000,
                          raising=True):
        w.select_variable(0)
