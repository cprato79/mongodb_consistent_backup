import logging


class Archive:
    def __init__(self, config, backup_dir):
        self.config     = config
        self.backup_dir = backup_dir

        self._archiver = None
        self.init()

    def init(self):
        archive_method = self.config.archive.method
        if archive_method is None:
            logging.info("Archiving disabled, skipping")
        else:
            config_vars = ""
            for key in self.config.archive:
                config_vars += "%s=%s," % (key, self.config.archive[key])
            logging.info("Using archiving method: %s (options: %s)" % archive_method, config_vars[:-1])
            try:
                self._archiver = globals()[archive_method](
                    self.config,
                    self.backup_dir
                )
            except Exception, e:
                raise e

    def archive(self):
        if self._archiver:
            return self._archiver.run()

    def close(self):
        if self._archiver:
            return self._archiver.close()
