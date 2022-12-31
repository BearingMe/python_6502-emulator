import json

with open("data/instruction_set.json", "r") as file:
    instruction_set = json.load(file)

class Instructions:
    lookup = instruction_set

    def _fetch(self):
        instruction = list(filter(
            lambda x: x["instruction"] == self.opcode,
            self.lookup
        ))

        if len(instruction) == 0:
            raise KeyError(f"{self.opcode} is a invalid Opcode")

        self.fetched = 0

        if not instruction[0]["addressing_mode"] == "IMP":
            self.fetched = self.read(self.addr_abs)

        return self.fetched
