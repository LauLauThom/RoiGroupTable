'''
This custom table model is designed to support the data as columns
With 2 columns: 1 for group numbers, the second for group names
'''
from javax.swing.table import AbstractTableModel
from ij.gui   import Roi


class RoiGroupTableModel(AbstractTableModel):
    
    def __init__(self):
        super(RoiGroupTableModel, self).__init__()
        groupNames  = Roi.getGroupNames().split(",") # groupNames is a list then
        self.headers = ["Group", "Name"]
        self.columns = [[],[]] # 2 columns
        self.columns[0] = range(1, len(groupNames)+1)
        self.columns[1] = groupNames

    def getColumnClass(self, index):
        return int if index==0 else str
    
    def getRowCount(self):
        return len(self.columns[0])

    def getColumnCount(self):
        return 2

    def getValueAt(self, row, column):
        return self.columns[column][row]
    
    def getColumn(self, column):
        return self.columns[column]
    
    def getColumnName(self, column):
        return self.headers[column]
    
    def isCellEditable(self, row, col):
        return True  # does not work for integer column

    def setValueAt(self, value, row, column):
        self.columns[column][row] = value
        self.fireTableCellUpdated(row, column)
    
    def addRow(self, group, name):
        self.columns[0].append(group)
        self.columns[1].append(name)
        n = len(self.columns[0])
        self.fireTableRowsInserted(n-1, n-1)
    
    def deleteRow(self, row): 
        del(self.columns[0][row])
        del(self.columns[1][row])
        self.fireTableRowsDeleted(row, row)
    
    def deleteRows(self, first, last):
        for i in range(first, last+1):
            del(self.columns[0][row])
            del(self.columns[1][row])
        
        self.fireTableRowsDeleted(first, last)

if __name__ in ['__builtin__', '__main__']:
    '''
    Test the table model by generating a simple window with just the table
    1) Initialized a JTable with the RoiGroupTableModel
    2) Put the JTable in a JScrollPane
    3) Put the JScrollPane in a Panel
    4) Put the Panel in a Generic Dialog
    5) Display the GenericDialog
    '''
    
    from javax.swing import JTable, JScrollPane
    from ij.gui import GenericDialog
    from java.awt import Panel
    
    tableModel = RoiGroupTableModel()
    table = JTable(tableModel)
    tablePane = JScrollPane(table)
    table.setFillsViewportHeight(True)

    gd = GenericDialog("Roi-group table")
    panel = Panel()
    panel.add(tablePane)
    gd.addPanel(panel) # Add current table instance to panel
    gd.showDialog()