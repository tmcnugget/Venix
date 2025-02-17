cd ~
sudo rm -rf Venix/
git clone https://github.com/tmcnugget/Venix.git

confirm() {
	if $FORCE; then
		true
	else
		read -r -p "$1 [y/N] " response < /dev/tty
		if [[ $response =~ ^(yes|y|Y)$ ]]; then
			true
		else
			false
		fi
	fi
}

if confirm "Would you like to reboot now?"; then
  sudo reboot now
