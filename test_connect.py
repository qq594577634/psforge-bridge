"""Simple PS connection test without emoji."""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=== PSForge Connection Test ===")

# Step 1: Try photoshop-python-api directly
print("\n[1] Testing photoshop-python-api direct connection...")
try:
    from photoshop import Session
    s = Session()
    s.__enter__()
    ver = s.app.version
    print(f"  OK! Photoshop version: {ver}")
    s.__exit__(None, None, None)
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()

# Step 2: Try PSForge adapter
print("\n[2] Testing PSForge PhotoshopApp...")
try:
    from psforge.ps_adapter import PhotoshopApp
    app = PhotoshopApp()
    ver2 = app.get_photoshop_version()
    print(f"  OK! PSForge connected, version: {ver2}")
    has_doc = app.has_active_document()
    print(f"  Active document: {has_doc}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Try executing a simple script
print("\n[3] Testing execute_javascript...")
try:
    app = PhotoshopApp()
    result = app.execute_javascript("app.version")
    print(f"  OK! Result: {result}")
except Exception as e:
    print(f"  FAILED: {e}")

print("\n=== Done ===")
