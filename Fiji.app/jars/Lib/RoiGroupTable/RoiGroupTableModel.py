'''
Test using list instead of vectors
'''
import java.util.*
import javax.swing.*
from javax.swing import JTable
from javax.swing.table import AbstractTableModel
from java.awt import Panel
from ij.gui   import Roi, GenericDialog


class RoiGroupTableModel(AbstractTableModel):
	
	headers = ["Group number", "Name"]
	columns = Vector(2) # 2 columns
	
	def __init__(self):
		super(RoiGroupTableModel, self).__init__()
		groupNames  = Roi.getGroupNames().split(",") # groupNames is a list then
		self.dicoGroup = { item[0], item[1] for item in enumerate(groupNames)] 
		#self.groupNames = new TreeMap<Integer, String>(groupNames) # sort the map by keys to makes sure keySet and values are ordered the same
		
		# Populate the column vectors
		size = len(self.groupNames)
		columnGroups = Vector(size) # contain group numbers
		columnNames  = Vector(size) # contains group names
		
		for entry in self.groupNames.entrySet():
			columnGroups.add(entry.getKey().intValue())
			columnNames.add(entry.getValue())
		
		# Populate the 2D-data vector containing the 2 column vector
		self.columns.add(columnGroups)
		self.columns.add(columnNames)
		
	
	def getColumnClass(self, index):
		return int.class if index==0 else String.class
	
	def getRowCount(self):
        return self.columns.get(0).size()

	def getColumnCount(self):
        return 2

	def getValueAt(self, row, column):
		return self.columns.get(column).get(row)
	
    
	def getColumn(self, column):
		return self.columns.get(column)
	
	
	def getColumnName(self, column):
        return RoiGroupTableModel.headers[column]
    
	def isCellEditable(self, row, col):
        return True  # does not work for integer column

    def setValueAt(self, value, row, column):
    	self.columns.get(column).set(row, value)
		fireTableCellUpdated(row, column)
    
    
    def addRow(self, group, name):
    	self.columns.get(0).add(group)
    	self.columns.get(1).add(name)
    	n = self.getRowCount()
    	fireTableRowsInserted(n-1, n-1)
    
    
    def deleteRow(self, row): 
    	self.columns.get(0).removeElementAt(row)
    	self.columns.get(1).removeElementAt(row)
    	fireTableRowsDeleted(row, row)
    
    
    def deleteRows(self, first, last):
    	pass
    	#self.columns.get(0).removeRange(first, last) #removeRange is protected ><
