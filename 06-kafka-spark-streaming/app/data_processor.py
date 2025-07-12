import json
from datetime import datetime
from typing import Dict, Any

def validate_user_event(data: Dict[str, Any]) -> bool:
    """Validate user event data"""
    required_fields = ['user_id', 'event_type', 'timestamp']
    return all(field in data for field in required_fields)

def validate_sensor_data(data: Dict[str, Any]) -> bool:
    """Validate sensor data"""
    required_fields = ['sensor_id', 'temperature', 'humidity', 'pressure', 'timestamp']
    if not all(field in data for field in required_fields):
        return False
    
    # Validate temperature range
    if not (0 <= data['temperature'] <= 50):
        return False
    
    # Validate humidity range
    if not (0 <= data['humidity'] <= 100):
        return False
    
    return True

def validate_transaction(data: Dict[str, Any]) -> bool:
    """Validate transaction data"""
    required_fields = ['transaction_id', 'user_id', 'amount', 'currency', 'timestamp']
    if not all(field in data for field in required_fields):
        return False
    
    # Validate amount
    if data['amount'] <= 0:
        return False
    
    # Validate currency
    valid_currencies = ['USD', 'EUR', 'GBP']
    if data['currency'] not in valid_currencies:
        return False
    
    return True

def enrich_user_event(data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich user event with additional metadata"""
    enriched = data.copy()
    enriched['processed_at'] = datetime.now().isoformat()
    enriched['data_source'] = 'kafka_stream'
    
    # Add user segment based on user_id
    user_id = data.get('user_id', 0)
    if user_id <= 100:
        enriched['user_segment'] = 'premium'
    elif user_id <= 500:
        enriched['user_segment'] = 'regular'
    else:
        enriched['user_segment'] = 'new'
    
    return enriched

def enrich_sensor_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich sensor data with calculated fields"""
    enriched = data.copy()
    enriched['processed_at'] = datetime.now().isoformat()
    enriched['data_source'] = 'kafka_stream'
    
    # Calculate derived metrics
    temperature = data.get('temperature', 0)
    humidity = data.get('humidity', 0)
    
    # Heat index calculation (simplified)
    if temperature > 27 and humidity > 40:
        enriched['heat_index'] = temperature + 0.5 * humidity
    else:
        enriched['heat_index'] = temperature
    
    # Add alert flags
    enriched['temperature_alert'] = temperature > 35 or temperature < 5
    enriched['humidity_alert'] = humidity > 90 or humidity < 10
    
    return enriched

def enrich_transaction(data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich transaction data with business logic"""
    enriched = data.copy()
    enriched['processed_at'] = datetime.now().isoformat()
    enriched['data_source'] = 'kafka_stream'
    
    amount = data.get('amount', 0)
    
    # Add transaction category
    if amount < 50:
        enriched['transaction_category'] = 'small'
    elif amount < 200:
        enriched['transaction_category'] = 'medium'
    else:
        enriched['transaction_category'] = 'large'
    
    # Add fraud risk score (simplified)
    if amount > 1000:
        enriched['fraud_risk'] = 'high'
    elif amount > 500:
        enriched['fraud_risk'] = 'medium'
    else:
        enriched['fraud_risk'] = 'low'
    
    return enriched

def aggregate_user_events(events: list) -> Dict[str, Any]:
    """Aggregate user events for analytics"""
    if not events:
        return {}
    
    event_types = {}
    user_activity = {}
    
    for event in events:
        event_type = event.get('event_type', 'unknown')
        user_id = event.get('user_id', 0)
        
        # Count event types
        event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Track user activity
        if user_id not in user_activity:
            user_activity[user_id] = []
        user_activity[user_id].append(event_type)
    
    return {
        'total_events': len(events),
        'event_type_counts': event_types,
        'active_users': len(user_activity),
        'avg_events_per_user': len(events) / len(user_activity) if user_activity else 0
    }

def aggregate_sensor_data(sensor_readings: list) -> Dict[str, Any]:
    """Aggregate sensor data for monitoring"""
    if not sensor_readings:
        return {}
    
    temperatures = [r.get('temperature', 0) for r in sensor_readings]
    humidities = [r.get('humidity', 0) for r in sensor_readings]
    pressures = [r.get('pressure', 0) for r in sensor_readings]
    
    return {
        'total_readings': len(sensor_readings),
        'avg_temperature': sum(temperatures) / len(temperatures),
        'avg_humidity': sum(humidities) / len(humidities),
        'avg_pressure': sum(pressures) / len(pressures),
        'max_temperature': max(temperatures),
        'min_temperature': min(temperatures),
        'alerts': len([r for r in sensor_readings if r.get('temperature_alert', False)])
    }

def aggregate_transactions(transactions: list) -> Dict[str, Any]:
    """Aggregate transaction data for business analytics"""
    if not transactions:
        return {}
    
    amounts = [t.get('amount', 0) for t in transactions]
    currencies = {}
    merchants = {}
    
    for transaction in transactions:
        currency = transaction.get('currency', 'unknown')
        merchant = transaction.get('merchant', 'unknown')
        
        currencies[currency] = currencies.get(currency, 0) + transaction.get('amount', 0)
        merchants[merchant] = merchants.get(merchant, 0) + 1
    
    return {
        'total_transactions': len(transactions),
        'total_amount': sum(amounts),
        'avg_amount': sum(amounts) / len(amounts),
        'currency_totals': currencies,
        'merchant_counts': merchants,
        'max_transaction': max(amounts),
        'min_transaction': min(amounts)
    } 