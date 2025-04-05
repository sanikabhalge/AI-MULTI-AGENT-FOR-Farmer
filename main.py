import subprocess

def main():
    print("🌾 Welcome to the Farmer Advisor Agent 🌦️\n")
    
    # Take user input
    try:
        soil_pH = float(input("📥 Enter Soil pH: "))
        soil_moisture = float(input("📥 Enter Soil Moisture (%): "))
        temperature = float(input("📥 Enter Temperature (°C): "))
        rainfall = float(input("📥 Enter Rainfall (mm): "))
    except ValueError:
        print("⚠️ Please enter valid numerical inputs.")
        return

    print("\n🔍 Filtering crops based on environmental conditions...")
    subprocess.run(["python", "sql_query.py", str(soil_pH), str(soil_moisture), str(temperature), str(rainfall)])

    print("📊 Ranking crops using TOPSIS method...")
    subprocess.run(["python", "topsis.py"])

    print("🤝 Finalizing recommendation using market research data...\n")
    result_combined = subprocess.run(["python", "combined_agent.py"], capture_output=True, text=True)
    print(result_combined.stdout)

if __name__ == "__main__":
    main()
