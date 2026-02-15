#!/bin/bash
# 🜂 SISTEMSKI INVENTAR - Pregled vseh sistemskih komponent 🜂

echo "=== SISTEMSKI INVENTAR ==="
echo "Datum: $(date)"
echo "Uporabnik: $USER"
echo ""

echo "1. HARDWARE PODATKI:"
echo "-------------------"
echo "CPU: $(lscpu | grep 'Model name:' | cut -d':' -f2 | xargs)"
echo "GPU: $(lspci | grep -i nvidia | head -1 | cut -d ':' -f3)"
echo "RAM: $(free -h | grep 'Mem:' | awk '{print $2}') total, $(free -h | grep 'Mem:' | awk '{print $7}') available"
echo ""

echo "2. DRIVERJI:"
echo "------------"
echo "NVIDIA verzija:"
nvidia-smi 2>/dev/null | head -4 | tail -2
echo ""

echo "3. AKTIVNI SERVISI:"
echo "-------------------"
systemctl list-units --type=service --state=running | grep -E "(ollama|docker|sddm|openclaw)" | wc -l
echo "Pomembni aktivni servisi:"
systemctl list-units --type=service --state=running | grep -E "(ollama|docker|sddm|openclaw)"
echo ""

echo "4. DISK UPORABA:"
echo "----------------"
df -h | grep -E "(/$|Size)"
echo ""

echo "5. RAM UPORABA:"
echo "---------------"
free -h
echo ""

echo "6. VES SISTEMI:"
echo "---------------"
echo "Število VES map:"
find ~/VES -type d | wc -l
echo "Aktivacijski skript:"
ls -la ~/VES/ACTIVATE_SYSTEMS.sh 2>/dev/null || echo "Ni najden"
echo "Optimiziran aktivacijski skript:"
ls -la ~/OPTIMIZIRAN_ACTIVATE_SYSTEMS.sh 2>/dev/null || echo "Ni najden"
echo ""

echo "7. AI INFRASTRUKTURA:"
echo "---------------------"
echo "Ollama status:"
systemctl is-active ollama 2>/dev/null || echo "Ni aktivno"
echo "OpenClaw gateway:"
pgrep -f openclaw-gateway >/dev/null && echo "Teče" || echo "Ne teče"
echo ""

echo "8. POMEMBNE DATOTEKE:"
echo "--------------------"
echo "AI workspace:"
ls -la ~/AI_WORKSPACE/ 2>/dev/null | wc -l
echo "Organizacijska mapa:"
ls -la ~/ORGANIZACIJA_SISTEMA/ 2>/dev/null | wc -l
echo ""

echo "9. KONFIGURACIJE:"
echo "-----------------"
echo "Sysctl konfiguracije:"
cat /etc/sysctl.d/99-swap.conf 2>/dev/null || echo "Ni najdena"
echo ""

echo "10. POSODOBLJENOST:"
echo "------------------"
echo "Zadnji sistemski update:"
last | grep shutdown | head -1
echo ""

echo "Inventar zaključen: $(date)"