"""Quick test to verify web server can start"""
import sys
sys.path.insert(0, r'c:\Users\sfaith\Dev\Investments')

try:
    from tech_crawler.web.app import create_app
    print("✓ Flask app created successfully")
    
    app = create_app()
    print("✓ Flask app initialized")
    
    # Test routes exist
    with app.app_context():
        print("✓ App context working")
        print("\nAvailable routes:")
        for rule in app.url_map.iter_rules():
            if not rule.rule.startswith('/static'):
                print(f"  {rule.rule} -> {rule.endpoint}")
    
    print("\n✓ Web interface setup complete!")
    print("\nTo start the server, run:")
    print("  python web_server.py")
    print("\nThen open: http://localhost:5000")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
