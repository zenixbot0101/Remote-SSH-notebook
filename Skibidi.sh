rm -rf ngrok ngrok.zip ngrok.sh > /dev/null 2>&1

wget -O ng.sh https://raw.githubusercontent.com/zenixbot0101/Remote-SSH-notebook/refs/heads/main/GCngrok.sh > /dev/null 2>&1
chmod +x ng.sh
./ng.sh

clear
echo "======================="
echo "Auto chọn region: Japan (jp)"
echo "======================="

# AUTO REGION
CRP="jp"
./ngrok tcp --region $CRP 22 &>/dev/null &

echo "======================="
echo Updating Please Wait
echo "======================="

sudo apt update > /dev/null 2>&1
sudo apt install openssh-server -y > /dev/null 2>&1

mkdir -p /var/run/sshd

# tránh bị ghi trùng nhiều lần
sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config

echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc
echo "export LD_LIBRARY_PATH" >> /root/.bashrc

sudo service ssh start

echo "===================================="

# lấy link SSH
curl --silent http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"tcp:..([^"]*).*/\1/p'

echo "create root password"
passwd

echo "===================================="
