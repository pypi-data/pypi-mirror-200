#!/usr/bin/env python3
from __future__ import annotations


def get_identifiers(config):
    identifiers = {}
    identifiers["ChipID"] = config["RD53B"]["Parameter"]["ChipId"]
    identifiers["Name"] = config["RD53B"]["Parameter"]["Name"]
    identifiers["Institution"] = ""
    identifiers["ModuleSN"] = ""
    return identifiers


def get_meta_data(config):
    meta_data = {
        "FirmwareVersion": "",
        "FirmwareIdentifier": "",
        "ChannelConfig": "",
        "SoftwareVersion": "",
        "ChipConfigs": config,
        "SoftwareType": "",
        "SoftwareVersion": "",
    }
    return meta_data
