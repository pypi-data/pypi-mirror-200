# main



Dependency:[[main-module-dependency|main]]



## Ba-billing-account-adr component



File: **src/main/webapp/app/forms/billing-account/ba-billing-account-adr/update/ba-billing-account-adr.component.html**


## Description

This page allows the user to edit the address information associated with a billing account. The user can enter the country, place name, post number, post name, street name, home number, home letter, and formatted address. The page provides auto-complete suggestions for some of the fields, and it formats the full address automatically based on the user input.

## Instructions

1. To edit an address, ensure that there is a current record for the billing account.
2. Enter the relevant address information into the corresponding fields.
3. For the fields with an auto-complete feature, type the desired value and select it from the suggestions.
4. If needed, satisfy the requirements specified in the labels for each field.
5. If needed, format the full address by entering the home number and letter, and then navigating away from those fields.
6. Click on the "Cancel" button to discard any changes and return to the previous page.
7. Click on the "Save" button to save the changes to the billing account address. Note that this button will be disabled until all required fields are filled out or selected, and until the form is in a dirty state.

## Ba-billing-account-assigned-persons component



File: **src/main/webapp/app/forms/billing-account/ba-billing-account-assigned-persons/list/ba-billing-account-assigned-persons.component.html**


## Description

The Billing Account Assigned Persons page allows you to view, create, and delete assignments of persons to billing accounts. You can see the person's name and their status for each assignment.

## Instructions

To view the list of assignments:
1. Load the page.
2. Refresh the list by clicking on the "Refresh" button if needed.

To create a new assignment:
1. Click the "Create" button.
2. Fill out the required fields in the form that appears.
3. Click the "Save" button to create the assignment.
4. The new assignment will be added to the list.

To delete an assignment:
1. Select the assignment by clicking on the corresponding row.
2. Click the delete button next to the assignment.
3. Confirm the deletion when prompted.
4. The assignment will be removed from the list.

## Ba-billing-account-basic-info component



File: **src/main/webapp/app/forms/billing-account/ba-billing-account-basic-info/update/ba-billing-account-basic-info.component.html**


# Page Description

This page is used to edit basic information about a billing account.

# Instructions

To edit the information on this page, follow these steps:

1. Enter the name of the billing account in the "Name" field.
2. Enter the organization associated with the billing account in the "Organization" field. You can type the name, and suggestions will appear for you to select from. 
3. (Optional) Enter a description of the billing account in the "Description" field.
4. Click the "Cancel" button to discard any changes and return to the previous screen.
5. Click the "Save" button to save any changes made. The button will be disabled until all required fields are completed and there are unsaved changes.

## Ba-billing-account-status component



File: **src/main/webapp/app/forms/billing-account/ba-billing-account-status/update/ba-billing-account-status.component.html**


# BA Billing Account Status Edit Page

This page allows you to edit the status of a billing account.

## Instructions

1. When the page loads, the status field will display the current status of the billing account.
2. To change the status, use the drop-down menu to select a new status.
3. Next, provide a valid date range using the "Valid From" and "Valid Until" fields.
4. Enter a code for the billing account status in the "Code" field.
5. To save the changes, click the "Save" button at the bottom of the page.
6. If you want to abandon the changes, click the "Cancel" button.

## Ba-billing-account component



File: **src/main/webapp/app/forms/billing-account/ba-billing-account/layout/ba-billing-account.component.html**


# Billing Account Information Page

The Billing Account Information Page displays important information about the billing account that you are managing. The page is divided into four sections: Basic Information, Address, Status, and Assigned Persons.


## Using the Billing Account Information Page

1. To view the Basic Information section, select the corresponding tab on the top of the page.
2. The Basic Information section displays details of the billing account, such as the account number, currency, and payment method.
3. To view the Address section, select the corresponding tab on the top of the page.
4. The Address section displays the billing account's primary address and its contact details.
5. To view the Status section, select the corresponding tab on the top of the page.
6. The Status section displays the current status of the billing account, such as whether it is active or inactive.
7. To view the Assigned Persons section, select the corresponding tab on the top of the page.
8. The Assigned Persons section displays the names and roles of the persons assigned to manage the billing account.
9. You can edit and update the information within each section as necessary.
10. To navigate back to the Dashboard, click the Back button or select another page from the top navigation menu.

## Ba-tabs component



File: **src/main/webapp/app/forms/billing-account/ba-tabs/layout/ba-tabs.component.html**


# User Perspective

This page displays two tabs labeled "BA Billing Accounts" and "CA Service Accounts". Each tab contains a table that displays relevant information regarding the respective accounts.

# Using the Page

1. To switch between the "BA Billing Accounts" and "CA Service Accounts" tabs, click on the corresponding tab.
2. To view detailed information for a particular account listed in the table, click on the row representing that account.
3. To perform actions related to a particular account, use the buttons available in the row representing that account (depending on your permissions):
   - Edit: Opens a form where you can modify the account information and save the changes.
   - Delete: Deletes the account from the system. Be cautious while using this option as it cannot be undone.
4. To add a new account, click on the "Create New" button at the top-right corner of the relevant table (depending on your permissions). Once clicked, a form opens up where you can fill in the details of the new account and save it.

## Baba-assigned-person-det component



File: **src/main/webapp/app/forms/billing-account/baba-assigned-person-det/update/baba-assigned-person-det.component.html**


# Edit Assigned Person Details

This page allows you to edit the details of an assigned person. You can update the person's name, status, and the period of validity.

## Instructions

1. Enter the new or updated person's name in the "Person" field. You can search for a person by typing their name in the search box, and suggestions will appear below it. Select the correct suggestion.
2. In the "Status" field, select the appropriate status from the dropdown list provided.
3. Fill in the "Valid From" and "Valid Until" fields to update the validity period of the assigned person details. You can use the calendar widget provided to select the dates.
4. Click on the "Cancel" button to discard any changes you have made and return to the previous page.
5. If you are satisfied with your changes, click on the "Save" button. This button is disabled until all required fields are complete and valid.

## Baba-assigned-person-role-det component



File: **src/main/webapp/app/forms/billing-account/baba-assigned-person-role-det/update/baba-assigned-person-role-det.component.html**


# User Manual for Form Page

## Description
The Form page is designed to allow users to edit and save information about a specific role. Users can edit the name of the role, the status, and the time period during which the role is valid.

## Usage Instructions
1. Start by filling out the fields on the left-hand side of the page. 
2. Begin by entering the name of the role under the "Orgrole" field. You may use the autofill function by typing in the first letters of the item and selecting it from the suggestions.
3. Next, select the status of the role under the "Status" field. You may choose from the options from the dropdown menu and select "..." if you wish to clear your choice.
4. Fill out the "Valid From" field to input the time period when the role will be valid, and the "Valid Until" field to input the time period until when the role will be active. Use the date picker by clicking on the field and selecting the appropriate date.
5. Once you have finished inputting data, you may choose to "Cancel" the action by clicking on the "Cancel" button on the right side of the page. 
6. To save the changes on the page, click on the "Save" button. The button is located beside the "Cancel" button. You will receive an error message if any field is invalid, and the "Save" button will be non-functional until a valid input has been made.

## Baba-assigned-person-roles component



File: **src/main/webapp/app/forms/billing-account/baba-assigned-person-roles/list/baba-assigned-person-roles.component.html**


# Overview
This page displays a table of assigned roles for a specific user. Users can view, create, edit, and delete assigned roles in the table.

# Instructions
To view assigned roles:
1. Load the page.
2. The assigned roles will be shown in the table.

To create a new assigned role:
1. Click the "Create" button.
2. Fill out the required fields in the form that appears.
3. Click the "Save" button.

To edit an assigned role:
1. Click on the assigned role's row in the table.
2. Click the "Edit" button in the form that appears.
3. Edit the fields as desired.
4. Click the "Save" button.

To delete an assigned role:
1. Click on the assigned role's row in the table.
2. Click the "Delete" button.
3. Confirm the action when prompted.

## Baba-assigned-person-tab component



File: **src/main/webapp/app/forms/billing-account/baba-assigned-person-tab/layout/baba-assigned-person-tab.component.html**


# Page Description

This page displays two tabs, each containing different information related to assigned persons in the BABA system. The first tab shows assigned person details, while the second tab displays their assigned roles.

# Usage Instructions

1. To switch between tabs, click on the respective tab header.
2. In the "Assigned Person Details" tab, you can view information such as the assigned person's name, contact details, and employment status.
3. In the "Assigned Person Roles" tab, you can view the different roles assigned to the selected person.
4. To view more details of a specific assigned person or role, click on the respective row to open its details page.
5. To add a new assigned person, click on the "Add Assigned Person" button displayed on the top right corner of the page.
6. To edit or delete an existing assigned person or role, click on the respective row to open its details page and choose the appropriate action.

## Ca-ba-accordtion component



File: **src/main/webapp/app/forms/billing-account/ca-ba-accordtion/layout/ca-ba-accordtion.component.html**


# Page Description

This is a page containing two accordion tabs: "Basic Information" and "Status". The tabs toggle the display of content related to an account in a card format.

# Instructions

1. To view the "Basic Information" tab by default, navigate to the page.
2. To view the "Status" tab, click on the tab header labeled "Status".
3. To return to the "Basic Information" tab, click on the tab header labeled "Basic Information".
4. The content displayed in each tab is related to an account and is shown in a card format.

## Ca-ba-basic-info component



File: **src/main/webapp/app/forms/billing-account/ca-ba-basic-info/update/ca-ba-basic-info.component.html**


# Description
This page allows the user to edit basic information about a record. The user can change the code, name, organization, and description of the record. The user can also save the changes or cancel the operation.

# Instructions
1. To edit a record, first select it from the table.

2. Once the record is selected, its basic information will be displayed on the page.

3. Modify the fields as needed. The fields that are marked with an asterisk (*) are required.

4. When finished, click on the "Save" button to save the changes.

5. If you decide to cancel the operation without saving the changes, click on the "Cancel" button.

6. If any of the required fields are not filled out, an error message will be displayed next to the respective field. Fix any errors and try again.

7. If you need to find a specific organization, start typing its name in the "Organization" field. The field will display a dropdown with suggestions that match your search. Click on the desired option to select it.

8. If you need more space to write a longer description, you can make the text area bigger by dragging its border with your cursor.

## Ca-ba-status component



File: **src/main/webapp/app/forms/billing-account/ca-ba-status/update/ca-ba-status.component.html**


# Edit CA Ba Status Page

This page allows the user to edit the status information for a CA Ba record. The page displays fields for the status, valid from, and valid until dates.

## Instructions

1. Select a status from the "Status" dropdown list.
2. Select a date from the "Valid From" and "Valid Until" date fields using the calendar pop-up.
3. Click the "Cancel" button to discard changes and return to the previous page.
4. Click the "Save" button to save changes to the record. The button will be disabled until all required fields have been filled and changes have been made.

## Ca-ba-tabs component



File: **src/main/webapp/app/forms/billing-account/ca-ba-tabs/layout/ca-ba-tabs.component.html**


# User Perspective:

This page displays a collapsible accordion menu containing information related to a CA (Certificate Authority) and BA (Business Activity) account. 

# How to Use:

To view the information, click on the header of the accordion menu. This will expand the menu and display the relevant information. To collapse the menu, click on the header again. 

Note: The information displayed may vary depending on the specific CA and BA account information available.

## Ca-service-accounts component



File: **src/main/webapp/app/forms/billing-account/ca-service-accounts/list/ca-service-accounts.component.html**


# CA Service Accounts Table Page

The CA Service Accounts Table page displays a table of CA Service Accounts. Each row in the table represents a single CA Service Account and displays its code, name, description, address, and status. 

## How to Use the CA Service Accounts Table Page

To refresh the list of CA Service Accounts, click the "Refresh List" button. To create a new CA Service Account, click the "Create" button. To view details of a selected CA Service Account, click the "Details" button. 

To delete a CA Service Account, click the trash can icon in the row for that account.

To view or edit details of a selected CA Service Account, click on the row for that account. This will open a new page with tabs for additional details and options for editing.

## Billing-account component



File: **src/main/webapp/app/forms/billing-account/list/billing-account.component.html**


## Description

The Billing Accounts page displays a list of all billing accounts in the system. Users can view details such as name, description, address, and code. The page also allows users to create a new billing account, search for an existing account, and delete an account if necessary.

## Instructions

To refresh the list of billing accounts, click the "Refresh List" button. To create a new billing account, click the "Create" button. To search for an existing account, enter the search term in the search bar and hit enter. To delete a billing account, select the account from the list and click the "Delete" button. 

Clicking on a row in the table will select the corresponding billing account, enabling the "Delete" button.

To view more details about a billing account, click on the desired row to select it and then click the "Edit" button. This will open a new page with additional tabs displaying more information about the billing account.

## Unit component



File: **src/main/webapp/app/forms/unit/list/unit.component.html**


# User Documentation: Unit Page

## Overview

The Unit page allows the user to view, create, and delete Unit records. The page displays a table with information regarding the available Units. Users can view details for each Unit, edit, or delete them. The page also includes a search function to easily find Units.

## Instructions

### View Unit Records

1. Navigate to the Unit page.
2. The table will display all the available units sorted by the code field.
3. To view the details of a Unit, click on the row. The details will appear in a new page.

### Create a New Unit

1. Navigate to the Unit page.
2. Click the 'Create' button.
3. Fill in the required information for the new Unit in the pop-up window.
4. Click the 'Save' button to create the new Unit.

### Edit an Existing Unit

1. Navigate to the Unit page.
2. Click the row for the Unit you want to edit.
3. The Unit details will open in a new page.
4. Edit the desired fields.
5. Click the 'Save' button to update the Unit.

### Delete a Unit

1. Navigate to the Unit page.
2. Click the row for the Unit you want to delete.
3. The Unit details will open in a new page.
4. Click the 'Delete' button.
5. A confirmation window will appear.
6. Click the 'Yes' button to confirm the delete operation or 'No' to cancel it.

## Unit-d-1 component



File: **src/main/webapp/app/forms/unit/unit-d-1/update/unit-d-1.component.html**


## Description
The Edit Unit Page is a form where users can edit the details of a particular unit. It consists of fields for editing the code, name, description, status, valid from and until date, sequence, and Id (if applicable). Users can save their edited details, or cancel and return to the previous page.

## Instructions

1. Access the Edit Unit Page by navigating to the respective unit's details page and clicking on the "Edit" button.
2. Edit the existing fields by typing in the desired changes. The mandatory fields are "Code" and "Name".
3. If any of the mandatory fields are empty, an error message will display, and the user will not be able to save the edits until all mandatory fields are filled.
4. The "Status" field has a dropdown where users can select the unit's status.
5. The "Valid From" and "Valid Until" fields have date and time pickers, respectively.
6. The "Id" field is not editable and will be visible only if the user is editing an existing unit.
7. Click on the "Cancel" button to cancel the edit and return to the previous page.
8. Click on the "Save" button to save the edits. If the form is invalid, the button will be disabled. Once the save is complete, the user will be redirected to the modified unit's details page.

## Unit-t component



File: **src/main/webapp/app/forms/unit/unit-t/layout/unit-t.component.html**


# Page Description

This is the Unit D-1 Home page of the application portal. 

# Instructions 
1. To access the Unit D-1 Home page, navigate to the homepage of the application portal.
2. Click on the Unit D-1 tab under the TabMenu.
3. Once on the Unit D-1 Home page, you can view and interact with the content of the page as required.
4. If you encounter any issues or have any queries regarding the Unit D-1 page, kindly reach out to the application support team.

