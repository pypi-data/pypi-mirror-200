from scinode.profile.base_config import Config
from pathlib import Path

default_profile = {
    "name": "default",
    "computer": "localhost",
    "db_address": "mongodb://localhost:27017/",
    "db_name": "scinode_db",
    "config_path": str(Path.home() / ".scinode"),
    "celery": False,
    "broker_url": "amqp://localhost//",
}


class ScinodeProfile(Config):
    """Profile for SciNode."""

    name = "profile"

    def __init__(self) -> None:
        super().__init__()

    def load_activate_profile(self):
        """Load activate profile.
        - first from environmental variable
        - then from json file.

        Returns:
            list: a list of the profile datas.
        """
        import os

        # first from environment variable
        db_address = os.environ.get("scinode_db_address", None)
        db_name = os.environ.get("scinode_db_name", None)
        computer = os.environ.get("scinode_computer", None)
        name = os.environ.get("scinode_profile_name", None)
        celery = os.environ.get("scinode_celery", False)
        broker_url = os.environ.get("scinode_broker_url", False)
        if db_address and db_name and computer and name:
            datas = {
                "name": name,
                "computer": computer,
                "db_address": db_address,
                "db_name": db_name,
                "celery": celery,
                "broker_url": broker_url,
            }
            return datas
        # then read json file
        datas = self.load_activate_profile_from_file()
        if not datas:
            # set default
            datas = default_profile
            default_profile["activate"] = True
            self.saveDatas([datas])
        return datas

    def load_profile_from_file(self, name):
        """Load profile data.

        Args:
            name (str): name of the profile

        Returns:
            dict: _description_
        """
        datas = self.loadDatas()
        for data in datas:
            if data["name"] == name:
                return data
        return None

    def load_activate_profile_from_file(self):
        """Load activate profile from profile.json file."""
        datas = self.loadDatas()
        for data in datas:
            if data["activate"]:
                return data
        return None

    def show(self, name=None):
        """Show profile

        Args:
            name (str, optional): name of the profile. Defaults to None.
        """
        from colorama import Fore, Style

        if not name:
            data = self.load_activate_profile()
        else:
            data = self.load_profile_from_file(name)
        if data is None:
            print(Fore.RED + f"Profile {name} does not exist." + Style.RESET_ALL)
            return
        print("")
        print(
            "Name:              {}".format(Fore.CYAN + data["name"] + Style.RESET_ALL)
        )
        print(
            "Computer:          {}".format(
                Fore.CYAN + data["computer"] + Style.RESET_ALL
            )
        )
        print(
            "Database address:  {}".format(
                Fore.CYAN + data["db_address"] + Style.RESET_ALL
            )
        )
        print(
            "Database name:     {}".format(
                Fore.CYAN + data["db_name"] + Style.RESET_ALL
            )
        )
        print(
            "Configuration path: {}".format(
                Fore.CYAN + data["config_path"] + Style.RESET_ALL
            )
        )
        print(
            "Celery:            {}".format(
                Fore.CYAN + str(data["celery"]) + Style.RESET_ALL
            )
        )
        if data["celery"]:
            print(
                "Broker URL:        {}\n".format(
                    Fore.CYAN + str(data["broker_url"]) + Style.RESET_ALL
                )
            )

    def list(self):
        """List all profiles."""
        from colorama import Fore, Style

        datas = self.loadDatas()
        for data in datas:
            if data["activate"]:
                print(Fore.GREEN + "- {}*".format(data["name"]) + Style.RESET_ALL)
            else:
                print("- {}".format(data["name"]))

    def use(self, name):
        """Use profile

        Args:
            name (str): name of the profile.
        """
        from colorama import Fore, Style

        datas = self.loadDatas()
        exist = False
        for data in datas:
            if data["name"] == name:
                data["activate"] = True
                exist = True
            else:
                data["activate"] = False
        if not exist:
            print(Fore.RED + f"\nProfile {name} does not exist!\n" + Style.RESET_ALL)
        else:
            self.saveDatas(datas)
            print(
                Fore.GREEN + f"\nUse profile {name} successfully!\n" + Style.RESET_ALL
            )


p = ScinodeProfile()
profile_datas = p.load_activate_profile()

if __name__ == "__main__":
    p = ScinodeProfile()
    data = p.loadDatas()
    print(data)
