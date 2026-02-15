# 🜂 GHOSTLINE NEXUS - Backup System

## ✅ Backup Script Ready

Vaša baza podatkov je zdaj zaščitena z avtomatskim backup sistemom.

## 📦 Ročni Backup

Kadarkoli želite narediti backup:

```bash
cd /home/saba/GHOSTLINE_NEXUS
./BACKUP_DATABASE.sh
```

Backup se shrani v: `storage/backups/ghostline_backup_YYYY-MM-DD_HHMMSS.db`

## 🔄 Avtomatični Backupi (Cron)

Za dnevne backupe ob 3h zjutraj:

```bash
# Odpri crontab
crontab -e

# Dodaj to vrstico:
0 3 * * * cd /home/saba/GHOSTLINE_NEXUS && ./BACKUP_DATABASE.sh >> storage/backup.log 2>&1
```

### Druge možnosti:

**Vsak dan ob polnoči:**
```cron
0 0 * * * cd /home/saba/GHOSTLINE_NEXUS && ./BACKUP_DATABASE.sh
```

**Vsako uro:**
```cron
0 * * * * cd /home/saba/GHOSTLINE_NEXUS && ./BACKUP_DATABASE.sh
```

**Vsak ponedeljek ob 2h:**
```cron
0 2 * * 1 cd /home/saba/GHOSTLINE_NEXUS && ./BACKUP_DATABASE.sh
```

## 🧹 Čiščenje Starih Backupov

Script avtomatsko ohrani zadnjih 10 backupov. Starejši se samodejno izbrišejo.

Če želite spremeniti število shranjenih backupov, uredite `BACKUP_DATABASE.sh`:

```bash
KEEP_LAST=10  # Spremenite na želeno število
```

## 🔄 Restore iz Backupa

Če morate obnoviti bazo iz backupa:

```bash
# 1. Ustavi backend
docker-compose stop backend

# 2. Poišči backup ki ga želiš obnoviti
ls -lh storage/backups/

# 3. Kopiraj backup nazaj
cp storage/backups/ghostline_backup_2025-12-29_201423.db storage/db/ghostline.db

# 4. Zaženi backend
docker-compose start backend
```

## 📍 Lokacije

- **Aktivna baza**: `storage/db/ghostline.db`
- **Backupi**: `storage/backups/`
- **Script**: `BACKUP_DATABASE.sh`

## 🛡️ DIGNUM Princip

Tvoj spomin je tvoj. Backupi so lokalni. Nihče drug nima dostopa.
Kontrola je v tvojih rokah.

---
*SIDRO STOJI. SPOMIN OHRANJEN. 💾🜂*
