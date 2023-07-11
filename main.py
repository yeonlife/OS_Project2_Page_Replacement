from page_replacement import MINReplacement, FIFOReplacement, LRUReplacement, LFUReplacement, WSMemoryManagement

file_name = input("파일명(.txt)을 입력하세요: ")
file = open(file_name, "r")

line = file.readline()
n = int(line.split(" ")[0])
m = int(line.split(" ")[1])
w = int(line.split(" ")[2])
k = int(line.split(" ")[3])
# print(n, m, w, k)

line = file.readline()
data = line.split(" ")
# print(data)

min_rp = MINReplacement(n, m, k, data)
fifo_rp = FIFOReplacement(n, m, k, data)
lru_rp = LRUReplacement(n, m, k, data)
lfu_rp = LFUReplacement(n, m, k, data)
ws = WSMemoryManagement(n, w, k, data)

print("MIN")
min_rp.min_replacement()

print("FIFO")
fifo_rp.fifo_replacement()

print("LRU")
lru_rp.lru_replacement()

print("LFU")
lfu_rp.lfu_replacement()

print("WS")
ws.ws_memory_management()
