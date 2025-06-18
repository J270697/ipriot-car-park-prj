class Display:
    def __init__(self, id, message="", is_on=False):
        self.id = id
        self.message = message
        self.is_on = is_on

    def __str__(self):
        return f"Display {self.id}: {self.message}"

    def update(self, data):
        if self.is_on:
            # If a message is explicitly passed, use it
            if "message" in data:
                self.message = data["message"]
            else:
                # Otherwise, build default message
                self.message = f"{data['available_bays']} bays available. Temp: {data['temperature']}°C"
            return f"Display {self.id} updated: {self.message}"
        else:
            return f"Display {self.id} is off."
