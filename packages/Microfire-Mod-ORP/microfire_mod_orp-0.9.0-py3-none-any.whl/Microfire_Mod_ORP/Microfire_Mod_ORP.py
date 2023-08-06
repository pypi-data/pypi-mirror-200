import math
import struct
import time
import smbus  # pylint: disable=E0401

ORP_MEASUREMENT_TIME = 750

UFIRE_MOD_ORP = 0x0e

MEASURE_ORP_TASK = 80       # Command to start a pH measure
CALIBRATE_SINGLE_TASK = 4   # Command to calibrate the high point of the probe
I2C_TASK = 2                # Command to change the i2c address

HW_VERSION_REGISTER = 0                 # hardware version register
FW_VERSION_REGISTER = 1                 # firmware version  register
TASK_REGISTER = 2                       # task register
STATUS_REGISTER = 3                     # status register
MV_REGISTER = 4                         # mV register
CALIBRATE_SINGLE_OFFSET_REGISTER = 12   # single-point calibration register

def exception_catch(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return func_wrapper


class i2c(object):
    mV = 0
    calibrationSingleOffset = 0
    hwVersion = 0
    fwVersion = 0
    status = 0
    _address = 0
    _i2cPort = 0
    status_string = ["no error", "system error"]

    @exception_catch
    def begin(self, i2c_bus=1, address=UFIRE_MOD_ORP):
        self._address = address
        self._i2cPort = smbus.SMBus(i2c_bus)

        return self.connected()

    @exception_catch
    def connected(self):
        try:
            self._i2cPort.write_quick(self._address)
            return True
        except IOError:
            return False

    @exception_catch
    def calibrateSingle(self, solution_mV, blocking=True):
        self._write_4_bytes(MV_REGISTER, solution_mV)

        self._send_command(CALIBRATE_SINGLE_TASK)
        if (blocking):
            time.sleep(ORP_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo()
        return self.status

    @exception_catch
    def getDeviceInfo(self):
        self.calibrationSingleOffset = self._read_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER)
        self.hwVersion = self._read_byte(HW_VERSION_REGISTER)
        self.fwVersion = self._read_byte(FW_VERSION_REGISTER)
        self.status = self._read_byte(STATUS_REGISTER)

    @exception_catch
    def measureORP(self, blocking=True):
        self._send_command(MEASURE_ORP_TASK)
        if (blocking):
            time.sleep(ORP_MEASUREMENT_TIME / 1000.0)

        self._updateRegisters()

        return self.mV

    @exception_catch
    def reset(self):
        NAN = float('nan')
        self._write_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER, NAN)

    @exception_catch
    def setDeviceInfo(self, calibrationSingleOffset):
        self._write_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER, calibrationSingleOffset)

    @exception_catch
    def setI2CAddress(self, i2cAddress):
        self._write_4_bytes(MV_REGISTER, i2cAddress)
        self._send_command(I2C_TASK)
        self._address = i2cAddress

    @exception_catch
    def update(self):
        self._updateRegisters()

    @exception_catch
    def _updateRegisters(self):
        self.status = self._read_byte(STATUS_REGISTER)
        self.mV = self._read_4_bytes(MV_REGISTER)

        if (self.status != 0):
            self.mV = 0


    @exception_catch
    def _send_command(self, command):
        self._i2cPort.write_byte_data(self._address, TASK_REGISTER, command)
        time.sleep(10 / 1000.0)

    @exception_catch
    def _write_4_bytes(self, reg, f):
        fd = bytearray(struct.pack("f", f))
        data = [0, 0, 0, 0]
        data[0] = fd[0]
        data[1] = fd[1]
        data[2] = fd[2]
        data[3] = fd[3]
        self._i2cPort.write_i2c_block_data(self._address, reg, data)

    @exception_catch
    def _read_4_bytes(self, reg):
        data = [0, 0, 0, 0]
        self._i2cPort.write_byte(self._address, reg)
        data = self._i2cPort.read_i2c_block_data(self._address, reg, 4)
        ba = bytearray(data)
        f = struct.unpack('f', ba)[0]
        return f

    @exception_catch
    def _write_byte(self, reg, val):
        self._i2cPort.write_byte_data(self._address, reg, val)

    @exception_catch
    def _read_byte(self, reg):
        self._i2cPort.write_byte(self._address, reg)
        return self._i2cPort.read_byte(self._address)
