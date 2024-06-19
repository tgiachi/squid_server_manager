import os.path
import tarfile
from urllib.request import urlretrieve
from python_event_bus import EventBus
import context
import events_types
import logger_utils
import subprocess

STEAMCMD_LINUX_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"


class SteamCmdManager:
    def __init__(self, ctx: context.AgentContext):
        self.context = ctx
        self.steam_bin = os.path.join(self.context.a_args.steam_cmd_path, 'steamcmd.sh')
        self.logger = logger_utils.init_logger(__name__)
        self.check_prerequisites()
        self.bootstrap_client()

    def check_prerequisites(self):
        if not os.path.exists(os.path.join(self.steam_bin)):

            if not os.path.exists(self.context.a_args.steam_cmd_path):
                os.mkdir(self.context.a_args.steam_cmd_path)

            self.logger.info("Downloading Steam CMD...")
            urlretrieve(STEAMCMD_LINUX_URL, "steamcmd_linux.tar.gz")
            self.logger.info("Extracting Steam CMD...")
            tar = tarfile.open("steamcmd_linux.tar.gz")
            tar.extractall(self.context.a_args.steam_cmd_path)
            tar.close()
            os.remove("steamcmd_linux.tar.gz")
            self.logger.info("Steam CMD ready")

        EventBus.call(events_types.STEAMCMD_READY_EVENT)

    def bootstrap_client(self):
        self.logger.info("Bootstrapping client")
        process = subprocess.Popen([self.steam_bin, "+quit"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                self.logger.info(f"Steam CMD: {output.decode('utf-8').strip()}")

        while True:
            output = process.stderr.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                self.logger.error(f"Steam CMD: {output.decode('utf-8').strip()}")

        return_code = process.wait()
        if return_code != 0:
            self.logger.error("Failed to bootstrap Steam CMD")
            return
        EventBus.call(events_types.STEAMCMD_BOOTSTRAP_EVENT)
