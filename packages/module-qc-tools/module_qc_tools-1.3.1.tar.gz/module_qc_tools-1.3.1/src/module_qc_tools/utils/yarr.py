#!/usr/bin/env python3
from __future__ import annotations

import json
import logging

from module_qc_tools.utils.hardware_control_base import hardware_control_base

# if sys.version_info >= (3, 9):
#    from importlib import resources
# else:
#    import importlib_resources as resources

log = logging.getLogger(__name__)


class yarr(hardware_control_base):
    def __init__(self, config, name="yarr", *args, **kwargs):
        self.controller = ""
        self.connectivity = ""
        self.scanConsole_exe = ""
        self.write_register_exe = ""
        self.read_register_exe = ""
        self.read_adc_exe = ""
        self.emulator = False
        super().__init__(config, name, *args, **kwargs)
        if "emulator" in self.scanConsole_exe:
            self.emulator = True
            log.info(f"[{name}] running scanConsole emulator!!")
        if "emulator" in self.write_register_exe:
            self.emulator = True
            log.info(f"[{name}] running write_register emulator!!")
        connect_spec = self.get_connectivity()
        self._number_of_chips = len(connect_spec["chips"])
        self._disabled_chip_positions = set()
        for chip in range(self._number_of_chips):
            if not connect_spec["chips"][chip]["enable"]:
                self._disabled_chip_positions.add(chip)
        self._register = [{} for chip in range(self._number_of_chips)]

    def running_emulator(self):
        return self.emulator

    def configure(self, skip_reset=False):

        cmd = f'{self.scanConsole_exe} -r {self.controller} -c {self.connectivity} {"--skip-reset" if skip_reset else ""}'

        currLevel = logging.getLogger("module_qc_tools.utils").getEffectiveLevel()
        logging.getLogger("module_qc_tools.utils").setLevel(logging.DEBUG)
        result = self.send_command(cmd, purpose="configure module")
        logging.getLogger("module_qc_tools.utils").setLevel(currLevel)
        return result

    def write_register(self, name, value, chip_position=None):

        if chip_position in self._disabled_chip_positions:
            return 0
        if (
            chip_position is not None
            and self._register[chip_position].get(name) == value
        ):
            return 0
        cmd = f'{self.write_register_exe} -r {self.controller} -c {self.connectivity} {"-i "+str(chip_position) if chip_position is not None else ""} {name} {value}'
        status = self.send_command(cmd, purpose="write register")
        if chip_position is not None:
            self._register[chip_position][name] = value
        else:
            for chip in range(self._number_of_chips):
                self._register[chip][name] = value

        return status

    def read_register(self, name, chip_position=None):

        if chip_position in self._disabled_chip_positions:
            return 0
        cmd = f'{self.read_register_exe} -r {self.controller} -c {self.connectivity} {"-i "+str(chip_position) if chip_position is not None else ""} {name}'
        status = self.send_command(cmd, purpose="read register")

        return status

    def read_adc(self, vmux, chip_position=None, readCurrent=False, rawCounts=False):

        if chip_position in self._disabled_chip_positions:
            return 0
        cmd = f'{self.read_adc_exe} -r {self.controller} -c {self.connectivity} {"-i "+str(chip_position) if chip_position != None else ""} {"-I " if readCurrent else ""} {"-R " if rawCounts else ""} {vmux}'
        status = self.send_command_and_read(cmd, type=str, purpose="read adc")
        return status

    def set_mux(self, chip_position, v_mux=-1, i_mux=-1, reset_other_chips=True):

        status = 0
        for chip in range(self._number_of_chips):
            if chip == chip_position:
                # status = self.write_register(name="MonitorEnable", value=1, chip_position=str(chip)) and status

                # Set Vmux=1 to measure the I_mux pad voltage when a non-negative I_mux value is passed.
                if i_mux >= 0:
                    v_mux = 1
                # Set Imux=63 when measuring NTC pad voltage through Vmux2.
                if v_mux == 2:
                    status = (
                        self.write_register(
                            name="MonitorI", value=63, chip_position=chip
                        )
                        and status
                    )
                status = (
                    self.write_register(
                        name="MonitorV", value=v_mux, chip_position=chip
                    )
                    and status
                )
                if i_mux >= 0:
                    self.write_register(
                        name="MonitorI", value=i_mux, chip_position=chip
                    ) and status
            elif reset_other_chips:
                status = (
                    self.write_register(name="MonitorV", value=63, chip_position=chip)
                    and status
                )

        return status

    def reset_tempsens_enable(self, chip_position):
        status = 0

        status = (
            self.write_register(
                name="MonSensSldoAnaEn", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensSldoDigEn", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensAcbEn", value=0, chip_position=chip_position
            )
            and status
        )
        return status

    def reset_tempsens_bias(self, chip_position):
        status = 0

        status = (
            self.write_register(
                name="MonSensSldoAnaBias", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensSldoDigBias", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensAcbBias", value=0, chip_position=chip_position
            )
            and status
        )
        return status

    def reset_tempsens_dem(self, chip_position):
        status = 0

        status = (
            self.write_register(
                name="MonSensSldoAnaDem", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensSldoDigDem", value=0, chip_position=chip_position
            )
            and status
        )
        status = (
            self.write_register(
                name="MonSensAcbDem", value=0, chip_position=chip_position
            )
            and status
        )
        return status

    def reset_tempsens(self, chip_position):
        status = 0

        status = (
            self.reset_tempsens_enable(chip_position=chip_position)
            and self.reset_tempsens_bias(chip_position=chip_position)
            and self.reset_tempsens_dem(chip_position=chip_position)
            and status
        )
        return status

    def enable_tempsens(self, chip_position, v_mux=-1, reset_other_chips=True):
        status = 0

        # First reset all MOS sensors.
        status = self.reset_tempsens_enable(chip_position=chip_position) and status
        for chip in range(self._number_of_chips):
            if chip == chip_position:
                if v_mux == 14:
                    status = (
                        self.write_register(
                            name="MonSensSldoAnaEn", value=1, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 16:
                    status = (
                        self.write_register(
                            name="MonSensSldoDigEn", value=1, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 18:
                    status = (
                        self.write_register(
                            name="MonSensAcbEn", value=1, chip_position=chip
                        )
                        and status
                    )
                else:
                    status = -1
                if status < 0:
                    raise RuntimeError(
                        "Incorrect VMUX value for measuring temperature!"
                    )
            elif reset_other_chips:
                status = self.reset_tempsens_enable(chip_position=chip) and status

        return status

    def set_tempsens_bias(
        self, chip_position, v_mux=-1, bias=0, reset_other_chips=True
    ):
        status = 0
        for chip in range(self._number_of_chips):
            if chip == chip_position:
                if v_mux == 14:
                    status = (
                        self.write_register(
                            name="MonSensSldoAnaSelBias", value=bias, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 16:
                    status = (
                        self.write_register(
                            name="MonSensSldoDigSelBias", value=bias, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 18:
                    status = (
                        self.write_register(
                            name="MonSensAcbSelBias", value=bias, chip_position=chip
                        )
                        and status
                    )
                else:
                    status = -1
                if status < 0:
                    raise RuntimeError(
                        "Incorrect VMUX value for measuring temperature!"
                    )
            elif reset_other_chips:
                status = self.reset_tempsens(chip_position=chip)

        return status

    def set_tempsens_dem(self, chip_position, v_mux=-1, dem=0, reset_other_chips=True):
        status = 0

        for chip in range(self._number_of_chips):
            if chip == chip_position:
                if v_mux == 14:
                    status = (
                        self.write_register(
                            name="MonSensSldoAnaDem", value=dem, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 16:
                    status = (
                        self.write_register(
                            name="MonSensSldoDigDem", value=dem, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 18:
                    status = (
                        self.write_register(
                            name="MonSensAcbDem", value=dem, chip_position=chip
                        )
                        and status
                    )
                else:
                    status = -1
                if status < 0:
                    raise RuntimeError(
                        "Incorrect VMUX value for measuring temperature!"
                    )
            elif reset_other_chips:
                status = self.reset_tempsens(chip_position=chip)

        return status

    def set_trim(self, chip_position, v_mux=-1, trim=0, reset_other_chips=True):

        status = 0
        for chip in range(self._number_of_chips):
            if chip == chip_position:
                if v_mux == 34:
                    status = (
                        self.write_register(
                            name="SldoTrimA", value=trim, chip_position=chip
                        )
                        and status
                    )
                elif v_mux == 38:
                    status = (
                        self.write_register(
                            name="SldoTrimD", value=trim, chip_position=chip
                        )
                        and status
                    )
                else:
                    status = -1
                if status < 0:
                    raise RuntimeError("Incorrect VMUX value for setting trim!")
            elif reset_other_chips:
                status = (
                    self.write_register(name="SldoTrimA", value=0, chip_position=chip)
                    and status
                )
                status = (
                    self.write_register(name="SldoTrimD", value=0, chip_position=chip)
                    and status
                )

        return status

    def get_connectivity(self):
        with open(self.connectivity) as file:
            spec = json.load(file)

        return spec

    def get_config(self, chip_position):
        connect_spec = self.get_connectivity()
        config_path = connect_spec["chips"][chip_position]["config"]
        path = self.connectivity.rsplit("/", 1)[0] + "/" + config_path

        with open(path) as file:
            spec = json.load(file)

        try:
            spec["RD53B"].pop("PixelConfig")
        except KeyError:
            pass

        return spec
