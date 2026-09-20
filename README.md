# Discord Deal Bot

Bot Discord qui collecte automatiquement codes promo, jeux gratuits et codes d'échange.

## Installation

1. **Cloner le projet**
   ```bash
   git clone <repo>
   cd discord_deal_bot
   ```

2. **Créer un fichier .env**
   ```env
   DISCORD_TOKEN=votre_token_ici
   CHANNEL_ID=123456789012345678
   REPORT_HOUR=20
   REPORT_MINUTE=0
   TIMEZONE=Europe/Paris
   MENTION_ROLE=@everyone
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer le bot**
   ```bash
   python bot.py
   ```

## Commandes

- `/status` - Voir le statut du bot
- `/rapport_now` - Forcer l'envoi du rapport
- `/clear` - Vider la base de données

## Fonctionnement

- Collecte toutes les 2h de 8h à 20h
- Rapport quotidien à 20h (heure de Paris)
- Filtre les doublons automatiquement
- Stocke les données dans SQLite
