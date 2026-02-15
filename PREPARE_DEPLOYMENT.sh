#!/usr/bin/env zsh
echo "\033[1;36m🌀 GHOSTLINE // GITHUB LOGIN PROTOCOL\033[0m"
echo "--------------------------------------"
echo "Ta skripta ti bo pomagala pri prijavi v GitHub, da lahko lanserava tvoj app."
echo ""
echo "Navodila:"
echo "1. Ko te vpraša 'preferred protocol', izberi \033[1;33mHTTPS\033[0m."
echo "2. Ko vpraša 'Authenticate Git with your GitHub credentials', izberi \033[1;33mY\033[0m."
echo "3. Ko vpraša 'How would you like to authenticate', izberi \033[1;33mLogin with a web browser\033[0m."
echo "4. Dobil boš 8-mestno kodo. Kopiraj jo in jo vnesi na strani, ki se bo odprla."
echo ""
read -q "REPLY?Si pripravljen? (y/n) "
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    gh auth login
    echo ""
    echo "\033[1;32m✅ Če je prijava uspela, mi v chat napiši svoje GitHub uporabniško ime!\033[0m"
else
    echo "Prekinjeno. Javi mi, ko boš pripravljen."
fi
