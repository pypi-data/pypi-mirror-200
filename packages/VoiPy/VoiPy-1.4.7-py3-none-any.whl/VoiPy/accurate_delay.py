import ctypes
import os

# Constants:
VERSION = '0.2.1'

if os.name == 'nt':  # for Windows:
    def micros():
        "return a timestamp in microseconds (us)"
        tics = ctypes.c_int64()  # use *signed* 64-bit variables; see the "QuadPart" variable here: https://msdn.microsoft.com/en-us/library/windows/desktop/aa383713(v=vs.85).aspx
        freq = ctypes.c_int64()

        # get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        # get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

        t_us = tics.value * 1e6 / freq.value
        return t_us


    def millis():
        """return a timestamp in milliseconds (ms)"""
        tics = ctypes.c_int64()  # use *signed* 64-bit variables; see the "QuadPart" variable here: https://msdn.microsoft.com/en-us/library/windows/desktop/aa383713(v=vs.85).aspx
        freq = ctypes.c_int64()

        # get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        # get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

        t_ms = tics.value * 1e3 / freq.value
        return t_ms

elif os.name == 'posix':  # for Linux:

    # Constants:
    CLOCK_MONOTONIC_RAW = 4  # see <linux/time.h> here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h


    # prepare ctype timespec structure of {long, long}
    # -NB: use c_long (generally signed 32-bit) variables within the timespec C struct, per the definition here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h
    class timespec(ctypes.Structure):
        _fields_ = \
            [
                ('tv_sec', ctypes.c_long),
                ('tv_nsec', ctypes.c_long)
            ]


    # Configure Python access to the clock_gettime C library, via ctypes:
    # Documentation:
    # -ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
    # -librt.so.1 with clock_gettime: https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html #-
    # -Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
    librt = ctypes.CDLL('librt.so.1', use_errno=True)
    clock_gettime = librt.clock_gettime
    # specify input arguments and types to the C clock_gettime() function
    # (int clock_ID, timespec* t)
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]


    def monotonic_time():
        "return a timestamp in seconds (sec)"
        t = timespec()
        # (Note that clock_gettime() returns 0 for success, or -1 for failure, in
        # which case errno is set appropriately)
        # -see here: http://linux.die.net/man/3/clock_gettime
        if clock_gettime(CLOCK_MONOTONIC_RAW, ctypes.pointer(t)) != 0:
            # if clock_gettime() returns an error
            errno_ = ctypes.get_errno()
            raise OSError(errno_, os.strerror(errno_))
        return t.tv_sec + t.tv_nsec * 1e-9  # sec


    def micros():
        "return a timestamp in microseconds (us)"
        return monotonic_time() * 1e6  # us


    def millis():
        "return a timestamp in milliseconds (ms)"
        return monotonic_time() * 1e3  # ms


def _constrain(val, min_val, max_val):
    """constrain a number to be >= min_val and <= max_val"""
    if val < min_val:
        val = min_val
    elif val > max_val:
        val = max_val
    return val


def delay(delay_ms):
    """delay for delay_ms milliseconds (ms)"""
    delay_ms = _constrain(delay_ms, 0, (1 << 32) - 1)
    t_start = millis()
    while (millis() - t_start) % (1 << 32) < delay_ms:  # use modulus to force C uint32_t-like underflow behavior
        pass  # do nothing
    return


def delayMicroseconds(delay_us):
    "delay for delay_us microseconds (us)"
    # constrain the commanded delay time to be within valid C type uint32_t limits
    delay_us = _constrain(delay_us, 0, (1 << 32) - 1)
    t_start = micros()
    while (micros() - t_start) % (1 << 32) < delay_us:  # use modulus to force C uint32_t-like underflow behavior
        pass  # do nothing
    return
