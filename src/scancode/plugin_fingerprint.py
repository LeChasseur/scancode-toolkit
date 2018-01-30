#
# Copyright (c) 2018 nexB Inc. and others. All rights reserved.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict

from commoncode import filetype
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from scancode import CommandLineOption
from scancode import SCAN_GROUP


@scan_impl
class FingerprintScanner(ScanPlugin):
    """
    Calculate the Halo Hash and Hailstorm fingerprint value of a Resource.
    """
    sort_order = 4

    options = [
        CommandLineOption(('-g', '--fingerprints',),
            is_flag=True, default=False,
            help='Calculate the Halo Hash and Hailstorm fingerprint values for <input>.',
            help_group=SCAN_GROUP)
    ]

    def is_enabled(self):
        return self.is_command_option_enabled('fingerprints')

    def get_scanner(self, **kwargs):
        return get_fingerprint


def get_fingerprint(location, **kwargs):
    """
    Return a list with a single OrderedDict that contains the bit average
    Halo hash and Hailstorm fingerprint values.
    """
    from licensedcode.tokenize import ngrams
    from licensedcode.tokenize import select_ngrams
    from scancode.halohash import BitAverageHaloHash

    chunk_size = 1024
    ngram_length = 4

    if not filetype.is_file(location):
        return []

    bah = BitAverageHaloHash()
    slices = []
    with open(location, 'rb') as f:
        first_chunk = None
        last_processed_chunk = None
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            # We keep track of the first and last chunk to ensure that the
            # first and last ngrams are selected
            if not first_chunk:
                first_chunk = chunk
            last_processed_chunk = chunk

            # Process data
            bah.update(chunk)
            slices.extend(ngrams(chunk, ngram_length))

    selected_slices = list(select_ngrams(slices))

    # Check to see if the first and last ngrams were selected
    first_ngram = list(ngrams(first_chunk, ngram_length))[0]
    last_ngram = list(ngrams(last_processed_chunk, ngram_length))[-1]
    assert first_ngram in selected_slices
    assert last_ngram in selected_slices

    # Join slices together as a single bytestring
    hashable = b''.join(b''.join(slice) for slice in selected_slices)
    hailstorm = BitAverageHaloHash(hashable)

    # Set values
    fingerprints = OrderedDict()
    fingerprints['bah128'] = bah.hexdigest()
    fingerprints['hailstorm'] = hailstorm.hexdigest()

    return [fingerprints]
