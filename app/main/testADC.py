from mcp3424 import MCP3424

adc = MCP3424()

dat = adc.getData()
print(dat)