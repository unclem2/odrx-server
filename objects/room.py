from objects.player import Player
from objects.beatmap import Beatmap
from objects import glob
from enum import IntEnum, unique
from typing import Dict


class RoomStatus(IntEnum):
    OPEN = 1
    LOCKED = 2
    INGAME = 3

    def __repr__(self) -> str:
        return {
            self.OPEN: 'Open',
            self.LOCKED: 'Locked',
            self.INGAME: 'Ingame'
        }[self.value]
        
class PlayerStatus(IntEnum):  #finished
    IDLE = 0
    READY = 1
    NOMAP = 2
    PLAYING = 3
    
    def __repr__(self) -> str:
        return {
            self.IDLE: 'Idle',
            self.READY: 'Ready',
            self.NOMAP: 'NoMap',
            self.PLAYING: 'Playing'
        }[self.value]
        
class Mods:  
    def __init__(self):
        self.mods: str = ''
        self.speedMultiplier: float = 1.0
        self.flFollowDelay: float = 0.12
        
    def as_json(self) -> Dict[str, str]:
        return {
            'mods': self.mods,
            'speedMultiplier': self.speedMultiplier,
            'flFollowDelay': self.flFollowDelay
        }

class PlayerMulti:  
    def __init__(self):
        self.uid: int = 0
        self.username: str = ''
        self.status: PlayerStatus = PlayerStatus.IDLE
        self.team: int = 0
        self.mods: Mods = Mods()
    
    def as_json(self) -> Dict[str, str]:
        return {
            'uid': self.uid,
            'username': self.username,
            'status': self.status,
            'team': self.team,
            'mods': self.mods
        }
    
    def player(self, id):
        player = glob.players.get(id=int(id))
        self.uid = player.id
        self.username = player.name
        self.status = PlayerStatus.IDLE
        self.team = "null"
        self.mods = Mods().as_json()
        return self
    
        
class RoomSettings:  
    def __init__(self):
        self.isRemoveSliderLock: bool = False
        self.isFreeMod: bool = False
        self.allowForceDifficultyStatistics: bool = False  
    
    def as_json(self) -> Dict[str, str]:
        return {
            'isRemoveSliderLock': self.isRemoveSliderLock,
            'isFreeMod': self.isFreeMod,
            'allowForceDifficultyStatistics': self.allowForceDifficultyStatistics
        }
            

class Room:
    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.map: Beatmap = None
        self.host: PlayerMulti = PlayerMulti()
        self.isLocked: bool = False
        self.gameplaySettings: RoomSettings = RoomSettings()
        self.maxPlayers: int = 0
        self.mods: Mods = Mods()
        self.players: list = []
        self.status: RoomStatus = RoomStatus.OPEN
        self.teamMode: int = 0
        self.winCondition: int = 0
        self.password: str = ''
        
    
        
