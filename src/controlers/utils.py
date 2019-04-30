import numpy as np


def b(s):
    return s.encode("latin-1")


def read_str(fid, count = 1):
    """Read string from a different ascii/binary format file in a python version compatible way."""
    dtype = np.dtype('>S%i' % count)  # Zero-terminate bytes and number (count)integer
    string = fid.read(dtype.itemsize)
    data = np.frombuffer(string, dtype = dtype)[0]  # Make data readeable
    bytestr = b('').join([data[0:data.index(b('\x00')) if b('\x00') in data else count]])  # Join all the data until the end
    
    return str(bytestr.decode('ascii'))
