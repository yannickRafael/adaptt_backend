import data_persistence
from constants import CRITICAL_DOCS_MAP

def calculate_transparency_score(project_id):
    """
    Calculates the Transparency Score (IT) for a given project.
    Returns a dictionary with the score, alert color, message, and missing documents.
    """
    # 1. Fetch raw data
    data = data_persistence.get_raw_project_data(project_id)
    if not data:
        return None

    # 2. Check for presence of critical documents
    published_weight = 0.0
    missing_documents = []
    
    # Extract all available documents from the project data
    # We look into the aggregated 'documents' list if available, or search in phases
    # Ideally, we should check where the document *should* be based on oc4ids_type,
    # but for simplicity and robustness, we'll check if it exists anywhere in the project.
    
    available_docs = []
    
    # Helper to collect docs from a list
    def collect_docs(doc_list):
        if isinstance(doc_list, list):
            for d in doc_list:
                if isinstance(d, dict):
                    # Normalize type to match keys in CRITICAL_DOCS_MAP if possible
                    # The API might return 'type': 'signedContract' or similar.
                    available_docs.append(d.get('type'))

    # Collect from top-level
    collect_docs(data.get('documents'))
    
    # Collect from phases
    phases = ['identification', 'preparation', 'procurement', 'implementation', 'completion']
    for phase in phases:
        phase_data = data.get(phase)
        if isinstance(phase_data, dict):
            collect_docs(phase_data.get('documents'))

    # 3. Calculate Score
    for doc_key, doc_meta in CRITICAL_DOCS_MAP.items():
        # Check if doc_key is in available_docs
        # We assume the API 'type' matches the keys in CRITICAL_DOCS_MAP
        if doc_key in available_docs:
            published_weight += doc_meta['weight']
        else:
            missing_documents.append(doc_meta['name'])

    score_it = round(published_weight * 10)

    # 4. Generate Alert
    alert_data = generate_simple_alert(score_it, missing_documents)

    return {
        "project_id": project_id,
        "transparency_score": score_it,
        "alert_color": alert_data['color'],
        "simple_message": alert_data['message'],
        "missing_documents_list": missing_documents
    }

def generate_simple_alert(score, missing_documents):
    """Generates the alert color and message based on the score."""
    if score < 4:
        color = "RED"
        # Combine risks for the first 2 missing docs to keep it concise
        msg = "ALERTA CRÍTICO: Risco de opacidade severa. "
        if missing_documents:
            msg += f"Faltam: {', '.join(missing_documents[:2])}. "
        msg += "Ação: Exija estes documentos."
    elif score < 7:
        color = "YELLOW"
        msg = "ALERTA: Transparência parcial. "
        if missing_documents:
            msg += f"Falta: {missing_documents[0]}. "
        msg += "Fiscalize o cumprimento."
    else:
        color = "GREEN"
        msg = "Transparência adequada. Documentos principais publicados."

    return {"color": color, "message": msg}
