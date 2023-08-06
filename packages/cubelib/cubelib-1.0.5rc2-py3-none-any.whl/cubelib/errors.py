class BufferExhaustedException(Exception):
    """
        Raised when buffer read() returned less than need
    """
    pass

class BadPacketException(Exception):
    """
        Raised when bad packet passed to one of read() functions
    """
    pass

class DecoderException(Exception):
    """
        Raised when error occured in Night.destroy (Decoder)
    """
    pass
