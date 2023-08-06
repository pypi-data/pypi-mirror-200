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

    File: qtest/test_case_fields.py

    Notes:
        DEPRECATION NOTICE: This QTestTestCaseFields will be deprecated in favor of the method
        'test_case_properties_fields_payload' in the '/data_mapper/field_manager.py' file. The new method will build
        the properties field array dynamically at runtime. This file may still be used at time to time for one off
        migration scenarios with static values set.

        This is a data class to hold data for a 'test case fields' object. Class has a get_json_data return method to
        return Python dictionary used to create a JSON string data as needed by the qTest REST API.

        This class currently has hardcoded field ID's that will need to be updated for a new qTest project. The
        test case fields will also need to be updated as we add new fields. Testing for a more dynamic field building
        method is underway but focus is on speed of migration for now.

    Dependencies:

        Non Standard Python Libraries -

        Migration Utility Modules & Files -

        External Programs / Code Libraries -

"""


class QTestTestCaseFields:
    """docstring for qtest_testcase."""
    def __init__(self,
                 application,
                 status=None,
                 precondition=None,
                 priority=None,
                 test_group=None,
                 channel=None,
                 tcer_id=None,
                 test_phase=None,
                 business_area=None,
                 ard=None,
                 qc_project=None,
                 qc_test_id=None,
                 ):

        self.application = "" if application is None else application
        self.status = "" if status is None else status
        self.precondition = "" if precondition is None else precondition
        self.priority = "" if priority is None else priority
        self.test_group = "" if test_group is None else test_group
        self.channel = "" if channel is None else channel
        self.tcer_id = "" if tcer_id is None else tcer_id
        self.test_phase = "" if test_phase is None else test_phase
        self.business_area = "" if business_area is None else business_area
        self.ard = "" if ard is None else ard
        self.qc_project = qc_project
        self.qc_test_id = qc_test_id

    def get_fields_list(self):
        properties = [
            {
                "field_id": 1924,
                "field_name": "Status",
                "field_value": self.status
            },
            {
                "field_id": 1928,
                "field_name": "Precondition",
                "field_value": self.precondition
            },
            {
                "field_id": 1929,
                "field_name": "Priority",
                "field_value": self.priority
            },
            {
                "field_id": 1970,
                "field_name": "Application",
                "field_value": self.application
            },
            {
                "field_id": 1971,
                "field_name": "Test Group",
                "field_value": self.test_group
            },
            {
                "field_id": 1972,
                "field_name": "Channel",
                "field_value": self.channel
            },
            {
                "field_id": 1973,
                "field_name": "TCER ID",
                "field_value": self.tcer_id
            },
            {
                "field_id": 1974,
                "field_name": "Test Phase",
                "field_value": self.test_phase
            },
            {
                "field_id": 1975,
                "field_name": "Business Area",
                "field_value": self.business_area
            },
            {
                "field_id": 1976,
                "field_name": "ARD",
                "field_value": self.ard
            },
            {
                "field_id": 2025,
                "field_name": "QC Project",
                "field_value": self.qc_project
            },
            {
                "field_id": 2026,
                "field_name": "QC Test ID",
                "field_value": self.qc_test_id
            }
        ]

        return properties
