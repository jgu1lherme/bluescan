<img src="./assets/LOGO.png" alt="BLUESCAN" width="600">
🚀 BLUESCAN – Entry Scanner by IP

O BLUESCAN é um aplicativo para comunicação entre coletores de código de barras e computadores via IP/TCP.
Ele recebe códigos enviados por dispositivos como DWDEMO (Datalogic) e os insere automaticamente no sistema ativo, seja via colagem (CTRL+V) ou digitação simulada.

Fácil de usar, rápido e ideal para aumentar a produtividade em sistemas ERP, planilhas, aplicações web e automações diversas.

📌 Recursos Principais
✔ Recebimento de códigos via IP

O BLUESCAN opera como servidor local, recebendo em tempo real os códigos transmitidos pelo coletor.

✔ Modos de entrada altamente eficientes

🔹 Paste (CTRL+V) – cola automaticamente o código
🔹 PyType (digitação simulada via pyautogui) – digita caractere por caractere

✔ Enter Automático

Opcionalmente envia a tecla ENTER após cada código processado.

✔ Log detalhado

Exibe cada entrada recebida na tela, facilitando auditoria e testes.

✔ Configuração de porta TCP

Você pode alterar a porta de escuta do servidor rapidamente.

✔ Detecção automática do IPv4

Mostra o endereço correto que deve ser configurado no coletor.

✔ Guia integrado

A aba “Guia” inclui instruções para configurar o DWDEMO.

🖥️ Como Usar o BLUESCAN
1️⃣ Abra o programa

Execute o BLUESCAN normalmente.

2️⃣ Configure o coletor (DWDEMO ou similar)

No aplicativo do coletor:

Configurações → IP OUTPUT → Address


Defina o IPv4 exibido na aba Guia do BLUESCAN.
Porta padrão: 65432

Modo recomendado: 2D Scan

3️⃣ Inicie o servidor

Na aba Leitor, clique em:

🔵 INICIAR

O BLUESCAN começará a aceitar conexões.

4️⃣ Ative a automação (opcional)

Marcando:

Colagem / Entrada Automática

Enter Automático

E escolha o modo:

📌 Configurações → Modo de Entrada (Paste ou PyType)

5️⃣ Escaneie e pronto!

Tudo que você escanear aparecerá instantaneamente no programa que estiver ativo no seu computador.

⚙️ Modos de Entrada Explicados
🔹 Paste (CTRL+V)

O código é copiado para a área de transferência e colado automaticamente

Extremamente rápido

Ideal para ERP, navegadores e apps normais

🔹 PyType (digitação simulada)

O BLUESCAN digita caractere por caractere

Perfeito para sistemas que bloqueiam colagem

Delay configurável (0–200ms)

📡 Como o BLUESCAN Funciona Internamente

Abre um servidor TCP no IP/porta escolhidos

Recebe os dados enviados pelo coletor

Os processa automaticamente

Simula colagem ou digitação

Pode enviar o ENTER se habilitado

Registra tudo no log

📞 Contato / Suporte

Na aba Sobre, há um botão direto para suporte via WhatsApp:

📱 (22) 97404-0083
