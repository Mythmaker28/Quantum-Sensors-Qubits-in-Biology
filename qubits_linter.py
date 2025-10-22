#!/usr/bin/env python3
"""
Linter pour biological_qubits.csv — Atlas des Qubits Biologiques v1.2
Vérifie cohérence, unités, plages de valeurs et génère QC_REPORT.md
"""

import csv
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass, field

@dataclass
class LintIssue:
    """Issue détectée par le linter"""
    ligne: int
    systeme: str
    colonne: str
    severite: str  # ERROR, WARNING, INFO
    message: str
    valeur_actuelle: str
    suggestion: str = ""

@dataclass
class LintStats:
    """Statistiques du linting"""
    total_lignes: int = 0
    erreurs: int = 0
    warnings: int = 0
    infos: int = 0
    systemes_ok: int = 0
    issues: List[LintIssue] = field(default_factory=list)

class QubitsLinter:
    """Linter pour le dataset des qubits biologiques"""
    
    def __init__(self, csv_path: str = "biological_qubits.csv"):
        self.csv_path = csv_path
        self.stats = LintStats()
        self.data = []
        
    def load_csv(self) -> List[Dict]:
        """Charge le CSV"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
            self.stats.total_lignes = len(self.data)
        return self.data
    
    def add_issue(self, ligne: int, systeme: str, colonne: str, severite: str, 
                  message: str, valeur: str, suggestion: str = ""):
        """Ajoute une issue"""
        issue = LintIssue(ligne, systeme, colonne, severite, message, valeur, suggestion)
        self.stats.issues.append(issue)
        
        if severite == "ERROR":
            self.stats.erreurs += 1
        elif severite == "WARNING":
            self.stats.warnings += 1
        else:
            self.stats.infos += 1
    
    def check_contraste(self, row: Dict, idx: int):
        """Vérifie Contraste_% dans [0-100] ou NA"""
        contraste = row.get('Contraste_%', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if contraste and contraste != 'NA':
            try:
                val = float(contraste)
                if val < 0 or val > 100:
                    self.add_issue(idx+2, systeme, 'Contraste_%', 'ERROR',
                                   f'Contraste hors plage [0-100]%', contraste,
                                   'Vérifier source ou mettre NA si non applicable')
                elif val > 50:
                    self.add_issue(idx+2, systeme, 'Contraste_%', 'WARNING',
                                   f'Contraste >50% inhabituel pour ODMR/ESR', contraste,
                                   'Vérifier si ce n est pas T2 ou autre paramètre')
            except ValueError:
                self.add_issue(idx+2, systeme, 'Contraste_%', 'ERROR',
                               f'Contraste non numérique', contraste,
                               'Format attendu : nombre ou NA')
    
    def check_nv_frequency(self, row: Dict, idx: int):
        """Vérifie NV à 2.87 GHz ±0.3 GHz"""
        defaut = row.get('Defaut', '').strip()
        freq = row.get('Frequence', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if defaut == 'NV' and freq:
            # Extraire la fréquence numérique
            match = re.search(r'([\d.]+)\s*GHz', freq)
            if match:
                freq_val = float(match.group(1))
                if abs(freq_val - 2.87) > 0.3:
                    self.add_issue(idx+2, systeme, 'Frequence', 'ERROR',
                                   f'NV doit être à 2.87±0.3 GHz (à B0~5 mT)', freq,
                                   f'Vérifier source ou champ B0_Tesla')
            else:
                self.add_issue(idx+2, systeme, 'Frequence', 'WARNING',
                               f'Format fréquence non reconnu pour NV', freq,
                               'Format attendu : "2.87 GHz"')
    
    def check_sic_defaut(self, row: Dict, idx: int):
        """Vérifie que les SiC ont un défaut renseigné"""
        systeme = row.get('Systeme', 'Inconnu').lower()
        defaut = row.get('Defaut', '').strip()
        
        if 'sic' in systeme and (not defaut or defaut == 'NA'):
            self.add_issue(idx+2, systeme, 'Defaut', 'ERROR',
                           f'Système SiC sans défaut spécifié', defaut,
                           'Renseigner VSi, VV, TiC ou autre')
    
    def check_nmr_b0(self, row: Dict, idx: int):
        """Vérifie que les NMR ont B0_Tesla renseigné"""
        methode = row.get('Methode_lecture', '').strip()
        b0 = row.get('B0_Tesla', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if methode == 'NMR' and (not b0 or b0 == 'NA' or b0 == '0.0'):
            self.add_issue(idx+2, systeme, 'B0_Tesla', 'ERROR',
                           f'Système NMR sans champ B0_Tesla', b0,
                           'Renseigner champ du spectromètre (ex: 3.0 pour 3T)')
    
    def check_hyperpol_t1(self, row: Dict, idx: int):
        """Vérifie que les hyperpolarisés ont T1_s renseigné"""
        hyperpol = row.get('Hyperpol_flag', '').strip()
        t1 = row.get('T1_s', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if hyperpol == '1' and (not t1 or t1 == 'NA'):
            self.add_issue(idx+2, systeme, 'T1_s', 'ERROR',
                           f'Hyperpolarisé sans T1_s (critique pour fenêtre temporelle)', t1,
                           'Renseigner T1 en secondes (ex: 60 pour pyruvate)')
    
    def check_temperature(self, row: Dict, idx: int):
        """Vérifie température cohérente avec contexte biologique"""
        temp = row.get('Temperature_K', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        in_vivo = row.get('In_vivo_flag', '').strip()
        
        if temp and temp != 'NA':
            try:
                temp_val = float(temp)
                # In vivo doit être 295-310 K
                if in_vivo == '1' and (temp_val < 290 or temp_val > 315):
                    self.add_issue(idx+2, systeme, 'Temperature_K', 'WARNING',
                                   f'Température in vivo inhabituelle : {temp} K', temp,
                                   'In vivo typiquement 295-310 K')
                # Cryogénique <100 K incompatible biologie
                if temp_val < 100:
                    qualite = row.get('Qualite', '').strip()
                    if qualite != '1':
                        self.add_issue(idx+2, systeme, 'Temperature_K', 'WARNING',
                                       f'Cryogénique {temp} K devrait avoir Qualite=1', temp,
                                       'Systèmes cryo non applicables biologie → Qualité 1')
            except ValueError:
                self.add_issue(idx+2, systeme, 'Temperature_K', 'ERROR',
                               f'Température non numérique', temp,
                               'Format attendu : nombre en Kelvin')
    
    def check_doi_format(self, row: Dict, idx: int):
        """Vérifie format DOI"""
        doi = row.get('DOI', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if doi and not re.match(r'10\.\d{4,}/[\w\-.;()/]+', doi):
            self.add_issue(idx+2, systeme, 'DOI', 'WARNING',
                           f'Format DOI potentiellement invalide', doi,
                           'Format attendu : 10.xxxx/yyyyy')
    
    def check_verification_status(self, row: Dict, idx: int):
        """Vérifie statut de vérification"""
        status = row.get('Verification_statut', '').strip()
        systeme = row.get('Systeme', 'Inconnu')
        
        if status not in ['verifie', 'a_confirmer']:
            self.add_issue(idx+2, systeme, 'Verification_statut', 'ERROR',
                           f'Statut invalide : {status}', status,
                           'Valeurs autorisées : verifie, a_confirmer')
    
    def check_source_provenance(self, row: Dict, idx: int):
        """Vérifie que les valeurs clés ont une source"""
        systeme = row.get('Systeme', 'Inconnu')
        
        # T2 présent → Source_T2 devrait être renseignée
        t2 = row.get('T2_us', '').strip()
        source_t2 = row.get('Source_T2', '').strip()
        if t2 and t2 != 'NA' and (not source_t2 or source_t2 == 'NA'):
            self.add_issue(idx+2, systeme, 'Source_T2', 'WARNING',
                           f'T2 sans source de provenance', source_t2,
                           'Ajouter DOI:xxx Fig.X ou estimation si calculé')
        
        # Contraste présent → Source_Contraste
        contraste = row.get('Contraste_%', '').strip()
        source_contraste = row.get('Source_Contraste', '').strip()
        if contraste and contraste != 'NA' and (not source_contraste or source_contraste == 'NA'):
            self.add_issue(idx+2, systeme, 'Source_Contraste', 'WARNING',
                           f'Contraste sans source', source_contraste,
                           'Ajouter référence publication')
    
    def check_t2_t1_relation(self, row: Dict, idx: int):
        """Vérifie relation T2 ≤ 2×T1 (si les deux présents)"""
        systeme = row.get('Systeme', 'Inconnu')
        t1_str = row.get('T1_s', '').strip()
        t2_str = row.get('T2_us', '').strip()
        
        if t1_str and t1_str != 'NA' and t2_str and t2_str != 'NA':
            try:
                t1_s = float(t1_str)
                t2_us = float(t2_str)
                t2_s = t2_us / 1e6  # Convertir µs en s
                
                if t2_s > 2 * t1_s:
                    self.add_issue(idx+2, systeme, 'T2_us', 'WARNING',
                                   f'T2 > 2×T1 (physiquement impossible)', 
                                   f'T2={t2_us}µs, T1={t1_s}s',
                                   'Vérifier valeurs ou unités')
            except ValueError:
                pass  # Déjà géré par d'autres checks
    
    def lint_all(self):
        """Exécute tous les checks"""
        print(f"[LINT] Analysing {self.csv_path}...")
        self.load_csv()
        
        for idx, row in enumerate(self.data):
            self.check_contraste(row, idx)
            self.check_nv_frequency(row, idx)
            self.check_sic_defaut(row, idx)
            self.check_nmr_b0(row, idx)
            self.check_hyperpol_t1(row, idx)
            self.check_temperature(row, idx)
            self.check_doi_format(row, idx)
            self.check_verification_status(row, idx)
            self.check_source_provenance(row, idx)
            self.check_t2_t1_relation(row, idx)
        
        self.stats.systemes_ok = self.stats.total_lignes - len(set(
            issue.ligne for issue in self.stats.issues if issue.severite == 'ERROR'
        ))
        
        print(f"[OK] Lint completed: {self.stats.total_lignes} systems analysed")
        print(f"   [ERROR] Errors: {self.stats.erreurs}")
        print(f"   [WARN]  Warnings: {self.stats.warnings}")
        print(f"   [INFO]  Infos: {self.stats.infos}")
        print(f"   [OK]    Systems OK: {self.stats.systemes_ok}")
        
        return self.stats
    
    def generate_report_md(self, output_path: str = "QC_REPORT.md"):
        """Génère le rapport QC en Markdown"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 🔍 Rapport de Contrôle Qualité — Atlas des Qubits Biologiques v1.2\n\n")
            f.write(f"**Date** : {self._get_date()}\n")
            f.write(f"**Fichier** : `{self.csv_path}`\n\n")
            
            f.write("## 📊 Statistiques\n\n")
            f.write(f"- **Total systèmes analysés** : {self.stats.total_lignes}\n")
            f.write(f"- **❌ Erreurs bloquantes** : {self.stats.erreurs}\n")
            f.write(f"- **⚠️ Warnings** : {self.stats.warnings}\n")
            f.write(f"- **ℹ️ Informations** : {self.stats.infos}\n")
            f.write(f"- **✅ Systèmes sans erreur** : {self.stats.systemes_ok}\n\n")
            
            if self.stats.erreurs == 0:
                f.write("### ✅ Aucune erreur bloquante détectée !\n\n")
                f.write("Le dataset est prêt pour publication.\n\n")
            else:
                f.write("### ❌ Corrections requises\n\n")
                f.write(f"{self.stats.erreurs} erreur(s) bloquante(s) doivent être corrigées avant publication.\n\n")
            
            # Issues par sévérité
            for severite in ['ERROR', 'WARNING', 'INFO']:
                issues = [i for i in self.stats.issues if i.severite == severite]
                if not issues:
                    continue
                
                icon = {'ERROR': '❌', 'WARNING': '⚠️', 'INFO': 'ℹ️'}[severite]
                f.write(f"## {icon} {severite}S ({len(issues)})\n\n")
                
                for issue in issues:
                    f.write(f"### Ligne {issue.ligne} : {issue.systeme}\n\n")
                    f.write(f"**Colonne** : `{issue.colonne}`\n\n")
                    f.write(f"**Problème** : {issue.message}\n\n")
                    f.write(f"**Valeur actuelle** : `{issue.valeur_actuelle}`\n\n")
                    if issue.suggestion:
                        f.write(f"**Suggestion** : {issue.suggestion}\n\n")
                    f.write("---\n\n")
            
            # Résumé des systèmes à confirmer
            f.write("## 📝 Systèmes à confirmer (Verification_statut=a_confirmer)\n\n")
            a_confirmer = [row for row in self.data if row.get('Verification_statut') == 'a_confirmer']
            f.write(f"**Total** : {len(a_confirmer)} systèmes\n\n")
            
            for row in a_confirmer:
                systeme = row.get('Systeme', 'Inconnu')
                classe = row.get('Classe', '?')
                doi = row.get('DOI', 'N/A')
                f.write(f"- **{systeme}** (Classe {classe}) — DOI: {doi}\n")
            
            f.write("\n---\n\n")
            f.write("*Rapport généré automatiquement par `qubits_linter.py`*\n")
        
        print(f"[OK] Report generated: {output_path}")
    
    def _get_date(self) -> str:
        """Retourne la date actuelle"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")

def main():
    """Point d'entrée principal"""
    linter = QubitsLinter("biological_qubits.csv")
    stats = linter.lint_all()
    linter.generate_report_md("QC_REPORT.md")
    
    # Code de sortie : 1 si erreurs bloquantes, 0 sinon
    exit_code = 1 if stats.erreurs > 0 else 0
    if exit_code == 0:
        print("\n[OK] No blocking errors. Dataset ready for publication!")
    else:
        print(f"\n[ERROR] {stats.erreurs} blocking error(s) to fix.")
    
    return exit_code

if __name__ == "__main__":
    exit(main())

