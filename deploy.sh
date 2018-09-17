# 1. 拉代码到 /var/www/magic-serve
# 2. 执行 bash deploy.sh

set -ex


# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
cp /var/www/magic-serve/magic-serve.conf /etc/supervisor/conf.d/magic-serve.conf
# 不要再 sites-available 里面放任何东西
cp /var/www/magic-serve/magic-serve.nginx /etc/nginx/sites-enabled/magic-serve
chmod -R o+rwx /var/www/magic-serve

# 初始化
cd /var/www/magic-serve
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I