+ https
+ обновление
+ домен

!php7-fpm = php7.0-fpm
!php7-json = php7.0-json
!php7-gd = php7.0-gd
!php7-xml = php7.0-xml
!php7-sqlite3 = php7.0-sqlite3
php7-openssl
php7-session
php7-zip = php7.0-zip
php7-zlib
php7-cgi = php7.0-cgi
php7-pdo_sqlite



conf data - полностью заменять моими настройками
lib/tpl - dokuwiki возможно стоит оставить оригинальным, а остальное заменять моим


mkdir /tmp/backup
cd /
tar -Jcf /tmp/backup/dokuwiki_backup.tar.bz2 rsnapshot
tar -Jcvf

backup:
cd /home/rean/docker/data/dokuwiki/
tar -cvjf ~/dokuwiki_backup.tar.bz2 conf data lib/plugins lib/tpl
scp -P 2222 rean@192.168.1.9:~/dokuwiki_backup.tar.bz2 ~/tmp


restore:
scp ~/tmp/dokuwiki_backup.tar.bz2 82.202.236.207:/tmp
rm -rf /dokuwiki/conf /dokuwiki/data /dokuwiki/lib/plugins /dokuwiki/lib/tpl
tar -xvf /tmp/dokuwiki_backup.tar.bz2 -C /dokuwiki/
rm /tmp/dokuwiki_backup.tar.bz2

chown -R www-data:www-data /dokuwiki
chmod -R 644 /dokuwiki
find /dokuwiki/ -type d -exec chmod 0755 {} ';'

service php7.0-fpm reload && service nginx reload 
