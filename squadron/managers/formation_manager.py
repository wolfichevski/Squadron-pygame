from settings import SET

class FormationManager:
    def __init__(self):
        self.current = SET.Formation.MEDIUM

    def cycle(self):
        if self.current == SET.Formation.CLOSE:
            self.current = SET.Formation.MEDIUM
        elif self.current == SET.Formation.MEDIUM:
            self.current = SET.Formation.WIDE
        else:
            self.current = SET.Formation.CLOSE

    def set_by_number(self, num: int):
        if num == 1:
            self.current = SET.Formation.CLOSE
        elif num == 2:
            self.current = SET.Formation.MEDIUM
        elif num == 3:
            self.current = SET.Formation.WIDE

    def get_gap(self):
        if self.current == SET.Formation.CLOSE:
            return SET.PLANE_GAP_CLOSE
        if self.current == SET.Formation.MEDIUM:
            return SET.PLANE_GAP_MEDIUM
        return SET.PLANE_GAP_WIDE
