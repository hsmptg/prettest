import smbus

ADDR = 0x68

class MCP3424:
    def __init__(self):
        self.smbus = smbus.SMBus(1)
        self.cmd = 0xF0


    def getData(self):
        self.smbus.write_byte(ADDR, self.cmd)
        while True:
            dat = self.smbus.read_i2c_block_data(ADDR, self.cmd, 3)
            #print(dat[2])
            if dat[2] < 128:
                break;
        return (dat[0]<<8) + dat[1]


