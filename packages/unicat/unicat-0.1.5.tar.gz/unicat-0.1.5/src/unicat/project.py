class UnicatProject:
    def __init__(self, unicat, gid):
        self._unicat = unicat
        self._data = self._unicat.projects[gid]

    @property
    def gid(self):
        return self._data["gid"]

    @property
    def name(self):
        return self._data["name"]

    @property
    def owner(self):
        from .user import UnicatUser

        return UnicatUser(self._unicat, self._data["owner"])

    @property
    def status(self):
        return self._data["status"]

    @property
    def channels(self):
        return self._data["options"]["channels"]

    def channel_key_by_name(self, name):
        return list(self.channels.keys())[list(self.channels.values()).index(name)]

    @property
    def ordered_channels(self):
        return self._data["options"]["orderedchannels"]

    @property
    def languages(self):
        return self._data["options"]["languages"]

    @property
    def orderings(self):
        return self._data["options"]["orderings"]

    def ordering_key_by_name(self, name):
        return list(self.orderings.keys())[list(self.orderings.values()).index(name)]

    @property
    def ordered_orderings(self):
        return self._data["options"]["orderedorderings"]

    @property
    def fieldlists(self):
        return self._data["options"]["fieldlists"]

    def fieldlist_key_by_name(self, name):
        return list(self.fieldlists.keys())[list(self.fieldlists.values()).index(name)]

    @property
    def ordered_fieldlists(self):
        return self._data["options"]["orderedfieldlists"]

    @property
    def members(self):
        from .projectmember import UnicatProjectMember

        return [
            UnicatProjectMember(self._unicat, project_member)
            for project_member in self._unicat.projects_members.values()
            if project_member["project_gid"] == self.gid
        ]
