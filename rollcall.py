import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List
import interactions

class MemberType(Enum):
    HITTER = 1
    SETTER = 2

@dataclass
class Member:
    membertype: MemberType
    user: interactions.User
    rallied: bool = False

@dataclass
class Rollcall:
    id: int
    timestamp: float
    coords: str
    members: List[Member] = field(default_factory=list)

    def get_hitters(self):
        return [member for member in self.members if member.membertype == MemberType.HITTER]

    def get_setters(self):
        return [member for member in self.members if member.membertype == MemberType.SETTER]

    def get_hitters_string(self):
        hitters = self.get_hitters()
        if len(hitters) == 0: return "No setters"
        hitters_string = ""
        for hitter in hitters:
            if hitter.membertype is None: continue
            emoji = ' 🔥' if hitter.rallied else ''
            hitters_string += f"- {hitter.user.username}{emoji}\n"
        return hitters_string

    def get_setters_string(self):
        setters = self.get_setters()
        if len(setters) == 0: return "No setters"
        setters_string = ""
        for setter in setters:
            if setter.membertype is None: continue
            emoji = ' 🔥' if setter.rallied else ''
            setters_string += f"- {setter.user.username}{emoji}\n"
        return setters_string

    def set_user_as_hitter(self, user: interactions.User):
        for member in self.members:
            if member.user == user: 
                member.membertype = MemberType.HITTER
                return
        self.members.append(Member(MemberType.HITTER, user))

    def set_user_as_setter(self, user: interactions.User):
        for member in self.members:
            if member.user == user: 
                member.membertype = MemberType.SETTER
                return
        self.members.append(Member(MemberType.SETTER, user))

    def set_user_as_rallied(self, user: interactions.User):
        for member in self.members:
            if member.user == user: 
                member.rallied = not member.rallied
                return
        self.members.append(Member(None, user))

    def generate_rollcall_prompt(self):
        return "Please react to your respective button if you are online and available:"

    def generate_rollcall_embed(self):
        embed = interactions.Embed(title=f"Rollcall {self.id}", description=f"Coordinates: {self.coords if self.coords != '' else 'None'}")
        embed.add_field(name="Hitters", value=self.get_hitters_string())
        embed.add_field(name="Setters", value=self.get_setters_string())
        return embed

@dataclass
class RollcallHistory:
    rollcalls: Rollcall = field(default_factory=list)

    def clean(self):
        cutoff = 60 * 60 * 24
        current_time = time.time()
        self.rollcalls = [rollcall for rollcall in self.rollcalls if current_time - rollcall.timestamp < cutoff]

    def get_rollcall_from_embed_title(self, title: str):
        id = int(title.split(" ")[1])
        for rollcall in self.rollcalls:
            if rollcall.id == id: return rollcall

    def set_rollcall(self, rollcall: Rollcall):
        for i in range(len(self.rollcalls)):
            if self.rollcalls[i].id == rollcall.id: self.rollcalls[i] = rollcall

    def add_rollcall(self, rollcall: Rollcall):
        self.rollcalls.append(rollcall)
