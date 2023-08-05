#!/usr/bin/env python
from __future__ import annotations

import json
import logging
import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import numpy as np
import pkg_resources
from module_qc_data_tools import (
    get_sn_from_connectivity,
    load_json,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)
from tabulate import tabulate

from module_qc_tools import data
from module_qc_tools.utils.misc import get_identifiers, get_meta_data
from module_qc_tools.utils.multimeter import multimeter
from module_qc_tools.utils.ntc import ntc
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    action="store",
    default=data / "configs/example_merged_vmux.json",
    help="Config file",
)
parser.add_argument(
    "-i", "--input-file", action="store", nargs="*", help="input file if exists"
)
parser.add_argument(
    "-o",
    "--output-dir",
    action="store",
    default="outputs",
    help="output directory",
)
parser.add_argument(
    "-m",
    "--module-connectivity",
    action="store",
    help="path to the module connectivity. Used also to identify the module SN, and to set the default output directory",
)
parser.add_argument(
    "--perchip",
    action="store_true",
    help="Store results in one file per chip (default: one file per module)",
)
parser.add_argument("--verbose", action="store_true", help="verbose mode")
args = parser.parse_args()


def run(data, SLDOVI_config, ps, yr, meter, nt):
    # turn on power supply and configure all chips
    ps.set(v=SLDOVI_config["v_max"], i=SLDOVI_config["i_config"])
    status = yr.configure()

    currents = sorted(
        np.concatenate(
            [
                np.linspace(
                    SLDOVI_config["i_min"],
                    SLDOVI_config["i_max"],
                    SLDOVI_config["n_points"],
                ),
                np.array(SLDOVI_config["extra_i"]),
            ]
        ),
        reverse=True,
    )
    for i in currents:
        # set and measure current for power supply
        ps.set(v=SLDOVI_config["v_max"], i=i)
        current, status = ps.getI()
        i_mea = [{} for _ in range(yr._number_of_chips)]
        for chip in range(yr._number_of_chips):
            if chip in yr._disabled_chip_positions:
                continue
            i_mea[chip]["SetCurrent"] = [i]
            i_mea[chip]["Current"] = [current]
            # measure temperature from NTC
            temp, status = nt.read()
            i_mea[chip]["Temperature"] = [temp]
            # measure v_mux
            for v_mux in SLDOVI_config["v_mux"]:
                yr.set_mux(
                    chip_position=chip,
                    v_mux=v_mux,
                    reset_other_chips=SLDOVI_config["share_vmux"],
                )
                mea, status = meter.measure_dcv(
                    channel=SLDOVI_config["v_mux_channels"][chip]
                )
                i_mea[chip][f"Vmux{v_mux}"] = [mea]
            # measure i_mux
            for i_mux in SLDOVI_config["i_mux"]:
                yr.set_mux(
                    chip_position=chip,
                    i_mux=i_mux,
                    reset_other_chips=SLDOVI_config["share_vmux"],
                )
                mea, status = meter.measure_dcv(
                    channel=SLDOVI_config["v_mux_channels"][chip]
                )
                i_mea[chip][f"Imux{i_mux}"] = [mea]
            data[chip].add_data(i_mea[chip])
            log.info(
                "--------------------------------------------------------------------------"
            )
            log.info(f"Chip-{chip+1}")
            log.info(tabulate(i_mea[chip], headers="keys", floatfmt=".3f"))

    # Return to initial state
    ps.set(v=SLDOVI_config["v_max"], i=SLDOVI_config["i_config"])


def main():

    log.info("[run_SLDOVI] Start VI scan!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_SLDOVI] TimeStart: {timestart}")

    with resources.as_file(Path(args.config)) as path:
        config = json.loads(path.read_text())

    # Need to pass module connectivity path to yarr class (except in case we are running the emulator)
    if args.module_connectivity:
        config["yarr"]["connectivity"] = args.module_connectivity

    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    if "emulator" not in args.config and not args.module_connectivity:
        raise RuntimeError(
            "must supply path to connectivity file [-m --module-connectivity]"
        )

    SLDOVI_config = config["tasks"]["SLDO"]
    ps = power_supply(config["power_supply"], verbose=args.verbose)
    yr = yarr(config["yarr"], verbose=args.verbose)

    meter = multimeter(config["multimeter"], verbose=args.verbose)
    nt = ntc(config["ntc"], verbose=args.verbose)

    # Define identifires for the output files.
    # Taking the module SN from YARR path to config in the connectivity file.
    # Taking the test-type from the script name which is the test-code in ProdDB.
    module_serial = get_sn_from_connectivity(config["yarr"]["connectivity"])
    test_type = os.path.basename(__file__).split(".py")[0]

    # if -o option used, overwrite the default output directory
    if args.module_connectivity:
        output_dir = args.module_connectivity.rsplit("/", 1)[0]
    else:
        output_dir = args.output_dir

    if "outputs" != args.output_dir:
        output_dir = args.output_dir

    input_files = (
        [None] * yr._number_of_chips if not args.input_file else args.input_file
    )
    data = [
        load_json(input_file)
        if input_file
        else qcDataFrame(
            columns=["Temperature", "SetCurrent", "Current"]
            + [f"Vmux{v_mux}" for v_mux in SLDOVI_config["v_mux"]]
            + [f"Imux{i_mux}" for i_mux in SLDOVI_config["i_mux"]],
            units=["C", "A", "A"]
            + ["V" for v_mux in SLDOVI_config["v_mux"]]
            + ["V" for i_mux in SLDOVI_config["i_mux"]],
        )
        for input_file in input_files
    ]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].set_x("Current", True)
        data[chip]._meta_data = get_identifiers(yr.get_config(chip))
        data[chip].add_meta_data("ModuleSN", module_serial)
        data[chip].add_meta_data("TimeStart", round(datetime.timestamp(datetime.now())))
        data[chip]._meta_data.update(get_meta_data(yr.get_config(chip)))
        data[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )

    try:
        run(data, SLDOVI_config, ps, yr, meter, nt)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
    except Exception as err:
        log.exception(err)
        sys.exit(1)

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].add_meta_data("TimeEnd", round(datetime.timestamp(datetime.now())))
        data[chip].add_meta_data(
            "AverageTemperature", np.average(data[chip]["Temperature"])
        )

    # save results in json
    log.info(
        "==================================Summary=================================="
    )
    alloutput = []
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        log.info(f"Chip-{chip+1}")
        log.info(data[chip])
        chip_name = data[chip]._meta_data["Name"]
        outputDF = outputDataFrame()
        outputDF.set_test_type(test_type)
        outputDF.set_results(data[chip])
        if args.perchip:
            save_dict_list(
                f"{output_dir}/Measurements/{test_type}/{timestart}/{chip_name}.json",
                [outputDF.to_dict()],
            )
        else:
            alloutput += [outputDF.to_dict()]
    if not args.perchip:
        save_dict_list(
            f"{output_dir}/Measurements/{test_type}/{timestart}/{module_serial}.json",
            alloutput,
        )

    log.info(
        f"Writing output measurements in {output_dir}/Measurements/{test_type}/{timestart}/"
    )
    log.info("[run_SLDOVI] Done!")
    log.info(f"[run_SLDOVI] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}")


if __name__ == "__main__":
    main()
