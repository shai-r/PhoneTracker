from datetime import datetime

from app.db.models import Interaction


def convert_interaction_to_model(interaction_data: dict) -> Interaction:
    try:
        return Interaction(
            method=interaction_data['method'],
            timestamp=datetime.fromisoformat(interaction_data['timestamp']),
            bluetooth_version=interaction_data.get('bluetooth_version'),
            signal_strength_dbm=interaction_data.get('signal_strength_dbm'),
            distance_meters=interaction_data.get('distance_meters'),
            duration_seconds=interaction_data.get('duration_seconds')
        )
    except KeyError as e:
        print(f"Missing field in interaction data: {e}")
        return None
