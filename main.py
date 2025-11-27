import db_manager
import sync_orchestrator

def main():
    """Main entry point for the synchronization process."""
    db_manager.initialize_db()
    print("Starting synchronization...")
    
    # Start notification worker
    from notification_worker import notification_worker
    notification_worker.start()
    print("Notification worker started...")
    
    sync_orchestrator.run_full_sync()

if __name__ == "__main__":
    main()
