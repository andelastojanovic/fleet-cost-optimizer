import numpy as np
import pandas as pd

def ottimizza_varchi_doganali(arrivi_camion_ora, varchi_attivi):
    """
    Simula e ottimizza i tempi di attesa (Border Crossing Time) 
    per il corridoio Trieste-Belgrado nel Port Community System.
    """
    # Capacità di elaborazione media di un varco doganale (camion/ora)
    capacita_singolo_varco = 15 
    capacita_totale = varchi_attivi * capacita_singolo_varco
    
    # Calcolo del collo di bottiglia e della coda
    if arrivi_camion_ora > capacita_totale:
        camion_in_coda = arrivi_camion_ora - capacita_totale
        tempo_attesa_ore = camion_in_coda / capacita_totale
        status = "CRITICO - Saturazione Varco"
    else:
        camion_in_coda = 0
        tempo_attesa_ore = 0.15 # Tempo tecnico minimo di controllo (9 minuti)
        status = "OTTIMALE - Flusso Fluido"
        
    return {
        "Stato Varco": status,
        "Camion in Coda": camion_in_coda,
        "Border Crossing Time (Ore)": round(tempo_attesa_ore, 2)
    }

# Simulazione di picco di flusso sul corridoio Adriatico-Balcanico
flusso_trieste_belgrado = ottimizza_varchi_doganali(arrivi_camion_ora=50, varchi_attivi=3)
print(flusso_trieste_belgrado)
