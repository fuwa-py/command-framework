class InteractionInfo:
    def __init__(self, data: dict):
        self._raw_data = data
        self.data = data["data"]

        self.token = data["token"]
        self.id = data["id"]
        self.version = int(data["version"])
        self.type = int(data["type"])

        self.resolved = self.data.get("resolved")

        self.channel_id = int(data["channel_id"])
        self.guild_id = int(data["guild_id"])
        self.guild_locale = data["guild_locale"]
        self.locale = data["locale"]
        self.member = data["member"]

