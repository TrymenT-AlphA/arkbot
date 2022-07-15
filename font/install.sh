mkdir -p /usr/share/fonts/arkbot
cp ./font/*.ttf /usr/share/fonts/arkbot/
chmod 644 /usr/share/fonts/arkbot/*.ttf
mkfontscale
mkfontdir
fc-cache -fv
