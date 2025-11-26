import db_manager
import sync_orchestrator

def main():
    """Main entry point for the application."""
    print("Initializing database...")
    db_manager.initialize_db()
    
    print("Starting synchronization...")
    sync_orchestrator.run_full_sync()

if __name__ == "__main__":
    main()
