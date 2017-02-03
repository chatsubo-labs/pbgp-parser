#
# This file is part of PCAP BGP Parser (pbgpp)
#
# Copyright 2016-2017 DE-CIX Management GmbH
# Author: Tobias Hannaske <tobias.hannaske@de-cix.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import struct

from pbgpp.BGP.Statics import BGPStatics
from pbgpp.BGP.Translation import BGPTranslation
from pbgpp.BGP.Update.Community import BGPUpdateCommunity
from pbgpp.BGP.Update.PathAttribute import BGPPathAttribute


class PathAttributeCommunities(BGPPathAttribute):
    def __init__(self, payload):
        BGPPathAttribute.__init__(self, payload)
        self.type = BGPStatics.UPDATE_ATTRIBUTE_COMMUNITIES

        # Path attribute specific variable
        self.communities = []

        self.__parse()

    def __str__(self):
        return_string = ""
        first = True

        for community in self.communities:
            if first:
                first = False
                return_string += str(community)
                continue

            return_string += " " + str(community)

        return None if len(return_string) == 0 else return_string

    def __parse(self):
        try:
            self.parsed = True
            self.error = False

            community_count = len(self.payload) / 4
            current_count = 1
            current_byte_position = 0

            while current_count <= community_count:
                fields = struct.unpack("!HH", self.payload[current_byte_position:current_byte_position + 4])
                asn = fields[0]
                value = fields[1]
                self.communities.append(BGPUpdateCommunity(asn, value))

                current_count += 1
                current_byte_position += 4

        except Exception as e:
            self.error = True

    def json(self):
        r = {
            "type": self.type,
            "type_string": BGPTranslation.path_attribute(self.type),
            "error": self.error,
            "communities": []
        }

        for community in self.communities:
            r["communities"].append(community.json())

        return r
