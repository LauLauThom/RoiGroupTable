import javax.swing.*
import java.awt.*
from java.awt.event import ActionEvent, ActionListener
import java.util.*
from RoiGroupTable import RoiGroupTableModel

# Class defining action of button : Adding a row to table
class AddButton (JButton, ActionListener):

    def __init__(self):
        super("Add/Update row")
        self.addActionListener(self)

    def actionPerformed(self, event):
        
        # Get group number and name
        spinModel = SpinnerNumberModel(spinner.getModel())
        Number    = spinModel.getNumber().intValue() 
        Group     = nameField.getText()
        
        # Check if group number already in table
        numbers = tableModel.getColumn(0)
        row = numbers.indexOf(Number)
        
        if row==-1 :
            #  Number not in table -> Add a  row
            tableModel.addRow(Number, Group)
        
        else:
            # Update existing row
            tableModel.setValueAt(Group, row, 1)


# Class defining action of button : Adding a row to table
class DeleteButton(JButton, ActionListener):
    
    def __init__(self): 
        super("Delete selected row")
        self.addActionListener(self)
    
                 
    def actionPerformed(self, event):
        row = table.getSelectedRow() # Had to set Table to final
        if ( row!=-1 ):
            tableModel.deleteRow(row)



class RoiGroupTable(Panel):
    """
    Implement a table with 2 columns: Roi group number and associated name.
    self table can be edited to set  names for roi groups
    """
    
    def __init___(self):
        
        super(GridLayout(0,1)) # 1 column, as many rows as necessary
        
        self.tableModel = RoiGroupTableModel() 
        table = JTable(tableModel)
        table.setPreferredScrollableViewportSize( Dimension(500, 70) )
        table.setFillsViewportHeight(true)
        
        # Handle row selection
        #table.getSelectionModel().addListSelectionListener( RowListener())
        #table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        table.setRowSelectionAllowed(true)


        #Create the scroll pane and add the table to it.
        scrollPane =  JScrollPane(table)
        #ScrollPane scrollPane =  ScrollPane()
        #scrollPane.add(table)
        
        #Add the scroll pane to self panel.
        add(scrollPane)
        
        
        # LABEL PANEL
        labelPanel =  JPanel( GridLayout(0,2))
        #Panel labelPanel =  Panel( GridLayout(0,2))
        #Panel labelPanel =  Panel() # looks bad when resizing
        
        # Add label 
        label1 =  JLabel("Group number")
        label2 =  JLabel("Name")
        labelPanel.add(label1)
        labelPanel.add(label2)
        add(labelPanel)
        
        
        # BUTTON PANNEL
        buttonPanel =  JPanel( GridLayout(0,3))
        #Panel buttonPanel =  Panel()
        
        # Add spinner for group number
        rangeInt =  SpinnerNumberModel(0,0,255,1)
        spinner =  JSpinner(rangeInt) # final needed here for some reason
        buttonPanel.add(spinner)
        
        # Add text field for group name
        nameField =  JTextField(" group")
        buttonPanel.add(nameField)
        
        
        # Button "Add Row"
        #JButton buttonAdd =  AddButton()
        buttonPanel.add( AddButton())
        buttonPanel.add( DeleteButton())
        
        # Add button panel to main panel
        add(buttonPanel)
        
        
        
    def showTable(self):
        """
        Create the GUI and show it.  For thread safety,
        self method should be invoked from the
        event-dispatching thread.
        """
        GenericDialog gd = GenericDialog("Roi-group table")
        gd.addPanel(self) # Add current table instance to panel
        gd.showDialog()
        
        if ( gd.wasOKed() ) 
            columnGroups = self.tableModel.getColumn(0)
            columnNames  = self.tableModel.getColumn(1) 
            
            nRows = self.tableModel.getRowCount()
            Mapping =  HashMap<Integer, String>(nRows)
            
            for (int i=0 i<nRows i++) 
                Mapping.put( columnGroups.get(i) , columnNames.get(i) )
            
            Roi.setGroupNameMap(Mapping)
            
    
    
    def getTableModel(self):
        return self.tableModel 


