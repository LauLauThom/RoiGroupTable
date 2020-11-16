'''
This custom table model is designed to support the data as columns
The datamodel is done via OrderedDict to be able to sort easily by group numbers
With 2 columns: 1 for group numbers, the second for group names
This is NOT WORKING see method setValue getting super complicated
Maybe easier to rely on table doing the sorting
'''
from collections import OrderedDict
from javax.swing.table import AbstractTableModel
from ij.gui   import Roi


class TableModel(AbstractTableModel):
    
    def __init__(self):
        super(TableModel, self).__init__()
        groupNames  = Roi.getGroupNames().split(",") # groupNames is a list then
        self.headers = ["Group", "Name"]
        self.data = OrderedDict( { index+1:groupName for (index, groupName) in enumerate(groupNames) } )

    def getColumnClass(self, index):
        return int if index==0 else str
    
    def getRowCount(self):
        return len(self.data)

    def getColumnCount(self):
        return 2

    def getValueAt(self, row, column):
        if column == 0:
        	return self.data.keys()[row]
        
        elif column == 1:	
        	return self.data.values()[row]
    
    def getColumn(self, column):
        if column == 0:
        	return self.data.keys()
        
        elif column == 1:	
        	return self.data.values()
    
    def getColumnName(self, column):
        return self.headers[column]
    
    def isCellEditable(self, row, col):
        return True  # does not work for integer column

    def setValueAt(self, value, row, column):
        """
        THIS WONT WORK for column==0
        There is now way to rename a dictionary key while keeping the order !!!
        To rename a key is to remove the entry and add a new entry with the same key but different value
        since OrderedDict does not support insertion at arbitrary index, we cannot update a key while keeping the key order
        The solution would to store the keys in a list which give the order of the keys and a dict for the mappings, but this is getting too complicated
        """
        if column == 0: # renaming a key: meaning we remove the previous entry and add a new one with the same previous value
        	
        	# Get previous dicoKey and dicoValue, and remove the dico entry
        	oldKey    = self.data.keys()[row]
        	dicoValue = self.data[oldKey]
        	del(self.data[oldKey])

        	# Add new dico entry
        	self.data[value] = dicoValue
        	
		elif column == 1:
			# rename value (ie group), meaning we first recover the associated dico key from the row position and then update the value 
			key = self.data.keys()[row]
			self.data[key] = value
        
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
    
    tableModel = TableModel()
    table = JTable(tableModel)
    tablePane = JScrollPane(table)
    table.setFillsViewportHeight(True)

    gd = GenericDialog("Roi-group table")
    panel = Panel()
    panel.add(tablePane)
    gd.addPanel(panel) # Add current table instance to panel
    gd.showDialog()