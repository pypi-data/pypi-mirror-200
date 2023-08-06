from pathlib import Path

import PySide6.QtWidgets as QtW
from pytest import raises

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations
from ScenarioGUI import global_settings as globs


def test_global_settings(qtbot):
    """
    test if two scenarios can have the same name.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    assert main_window.dia.font().family() == globs.FONT == "Arial"
    assert main_window.dia.font().pointSize() == 10 == globs.FONT_SIZE

    assert globs.WHITE == "rgb(255, 255, 255)"
    assert globs.LIGHT == "rgb(84, 188, 235)"
    assert globs.LIGHT_SELECT == "rgb(42, 126, 179)"
    assert globs.DARK == "rgb(0, 64, 122)"
    assert globs.GREY == "rgb(100, 100, 100)"
    assert globs.WARNING == "rgb(255, 200, 87)"
    assert globs.BLACK == "rgb(0, 0, 0)"

    assert globs.FILE_EXTENSION == "scenario"
    assert globs.GUI_NAME == "Scenario GUI"
    assert globs.ICON_NAME == "icon.svg"

    assert globs.path.joinpath("./ScenarioGUI") == globs.FOLDER
    # test get_path_for_file function
    assert globs.path == globs.get_path_for_file(globs.path.joinpath("./ScenarioGUI/gui_classes/gui_structure_classes"), "gui_config.ini")
    # test file not found error
    with raises(FileNotFoundError):
        assert globs.path == globs.get_path_for_file(globs.path.joinpath("./ScenarioGUI/gui_classes/gui_structure_classes"), "not_exists.ini")

    main_window.delete_backup()
