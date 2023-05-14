from EDNAuto import EDNAuto

try:
    with open("token", "r", encoding="utf-8") as f:
        TOKEN = f.read().replace("\n", "").strip()
except:
    print(" !!! Please create a file named `token`, then put your token there!")
    exit(0)

edn_auto = EDNAuto(TOKEN)

# try:
#     while True:
#         edn_auto.start()
# except:
#     print("\n\tBYE!")
#     exit(0)

edn_auto.start()
