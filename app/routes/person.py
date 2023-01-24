# The below library enables the logic for the CRUD functionality of our APIs.
from flask_restful import Resource
# The os library enables the app find the location of the database file so that the file can be read and written to.
import os
# The below library enables us to instantiate and work with the SQLite DB.
import sqlite3
# The below library is used to parse the PATCH request's transmitted parameters.
from flask_restful import request

# Define global variabls
cwd = os.getcwd()
path_to_database = cwd+"/var/Database"
conn = sqlite3.connect(path_to_database, check_same_thread=False)
cursor = conn.cursor()
# The variable 'table_column_names' is zipped together with their respective values 
# (which is the data that is retrieved from the database) so that the output that is
# returned to the user can be a dictionary with key,value pairs.
table_column_names = ("row_id", "name", "phone", "email",
                      "address", "postalZIP", "region", "country")
# This list contains all of the dictionary objects that contain the row data
# which is retrieved by the class 'Query_all_rows_of_data_from_database'.
final_list_of_row_data_as_dictionary_objects = []


# Below we define the funcitons that define the logic for the HTTP verbs for this route.

# Class 1: Create a person by saving the data about that person in the database.
class CREATE_and_read_all_people(Resource):
    """
    This class defines the logic of two operations:
    the one to create a person (by adding al of the transmitted data about
    the person to the database) as well as the operation to read all of the 
    data about all of the people from the database.
    """

    def post(self):
        #post_params is the flask request object that contains the request's transmitted payload
        #the flask request object does not behave the same way as a python dictionary even though they look the same
        post_params = request.get_json()
        # Step 1: Check to see if all 7 required parameters are transmitted with the PUT request.
        if len(post_params) != 7:
            return {"400": "Provide one value (in string format) for each of the 7 required parameters."}
        # If all of the 7 required parameters are transmitted with the put request then:
        else:
            # Save the user's transmitted data to a new variable so that we can use data in INSERT INTO SQL statement.
            post_name = post_params["name"]
            post_phone = post_params["phone"]
            post_email = post_params["email"]
            post_address = post_params["address"]
            post_postalZIP = post_params["postalZIP"]
            post_region = post_params["region"]
            post_country = post_params["country"]
            # Reorganize the data into a list so that the data can be accessed by the INSERT INTO statement.
            data = [post_name, post_phone, post_email, post_address,
                    post_postalZIP, post_region, post_country]
            # Insert the data from the 'data' list into the Customers table using the questionmarks which represent each parameter in the list.
            # We need to use the questionmarks to represent the pieces of data in the 'data' list because it is not possible to substitute the variables
            # directly into the 'values' portion of the INSERT INTO statement.
            insert_into_statement = """INSERT INTO Customers
                                    (name,phone,email,address,postalZIP,region,country)
                                     VALUES (?,?,?,?,?,?,?);
                                    """
            # Run the INSERT INTO statement to actually insert the data into the database.
            cursor.execute(insert_into_statement, data)
            # Finally we need to commit data to DB so that the data is actually inserted.
            conn.commit()
            # Step 3: Return the newly appended row of data to the user.
            # Once the record is appended to the database, we want to return the record with its new row_id number to the user.
            post_select_statement_to_get_max_row_id = "SELECT max(row_id) FROM Customers;"
            # The fetchone() method returns this output: "SELECT * FROM Customers WHERE row_id=(507,);" so we have to index the tuple to get the row_id value.
            post_max_row_id = cursor.execute(
                post_select_statement_to_get_max_row_id).fetchone()[0]
            # Create the SQL statement that queries the last row of data from the database.
            post_select_statement_to_return_last_Row = f"SELECT * FROM Customers WHERE row_id={post_max_row_id};"
            # Execute the SQL statement that queries the last row of data from the database.
            post_last_row_of_data_in_list_format = cursor.execute(
                post_select_statement_to_return_last_Row).fetchall()[0]
            # Zip the list contents from previous line with global variable 'table_column_names' to create dictionary.
            post_last_row_of_data_in_dictionary_format = dict(
                zip(table_column_names, post_last_row_of_data_in_list_format))
            # Return the last row of data from the database to the user.
            return (post_last_row_of_data_in_dictionary_format)

    def get(self):
        # Create the select statement that we will use to query the data.
        select_statement_to_query_all_of_the_databases_data = "SELECT * from Customers;"
        # Execute the select statement.
        all_of_the_data_to_return_to_user_in_nested_list_format = cursor.execute(
            select_statement_to_query_all_of_the_databases_data).fetchall()
        # The variable 'all_of_the_data_to_return_to_user' is a list that contains nested lists where each nested list contains
        #   all of the data from one row in the database where the individual fields are seperated by commas.
        # We want to access the nested lists that contain the data from each database row which is why we need to index 'all_of_the_data_to_return_to_user'
        #  as done below:
        # In the code below we are taking each nested list with row data.
        for row in all_of_the_data_to_return_to_user_in_nested_list_format:
            # Then we are creating a dictionary for each row's data where the keys are the items from the global list 'table_column_names'
            #  and the values are the fields of data that are represented by the 'row' variable.
            data_in_row_in_dictionary_format = dict(
                zip(table_column_names, row))
            # Then we append each dictionary of row data to the global list 'final_list_of_row_data_as_dictionary_objects'.
            final_list_of_row_data_as_dictionary_objects.append(
                data_in_row_in_dictionary_format)
        # Then we return the global list with the row data in dictionary format.
        return final_list_of_row_data_as_dictionary_objects


# Class 2: Get the data about one person from the database.
class GET_UPDATE_DELETE_person(Resource):
    """   
    This class contains three functions that get the informatio about one
    person (one row) from the database (GET), update the data about one person
    in the database (PATCH) and delete the information about one person from the 
    database (DELETE). 
    """
    # Get the information about one person from the database.
    def get(self, row_id):
        # Create the SQL query that checks to see if the row of data exists in the database.
        get_query_to_check_to_see_if_requested_row_exists_in_db = f"select exists(select * from Customers where row_id = {row_id});"
        # Run the SQL query against the database. The result output is a tuple that looks like this: (0,) or (1,)
        get_query_tuple_with_zero_or_one_to_denote_if_row_exists_or_not = cursor.execute(
            get_query_to_check_to_see_if_requested_row_exists_in_db).fetchone()
        # Index the integer value from the tuple result from the previous line.
        get_query_int_value_zero_or_one_to_denote_if_data_exists_in_db = get_query_tuple_with_zero_or_one_to_denote_if_row_exists_or_not[
            0]
        # If the row of data does not exist in the database, then return the error message.
        if get_query_int_value_zero_or_one_to_denote_if_data_exists_in_db == 0:
            return {"404": "Row of data you are trying to query does not exist in database."}
        else:
            # Create the select statement that we need to select the specifc row of data from the database.
            select_statement = f"SELECT * FROM Customers WHERE row_id = {row_id};"
            # Here we run the select query to get the data from the database.
            # We use the fetchone() method to return only the single row.
            # The fetchone() method retrns the row of data in tuple format.
            data_to_retrieve = cursor.execute(select_statement).fetchone()
            # Here e create the dictionary that is returned to the user as the API response.
            # The dictionary is created by zipping the global tuple object 'table_column_names' with the tuple
            #   that contains the data frm the database called 'data_to_retrieve'.
            api_response = dict(zip(table_column_names, data_to_retrieve))
            # Return the data as the  API response to the user.
            return api_response

    # Update the information about one person from the database.
    def patch(self, row_id):
        # Step 1a) Check to see if the row of data that the user wants to update exists in the database.
        # Create the SQL query that checks to see if the row of data for the user's desired row exists in the database.
        patch_query_to_check_to_see_if_requested_row_exists_in_db = f"select exists(select * from Customers where row_id = {row_id});"
        # Run the SQL query against the database. The result output is a tuple that looks like this: (0,) or (1,)
        patch_tuple_with_zero_or_one_to_denote_if_row_exists_or_not = cursor.execute(
            patch_query_to_check_to_see_if_requested_row_exists_in_db).fetchone()
        # Index the integer value from the tuple result from the previous line.
        patch_int_value_zero_or_one_to_denote_if_data_exists_in_db = patch_tuple_with_zero_or_one_to_denote_if_row_exists_or_not[
            0]
        # If the row of data does not exist in the database, then return the error message.
        if patch_int_value_zero_or_one_to_denote_if_data_exists_in_db == 0:
            return {"404": " The row of data you are trying to update does not exist in database."}
        else:
            # Step 1b) Retrieve the user's transmitted parameters from the request.
            patch_params = request.json
            #return (patch_params)
            # Step 2) Save the user's transmitted parameters to a new variable.
            for key, value in patch_params.items():
                if "name" in patch_params.keys():
                    new_name_value = patch_params["name"]
                else:
                    new_name_value = 0
                if "phone" in patch_params.keys():
                    new_phone_value = patch_params["phone"]
                else:
                    new_phone_value = 0
                if "email" in patch_params.keys():
                    new_email_value = patch_params["email"]
                else:
                    new_email_value = 0
                if "address" in patch_params.keys():
                    new_address_value = patch_params["address"]
                else:
                    new_address_value = 0
                if "postalZIP" in patch_params.keys():
                    new_postalZIP_value = patch_params["postalZIP"]
                else:
                    new_postalZIP_value = 0
                if "region" in patch_params.keys():
                    new_region_value = patch_params["region"]
                else:
                    new_region_value = 0
                if "country" in patch_params.keys():
                    new_country_value = patch_params["country"]
                else:
                    new_country_value = 0

            # Step 3) Insert the updated values into the respective database fields.
            # If the user does not want to update this field, then do nothing.
            if new_name_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_name_to_replace = f"SELECT name FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                name_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_name_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                name_that_we_will_replace_which_is_in_string_format = "".join(
                    name_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_name_in_the_db = f"UPDATE Customers SET name = REPLACE(name,'{name_that_we_will_replace_which_is_in_string_format}','{new_name_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(sql_statement_that_replaces_the_name_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_phone_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_phone_to_replace = f"SELECT phone FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                phone_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_phone_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                phone_that_we_will_replace_which_is_in_string_format = "".join(
                    phone_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_phone_in_the_db = f"UPDATE Customers SET phone = REPLACE(phone,'{phone_that_we_will_replace_which_is_in_string_format}','{new_phone_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(sql_statement_that_replaces_the_phone_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_email_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_email_to_replace = f"SELECT email FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                email_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_email_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                email_that_we_will_replace_which_is_in_string_format = "".join(
                    email_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_email_in_the_db = f"UPDATE Customers SET email = REPLACE(email,'{email_that_we_will_replace_which_is_in_string_format}','{new_email_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(sql_statement_that_replaces_the_email_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_address_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_address_to_replace = f"SELECT address FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                address_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_address_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                address_that_we_will_replace_which_is_in_string_format = "".join(
                    address_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_address_in_the_db = f"UPDATE Customers SET address = REPLACE(address,'{address_that_we_will_replace_which_is_in_string_format}','{new_address_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(
                    sql_statement_that_replaces_the_address_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_postalZIP_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_postalZIP_to_replace = f"SELECT postalZIP FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                postalZIP_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_postalZIP_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                postalZIP_that_we_will_replace_which_is_in_string_format = "".join(
                    postalZIP_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_postalZIP_in_the_db = f"UPDATE Customers SET postalZIP = REPLACE(postalZIP,'{postalZIP_that_we_will_replace_which_is_in_string_format}','{new_postalZIP_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(
                    sql_statement_that_replaces_the_postalZIP_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_region_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_region_to_replace = f"SELECT region FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                region_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_region_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                region_that_we_will_replace_which_is_in_string_format = "".join(
                    region_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_region_in_the_db = f"UPDATE Customers SET region = REPLACE(region,'{region_that_we_will_replace_which_is_in_string_format}','{new_region_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(
                    sql_statement_that_replaces_the_region_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            # If the user does not want to update this field, then do nothing.
            if new_country_value == 0:
                pass
            else:
                # Write the select statement that we need, to get the data from the database (in string format) that we want to replace.
                select_statement_to_get_country_to_replace = f"SELECT country FROM Customers WHERE row_id = {row_id};"
                # Query the data from the database that we want to change.
                # Fetchone() returns a tuple which we need to convert to a string because the SQL replace method requires its inputs to be in string format.
                country_that_we_will_replace_which_is_in_tuple_format = cursor.execute(
                    select_statement_to_get_country_to_replace).fetchone()
                # Convert the tuple to a string because the SQL REPLACE method requires its inputs to be in string format.
                country_that_we_will_replace_which_is_in_string_format = "".join(
                    country_that_we_will_replace_which_is_in_tuple_format)
                # Create the SQL REPLACE statement.
                sql_statement_that_replaces_the_country_in_the_db = f"UPDATE Customers SET country = REPLACE(country,'{country_that_we_will_replace_which_is_in_string_format}','{new_country_value}') WHERE row_id = {row_id};"
                # Run the SQL REPLACE query.
                cursor.execute(
                    sql_statement_that_replaces_the_country_in_the_db)
                # Commit the replaced data which saves the change in the database.
                conn.commit()

            #Once the details about the person have been updated in the database, return the newly updated record to the user.
            # Once the record is appended to the database, we want to return the record with its new row_id number to the user.
            patch_select_statement_to_get_updated_row_of_data = f"SELECT * FROM Customers WHERE row_id = {row_id};"
            # Execute the above select statement.
            # The fetchone() method returns this output: "SELECT * FROM Customers WHERE row_id=(507,);" so we have to index the tuple to get the row_id value.
            patch_updared_data_to_return_in_list_format = cursor.execute(
                patch_select_statement_to_get_updated_row_of_data).fetchall()[0]
            # Zip the list contents from previous line with global variable 'table_column_names' to create dictionary.
            patch_updatd_data_to_return_in_dictionary_format = dict(
                zip(table_column_names, patch_updared_data_to_return_in_list_format))
            return patch_updatd_data_to_return_in_dictionary_format

    # Delete the information about one person from the database.
    def delete(self, row_id):
        # Create the SQL query that checks to see if the row of data exists in the database.
        delete_query_to_check_to_see_if_requested_row_exists_in_db = f"select exists(select * from Customers where row_id = {row_id});"
        # Run the SQL query against the database. The result output is a tuple that looks like this: (0,) or (1,).
        tuple_with_zero_or_one_to_denote_if_row_exists_or_not = cursor.execute(
            delete_query_to_check_to_see_if_requested_row_exists_in_db).fetchone()
        # Index the integer value from the tuple result from the previous line.
        int_value_zero_or_one_to_denote_if_data_exists_in_db = tuple_with_zero_or_one_to_denote_if_row_exists_or_not[
            0]
        # If the row of data does not exist in the database, then return the error message.
        if int_value_zero_or_one_to_denote_if_data_exists_in_db == 0:
            return {"404": "Row of data you are trying to delete does not exist in database."}
        else:
            # If the row of data does exist in the database, create the SQL DELETE statement.
            delete_sql_statement = f"DELETE FROM Customers WHERE row_id = {row_id}"
            # Run the SQL DELETE query.
            cursor.execute(delete_sql_statement)
            # Commit the deletion action to the database.
            conn.commit()
            # Return success message to user
            delete_success_message = f"The record at row {row_id} was deleted successfully."
            # Return the success message to the user.
            return {"200": delete_success_message}




    