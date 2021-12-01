from oslo_config import cfg

default_opts = [
    cfg.StrOpt("host", default="0.0.0.0", help="Address to bind letters server to"),
    cfg.IntOpt("port", default=19091, help="Port to bind letters server to"),
    cfg.StrOpt("mongo_host", default="localhost", help="database host"),
    cfg.IntOpt("mongo_port", default=19091, help="database port"),
    cfg.StrOpt("database_name", default="letters", help="database name")
]

CONF = cfg.CONF

CONF.register_cli_opts(default_opts)


def sanity_check():
    error_message = "letters conf not properly configured"
    if not any([cfg.CONF.host, cfg.CONF.port, cfg.CONF.mongo_host, cfg.CONF.mongo_port, cfg.CONF.database_name]):
        raise Exception(error_message)
