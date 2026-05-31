"""
ADB (Android Debug Bridge) Manager for device control
"""
import subprocess
from typing import List, Optional, Dict
import time


class ADBManager:
    """Manages ADB commands and device communication"""
    
    def __init__(self, device_id: Optional[str] = None):
        """
        Initialize ADB Manager
        
        Args:
            device_id: Device ID (if None, uses first connected device)
        """
        self.device_id = device_id
        self._ensure_adb_available()
    
    def _ensure_adb_available(self):
        """Check if ADB is available"""
        try:
            subprocess.run(["adb", "version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "ADB not found. Install Android SDK Platform Tools or use mock mode."
            )
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected devices"""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                check=True
            )
            devices = []
            for line in result.stdout.split("\n")[1:]:
                if "device" in line and not "devices" in line:
                    device_id = line.split()[0]
                    devices.append(device_id)
            return devices
        except Exception as e:
            print(f"Error getting devices: {e}")
            return []
    
    def execute_command(self, command: str) -> str:
        """Execute ADB command"""
        try:
            cmd = ["adb"]
            if self.device_id:
                cmd.extend(["-s", self.device_id])
            cmd.extend(command.split())
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except Exception as e:
            print(f"Error executing command: {e}")
            return ""
    
    def tap(self, x: int, y: int) -> bool:
        """Tap on screen at coordinates"""
        return self.execute_command(f"shell input tap {x} {y}") is not None
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 1000) -> bool:
        """Swipe on screen"""
        return self.execute_command(
            f"shell input swipe {x1} {y1} {x2} {y2} {duration}"
        ) is not None
    
    def type_text(self, text: str) -> bool:
        """Type text on screen"""
        # Escape special characters
        text = text.replace('"', '\\"')
        return self.execute_command(f"shell input text \"{text}\"") is not None
    
    def press_key(self, key: str) -> bool:
        """Press keyboard key (HOME, BACK, etc.)"""
        key_codes = {
            "HOME": 3,
            "BACK": 4,
            "ENTER": 66,
            "DEL": 67,
        }
        code = key_codes.get(key.upper(), key)
        return self.execute_command(f"shell input keyevent {code}") is not None
    
    def screenshot(self, filename: str = "/sdcard/screenshot.png") -> bool:
        """Take screenshot on device"""
        return self.execute_command(f"shell screencap -p {filename}") is not None
    
    def get_device_info(self) -> Dict:
        """Get device information"""
        try:
            android_version = self.execute_command("shell getprop ro.build.version.release").strip()
            brand = self.execute_command("shell getprop ro.product.brand").strip()
            model = self.execute_command("shell getprop ro.product.model").strip()
            
            return {
                "android_version": android_version,
                "brand": brand,
                "model": model,
                "device_id": self.device_id
            }
        except Exception as e:
            print(f"Error getting device info: {e}")
            return {}
    
    def is_connected(self) -> bool:
        """Check if device is connected"""
        devices = self.get_connected_devices()
        if self.device_id:
            return self.device_id in devices
        return len(devices) > 0
