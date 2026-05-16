import math

# --- RecomendeMe Intelligence Core Logic ---

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Define weights for different incident types. Higher weight means higher risk contribution.
# This simulates the "intelligence" aspect of RecomendeMe, learning what signals are stronger.
INCIDENT_TYPE_WEIGHTS = {
    "suspicious_job_ad": 1.5,
    "missing_person_report": 2.0,
    "anonymous_tip_trafficking": 3.0,
    "known_trafficker_location": 4.0,
    "border_crossing_anomaly": 2.5,
    "general_crime_report": 0.5, # Lower weight, less directly indicative
    "shelter_intake_victim": 3.5,
}

def analyze_incidents_for_risk_zones(incidents, radius_km=50):
    """
    Analyzes a list of incidents to identify potential human trafficking risk zones.
    It simulates 'RecomendeMe Intelligence' by clustering and scoring incidents.
    """
    risk_scores = []

    # Iterate through each incident to assess its surrounding risk
    for i, incident1 in enumerate(incidents):
        cluster_risk_score = 0
        # Start with the incident's own weighted risk
        cluster_risk_score += INCIDENT_TYPE_WEIGHTS.get(incident1["type"], 1.0) # Default weight if type not found

        # Check for nearby incidents within the defined radius
        for j, incident2 in enumerate(incidents):
            if i == j: # Don't compare an incident to itself
                continue

            dist = haversine_distance(incident1["lat"], incident1["lon"], incident2["lat"], incident2["lon"])

            if dist <= radius_km:
                # Add the weighted risk of nearby incidents to the cluster score
                # This simulates how RecomendeMe connects dots and identifies hotspots
                cluster_risk_score += INCIDENT_TYPE_WEIGHTS.get(incident2["type"], 1.0)

        risk_scores.append({
            "incident_id": incident1["id"],
            "location": f"({incident1['lat']:.2f}, {incident1['lon']:.2f})",
            "type": incident1["type"],
            "calculated_risk_score": round(cluster_risk_score, 2)
        })

    # Sort by risk score to recommend the highest priority zones
    risk_scores.sort(key=lambda x: x["calculated_risk_score"], reverse=True)
    return risk_scores

# --- Sample Data (Simulating real-world observations in Brazil) ---
# These incidents represent various data points RecomendeMe might process.
# Coordinates are approximate locations in Brazil.
sample_incidents = [
    {"id": 1, "lat": -23.55, "lon": -46.63, "type": "suspicious_job_ad"}, # São Paulo
    {"id": 2, "lat": -23.56, "lon": -46.64, "type": "missing_person_report"}, # São Paulo
    {"id": 3, "lat": -23.54, "lon": -46.62, "type": "anonymous_tip_trafficking"}, # São Paulo
    {"id": 4, "lat": -22.91, "lon": -43.17, "type": "general_crime_report"}, # Rio de Janeiro
    {"id": 5, "lat": -22.92, "lon": -43.18, "type": "suspicious_job_ad"}, # Rio de Janeiro
    {"id": 6, "lat": -3.12, "lon": -60.02, "type": "border_crossing_anomaly"}, # Manaus (Amazon)
    {"id": 7, "lat": -3.13, "lon": -60.03, "type": "shelter_intake_victim"}, # Manaus (Amazon)
    {"id": 8, "lat": -3.10, "lon": -60.01, "type": "known_trafficker_location"}, # Manaus (Amazon)
    {"id": 9, "lat": -15.78, "lon": -47.93, "type": "suspicious_job_ad"}, # Brasília
    {"id": 10, "lat": -15.79, "lon": -47.94, "type": "missing_person_report"}, # Brasília
    {"id": 11, "lat": -23.60, "lon": -46.68, "type": "general_crime_report"}, # São Paulo outskirts
    {"id": 12, "lat": -23.55, "lon": -46.63, "type": "anonymous_tip_trafficking"}, # São Paulo (same as 1)
    {"id": 13, "lat": -3.12, "lon": -60.02, "type": "shelter_intake_victim"}, # Manaus (same as 6)
    {"id": 14, "lat": -3.11, "lon": -60.01, "type": "anonymous_tip_trafficking"}, # Manaus
]

# --- Main Execution ---
if __name__ == "__main__":
    print("--- RecomendeMe Intelligence: Human Trafficking Risk Zone Analysis ---")
    print(f"Analyzing {len(sample_incidents)} incidents across Brazil...")

    # The 'RecomendeMe Intelligence' analyzes the data to find patterns and recommend actions.
    # Here, it identifies clusters of high-risk incidents.
    recommended_zones = analyze_incidents_for_risk_zones(sample_incidents, radius_km=30)

    print("\nTop Recommended Investigation Zones (by calculated risk score):")
    print("---------------------------------------------------------------")
    for i, zone in enumerate(recommended_zones[:5]): # Display top 5 recommendations
        print(f"{i+1}. Incident ID: {zone['incident_id']} | Location: {zone['location']} | Type: {zone['type']} | Risk Score: {zone['calculated_risk_score']}")

    print("\nThis simulation demonstrates how 'RecomendeMe Intelligence' uses data analysis")
    print("to 'map the darkness' and highlight areas requiring urgent attention in the fight against human trafficking.")
