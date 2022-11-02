from EDNAuto import EDNAuto

edn_auto = EDNAuto()
try:
  while True:
    edn_auto.start()
except:
  print("\n\nExiting...")