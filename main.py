from EDNAuto import EDNAuto

edn_auto = EDNAuto()
try:
  edn_auto.start()
except KeyboardInterrupt:
  print("\n\nExiting...")