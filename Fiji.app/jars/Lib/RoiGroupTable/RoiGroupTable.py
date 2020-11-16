from javax.swing import JButton, JTable, JScrollPane, JPanel, JLabel, SpinnerNumberModel, JSpinner, JTextField
from java.awt import GridLayout, Panel, Dimension
from java.awt.event import ActionEvent, ActionListener
from ij.gui import GenericDialog
from RoiGroupTable import RoiGroupTableModel
 

# Class defining action of button : Adding a row to table 
class AddButton(JButton, ActionListener): 
 
	def __init__(self, groupTable): 
		super(AddButton, self).__init__("Add/Update row")
		self.addActionListener(self) 
		self.groupTable = groupTable	  


	def actionPerformed(self, event): 
		
		# Get group number and name
		number	= self.groupTable.getGroupValue()
		groupName = self.groupTable.getNameField() 
		 
		# Check if group number already in table 
		tableModel = self.groupTable.tableModel
		numbers = tableModel.getColumn(0) 
		
		try:
			#search for the item
			rowIndex = numbers.index(number) # raise ValueError if number not in existing numbers
			columnIndex = 1
			tableModel.setValueAt(groupName, rowIndex, columnIndex)
		
		except ValueError:
			tableModel.addRow(number, groupName) 
			
 

# Class defining action of button : Adding a row to table 
class DeleteButton(JButton, ActionListener): 
	 
	def __init__(self, groupTable):  
		super(DeleteButton, self).__init__("Delete selected row")
		self.addActionListener(self) 
		self.groupTable = groupTable
				  
	def actionPerformed(self, event): 
		row = self.groupTable.table.getSelectedRow()
		if row!=-1: 
			self.groupTable.tableModel.deleteRow(row) 
 
 
 
class RoiGroupTable(Panel): 
	"""
	Implement a table with 2 columns: Roi group number and associated name. 
	The table exposes the 
	- tableModel: the raw data
	- table: a JTable which takes care of the visualization/interactions (clicks...) 
	"""
	 
	def __init__(self): 
		 
		super(RoiGroupTable, self).__init__(GridLayout(0,1)) # 1 column, as many rows as necessary
		 
		self.tableModel = RoiGroupTableModel.TableModel()  
		self.table = JTable(self.tableModel) 
		self.table.setPreferredScrollableViewportSize( Dimension(500, 70) ) 
		self.table.setFillsViewportHeight(True) 
		 
		# Handle row selection 
		#table.getSelectionModel().addListSelectionListener( RowListener()) 
		#table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION) 
		self.table.setRowSelectionAllowed(True) 
 
 
		#Create the scroll pane and add the table to it. 
		scrollPane = JScrollPane(self.table) 
		#ScrollPane scrollPane =  ScrollPane() 
		#scrollPane.add(table) 
		 
		#Add the scroll pane to self panel. 
		self.add(scrollPane) 
		 
		 
		# LABEL PANEL 
		labelPanel = JPanel( GridLayout(0,2)) 
		#Panel labelPanel =  Panel( GridLayout(0,2)) 
		#Panel labelPanel =  Panel() # looks bad when resizing 
		 
		# Add label  
		label1 = JLabel("Group number") 
		label2 = JLabel("Name") 
		labelPanel.add(label1) 
		labelPanel.add(label2) 
		self.add(labelPanel) 
		 
		 
		# BUTTON PANNEL 
		buttonPanel = JPanel( GridLayout(0,3) ) 
		#Panel buttonPanel =  Panel() 
		 
		# Add spinner for group number
		default, minVal, maxVal, step = 1,1,255,1
		self.spinnerModel = SpinnerNumberModel(default, minVal, maxVal, step) 
		spinner = JSpinner(self.spinnerModel)
		buttonPanel.add(spinner) 
		 
		# Add text field for group name 
		self.groupField = JTextField("group") 
		buttonPanel.add(self.groupField) 
		
		
		# Button "Add Row" 
		#JButton buttonAdd =  AddButton() 
		buttonPanel.add( AddButton(self) ) 
		buttonPanel.add( DeleteButton(self) ) 
		 
		# Add button panel to main panel 
		self.add(buttonPanel) 

	
	def getGroupValue(self):
		"""Get the current value of the group number field"""
		return self.spinnerModel.getNumber()
		

	def getNameField(self):
		"""Read the current state of the group name"""
		return self.groupField.getText()
		
		 
	def showTable(self): 
		"""
		Add the main panel to a GenericDialog and show it
		"""
		gd = GenericDialog("Roi-group table") 
		gd.addPanel(self) # Add current table instance to panel 
		gd.showDialog() 
		 
		if gd.wasOKed():
			pass
			columnGroups = self.tableModel.getColumn(0) 
			columnNames  = self.tableModel.getColumn(1)  
			
			nRows = self.tableModel.getRowCount()  
	 
	
	def getTableModel(self): 
		return self.tableModel


if __name__ in ['__builtin__', '__main__']:
	"""
	Initialize a RoiGroupTable and show it.
	"""
	table = RoiGroupTable()
	
	table.showTable()