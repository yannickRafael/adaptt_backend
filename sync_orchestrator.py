import api_fetcher
import data_persistence
import db_manager
import score_calculator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_all_projects():
    """Processes all unprocessed projects to calculate their transparency score."""
    logging.info("Starting Score IT calculation for unprocessed projects...")
    
    unprocessed_ids = db_manager.get_unprocessed_projects()
    logging.info(f"Found {len(unprocessed_ids)} projects to process.")
    
    for project_id in unprocessed_ids:
        try:
            score_data = score_calculator.calculate_transparency_score(project_id)
            if score_data:
                db_manager.update_project_score(project_id, score_data)
                logging.info(f"Calculated Score IT for {project_id}: {score_data['transparency_score']} ({score_data['alert_color']})")
            else:
                logging.warning(f"Could not calculate score for {project_id}")
        except Exception as e:
            logging.error(f"Error processing project {project_id}: {e}")
            
    logging.info("Score IT calculation completed.")

def run_full_sync():
    """Orchestrates the full synchronization process."""
    logging.info("Starting full synchronization...")

    # 0. Sync locations first
    logging.info("Syncing locations...")
    locations = api_fetcher.fetch_locations()
    for location in locations:
        data_persistence.insert_or_update_location(location)
    logging.info(f"Synced {len(locations)} locations.")

    # 1. Fetch all projects (bulk)
    projects = api_fetcher.fetch_public_projects()
    logging.info(f"Found {len(projects)} projects.")

    for project in projects:
        project_id = project.get('id')
        if not project_id:
            logging.warning("Project found without ID. Skipping.")
            continue

        logging.info(f"Syncing Project {project_id}...")
        
        # 2. Save project data
        data_persistence.insert_or_update_project(project_id, project)
        
        # 3. Save document status
        documents = []
        phases = ['identification', 'preparation', 'procurement', 'implementation', 'completion']
        
        for phase in phases:
            phase_data = project.get(phase, {})
            # Check if phase_data is a dictionary (it should be based on the JSON structure)
            if isinstance(phase_data, dict):
                phase_docs = phase_data.get('documents', [])
                if isinstance(phase_docs, list):
                    documents.extend(phase_docs)
        
        # Also check for top-level documents just in case
        top_level_docs = project.get('documents', [])
        if isinstance(top_level_docs, list):
            documents.extend(top_level_docs)

        data_persistence.insert_document_status(project_id, documents)
        
        logging.info(f"Successfully synced Project {project_id}.")

    logging.info("Full synchronization completed.")
    
    # Run Score IT calculation
    process_all_projects()

if __name__ == "__main__":
    run_full_sync()
