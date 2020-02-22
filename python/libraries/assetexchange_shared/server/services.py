
class AssetPushServiceInterface:
    # lists all supported asset types which can be pushed here
    def SupportedTypes(self, _):
        return []

    # checks if specific asset can be pushed here
    def PushAllowed(self, asset):
        return False

    # reacts to asset push intent
    def Push(self, data):
        return False
