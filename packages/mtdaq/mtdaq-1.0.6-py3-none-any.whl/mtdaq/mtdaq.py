# -*- coding: utf-8 -*-

from ctypes import *
import platform
import os
from itertools import chain


system = platform.system()
bit = platform.architecture()
if system == 'Windows': #Win
    if bit[0] == '32bit':
        dllpath = os.getenv('SystemDrive')+r'\ProgramData\MangoTree\DLL\x86\MTDAQ_x86.dll'
    elif bit[0] == '64bit':
        dllpath = os.getenv('SystemDrive')+r'\ProgramData\MangoTree\DLL\x64\MTDAQ_x64.dll'
elif system == 'Darwin': #MacOS
    if bit[0] == '64bit':
        dllpath = r'/Library/Application Support/MangoTree/DLL/MTDAQ.framework/MTDAQ'
    else:
        raise Exception("Python 64-bit Required on MacOS.")
elif system == "Linux": #Linux
    if bit[0] == '64bit':
        dllpath = r'/usr/local/MangoTree/DLL/MTDAQ_x64.so'
    else:
        raise Exception("Python 64-bit Required on Linux.")
else:
    raise Exception("Unsupported System.")

if os.path.isfile(dllpath):
    dll = cdll.LoadLibrary(dllpath)
else:
    raise Exception("MT-Master not Installed!")
    
_REFLEN = 20000
def _dev_start(config):    
    dll.MTDAQ_Start.argtypes = [c_char_p, c_char_p, POINTER(c_int32)]
    config_ = c_char_p(config.encode())
    task = create_string_buffer(_REFLEN)
    dll.MTDAQ_Start(config_, task, byref(c_int32(_REFLEN)))
    return task

def _dev_close(task):
    dll.MTDAQ_Close.argtypes = [c_char_p]
    dll.MTDAQ_Close(task)
    
def _reg_write(task, reg_name, reg_value):
    dll.MTDAQ_Custom_WriteU32.argtypes = [c_char_p, c_char_p, c_uint32]
    c_reg_name = c_char_p(reg_name.encode())
    dll.MTDAQ_Custom_WriteU32(task, c_reg_name, c_uint32(reg_value))
    
def _reg_read(task, reg_name):
    dll.MTDAQ_Custom_ReadU32.argtypes = [c_char_p, c_char_p, POINTER(c_uint32)]
    c_reg_name = c_char_p(reg_name.encode())
    reg_ptr = pointer(c_uint32())
    dll.MTDAQ_Custom_ReadU32(task, c_reg_name, reg_ptr)
    return reg_ptr.contents.value

def _data_ai(task, samples, channel_num, timeout):
    datalen = samples * channel_num
    ctype_aidata = c_float * datalen
    dll.MTDAQ_ReadAI.argtypes = [c_char_p, c_uint32, c_int32, ctype_aidata, c_int32]
    c_aidata = ctype_aidata()
    dll.MTDAQ_ReadAI(task, c_uint32(samples), timeout, c_aidata, datalen)
    return c_aidata
    
def _data_ao(task, aodata, timeout):
    ctype_aodata = c_float * len(aodata)
    c_aodata = ctype_aodata(*aodata)
    dll.MTDAQ_WriteAO.argtypes = [c_char_p, ctype_aodata, c_int32, c_int32, POINTER(c_uint32)]
    dll.MTDAQ_WriteAO(task, c_aodata, len(aodata), timeout, pointer(c_uint32()))
    
def _data_ldi(task):
    dll.MTDAQ_ReadLDI.argtypes = [c_char_p, POINTER(c_uint32)]
    c_ldi = pointer(c_uint32())
    dll.MTDAQ_ReadLDI(task, c_ldi)
    return c_ldi.contents
    
def _data_ldo(task, ldo_data):
    dll.MTDAQ_WriteLDO.argtypes = [c_char_p, c_uint32]
    dll.MTDAQ_WriteLDO(task, c_uint32(ldo_data))
    
def _data_hdi(task, samples, timeout):
    ctype_didata = c_uint32 * samples
    dll.MTDAQ_ReadDI.argtypes = [c_char_p, ctype_didata, c_int32, c_uint32, c_int32]
    c_didata = ctype_didata()
    dll.MTDAQ_ReadDI(task, c_uint32(samples), timeout, c_didata, samples)
    return c_didata
    
def _data_hdo(task, hdodata, timeout):
    ctype_dodata = c_uint32 * len(hdodata)
    dll.MTDAQ_WriteDO.argtypes = [c_char_p, ctype_dodata, c_int32, c_int32, POINTER(c_uint32)]
    c_dodata = ctype_dodata(ldodata)
    dll.MTDAQ_WriteDO(task, c_dodata, len(hdodata), timeout, pointer(c_uint32()))    
    
def _data_ci(task, samples, timeout):
    ctype_ci = c_float * samples
    dll.MTDAQ_ReadCI.argtypes = [c_char_p, c_uint32, c_int32, ctype_ci, c_int32]
    c_cidata = ctype_ci()
    dll.MTDAQ_ReadCI(task, c_uint32(samples), timeout, c_cidata, samples)
    return c_cidata    
    
def _data_pwm(task, pwmconfig):
    _pwmconfig = list(chain.from_iterable(pwmconfig))
    _len = len(_pwmconfig)
    if _len % 3 != 0:
        raise Exception("PWM Config Error.")
    chnum = _len // 3
    ctype_pwm = c_float * chnum
    dll.MTDAQ_WritePWM.argtypes = [c_char_p, ctype_pwm, ctype_pwm, ctype_pwm, c_int32]
    c_frequency = ctype_pwm(_pwmconfig[0::3])
    c_dutycircle = ctype_pwm(_pwmconfig[1::3])
    c_count = ctype_pwm(_pwmconfig[2::3])
    dll.MTDAQ_WritePWM(task, c_frequency, c_dutycircle, c_count, chnum)
    
def _data_encoder(task, samples, channel_num, timeout):
    datalen = samples * channel_num * 2
    ctype_encoder = c_int32 * datalen
    dll.MTDAQ_ReadEncoder.argtypes = [c_char_p, c_uint32, c_int32, ctype_encoder, c_int32]
    c_encoderdata = ctype_encoder()
    dll.MTDAQ_ReadEncoder(task, c_uint32(datalen), timeout, c_encoderdata, datalen)
    return c_encoderdata
    
def _data_rtd(task, channel_num):
    ctype_rtd = c_doule * channel_num
    dll.MTDAQ_ReadRTD.argtypes = [c_char_p, ctype_rtd, c_int32]
    c_rtd = ctype_rtd()
    dll.MTDAQ_ReadRTD(task, c_rtd, channel_num)
    return c_rtd
    
def _get_channel_num(task, channel_name):
    chnnel_num_dict = {
        "AI": 0,
        "AO": 1,
        "HSDI": 2,
        "HSDO": 3,
        "CI": 4,
        "CO": 5,
        "Encoder": 6,
        }
    ch = chnnel_num_dict.get(channel_name)
    if ch is not None:
        dll.MTDAQ_ComputingBinary.argtypes = [c_char_p, c_uint16, POINTER(c_uint32)]
        c_channel_num = pointer(c_uint32())
        dll.MTDAQ_ComputingBinary(task, c_uint16(ch), c_channel_num)
        return c_channel_num.contents.value
    return None

from enum import IntEnum
class Mode(IntEnum):
    General = 0
    AOSyncAI = 1
    AISyncEncoder = 2
    EncoderSyncAI = 3
    DITrigerAISyncAO = 4
    DITrigerAI = 5
    Custom = 6

def _c_char_p_init(char, default):
    return c_char_p(char.encode() if char is not None else default.encode())

def getConfig(mode=0, ip=None, device_name=None, device_id=None, slot=None, custom_rom_path=None):
    dll.MTDAQ_Config_Module.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_uint16, c_char_p, c_char_p, c_int32]
    c_ip = _c_char_p_init(ip, "")
    c_device = _c_char_p_init(device_name, "")
    c_id = _c_char_p_init(device_id, "*")
    c_slot = _c_char_p_init(slot, "*")
    c_mode = c_uint16(mode)    
    c_path = _c_char_p_init(custom_rom_path, "")
    c_config = create_string_buffer(20000)
    ret = dll.MTDAQ_Config_Module(c_ip, c_device, c_id, c_slot, c_mode, c_path, c_config, 20000)
    if ret == 12:
        raise Exception("Unknown Device.")
    return c_config.value.decode()
    
from functools import wraps
def is_running(func):
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        if not obj._run:
            raise Exception("Device not Running!")
        return func(obj, *args, **kwargs)
    return wrapper

class Device():
    def __init__(self, config):
        self.config = config
        self._task = None
        self._run = False
        self._chnum = {}
        
    def start(self):
        self._run = False
        self._chnum = {}
        self._task = _dev_start(self.config)
        if len(self._task.value) == 0:
            raise Exception("Failed to Open Device!")
        self._run = True
        
    def close(self):
        _dev_close(self._task)
        self._run = False
    
    @is_running
    def ai(self, samples, timeout=2500):
        if "AI" not in self._chnum.keys():
            self._chnum["AI"] = _get_channel_num(self._task, "AI")
        return _data_ai(self._task, samples, self._chnum["AI"], timeout)
    
    @is_running
    def ao(self, aodata, timeout=2500):
        return _data_ao(self._task, aodata, timeout)
    
    @is_running
    def lowspeed_di(self):
        return _data_ldi(self._task)
    
    @is_running
    def lowspeed_do(self, ldodata):
        return _data_ldo(self._task, ldodata)
    
    @is_running
    def highspeed_di(self, samples, timeout=2500):
        return _data_hdi(self._task, samples, timeout)
    
    @is_running
    def highspeed_do(self, hdodata, timeout=2500):
        return _data_hdo(self._task, hdodata, timeout)
        
    @is_running
    def ci(self, samples, timeout=2500):
        return _data_ci(self._task, samples, timeout)
    
    @is_running
    def pwm(self, pwmconfig):
        return _data_pwm(self._task, pwmconfig)
    
    @is_running
    def encoder(self, samples, timeout=2500):
        if "Encoder" not in self._chnum.keys():
            self._chnum["Encoder"] = _get_channel_num(self._task, "Encoder")
        return _data_ai(self._task, samples, self._chnum["Encoder"])
    
    @is_running
    def rtd(self):
        if "AI" not in self._chnum.keys():
            self._chnum["AI"] = _get_channel_num(self._task, "AI")
        return _data_rtd(self._task, self._chnum["AI"])
