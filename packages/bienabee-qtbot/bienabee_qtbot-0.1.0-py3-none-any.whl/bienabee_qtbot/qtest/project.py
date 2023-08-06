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


class QTestProject:
    """docstring for QTestProject."""
    def __init__(self,
                 name,
                 description,
                 template_id=None,
                 start_date=None,
                 end_date=None,
                 admins=None):
        self.name = name
        self.description = description
        self.template_id = template_id
        self.start_date = start_date
        self.end_date = end_date
        self.admins = [] if admins is None else admins
        self.user_ids = []
        self.id = None

    def get_json_data(self):
        data = {
             'name': self.name,
             'description': self.description,
             'template_id': self.template_id,
             'start_date': self.start_date,
             'end_date': self.end_date,
             'admins': self.admins,
             'automation': True
        }

        return data

    def get_json_user_data(self):
        data = {
            'project_id': self.id,
            'user_ids': self.user_ids
        }

        return data

    def add_user(self, user_id):
        self.user_ids.append(user_id)
