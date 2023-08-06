"""
Copyright 2017-2023 Bienabee, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import io
import re
import json
import os
import base64
import math
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DataUtils:
    """
    docstring for DataUtils.
    """
    def __init__(self):
        # qTest Field Type mapping ID's for 'data_type' values
        self.dtv_text_box = 1
        self.dtv_qtest_area = 2
        self.dtv_combo_box = 3
        self.dtv_date_picker = 4
        self.dtv_user_list = 5
        self.dtv_rich_text = 6
        self.dtv_number = 7
        self.dtv_check_box = 8
        self.dtv_url = 12
        self.dtv_multi_select_combo = 17

    ######################################################################
    @staticmethod
    def write_json_file(filename, json_data):

        if '.json' not in filename:
            filename = filename + '.json'

        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(json_data.encode('utf-8'))
            f.close()

    ######################################################################
    @staticmethod
    def read_json_file(filename):

        if os.path.isfile(filename):
            with open(filename) as f:
                file_data = json.load(f)
                data = json.dumps(file_data, indent=4)
                return data

    ######################################################################
    @staticmethod
    def check_for_file_and_create(file_name):
        # must pass in pathlib path
        exists = file_name.exists()

        if exists is False:
            f = open(file_name, "a")
            f.close()

        return exists

    ######################################################################
    @staticmethod
    def check_if_path_exists_and_create(path):
        # must pass in pathlib path
        exists = Path.exists(path)

        # If full path does not exist add all non-existing directories
        if exists is False:
            path.mkdir(parents=True, exist_ok=True)

        return exists

    ######################################################################
    @staticmethod
    def return_program_root_directory():

        root_path = Path(__file__).resolve().parent.parent
        strip_from_path = str(Path("bienabee_qtbot/utilities/data_utils.py"))
        directory = str(Path(os.path.realpath(__file__)))

        directory = directory.replace(strip_from_path, "")

        return Path(directory)

    ######################################################################
    @staticmethod
    def seconds_time_formatter(start, end):
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

    ############################################################################
    @staticmethod
    def get_past_iso_time(days_in_past: int):
        """
        This function will take an integer input and return an iso formatted date with
        zone designation for X number of days in the past from the present date.

        :param days_in_past: Int for days in past from today
        :return: The ISO formatted date
        """

        dt_now = datetime.now() - relativedelta(days=days_in_past)
        iso_date = dt_now.isoformat()
        iso_date = iso_date[:-3] + 'Z'

        return iso_date

    ######################################################################
    @staticmethod
    def year_month_day_string():
        date = datetime.now()
        return str(date.year) + "_" + str(date.month) + "_" + str(date.day)

    #########################################################################################################
    @staticmethod
    def build_date_format_regex(date_format):
        """
        This function can be used to take the input 'date_format' and build a regex from it to be used to search
        matching date formats. An example input could be "YYYY-MM-DD". The regular expression will search for integers
        for each alphanumeric char 'Year', 'Month' or 'Day' separated by the non alphanumeric separator character.

        :param date_format: The format of the date to be searched for.
        :return: The compiled regular expression object
        """

        regex_string = ""

        for c in date_format:
            if c.isalnum():
                regex_string += r"\d"
            else:
                regex_string += c

        return re.compile(regex_string)

    ####################################################################################################
    @staticmethod
    def round_up(number: float, decimals=0):
        """
        This function will take a number and round it up

        :param decimals: If you want to include decimals you can change this to an int with the number of decimals
        :param number: The number you wish to round up
        :return: Rounded up int
        """
        multiplier = 10 ** decimals
        return math.ceil(number * multiplier / multiplier)

    ######################################################################
    # This is not to be used as a cryptographically secure method, this is purely for obfuscation of data in config file
    @staticmethod
    def b64_encoder(string):
        return base64.b64encode(string.encode('utf-8'))

    ######################################################################
    @staticmethod
    def b64_decoder(string):
        return base64.b64decode(string).decode('utf-8')

    ######################################################################
    @staticmethod
    def field_values_dict_builder(all_fields, field_label, include_inactive=False):
        list_fields = {}

        for field in all_fields:

            # print("Field Label: " + str(field["label"]) + "    Data Type: " + str(field["data_type"]))

            if str(field["label"]) == field_label:

                for value in field["allowed_values"]:
                    if include_inactive is True:
                        list_fields[value["label"]] = value["value"]
                    else:
                        if value["is_active"] is True:
                            list_fields[value["label"]] = value["value"]

        return list_fields

    ######################################################################
    def field_values_clean_dict_builder(self, all_fields, field_label, include_inactive=False):
        list_fields = {}

        for field in all_fields:
            if str(field["label"]) == field_label:

                for value in field["allowed_values"]:
                    if include_inactive is True:
                        list_fields[self.cleanse_field_label_data(value["label"])] = value["value"]
                    else:
                        if value["is_active"] is True:
                            list_fields[self.cleanse_field_label_data(value["label"])] = value["value"]

        return list_fields

    ######################################################################
    def fields_data_dict_builder(self, all_fields, include_inactive=False):
        fields_data_dict = {}

        for field in all_fields:
            field_properties = {"id": field["id"],
                                "data_type": field["data_type"]}

            if field["data_type"] == self.dtv_combo_box:
                list_field_vals = {}

                for value in field["allowed_values"]:
                    if include_inactive is True:
                        list_field_vals[value["label"]] = value["value"]
                    else:
                        if value["is_active"] is True:
                            list_field_vals[value["label"]] = value["value"]

                field_properties["allowed_values"] = list_field_vals

            fields_data_dict[field["label"]] = field_properties

        return fields_data_dict

    ######################################################################
    def fields_data_clean_dict_builder(self, all_fields, include_inactive=False):
        clean_fields_data_dict = {}

        for field in all_fields:
            field_properties = {"id": field["id"],
                                "data_type": field["data_type"]}

            if field["data_type"] == self.dtv_combo_box:
                field_vals = {}

                for value in field["allowed_values"]:
                    clean_field = self.cleanse_field_label_data(value["label"])
                    clean_field = clean_field.lower()

                    if include_inactive is True:
                        field_vals[clean_field] = value["value"]
                    else:
                        if value["is_active"] is True:
                            field_vals[clean_field] = value["value"]

                field_properties["allowed_values"] = field_vals

            clean_fields_data_dict[field["label"]] = field_properties

        return clean_fields_data_dict

    ######################################################################
    # This method will be used to clean data for data comparison. Primairly used for comparing QC fields to qTest
    # fields and removing whitespace, lower casing, and removing additional unneeded chars.
    @staticmethod
    def cleanse_field_label_data(field: str):

        if type(field) is str:
            clean_field = re.sub('[()!\'_, -]', '', field)
            clean_field = clean_field.lower()
        else:
            # print("ERROR - cleanse_field_label_data  " + str(field) + " Field is type: " + str(type(field)))
            clean_field = None

        return clean_field

    ######################################################################
    def cleanse_list(self, fields_list: list):

        clean_list = []
        for field in fields_list:
            field = self.cleanse_field_label_data(str(field))
            if field not in clean_list:
                clean_list.append(field)

        return clean_list

    ######################################################################
    def cleanse_and_combine_lists(self, list_of_lists: list):

        master_list = []
        for lst in list_of_lists:
            cl = self.cleanse_list(lst)
            master_list = master_list + list(set(cl) - set(master_list))

        master_list.sort()

        return master_list

    ######################################################################
    @staticmethod
    def check_fields_dict_key_exists(fields_dict, key):

        if key in fields_dict.keys():
            exists = True
        else:
            exists = False

        return exists

    ######################################################################
    @staticmethod
    def find_called_tc_from_desc(description):

        test_name = None

        called_tests = re.search('Call &lt;(.+?)&gt;', description)
        if called_tests:
            test_name = called_tests.group(1)

        return test_name

    ######################################################################
    @staticmethod
    def check_for_string_match(string, value):
        found = False
        if re.search(r'\b' + value + r'\b', string):
            found = True

        return found

    ######################################################################
    @staticmethod
    def check_field_values_and_return_value_id(fields_dict, key, field_value):

        if key in fields_dict.keys():
            if field_value in fields_dict[key]["allowed_values"]:
                value = fields_dict[key]["allowed_values"][field_value]
            else:
                value = None
        else:
            value = None

        return value

    ######################################################################
    @staticmethod
    def check_fields_data_dict_and_return_value_id(fields_dict, key):

        if key in fields_dict.keys():
            value = fields_dict[key]["id"]
        else:
            value = ""

        return value

    ####################################################################################################
    @staticmethod
    def replace_unwanted_project_name_chars(original_str: str):
        """
        This function will allow us to pass in a string and remove unwanted characters, such as line breaks and other
        chars. This will be used to clean Jira or qTest project names with unwanted chars.

        :param original_str:
        :return: A string with all unwanted chars replaced
        """

        if type(original_str) is not str:
            return None

        # Not sure if of these removes are currently needed but there is no harm in including them, Need to verify
        # which are needed and why some jira project names still have line breaks in them

        # Remove line breaks and \xa0
        clean_str = original_str \
            .replace("\\xa0", " ") \
            .replace('\n', " ") \
            .replace('\r', " ") \
            .replace('\t', " ") \
            .replace("\\u00a0", " ") \
            .replace("\\r\\n", " ") \
            .replace(u"\u00a0", u" ") \
            .replace(u"\xa0", u" ")

        # Strip spaces from right side of string
        clean_str = clean_str.rstrip()

        return clean_str
