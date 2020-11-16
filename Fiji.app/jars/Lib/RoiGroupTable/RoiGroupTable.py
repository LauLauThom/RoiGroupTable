from javax.swing import JButton, JTable, JScrollPane, JPanel, JLabel, SpinnerNumberModel, JSpinner, JTextField
from java.awt import GridLayout, Panel, Dimension
from java.awt.event import ActionEvent, ActionListener
from ij.gui import GenericDialog, Roi
from RoiGroupTableModel import TableModel
 

# Class defining action of button : Adding a row to table 
class AddButton(JButton, ActionListener): 

	def __init__(self, groupTable): 
		super(AddButton, self).__init__("Add row")
		self.addActionListener(self) 
		self.groupTable = groupTable


	def actionPerformed(self, event): 
		
		# Get group name 
		groupName = self.groupTable.getNameField()  
		  
		# Check if group number already in table  
		tableModel = self.groupTable.tableModel 
		
		n = tableModel.getRowCount()
		tableModel.addRow(n+1, groupName)
		
 

# Class defining action of button : Adding a row to table 
class DeleteButton(JButton, ActionListener): 
	 
	def __init__(self, groupTable):	 
		super(DeleteButton, self).__init__("Delete last row")
		self.addActionListener(self) 
		self.groupTable = groupTable
	
	def actionPerformed(self, event): 
		"""Delete the last row"""
		tableModel = self.groupTable.tableModel
		nRows = tableModel.getRowCount()
		if nRows>0: tableModel.deleteRow(nRows-1)
 
 
 
class Table(Panel): 
	"""
	Implement a table with 2 columns: Roi group number and associated name. 
	The table exposes the 
	- tableModel: the raw data
	- table: a JTable which takes care of the visualization/interactions (clicks...) 
	"""
	 
	def __init__(self): 
		 
		super(Table, self).__init__(GridLayout(0,1)) # 1 column, as many rows as necessary
		 
		self.tableModel = TableModel()
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
		labelPanel = JPanel( GridLayout(0,1) )
		#Panel labelPanel =  Panel( GridLayout(0,2)) 
		#Panel labelPanel =  Panel() # looks bad when resizing 
		 
		# Add label  
		labelName = JLabel("Name") 
		labelPanel.add(labelName) 
		self.add(labelPanel) 
		 
		 
		# BUTTON PANNEL 
		buttonPanel = JPanel( GridLayout(0,2) ) 
		#Panel buttonPanel =  Panel() 
		 
		 
		# Add text field for group name 
		self.groupField = JTextField("new group") 
		buttonPanel.add(self.groupField) 
		
		
		# Button "Add Row" 
		#JButton buttonAdd =  AddButton() 
		buttonPanel.add( AddButton(self) ) 
		buttonPanel.add( DeleteButton(self) ) 
		 
		# Add button panel to main panel 
		self.add(buttonPanel) 


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
			# Update ImageJ Roi group names mapping
			stringGroup = ','.join( self.tableModel.getColumn(1) ) 
			Roi.setGroupNames(stringGroup) 
	
	
	
	def getTableModel(self): 
		return self.tableModel


if __name__ in ['__builtin__', '__main__']:
	"""
	Initialize a RoiGroupTable and show it.
	"""
	table = Table()
	
	table.showTable()