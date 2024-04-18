#!/usr/bin/env bash
# a bash script to get ready for deployment

if ! command -v nginx &> /dev/null;
then
    sudo apt update
    sudo apt install nginx -y
fi
sudo systemctl start nginx
if ! [ -d "/data/" ]
then
    sudo mkdir "/data/"
fi

if ! [ -d "/data/web_static/" ];
then
    sudo mkdir -p "/data/web_static/"
fi

if ! [ -d "/data/web_static/releases/" ];
then
    sudo mkdir "/data/web_static/releases/"
fi

if ! [ -d "/data/web_static/shared/" ];
then
    sudo mkdir "/data/web_static/shared/"
fi

if ! [ -d "/data/web_static/releases/test" ];
then
    sudo mkdir "/data/web_static/releases/test"
fi

if ! [ -f "/data/web_static/releases/test/index.html" ];
then
    sudo touch "/data/web_static/releases/test/index.html"
fi
echo "<html><body>Hello, this is a test index page.</body></html>" | sudo tee "/data/web_static/releases/test/index.html" > /dev/null
if [ -d "/data/web_static/current" ]
then
    sudo rm -rf "/data/web_static/current"
fi
sudo ln -s "/data/web_static/releases/test/" "/data/web_static/current"
sudo chown -R "ubuntu":"ubuntu" "/data"
sudo sed -i "s/root \/var\/www\/html/root \/data\/web_static\/current/" "/etc/nginx/sites-available/default"
sudo sed -i "s/server_name _;/server_name _;\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}/" "/etc/nginx/sites-available/default"
sudo systemctl reload nginx
