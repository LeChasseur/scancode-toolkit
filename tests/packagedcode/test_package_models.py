#
# Copyright (c) 2015 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import, print_function

import os.path

from commoncode.testcase import FileBasedTesting

from packagedcode.models import AssertedLicense
from packagedcode import models
from packagedcode.models import Package
from packagedcode.models import Party


class TestModels(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_model_creation_and_dump(self):
        aap = models.AndroidAppPackage()
        result = aap.to_primitive()
        assert 'Android app' == result['type']
        assert 'archive' == result['packaging']
        assert 'Java' == result['primary_language']

    def test_validate_package(self):
        package = Package(dict(
            name='Sample',
            summary='Some package',
            payload_type='source',
            authors=[Party(
                dict(
                    name='Some Author',
                    email='some@email.com'
                    )
                )
            ],
            keywords=['some', 'keyword'],
            vcs_tool='git',
            asserted_licenses=[
                AssertedLicense(dict(
                    license='apache-2.0'
                    )
                )
            ],
            )
        )
        assert 'Sample' == package.name
        assert 'Some package' == package.summary
        assert 'source' == package.payload_type
        assert 'Some Author' == package.authors[0].name
        assert ['some', 'keyword'] == package.keywords
        assert 'apache-2.0' == package.asserted_licenses[0].license
