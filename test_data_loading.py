#!/usr/bin/env python3
"""
Simple test script to verify data loading and merging functionality
"""
import sys
from pathlib import Path

# Add generator module to path
sys.path.insert(0, str(Path(__file__).parent))

from generator.io_loader import load_all_data_sources, get_data_summary
from generator.merger import merge_governor_profiles

def test_data_loading():
    """Test loading all data sources"""
    print("🧪 Testing data loading...")
    
    try:
        # Load data
        bundle = load_all_data_sources()
        
        # Get summary
        summary = get_data_summary(bundle)
        print(f"📊 Data summary: {summary}")
        
        # Test merging
        print("\n🔄 Testing profile merging...")
        profiles = merge_governor_profiles(bundle)
        
        print(f"✅ Successfully merged {len(profiles)} governor profiles")
        
        # Show a sample profile
        if profiles:
            sample_name = list(profiles.keys())[0]
            sample_profile = profiles[sample_name]
            print(f"\n📋 Sample profile for {sample_name}:")
            print(f"   Element: {sample_profile.element}")
            print(f"   Traits: {sample_profile.personality_traits[:3]}...")
            print(f"   Domains: {sample_profile.domains[:2]}...")
            print(f"   Essence: {sample_profile.essence[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_loading()
    sys.exit(0 if success else 1) 