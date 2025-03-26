periods = {"days": 24*60*60, "halfdays": 12*60*60, "quarterdays": 6*60*60, "minutes": 60, "seconds": 1, "hours": 1*60*60}
def converting(time, convert, mount):
    result = (periods[time]/periods[convert])*mount
    return result
def main():
    period = input("Select a time period: ").lower()
    if period not in periods:
      print("Invalid time period, please restart.")
      main()
    amount = input(f"Enter the amount of {period}: ")
    try:
      amount = int(amount)
    except:
      print("Invalid input, please restart.")
      main()
    conversion = input("Select a time period to convert to: ").lower()
    if conversion not in periods:
      print("Invalid time period, please restart.")
      main()
    print(f" There are {converting(period, conversion, amount)} {conversion} in {amount} {period}")
main()