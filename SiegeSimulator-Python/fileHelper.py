class AccessRoomInfo:
    def __init__(self, roomNum: int):
        if roomNum == 1:
            import Images.RoomOption1.roomInfo as ri
            self.size = ri.size
            self.agentStart = ri.agentStart
            self.enemyStart = ri.enemyStart
            self.roomWidth = ri.roomWidth
            self.roomHeight = ri.roomHeight
            self.wallCoords = ri.wallCoords
            self.obstacles = ri.obstacles
            self.agentScale = ri.agentScale
