# main



Dependency:[[main-module-dependency|main]]



## Unit component



File: **src/main/webapp/app/forms/unit/list/unit.component.html**


# User Manual: Units Page

## Description
The Units page displays a list of all the units in the system. Each unit is identified by a code and a name, and also has a description and a status. From this page, you can perform the following actions:

- Refresh the list of units
- Create a new unit
- Search for a unit by text filtering
- Sort the list by any column 
- Select a unit to update or delete

## Instructions

### Refreshing the List of Units
To refresh the list of units, click on the "Refresh" button located on the page. This button is marked with a refresh icon.

### Creating a New Unit
To create a new unit, click on the "Create" button located on the page. This button is marked with a plus icon. After clicking the "Create" button, a form will appear allowing the user to input the necessary information for the new unit. Once the form is completed, click on the "Save" button to add the new unit to the database. 

### Searching for a Unit
To search for a unit, use the search bar located above the unit list. Enter any search terms and press enter or click on the search icon to filter the list of units. The search is performed on both the code and name fields.

### Sorting the List of Units
To sort the list of units, click on the headers of the table. Each header is sortable and clicking on it will sort the table in ascending or descending order.

### Selecting a Unit
To select a unit, click on the row of the table that corresponds to the unit you wish to select. The row will be highlighted indicating that it has been selected. Once a unit is selected, the user can click on the "Delete" button located underneath the table. This button is marked with a trash can icon. A confirmation dialog will appear to confirm the deletion of the unit. After confirmation, the unit will be permanently deleted from the database.

### Updating a Unit
To update a unit, select the desired unit using the instructions above. Once the unit has been selected, click on the "Edit" button located underneath the table. This button is marked with a pen icon. After clicking the "Edit" button, a form will appear allowing the user to modify the information for the selected unit. Once the form is completed, click on the "Save" button to update the unit in the database.

## Unit-d-1 component



File: **src/main/webapp/app/forms/unit/unit-d-1/update/unit-d-1.component.html**


## User Manual: Edit Unit Form

### Description
The Edit Unit Form allows the user to modify information for a specific unit. The form contains fields for the unit's code, name, description, status, validity period, and sequence. The form also displays the unit's ID, which cannot be modified.

### Instructions

1. To access the Edit Unit Form, navigate to the unit that you want to modify in the application.
2. Click the 'Edit' button for the unit. This will open the Edit Unit Form.
3. Update the fields as necessary. Note that the 'Code' and 'Name' fields are required.
4. Use the 'Valid From' and 'Valid Until' fields to set the time frame for which the unit is valid.
5. Click the 'Save' button to submit your changes. If the form contains invalid data, the 'Save' button will be disabled until you correct the errors.
6. To cancel your changes and exit the form, click the 'Cancel' button.

## Unit-t component



File: **src/main/webapp/app/forms/unit/unit-t/layout/unit-t.component.html**


## Description

This HTML code creates a page for the "Unit D 1" module in the application. The page contains a single tab that shows the "Unit D 1" entity's home title.

## Instructions

To use this page, follow these steps:

1. Open the web application and navigate to the "Unit D 1" module.
2. Click on the tab that shows the "Unit D 1" entity's home title.
3. The corresponding data will be displayed on the page below the tab.

Note: The exact functionality of this page may vary depending on the specific implementation of the application. Please refer to the application's user manual or help resources for more information.

