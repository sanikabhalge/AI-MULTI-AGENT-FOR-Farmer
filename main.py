import subprocess

def main():
    # Take user input
    soil_pH = float(input("Enter Soil pH: "))
    soil_moisture = float(input("Enter Soil Moisture (%): "))
    temperature = float(input("Enter Temperature (°C): "))
    rainfall = float(input("Enter Rainfall (mm): "))

    # Run server.py to filter crops
    subprocess.run(["python", "sql_query.py", str(soil_pH), str(soil_moisture), str(temperature), str(rainfall)])

    # Run topsis.py to rank and get the best crop
    result = subprocess.run(["python", "topsis.py"], capture_output=True, text=True)
    
    # Print result
    print(result.stdout)

if __name__ == "__main__":
    main()
