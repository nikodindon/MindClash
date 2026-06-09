# EP001 — La thermodynamique de la civilisation (Jancovici synthesis)

> **Épisode pilote** de MindClash.
> Premier épisode test de la chaîne YouTube.

## Concept

Interview conversationnelle à 2 voix (Alex = host curieux, Marc = expert qui
a étudié les 8 cours) sur les 8 cours des Mines 2019 de Jean-Marc Jancovici.

**Différenciation** : pas un cours, pas un débat. Une vraie conversation entre
deux personnes, où l'une découvre et l'autre maîtrise. Tension pédagogique
naturelle.

## Sources

8 cours des Mines 2019 de Jancovici, analysés en depth=extreme via YT-Insight,
juin 2026. Disponibles dans `knowledge_base/science/jancovici/`.

## Statut

- [x] Concept défini
- [x] Profile Jancovici créé (`_profile.md`)
- [x] Script v1 écrit (`script.json`, 18 min, 2340 mots, 51 segments)
- [x] Show notes créées (`show_notes.md`)
- [ ] **Script v2** : étoffer pour atteindre 22-25 min (+700 mots)
- [ ] **Production audio** : TTS Orpheus/Kokoro, 2 voix distinctes
- [ ] **Mix audio** : ffmpeg, transitions musicales
- [ ] **Vidéo YouTube** : image de fond + waveform + texte overlay
- [ ] **Distribution** : upload YouTube + Spotify + Twitter clips
- [ ] **Anglais** : traduction / version EN (post-pilote)

## Fichiers de cet épisode

```
EP001_jancovici-synthesis/
├── README.md           ← ce fichier (statut)
├── script.json         ← dialogue structuré pour production audio
├── show_notes.md       ← titre YouTube, description, timestamps, tags
├── audio_segments/     ← (à remplir) segments audio .wav par id
└── debate_raw.json     ← (vide pour cet épisode, format débat = EP002+)
```

## Décisions clés

### Pourquoi 2 voix, pas un narrateur solo
- Plus vivant, plus engageant
- Tension pédagogique naturelle (curieux vs expert)
- Pattern éprouvé : Lex Fridman, The Drive, Huberman

### Pourquoi en français d'abord
- Source primaire en français (Jancovici)
- Pilotage plus rapide (pas de traduction)
- L'anglais viendra dans EP002+ ou v2 de cet épisode

### Pourquoi Jancovici et pas un autre
- Ses cours sont exceptionnels et structurés
- Sujet énergie-climat = quête existentielle pour la décennie
- 8 cours = matériel riche (16h de contenu) → synthèse en 25 min = forte valeur
- Position pro-nucléaire clivante = bon pour engagement YouTube

### Pourquoi un pilot mono-sujet avant un débat
- Tester le pipeline de bout en bout (TTS, mix, vidéo, distribution)
- Valider la durée, le format, le ton
- Le débat (Jancovici vs Lovins) sera EP002, plus complexe à produire

## Prochaines étapes concrètes

### Court terme (cette semaine)

1. **Étoffer le script** (700 mots) :
   - Transition climat→solutions (étoffer la respiration)
   - Ajouter l'analogie des 4 estomacs des vaches (manquante dans v1)
   - Renforcer l'analyse critique (sous-section monde non-OCDE)
   - Outro un peu plus longue (rappel des chiffres clés)
2. **Tester la production TTS** :
   - 2 voix FR d'Orpheus ou Kokoro
   - Générer 5-10 segments de test
   - Valider la qualité avant de tout produire

### Moyen terme (semaine prochaine)

3. **Production audio complète** (~50 min de calcul TTS)
4. **Mix audio** (ffmpeg + transitions)
5. **Vidéo YouTube** (image + waveform + overlays)

### Avant publication

6. **Miniature** (Photoshop ou Canva)
7. **Description YouTube** complète (dans `show_notes.md`)
8. **Upload + premier post** sur chaîne MindClash
9. **Mesures early** (rétention 30s, 50% mark, commentaires)

## Métriques de succès (pilote)

- **Acoustique** : pas de coupures audio, mixage propre, transitions douces
- **Rétention YouTube** : > 40% à 5 min, > 25% à 18 min (fin)
- **Engagement** : > 50 likes, > 10 commentaires en 1 semaine
- **Conversion** : > 100 abonnés générés si on hit 1000 vues
- **Sentiment** : commentaires majoritairement positifs/curieux (pas de flame)

## Liens internes

- **Profile de la personnalité** : `knowledge_base/science/jancovici/_profile.md`
- **Conférences sources** : `knowledge_base/science/jancovici/lectures/cours-mines-2019/`
- **Prochain épisode (débat)** : `episodes/EP001_jancovici-vs-lovins/` (à renommer en EP002)
- **README principal** : `../../README.md`

## Crédits

- **Script** : généré avec assistance IA (Hermes) à partir des MD Jancovici
- **Voix** : Orpheus ou Kokoro TTS (à confirmer en phase test)
- **Mix** : ffmpeg + Python audioop
- **Vidéo** : moviepy ou ffmpeg drawtext
- **Distribution** : YouTube Data API v3

## Disclaimer légal

Ce podcast est généré avec assistance IA. Les citations sont attribuées à
Jean-Marc Jancovici. Les thèses et opinions sont celles de Jancovici,
présentées ici dans un format conversationnel à des fins pédagogiques.
