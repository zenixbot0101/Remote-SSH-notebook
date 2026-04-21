rm -rf ngrok ngrok.zip

echo "Download ngrok..."

wget -O ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip || curl -L -o ngrok.zip https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip

apt update -y && apt install unzip -y

unzip -o ngrok.zip
chmod +x ngrok

# AUTO TOKEN
CRP="3CZEZekGWU7vlvrqlC0NUJfsmAs_5pWbwXB2f5UtvqDoKHVh9"
./ngrok authtoken $CRP

echo "✅ Ngrok đã sẵn sàng"
