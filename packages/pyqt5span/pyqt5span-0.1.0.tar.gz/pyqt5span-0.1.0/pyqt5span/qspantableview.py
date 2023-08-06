import typing
from PyQt5            import QtCore, QtWidgets
from .qspanheaderview import QSpanHeaderView

__all__ = [
    'QSpanTableView'
]

class QSpanTableView(QtWidgets.QTableView):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)

        hheader = QSpanHeaderView(QtCore.Qt.Orientation.Horizontal)
        vheader = QSpanHeaderView(QtCore.Qt.Orientation.Vertical)

        self.setHorizontalHeader(hheader)
        self.setVerticalHeader(vheader)
        
        hheader.sectionPressed.connect(self.onHorizontalHeaderSectionPressed)
        vheader.sectionPressed.connect(self.onVerticalHeaderSectionPressed)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        super().setModel(model)
        
        self.spanHeaderView(QtCore.Qt.Orientation.Horizontal).setSectionCount(model.columnCount())
        self.spanHeaderView(QtCore.Qt.Orientation.Vertical).setSectionCount(model.rowCount())

    def spanHeaderView(self, orientation: QtCore.Qt.Orientation) -> QSpanHeaderView:
        if orientation == QtCore.Qt.Orientation.Horizontal:
            return self.horizontalHeader()
        else:
            return self.verticalHeader()

    @QtCore.pyqtSlot(int, int)
    def onHorizontalHeaderSectionPressed(self, begin_section: int, end_section: int) -> None:
        self.clearSelection()
        old_selection_mode = self.selectionMode()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)

        for i in range(begin_section, end_section + 1):
            self.selectColumn(i)

        self.setSelectionMode(old_selection_mode)

    @QtCore.pyqtSlot(int, int)
    def onVerticalHeaderSectionPressed(self, begin_section: int, end_section: int) -> None:
        self.clearSelection()
        old_selection_mode = self.selectionMode()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)

        for i in range(begin_section, end_section + 1):
            self.selectRow(i)
            
        self.setSelectionMode(old_selection_mode)