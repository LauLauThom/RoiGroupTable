'''
This custom table model is designed to support the data as columns
With 2 columns: 1 for group numbers, the second for group names
'''
from javax.swing.table import AbstractTableModel
from ij.gui   import Roi


class TableModel(AbstractTableModel):
    
    def __init__(self):
        super(TableModel, self).__init__()
        self.headers = ["Group", "Name"]
        groupNames   = Roi.getGroupNames() # groupNames can be None !
        groupNames   = groupNames.split(",") if groupNames else [] # groupNames is a list then
        self.nRows   = len(groupNames)
        self.columns = [[],[]] # 2 columns
        self.columns[0] = range(1, len(groupNames)+1)
        self.columns[1] = groupNames

    def getColumnClass(self, index):
        return int if index==0 else str
    
    def getRowCount(self):
        return self.nRows

    def getColumnCount(self):
        return 2

    def getValueAt(self, row, column):
        return self.columns[column][row]
    
    def getColumn(self, column):
        return self.columns[column]
    
    def getColumnName(self, column):
        return self.headers[column]
    
    def isCellEditable(self, row, col):
        return True if col==1 else False

    def setValueAt(self, value, row, column):
        """Set value with 0-based row and column indexes"""
        self.columns[column][row] = value
        self.fireTableCellUpdated(row, column)
    
    def getGroupString(self):
        """Return the groups as a string of comma-separated values"""
        return ",".join( self.columns[1] )

    def setGroupColumn(self, groupString):
        """Set groups from a string of comma-delimited value"""
        groupList = groupString.split(",")
        nGroup = len(groupList)
        self.nRows = nGroup
        self.columns[0] = range(1, nGroup+1)
        self.columns[1] = groupList 
        self.fireTableDataChanged()
    
    def addRow(self, index, name):
        """Add row with 1-based index"""
        self.columns[0].append(index)
        self.columns[1].append(name)
        self.nRows+=1 # increment row number        
        self.fireTableRowsInserted(self.nRows-1, self.nRows-1) # except here 0-based index
    
    def deleteRow(self, row): 
        """Delete row with 0-based index"""
        del(self.columns[0][row])
        del(self.columns[1][row])
        self.fireTableRowsDeleted(row, row)
        self.nRows -= 1 # decrement row number
    
    def deleteRows(self, first, last):
        for i in range(first, last+1):
            del(self.columns[0][row])
            del(self.columns[1][row])
        
        self.fireTableRowsDeleted(first, last)
        self.nRows -= last-first+1

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
    
    tableModel = TableModel()
    table = JTable(tableModel)
    tableModel.setGroupColumn("A,B,C")
    print tableModel.getGroupString()
    
    tablePane = JScrollPane(table)
    table.setFillsViewportHeight(True)

    gd = GenericDialog("Roi-group table")
    panel = Panel()
    panel.add(tablePane)
    gd.addPanel(panel) # Add current table instance to panel
    gd.showDialog()