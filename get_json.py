from receive_remote import Socket


class JSON:
    def __init__(self):
        self.ip = "141.252.29.66"
        self.port = 5535
        self.data = None
        self.counter = 0
        self.socket = Socket(self.ip, self.port)
        self.socket.start_loop()

    def get_json(self):
        self.data = get_data()
        # data = {
        #     "joy1x": self.counter,
        #     "joy1y": self.counter + 50,
        #     "joy2x": self.counter + 100,
        #     "joy2y": self.counter + 150
        # }
        # self.data = json.dumps(data)
        # if self.counter > 800:
        #     self.counter = 0
        # else:
        #     self.counter += 10
        return self.data
