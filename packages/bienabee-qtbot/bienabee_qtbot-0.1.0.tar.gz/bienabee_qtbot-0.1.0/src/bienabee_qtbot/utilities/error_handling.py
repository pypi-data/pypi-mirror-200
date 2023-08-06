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

import json
import logging


class ErrorHandler:
    """
    # TODO - This should be cleaned up and improved, will need to add rate limiting handling by June 2023

    Error handler uses the logger to validate HTTP responses and evaluate success or failure and log results.

    """
    def __init__(self):
        # The error type variables will be used to understand how to parse the qTest HTTP response error data and
        # print the details to the error logger.
        self.error_type_message = "HTML Error"
        self.error_type_html = "Error Message"
        self.error_type_undefined = "Undefined Error"

    ###############################################################
    # qTest HTTP Response Codes - https://support.qasymphony.com/hc/en-us/articles/115002958146-qTest-API-Specification
    ###############################################################
    def check_http_status(self, http_status_code):

        http_status = str(http_status_code)
        http_status_text = ""
        success = True

        if http_status == "200":
            success = True
            http_status_text = "HTTP 200 - OK"
        elif http_status == "201":
            success = True
            http_status_text = "HTTP 201 - Created"
        elif http_status == "400":
            success = False
            http_status_text = "HTTP 400 - Bad Request"
        elif http_status == "401":
            success = False
            http_status_text = "HTTP 401 - Authentication Missing"
        elif http_status == "402":
            success = False
            http_status_text = "HTTP 402 - No API support with qTest Edition"
        elif http_status == "403":
            success = False
            http_status_text = "HTTP 403 - Forbidden"
        elif http_status == "404":
            success = False
            http_status_text = "HTTP 404 - Not Found"
        elif http_status == "405":
            success = False
            http_status_text = "HTTP 405 - Invalid Data Format for qTest"
        elif http_status == "412":
            success = False
            http_status_text = "HTTP 412 - Pre-conditions Failed"
        elif http_status == "500":
            success = False
            http_status_text = "HTTP 500 - Internal Server Error"
        elif http_status == "" or http_status == "None":
            success = False
            http_status_text = "HTTP - No HTTP Status Returned"
        else:
            success = False
            http_status_text = f"HTTP - {http_status}"

        return success, http_status_text

    # TODO - Need to update this parse error method to conform to the HTTP error response format of the qTest REST API
    ###############################################################
    def parse_error_response(self, response_text):

        if "<!doctype html>" in response_text:
            error_data = {
                "error": self.error_type_html,
                "description": response_text
            }
        else:
            response_data = json.loads(response_text)

            if "error" in response_data:
                error_data = {
                    "error": response_data["error"],
                    "description": response_data["error_description"]
                }
            elif "message" in response_data:
                error_data = {
                    "error": self.error_type_message,
                    "description": response_data["message"]
                }
            else:
                error_data = {
                    "error": self.error_type_undefined,
                    "description": response_data
                }

        return error_data

    ###############################################################
    def evaluate_response_log_errors(self, logger_module, http_status_code, response_text, optional_details=None):

        # Determine if the evaluated response was successful or if there were errors detected
        error_detected = False

        success, http_status_text = self.check_http_status(http_status_code)

        if success is False:

            # Enable debug logging
            '''
            logging_info = f"ERROR CHECKING DEBUG - " \
                           f"\nLOGGER MODULE: {logger_module} " \
                           f"\nHTTP STATUS: {http_status_code} " \
                           f"\nRESPONSE TEXT: {response_text}"

            logging.info(logging_info)
            '''

            error_data = self.parse_error_response(response_text)

            if optional_details is None:
                if error_data["error"] is self.error_type_undefined:
                    error_message = f" {http_status_text} - {json.dumps(error_data['description'])}"
                elif error_data["error"] is self.error_type_message:
                    error_message = f" {http_status_text} - {error_data['description']}"
                elif error_data["error"] is self.error_type_html:
                    error_message = f" {http_status_text} - {error_data['description']}"
                else:
                    error_message = f" {http_status_text} - {error_data['error']}\n" \
                                    f"    DESCRIPTION: {error_data['description']}"
            else:
                if error_data["error"] is self.error_type_undefined:
                    error_message = f" {http_status_text} - \n" \
                                    f"    DESCRIPTION: {json.dumps(error_data['description'])} \n" \
                                    f"    DETAILS: {optional_details}"
                elif error_data["error"] is self.error_type_message:
                    error_message = f" {http_status_text} - \n" \
                                    f"    DESCRIPTION: {error_data['description']} \n" \
                                    f"    DETAILS: {optional_details}"
                elif error_data["error"] is self.error_type_html:
                    error_message = f" {http_status_text} - \n" \
                                    f"    DESCRIPTION: {error_data['description']} \n" \
                                    f"    DETAILS: {optional_details}"
                else:
                    error_message = f" {http_status_text} - {error_data['error']} \n" \
                                    f"    DESCRIPTION: {error_data['description']} \n" \
                                    f"    DETAILS: {optional_details}"

            error_detected = True

            logging.error(f"{logger_module} - {error_message}")

        return error_detected
