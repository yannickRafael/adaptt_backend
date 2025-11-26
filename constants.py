CRITICAL_DOCS_MAP = {
    "signedContract": {
        "name": "Contrato Assinado",
        "oc4ids_type": "contract",
        "weight": 0.35,
        "alert_risk": "Risco Crítico de gestão de custos e corrupção.",
        "simple_msg": "Alto risco orçamental. Contrato final não publicado.",
    },
    "feasibilityStudy": {
        "name": "Estudo de Viabilidade",
        "oc4ids_type": "tender",
        "weight": 0.20,
        "alert_risk": "Risco de projeto desnecessário ou mal planeado.",
        "simple_msg": "Projeto sem prova de necessidade. Exija o estudo."
    },
    "progressReport": {
        "name": "Relatório de Progresso",
        "oc4ids_type": "implementation",
        "weight": 0.25,
        "alert_risk": "Risco de atrasos e desvios não monitorados.",
        "simple_msg": "Falta de acompanhamento. Exija relatórios de progresso."
    },
    "completionReport": {
        "name": "Relatório de Conclusão",
        "oc4ids_type": "completion",
        "weight": 0.20,
        "alert_risk": "Risco de qualidade final e falta de prestação de contas.",
        "simple_msg": "Obra terminada sem garantia de qualidade. Exija o relatório final."
    }
}
