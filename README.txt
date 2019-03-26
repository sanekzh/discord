
For more detailed sample you can go to tuttorial, but there are too much things. We only need supervisor ngnix and letsencrypt. Follow this instructons and also keep eye on it. https://simpleisbetterthancomplex.com/series/2017/10/16/a-complete-beginners-guide-to-django-part-7.html
1. step one update system and install needed software.
sudo apt-get update
sudo apt-get -y upgrade
udo apt-get install python3-dev libmysqlclient-dev
sudo apt-get -y install nginx
sudo apt-get -y install supervisor

1.1 Installig mysql. When it will end installation it will ask you for root password. Also asks some basic questions.
sudo apt-get -y install mysql-server

1.2 Running this command asks questions just accept them. https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04
mysql_secure_installation

1.3 getting into mysql cli (command line) asks for root password.
mysql -u root -p

1.4 creating database for our crazy bot. This will accept emojies xD. enter this command and exit.
CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


2. enable supervisor which is auto start and restart our website and bot.
sudo systemctl enable supervisor
sudo systemctl start supervisor

3. installing virtualenv. This is virtualenvirmoment for python.
sudo apt-get install python3-virtualenv

4. Adding user into ubuntu. We do not need to run our project under root user as it is not safe. `discord` is username you can change it.
adduser discord

5. adding newly created user to sudoes. for using sudo command.
gpasswd -a discord sudo

6. login to in to new user.
sudo su - discord

7. Creating virtualenvirmoment. We install python3 packages into it.
virtualenv venv -p python3

8. activating virtuanenvirmoment
source venv/bin/activate

9. installing pythton modules we need for our django website and bot to run.
pip install -r requirements.txt

10. There is gunicorn_start file locate into folder. That is needed for running our website.
chmod u+x gunicorn_start

11. Creating log and run folders.
mkdir run logs

12. Creating gunicorn.log file under logs folder.
touch logs/gunicorn.log

13. In folder you see supervisor config files. We are copying it to right destination.
cp website.conf /etc/supervisor/conf.d/website.conf 
cp discordbot.conf /etc/supervisor/conf.d/discordbot.conf 

14. Enabling supervisor configs. You can use commands for stop, start, restart  like this sudo supervisorctl restart website and sudo supervisorctl restart discordbot
sudo supervisorctl reread
sudo supervisorctl update

15. We are copying nginix config file. See that file maximum you have change is path inside it. If you create new user with not `boards` name then you should rewrite it with your username.
cp websitengnix /etc/nginx/sites-available/websitengnix

16. creating symlink for config file.
sudo ln -s /etc/nginx/sites-available/websitengnix /etc/nginx/sites-enabled/websitengnix

17. removing ngnix default config as long as we need it more.
sudo rm /etc/nginx/sites-enabled/default

18. restarting nginix server to accept our changes. Our new config for website.
sudo service nginx restart

19. Here we are getting letsencrypt ssl. Updating the ppa. Just enter this commands.
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx

20. We are getting ssl sertificate with this command. It will show you some basinc steps. entering your mail and choosing domain name for which you want the certificate.
sudo certbot --nginx

21. This is crontab. Crontab does cron jobs. This means running command when time comes. It will automatically update letsencrypt ssl.
sudo crontab -e
0 4 * * * /usr/bin/certbot renew --quiet

22. go to website folder where is located manage.py and run following commands. First 2 commands will create in to database tables.
python3 manage.py makemigrations
python3 manage.py migrate

23. collecting static files into one folder. just run this command. If it asks something just accept.
python3 manage.py collectstatic

24. creating superuser for the admin page access. just write following command and enter what it requests.
python3 manage.py createsuperuser

The database configuration is under file website/website/settings.py change credintinals with yours. it is under varianble ENGINES. In this file is located ALLOWED_HOSTS you should put there your domain. So change cookstart.io with new one if you wish. In this file on last 2 lines you see PAYPAL_RECEIVER_EMAIL variable. Change it if needed. Alse PAYPAL_TEST = False. If you set it to true you are going to use sandbox.

If something goes wrong and does not work just check in config files if you have written right passes to files. 

When everything is setup on main page there might appear some error. Just go in yourdomain.com/admin and login there.

25. Add new bots to the supervisorctl config
sudo su discord
cp ../home/discord/discord/website/paypal-discord-bot-[new owner name].conf ../etc/supervisor/conf.d/
    (e.g. cp ../home/discord/discord/website/paypal-discord-bot-anonymous.conf ../etc/supervisor/conf.d/ )
cd ../home/discord/
26. Update supervisorctl
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart website
