#!/usr/bin/bash

sudo ln -s $PYTHONPATH/certbot /usr/bin/certbot

DOMAIN1="fup-env.eba-ijpp3mdu.us-east-1.elasticbeanstalk.com"

if sudo certbot certificates | grep -q "$DOMAIN1"; then
    sudo certbot --nginx --cert-name $DOMAIN1 --reinstall
else
    sudo certbot --nginx --cert-name $DOMAIN1 -d $DOMAIN1 --agree-tos --non-interactive --register-unsafely-without-email
fi