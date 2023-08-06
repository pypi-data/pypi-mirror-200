class Config:
    MAX_CONTENT_SIZE = 1024 * 4
    """The maximum request content size allowed. Should
    be set to a sane value to prevent DoS-Attacks.
    """


rpc_config = Config()
