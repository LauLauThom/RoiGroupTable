'''
Simple but better to use custom table model to check if new group number is already in the column group numbers
'''
#from javax.swing import JPanel, JLabel, SpinnerNumberModel, JSpinner, JTextField
from javax.swing import *
from java.awt.event import ActionEvent, ActionListener
from java.awt import Panel, GridLayout
from ij.gui import Roi, GenericDialog

# Class defining action of button : Adding a row to table
class AddButton (JButton, ActionListener):

    def __init__(self, tableModel):
        super(AddButton, self).__init__("Add/Update row")
        #super("Add/Update row")
        self.addActionListener(self)
        self.tableModel = tableModel

    def actionPerformed(self, event):
        
        # Get group number and name
        spinModel = SpinnerNumberModel(spinner.getModel())
        number    = spinModel.getNumber().intValue() 
        group     = nameField.getText()
        
        # Check if group number already in table
        numbers = tableModel.getColumn(0)
        row = numbers.indexOf(number)
        
        if row==-1 :
            #  Number not in table -> Add a row
            self.tableModel.addRow(number, group)
        
        else:
            # Update existing row
            self.tableModel.setValueAt(group, row, 1)


# Class defining action of button : Adding a row to table
class DeleteButton(JButton, ActionListener):
    
    def __init__(self, tableModel): 
        super(DeleteButton, self).__init__("Delete selected row")
        #super("Delete selected row")
        self.addActionListener(self)
        self.tableModel = tableModel
          
    def actionPerformed(self, event):
        row = table.getSelectedRow() # Had to set Table to final
        if ( row!=-1 ):
            self.tableModel.deleteRow(row)


class RoiGroupTable(Panel):
    """
    Implement a table with 2 columns: Roi group number and associated name.
    self table can be edited to set  names for roi groups
    """
    
    def __init__(self):
        
        super(RoiGroupTable, self).__init__(GridLayout(0,1)) # 1 column, as many rows as necessary

        ### Table Panel ###
        # Prepare table data
        headers = ["Group number", "Name"]
        listNames = Roi.getGroupNames().split(",") # groupNames is a list then
        dataRows = [ [item[0]+1, item[1]] for item in enumerate(listNames)] # +1 since the group actually start at 1
        #print dataRows

        # Make the table pane
        table = JTable(dataRows, headers)
        #self.tableModel = table.getModel()
        #table.setPreferredScrollableViewportSize( Dimension(500, 70) )
        table.setFillsViewportHeight(True)
        
        # Handle row selection
        #table.getSelectionModel().addListSelectionListener( RowListener())
        #table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        table.setRowSelectionAllowed(True)

        # Create the scroll pane and add the table to it.
        tablePane =  JScrollPane(table)
        #ScrollPane scrollPane =  ScrollPane()
        #scrollPane.add(table)
        
        # Add the scrollpane to the main panel.
        self.add(tablePane)
        
        
        ### EDITING PANEL ###
        inputPanel = JPanel( GridLayout(0,2))
        #Panel inputPanel =  Panel( GridLayout(0,2))
        #Panel inputPanel =  Panel() # looks bad when resizing
        
        # Add label 
        label1 =  JLabel("Group number")
        label2 =  JLabel("Name")
        inputPanel.add(label1)
        inputPanel.add(label2)
        self.add(inputPanel)
        
        
        ### BUTTON PANNEL ###
        buttonPanel =  JPanel( GridLayout(0,3))
        #Panel buttonPanel =  Panel()
        
        # Add spinner for group number
        rangeInt =  SpinnerNumberModel(0,0,255,1)
        spinner  =  JSpinner(rangeInt) # final needed here for some reason
        buttonPanel.add(spinner)
        
        # Add text field for group name
        nameField =  JTextField(" group")
        buttonPanel.add(nameField)
        
        # Button "Add Row"
        #JButton buttonAdd =  AddButton()
        buttonPanel.add( AddButton(table.getModel()))
        buttonPanel.add( DeleteButton(table.getModel()))
        
        # Add button panel to main panel
        self.add(buttonPanel)
        
        
        
    def showTable(self):
        """
        Create the GUI and show it.  For thread safety,
        self method should be invoked from the
        event-dispatching thread.
        """
        gd =  GenericDialog("Roi-group table")
        gd.addPanel(self) # Add current table instance to panel
        gd.showDialog()
        '''
        if ( gd.wasOKed() ) 
            columnGroups = self.tableModel.getColumn(0)
            columnNames   = self.tableModel.getColumn(1) 
            
            nRows = self.tableModel.getRowCount()
            Mapping =  HashMap<Integer, String>(nRows)
            
            for (int i=0 i<nRows i++) 
                Mapping.put( columnGroups.get(i) , columnNames.get(i) )
            
            Roi.setGroupNameMap(Mapping)
        '''

if __name__ in ['__builtin__', '__main__']:
    
    table = RoiGroupTable()
    table.showTable()
    
    # once table closed, check new name mapping
    #print Roi.getGroupNameMap()