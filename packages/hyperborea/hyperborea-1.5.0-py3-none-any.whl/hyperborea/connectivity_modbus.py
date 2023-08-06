import functools
import logging
import struct
import threading

import numpy
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusServerContext
from pymodbus.interfaces import IModbusSlaveContext
from pymodbus.transaction import ModbusSocketFramer
from PySide6 import QtCore

from hyperborea.ringbuffer import RingBuffer
from hyperborea.connectivity_manager import BasicConnectivityHandler
from hyperborea.preferences import read_bool_setting
from hyperborea.preferences import read_int_setting
from hyperborea.proxy import DeviceLoggerAdapter

logger = logging.getLogger(__name__)


class ModbusSlave(IModbusSlaveContext):
    def __init__(self, unit_id, serial_number, channel_infos, logger):
        super().__init__()

        self.unit_id = unit_id
        self.serial_number = serial_number
        self.channel_infos = channel_infos
        self.logger = logger

        self.float_encoder = struct.Struct("<f")
        self.float_decoder = struct.Struct("<HH")

        self._create_ringbuffers()

    def _create_ringbuffers(self):
        self.callbacks = []
        self.mean_ringbuffers = []  # index by channel
        self.instant_ringbuffers = []  # index by modbus index
        self.last_instant_value = []  # index by modbus index
        self.modbus_indexes = []  # (channel, subchannel)

        for i, channel_info in enumerate(self.channel_infos):
            subchannel_count = len(channel_info.subchannel_names)

            self.mean_ringbuffers.append(
                RingBuffer(channel_info.mean_len, subchannel_count))

            for j in range(subchannel_count):
                self.instant_ringbuffers.append(
                    RingBuffer(channel_info.mean_len, 1))
                self.last_instant_value.append(0.0)

            modbus_index = len(self.modbus_indexes)
            self.callbacks.append(
                [functools.partial(self._data_callback, i, modbus_index)])

            self.modbus_indexes.extend((i, j) for j in range(subchannel_count))

    def _data_callback(self, channel_index, modbus_index, data):
        # NOTE: can't use the ringbuffer extend function as a callback directly
        # because the ringbuffer class changes at run time

        self.mean_ringbuffers[channel_index].extend(data)

        for i, subchannel_data in enumerate(data.T):
            ringbuffer = self.instant_ringbuffers[modbus_index + i]
            ringbuffer.extend(subchannel_data[:, None])

    def get_callbacks(self):
        return self.callbacks

    def reset(self):
        """ Resets all the datastores to their default values
        """
        pass

    def validate(self, fx, address, count=1):
        """ Validates the request to make sure it is in range

        :param fx: The function we are working with
        :param address: The starting address
        :param count: The number of values to test
        :returns: True if the request in within range, False otherwise
        """
        if self.decode(fx) != 'i':
            return False
        return True

    def getValues(self, fx, address, count=1):
        """ Get `count` values from datastore

        :param fx: The function we are working with
        :param address: The starting address
        :param count: The number of values to retrieve
        :returns: The requested values from a:a+c
        """
        read_address = address & ~1
        if read_address != address:
            words = (count + 2) // 2
        else:
            words = (count + 1) // 2

        results = []
        for i in range(words):
            words = self.read_register_words(read_address + i * 2)
            results.extend(words)

        if address != read_address:
            results = results[1:]

        results = results[:count]

        return results[:count]

    def setValues(self, fx, address, values):
        """ Sets the datastore with the supplied values

        :param fx: The function we are working with
        :param address: The starting address
        :param values: The new values to be set
        """
        return

    def mean_to_16bit(self, value, channel):
        try:
            if value >= channel.maximum:
                return 0xFFFF
            elif value <= channel.minimum:
                return 0
            else:
                ratio = ((value - channel.minimum) /
                         (channel.maximum - channel.minimum))
                return round(0xFFFF * ratio)
        except ValueError:
            return 0

    def std_to_16bit(self, value, channel):
        try:
            if value <= 0:
                return 0

            std_max = (channel.maximum - channel.minimum) / 2.0

            if value >= std_max:
                return 0xFFFF

            return round((value / std_max) * 0xFFFF)
        except ValueError:
            return 0

    def read_register_words(self, address):
        try:
            index = (address % 1000) // 2
            block = address // 1000
            return_type_float = (block & 1) == 0

            if index >= len(self.modbus_indexes) or block > 5:
                # out of range
                return [0, 0]

            channel, subchannel = self.modbus_indexes[index]

            channel_info = self.channel_infos[channel]
            scale = channel_info.unit_formatter.conversion_scale
            offset = channel_info.unit_formatter.conversion_offset

            if block in [0, 1]:
                # mean
                ringbuffer = self.mean_ringbuffers[channel]
                data = ringbuffer.get_contents()[:, subchannel]
                value = (numpy.mean(data) - offset) / scale
            elif block in [2, 3]:
                # std
                ringbuffer = self.mean_ringbuffers[channel]
                data = ringbuffer.get_contents()[:, subchannel]
                value = numpy.std(data) / scale
            elif block in [4, 5]:
                # instant
                ringbuffer = self.instant_ringbuffers[index]
                data = ringbuffer.get_contents()
                if data.size != 0:
                    value = (numpy.mean(data) - offset) / scale
                    self.last_instant_value[index] = value
                    ringbuffer.clear()
                else:
                    value = self.last_instant_value[index]

            if return_type_float:
                buffer = self.float_encoder.pack(value)
                return self.float_decoder.unpack(buffer)
            else:
                if block in [2, 3]:
                    value = self.std_to_16bit(value, channel_info.channel)
                else:
                    value = self.mean_to_16bit(value, channel_info.channel)
                return [value, value]
        except Exception:
            self.logger.exception("Exception in read_register_words")
            return [0, 0]


class ModbusHandler(BasicConnectivityHandler):
    def __init__(self):
        super().__init__()

        self.stopped = False

        self.settings = QtCore.QSettings()

        app = QtCore.QCoreApplication.instance()
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = app.organizationName()
        self.identity.ProductCode = app.applicationName()
        self.identity.VendorUrl = app.organizationDomain()
        self.identity.ProductName = app.applicationName()
        self.identity.ModelName = app.applicationName()
        self.identity.MajorMinorRevision = app.applicationVersion()

        self.context = ModbusServerContext(slaves={}, single=False)

        self.slaves = {}  # key: serial_number, value: ModbusSlave
        self.modbus_server = None
        self.thread = None

        self.update_settings()

    def stop(self):
        self.stopped = True
        self._stop_modbus()

    def join(self):
        if not self.stopped:
            self.stop()

        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def stop_device(self, serial_number):
        slave = self.slaves.pop(serial_number, None)
        if slave:
            del self.context[slave.unit_id]
            slave.logger.info(f"Modbus stopping (Unit ID %s)", slave.unit_id)

    def create_channel_callbacks(self, serial_number, channel_infos):
        modbus_enable = read_bool_setting(
            self.settings, f"{serial_number}/ModbusEnable", False)

        if not modbus_enable:
            return [None] * len(channel_infos)

        device_logger = DeviceLoggerAdapter(logger, serial_number)

        unit_id = read_int_setting(
            self.settings, f"{serial_number}/ModbusUnitID", 1)

        if self.modbus_server is None:
            device_logger.warning(f"Modbus server not running")
            return [None] * len(channel_infos)

        if unit_id in self.context:
            other_sn = "<UNKNOWN>"
            for slave in self.slaves.values():
                if unit_id == slave.unit_id:
                    other_sn = slave.serial_number
                    break
            device_logger.warning(f"Modbus Unit ID %s Already in use by %s",
                                  unit_id, other_sn)
            return [None] * len(channel_infos)

        slave = ModbusSlave(unit_id, serial_number, channel_infos,
                            device_logger)
        self.slaves[serial_number] = slave
        self.context[unit_id] = slave

        device_logger.info(f"Modbus starting (Unit ID %s)", unit_id)

        return slave.get_callbacks()

    def update_settings(self):
        if self.stopped:
            return

        modbus_enable = read_bool_setting(self.settings, "ModbusEnable", False)
        modbus_port = read_int_setting(self.settings, "ModbusPort", 502)

        address = ("", modbus_port)

        if modbus_enable:
            if self.modbus_server is None:
                self._start_modbus(address)
            else:
                if self.modbus_server.address != address:
                    # different address; restart
                    self._stop_modbus()
                    self._start_modbus(address)
        elif self.modbus_server is not None:
            self._stop_modbus()

    def _start_modbus(self, address):
        if self.thread is not None:
            self.thread.join()
            self.thread = None

        try:
            self.modbus_server = ModbusTcpServer(
                self.context, ModbusSocketFramer, self.identity, address)
        except Exception:
            logger.exception("Error starting modbus server")
            self.modbus_server = None
            return

        self.thread = threading.Thread(target=self._thread_run)
        self.thread.start()

        logger.debug("Starting modbus server on port %s", address[1])

    def _stop_modbus(self):
        if self.modbus_server:
            logger.debug("Stopping modbus server")
            self.modbus_server.shutdown()
            self.modbus_server = None

    def _thread_run(self):
        try:
            self.modbus_server.serve_forever()
        except Exception:
            logger.exception("Uncaught exception in _thread_run")
            self._stop_modbus()
