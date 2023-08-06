from dollar.plugin.dollarplugin import DollarExtensionPlugin
from dollar.dollarobject import DollarObject


class PageExtensionPlugin(DollarExtensionPlugin):

    def extends(self):
        return "dollar"

    def get_name(self):
        return "page"

    def get_secondaries(self):
        return []

    def get_primaries(self):
        return ["title", "description"]

    def validate_primary(self, dollar_object: DollarObject):
        count = 2
        ret = ""

        if "title" not in dollar_object.get_header():
            count = count - 1
            ret = "Type page requires \"title\" key"
        if "description" not in dollar_object.get_header():
            count = count - 1
            ret = "Type page requires \"description\" key"

        if count == 0:
            return "Type page requires \"title\" and \"description\" keys"
        elif count == 1:
            return ret

        return None

    def exec_primary(self, dollar_object: DollarObject):
        pass

    def exec_secondary(self, dollar_object: DollarObject):
        pass
