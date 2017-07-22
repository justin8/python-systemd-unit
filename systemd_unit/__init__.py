import logging
import os
import subprocess

log = logging.getLogger(__name__)


class Unit(object):

    def __init__(self, name, type="service", content=None):
        self.name = name
        self.service_name = "{name}.{type}".format(name=name, type=type)
        self.service_file_path = os.path.join("/etc/systemd/system", self.service_name)
        self.content = content

        try:
            self._systemctl(['--help'])
        except FileNotFoundError as e:
            log.error("Unable to find systemctl!")
            raise(e)
        log.debug("Initialized systemd.Unit for '{name}' with type '{type}'".format(name=name, type=type))

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def create_service_file(self):
        log.info("Creating/updating service file for '{name}' at '{service_file_path}'".format(name=self.name, service_file_path=self.service_file_path))
        with open(self.service_file_path, "w") as f:
            f.write(self._content)

    def ensure(self, restart=True, enable=True, content=None):
        if content:
            self.content = content
        self.create_service_file()
        self.reload()
        if restart:
            self.restart()
        if enable:
            self.enable()

    def remove(self):
        try:
            if os.path.exists(self.service_file_path):
                self.stop()
                self.disable()
        except subprocess.CalledProcessError:
            pass

        log.info("Removing service file for {name} from {service_file_path}".format(name=self.name, service_file_path=self.service_file_path))
        try:
            os.remove(self.service_file_path)
            log.debug("Successfully removed service file")
        except FileNotFoundError:
            log.debug("No service file found")
        self.reload()

    def _systemctl(self, args, stderr=None):
        try:
            subprocess.check_output(["systemctl"] + args, stderr=stderr)
        except subprocess.CalledProcessError as e:
            log.error("Failed to run systemctl with parameters {args}".format(args=args))
            raise(e)

    def reload(self):
        log.info("Reloading daemon files")
        self._systemctl(["daemon-reload"])

    def restart(self):
        log.info("Restarting {service_name}".format(service_name=self.service_name))
        self._systemctl(["restart", self.service_name])

    def stop(self):
        log.info("Stopping {service_name}".format(service_name=self.service_name))
        self._systemctl(["stop", self.service_name], stderr=subprocess.DEVNULL)

    def start(self):
        log.info("Starting {service_name}".format(service_name=self.service_name))
        self._systemctl(["start", self.service_name], stderr=subprocess.DEVNULL)

    def enable(self):
        log.info("Enabling {service_name}".format(service_name=self.service_name))
        self._systemctl(["enable", self.service_name])

    def disable(self):
        log.info("Disabling {service_name}".format(service_name=self.service_name))
        self._systemctl(["disable", self.service_name], stderr=subprocess.DEVNULL)
