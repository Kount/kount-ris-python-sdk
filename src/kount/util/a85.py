try:
    # python3
    from base64 import a85encode, a85decode
except ImportError:
    # python2
    from mom.codec.base85 import b85decode, b85encode as a85encode

    def a85decode(*args, **kwargs):
        try:
            return b85decode(*args, **kwargs)
        except (TypeError, OverflowError) as e:
            # behave like py3
            raise ValueError(e)

