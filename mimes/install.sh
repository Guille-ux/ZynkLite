#!/bin/bash

echo "Adding Zynk Lite MIME..."

xdg-mime install --mode user package/application-x-zynk.xml

xdg-icon-resource install --context mimetypes --size 512 icons/hicolor/512x512/mimetypes/application-x-zynk.png application-x-zynk

update-mime-database ~/.local/share/mime
gtk-update-icon-cache ~/.local/share/icons/hicolor

echo "Finnish."
