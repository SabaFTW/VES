#!/usr/bin/env python3
"""
ARSO Weather Data Connector for VES Elysia Portal

Fetches real-time weather data from ARSO (Agencija Republike Slovenije za okolje)
XML APIs and integrates with the Wolf Daemon ecosystem.

Features:
- Real-time weather data fetching
- XML parsing and data normalization
- Alert detection and thresholding
- Caching and offline capability
- CLI interface for testing

Author: VES Elysia Portal Team
License: MIT
"""

import asyncio
import aiohttp
import json
import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ARSOConnector")

# ARSO API Configuration
ARSO_BASE_URL = "https://www.arso.gov.si"
ARSO_WEATHER_XML = f"{ARSO_BASE_URL}/xml/meteorologija/observ_si_latest.xml"
ARSO_ALERTS_XML = f"{ARSO_BASE_URL}/xml/meteorologija/forecast/warnings_si.xml"
ARSO_FORECAST_XML = f"{ARSO_BASE_URL}/xml/meteorologija/forecast/si_forecast.xml"

# Cache configuration
CACHE_DIR = Path("./arso_cache")
CACHE_DURATION = 300  # 5 minutes


@dataclass
class WeatherStation:
    """Weather station information"""
    id: str
    name: str
    latitude: float
    longitude: float
    altitude: float
    active: bool = True


@dataclass
class WeatherData:
    """Current weather observation data"""
    station_id: str
    station_name: str
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[str] = None
    wind_gust: Optional[float] = None
    precipitation: Optional[float] = None
    visibility: Optional[float] = None
    cloud_cover: Optional[str] = None
    weather_condition: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass  
class WeatherAlert:
    """Weather alert/warning information"""
    alert_id: str
    level: str  # GREEN, YELLOW, ORANGE, RED
    type: str   # WIND, RAIN, SNOW, TEMPERATURE, etc.
    title: str
    description: str
    affected_regions: List[str]
    valid_from: datetime
    valid_until: datetime
    issued: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['valid_from'] = self.valid_from.isoformat()
        data['valid_until'] = self.valid_until.isoformat()
        data['issued'] = self.issued.isoformat()
        return data


@dataclass
class ForecastData:
    """Weather forecast data"""
    location: str
    date: datetime
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    condition: Optional[str] = None
    precipitation_probability: Optional[int] = None
    wind_speed: Optional[float] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data


class ARSOConnector:
    """
    Main ARSO weather data connector
    
    Handles fetching, parsing, and caching of ARSO weather data
    """
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.session = None
        self._setup_cache()
        
    def _setup_cache(self):
        """Setup cache directory"""
        if self.cache_enabled:
            CACHE_DIR.mkdir(exist_ok=True)
            
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'VES-Elysia-Portal/1.0'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for given key"""
        return CACHE_DIR / f"{cache_key}.json"
        
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file is still valid"""
        if not cache_path.exists():
            return False
        
        modified_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - modified_time < timedelta(seconds=CACHE_DURATION)
        
    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Load data from cache if valid"""
        if not self.cache_enabled:
            return None
            
        cache_path = self._get_cache_path(cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logger.warning(f"Invalid cache file: {cache_path}")
                
        return None
        
    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache"""
        if not self.cache_enabled:
            return
            
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
            
    async def _fetch_xml(self, url: str) -> Optional[ET.Element]:
        """Fetch and parse XML from ARSO"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    return ET.fromstring(content)
                else:
                    logger.error(f"HTTP {response.status} fetching {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
            
    def _parse_weather_xml(self, root: ET.Element) -> List[WeatherData]:
        """Parse weather observations XML"""
        observations = []
        
        for station in root.findall('.//postaja'):
            try:
                station_id = station.get('id', 'unknown')
                station_name = station.get('ime', 'Unknown')
                
                # Parse timestamp
                timestamp_str = station.find('.//datum_od').text if station.find('.//datum_od') is not None else None
                if timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.now()
                
                # Parse weather parameters
                weather = WeatherData(
                    station_id=station_id,
                    station_name=station_name,
                    timestamp=timestamp
                )
                
                # Temperature
                temp_elem = station.find('.//t')
                if temp_elem is not None and temp_elem.text:
                    weather.temperature = float(temp_elem.text)
                    
                # Humidity
                humidity_elem = station.find('.//rh')
                if humidity_elem is not None and humidity_elem.text:
                    weather.humidity = float(humidity_elem.text)
                    
                # Pressure
                pressure_elem = station.find('.//p')
                if pressure_elem is not None and pressure_elem.text:
                    weather.pressure = float(pressure_elem.text)
                    
                # Wind speed
                wind_elem = station.find('.//ws')
                if wind_elem is not None and wind_elem.text:
                    weather.wind_speed = float(wind_elem.text)
                    
                # Wind direction
                wind_dir_elem = station.find('.//wd')
                if wind_dir_elem is not None and wind_dir_elem.text:
                    weather.wind_direction = wind_dir_elem.text
                    
                # Precipitation
                precip_elem = station.find('.//rain')
                if precip_elem is not None and precip_elem.text:
                    weather.precipitation = float(precip_elem.text)
                
                observations.append(weather)
                
            except Exception as e:
                logger.warning(f"Error parsing station {station_id}: {e}")
                continue
                
        return observations
        
    def _parse_alerts_xml(self, root: ET.Element) -> List[WeatherAlert]:
        """Parse weather alerts XML"""
        alerts = []
        
        for alert in root.findall('.//opozorilo'):
            try:
                alert_id = alert.get('id', f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}")
                
                # Alert level and type
                level = alert.find('.//stopnja')
                level_text = level.text if level is not None else 'UNKNOWN'
                
                alert_type = alert.find('.//vrsta')
                type_text = alert_type.text if alert_type is not None else 'GENERAL'
                
                # Title and description
                title = alert.find('.//naslov')
                title_text = title.text if title is not None else 'Weather Alert'
                
                description = alert.find('.//opis')
                description_text = description.text if description is not None else ''
                
                # Validity period
                valid_from_elem = alert.find('.//velja_od')
                valid_until_elem = alert.find('.//velja_do')
                
                valid_from = datetime.now()
                valid_until = datetime.now() + timedelta(hours=24)
                
                if valid_from_elem is not None and valid_from_elem.text:
                    valid_from = datetime.fromisoformat(valid_from_elem.text.replace('Z', '+00:00'))
                    
                if valid_until_elem is not None and valid_until_elem.text:
                    valid_until = datetime.fromisoformat(valid_until_elem.text.replace('Z', '+00:00'))
                
                # Affected regions
                regions = []
                for region in alert.findall('.//obmocje'):
                    if region.text:
                        regions.append(region.text)
                        
                weather_alert = WeatherAlert(
                    alert_id=alert_id,
                    level=level_text,
                    type=type_text,
                    title=title_text,
                    description=description_text,
                    affected_regions=regions,
                    valid_from=valid_from,
                    valid_until=valid_until,
                    issued=datetime.now()
                )
                
                alerts.append(weather_alert)
                
            except Exception as e:
                logger.warning(f"Error parsing alert: {e}")
                continue
                
        return alerts
        
    async def get_current_weather(self, station_id: Optional[str] = None) -> List[WeatherData]:
        """
        Get current weather observations
        
        Args:
            station_id: Optional station ID to filter by
            
        Returns:
            List of weather observations
        """
        cache_key = f"weather_current_{station_id or 'all'}"
        
        # Try cache first
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            logger.info("Returning cached weather data")
            return [WeatherData(**item) for item in cached_data]
            
        # Fetch from ARSO
        logger.info("Fetching current weather from ARSO")
        root = await self._fetch_xml(ARSO_WEATHER_XML)
        
        if root is None:
            logger.error("Failed to fetch weather data")
            return []
            
        observations = self._parse_weather_xml(root)
        
        # Filter by station if requested
        if station_id:
            observations = [obs for obs in observations if obs.station_id == station_id]
            
        # Cache the results
        cache_data = [obs.to_dict() for obs in observations]
        self._save_to_cache(cache_key, cache_data)
        
        logger.info(f"Retrieved {len(observations)} weather observations")
        return observations
        
    async def get_weather_alerts(self) -> List[WeatherAlert]:
        """
        Get current weather alerts
        
        Returns:
            List of active weather alerts
        """
        cache_key = "weather_alerts"
        
        # Try cache first
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            logger.info("Returning cached alert data")
            return [WeatherAlert(**item) for item in cached_data]
            
        # Fetch from ARSO
        logger.info("Fetching weather alerts from ARSO")
        root = await self._fetch_xml(ARSO_ALERTS_XML)
        
        if root is None:
            logger.error("Failed to fetch alert data")
            return []
            
        alerts = self._parse_alerts_xml(root)
        
        # Cache the results
        cache_data = [alert.to_dict() for alert in alerts]
        self._save_to_cache(cache_key, cache_data)
        
        logger.info(f"Retrieved {len(alerts)} weather alerts")
        return alerts
        
    async def check_alert_thresholds(self, weather_data: List[WeatherData]) -> List[Dict]:
        """
        Check weather data against alert thresholds
        
        Args:
            weather_data: List of weather observations
            
        Returns:
            List of triggered alerts
        """
        triggered_alerts = []
        
        # Define thresholds
        thresholds = {
            'temperature_high': 35.0,  # °C
            'temperature_low': -15.0,  # °C
            'wind_speed_high': 50.0,   # km/h
            'wind_gust_high': 70.0,    # km/h
            'precipitation_high': 30.0  # mm/h
        }
        
        for obs in weather_data:
            alerts = []
            
            # High temperature
            if obs.temperature and obs.temperature > thresholds['temperature_high']:
                alerts.append({
                    'type': 'HIGH_TEMPERATURE',
                    'level': 'ORANGE',
                    'message': f"High temperature: {obs.temperature}°C",
                    'station': obs.station_name,
                    'value': obs.temperature,
                    'threshold': thresholds['temperature_high']
                })
                
            # Low temperature
            if obs.temperature and obs.temperature < thresholds['temperature_low']:
                alerts.append({
                    'type': 'LOW_TEMPERATURE',
                    'level': 'YELLOW',
                    'message': f"Low temperature: {obs.temperature}°C",
                    'station': obs.station_name,
                    'value': obs.temperature,
                    'threshold': thresholds['temperature_low']
                })
                
            # High wind speed
            if obs.wind_speed and obs.wind_speed > thresholds['wind_speed_high']:
                alerts.append({
                    'type': 'HIGH_WIND',
                    'level': 'ORANGE',
                    'message': f"Strong winds: {obs.wind_speed} km/h",
                    'station': obs.station_name,
                    'value': obs.wind_speed,
                    'threshold': thresholds['wind_speed_high']
                })
                
            # High precipitation
            if obs.precipitation and obs.precipitation > thresholds['precipitation_high']:
                alerts.append({
                    'type': 'HEAVY_RAIN',
                    'level': 'YELLOW',
                    'message': f"Heavy precipitation: {obs.precipitation} mm/h",
                    'station': obs.station_name,
                    'value': obs.precipitation,
                    'threshold': thresholds['precipitation_high']
                })
                
            triggered_alerts.extend(alerts)
            
        return triggered_alerts
        
    async def get_stations(self) -> List[WeatherStation]:
        """
        Get list of available weather stations
        
        Returns:
            List of weather stations
        """
        # For now, return major stations - this could be expanded
        # to parse station list from ARSO metadata XML
        stations = [
            WeatherStation("LJUBLJANA", "Ljubljana", 46.066, 14.514, 299),
            WeatherStation("MARIBOR", "Maribor", 46.556, 15.647, 275),
            WeatherStation("PORTOROZ", "Portorož", 45.514, 13.616, 2),
            WeatherStation("MURSKA_SOBOTA", "Murska Sobota", 46.661, 16.166, 188),
            WeatherStation("NOVO_MESTO", "Novo mesto", 45.806, 15.167, 220),
            WeatherStation("SLOVENJ_GRADEC", "Slovenj Gradec", 46.511, 15.080, 465)
        ]
        
        return stations


async def main():
    """CLI interface for testing ARSO connector"""
    parser = argparse.ArgumentParser(description='ARSO Weather Data Connector')
    parser.add_argument('command', choices=['weather', 'alerts', 'stations', 'test'],
                       help='Command to execute')
    parser.add_argument('--station', type=str, help='Station ID to filter by')
    parser.add_argument('--no-cache', action='store_true', help='Disable caching')
    
    args = parser.parse_args()
    
    connector = ARSOConnector(cache_enabled=not args.no_cache)
    
    try:
        async with connector:
            if args.command == 'weather':
                weather_data = await connector.get_current_weather(args.station)
                
                if not weather_data:
                    print("❌ No weather data available")
                    return
                    
                print(f"🌤️ Current Weather Data ({len(weather_data)} stations)")
                print("=" * 60)
                
                for obs in weather_data:
                    print(f"\n📍 {obs.station_name} ({obs.station_id})")
                    print(f"🕐 {obs.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if obs.temperature is not None:
                        print(f"🌡️  Temperature: {obs.temperature}°C")
                    if obs.humidity is not None:
                        print(f"💧 Humidity: {obs.humidity}%")
                    if obs.pressure is not None:
                        print(f"📊 Pressure: {obs.pressure} hPa")
                    if obs.wind_speed is not None:
                        wind_dir = f" {obs.wind_direction}" if obs.wind_direction else ""
                        print(f"🌪️  Wind: {obs.wind_speed} km/h{wind_dir}")
                    if obs.precipitation is not None:
                        print(f"🌧️  Precipitation: {obs.precipitation} mm")
                        
                # Check for threshold alerts
                threshold_alerts = await connector.check_alert_thresholds(weather_data)
                if threshold_alerts:
                    print(f"\n⚠️ Threshold Alerts ({len(threshold_alerts)})")
                    print("=" * 40)
                    for alert in threshold_alerts:
                        print(f"🚨 {alert['level']} - {alert['type']}")
                        print(f"   {alert['message']} at {alert['station']}")
                        
            elif args.command == 'alerts':
                alerts = await connector.get_weather_alerts()
                
                if not alerts:
                    print("✅ No active weather alerts")
                    return
                    
                print(f"⚠️ Active Weather Alerts ({len(alerts)})")
                print("=" * 50)
                
                for alert in alerts:
                    print(f"\n🚨 {alert.level} - {alert.type}")
                    print(f"📍 {', '.join(alert.affected_regions)}")
                    print(f"🕐 Valid: {alert.valid_from.strftime('%Y-%m-%d %H:%M')} - {alert.valid_until.strftime('%Y-%m-%d %H:%M')}")
                    print(f"ℹ️  {alert.description}")
                    
            elif args.command == 'stations':
                stations = await connector.get_stations()
                
                print(f"🗺️ Available Weather Stations ({len(stations)})")
                print("=" * 50)
                
                for station in stations:
                    status = "🟢" if station.active else "🔴"
                    print(f"{status} {station.name} ({station.id})")
                    print(f"   📍 {station.latitude:.3f}, {station.longitude:.3f}")
                    print(f"   🏔️  {station.altitude}m")
                    
            elif args.command == 'test':
                print("🧪 Testing ARSO connector...")
                
                # Test weather data
                weather_data = await connector.get_current_weather()
                print(f"✅ Weather data: {len(weather_data)} observations")
                
                # Test alerts
                alerts = await connector.get_weather_alerts()
                print(f"✅ Alerts: {len(alerts)} active")
                
                # Test stations
                stations = await connector.get_stations()
                print(f"✅ Stations: {len(stations)} available")
                
                print("\n🎉 All tests passed!")
                
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())